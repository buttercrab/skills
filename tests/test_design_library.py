"""Behavioral integrity checks for the portable annotated resource catalog."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / 'skills/design-with-intent/scripts/catalog.py'
SPEC = importlib.util.spec_from_file_location('design_catalog', SCRIPT)
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


def metadata(identity='example-one', **updates):
    record = {
        'id': identity, 'kind': 'example', 'title': identity.replace('-', ' ').title(),
        'summary': 'Compare information together and recover from an empty result.',
        'status': 'curated', 'availability': 'public',
        'facets': {'tasks': ['compare', 'recover'], 'contexts': ['operations'],
                   'platforms': ['web'], 'character': []},
        'sources': [{'url': 'https://example.org/source', 'title': 'Test source',
                     'locator': 'Correction section', 'revision': 'fixture-v1'}],
        'evidence': {'mode': ['source-inspected'], 'inspected_at': '2026-11-07',
                     'freshness': 'historical', 'scope': 'Synthetic integrity-test source, not a real recommendation.'},
        'reuse': 'Original synthetic test annotation.', 'related': [],
    }
    record.update(updates)
    return record


BODY = '''# Synthetic example

## When to use
Compare repeated operations and preserve a usable correction route.

## What to inspect
Inspect the supplied correction section and its alternatives.

## What to borrow and adapt
Use visible current state where the task requires comparison.

## Mismatches and limits
This test fixture is not a real product or a visual-inspection claim.
'''


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='design-catalog-tests-')
        self.root = Path(self.temporary.name) / 'package'
        (self.root / 'library/entries').mkdir(parents=True)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(SCRIPT, self.root / 'scripts/catalog.py')

    def tearDown(self):
        self.temporary.cleanup()

    def card(self, meta=None, body=BODY, *, filename=None):
        meta = metadata() if meta is None else meta
        path = self.root / 'library/entries' / (filename or (meta['id'] + '.md'))
        path.write_text('---\n' + json.dumps(meta, indent=2) + '\n---\n' + body)
        return path

    def args(self, **updates):
        fields = dict(query='', kind=[], status=[], availability=[], task=[], context=[], platform=[], character=[])
        fields.update(updates)
        return argparse.Namespace(**fields)

    def test_deterministic_views_and_detected_annotation_or_metadata_drift(self):
        path = self.card()
        catalog.build(self.root)
        original = (self.root / 'library/index.json').read_bytes()
        catalog.build(self.root)
        self.assertEqual(original, (self.root / 'library/index.json').read_bytes())
        catalog.build(self.root, check=True)
        changed = metadata(summary='A changed selection meaning must reach the index.')
        self.card(changed)
        with self.assertRaisesRegex(catalog.CatalogError, 'stale'):
            catalog.build(self.root, check=True)
        catalog.build(self.root)
        self.assertNotEqual(original, (self.root / 'library/index.json').read_bytes())
        # An annotation change is detected through its hash without copying prose.
        path.write_text(path.read_text().replace('preserve a usable correction route', 'retain the original user input'))
        with self.assertRaisesRegex(catalog.CatalogError, 'stale'):
            catalog.build(self.root, check=True)
        catalog.build(self.root)
        catalog.build(self.root, check=True)
        self.assertIn('retain the original user input', catalog.load_cards(self.root)[0]['body'])

    def test_discovery_only_cannot_be_promoted_but_historical_evidence_can(self):
        m = metadata()
        m['evidence']['mode'] = ['discovery-only']
        m['evidence']['inspected_at'] = None
        self.card(m)
        with self.assertRaisesRegex(catalog.CatalogError, 'curated'):
            catalog.load_cards(self.root)
        m['status'] = 'candidate'
        self.card(m)
        self.assertEqual('candidate', catalog.load_cards(self.root)[0]['meta']['status'])
        self.card(metadata())
        self.assertEqual('historical', catalog.load_cards(self.root)[0]['meta']['evidence']['freshness'])

    def test_partial_only_is_not_a_curated_inspection(self):
        m = metadata()
        m['evidence']['mode'] = ['partial']
        self.card(m)
        with self.assertRaisesRegex(catalog.CatalogError, 'substantive evidence'):
            catalog.load_cards(self.root)

    def test_visual_and_interaction_claims_require_specific_receipts(self):
        m = metadata()
        m['evidence']['mode'] = ['visual-inspected', 'interaction-tested']
        self.card(m)
        with self.assertRaisesRegex(catalog.CatalogError, 'visual_evidence'):
            catalog.load_cards(self.root)
        m['visual_evidence'] = [{'url': 'https://example.org/screen', 'locator': 'Empty view',
                                 'observed': 'A separate recovery button.', 'method': 'Synthetic test receipt.'}]
        m['flow_evidence'] = [{'url': 'https://example.org/flow', 'locator': 'Correction',
                               'sequence': ['Invalid', 'Corrected', 'Complete'], 'method': 'Synthetic test receipt.'}]
        self.card(m)
        with self.assertRaisesRegex(catalog.CatalogError, 'interaction_evidence'):
            catalog.load_cards(self.root)
        m['interaction_evidence'] = [{'url': 'https://example.org/flow', 'actions': ['Correct input'],
                                      'observed': 'Completion shown.', 'method': 'Synthetic test receipt.'}]
        self.card(m)
        self.assertEqual(1, len(catalog.load_cards(self.root)))

    def test_related_ids_must_resolve_and_not_self_reference(self):
        self.card(metadata(related=['missing-resource']))
        with self.assertRaisesRegex(catalog.CatalogError, 'unknown related ID'):
            catalog.load_cards(self.root)
        self.card(metadata(related=['example-one']))
        with self.assertRaisesRegex(catalog.CatalogError, 'itself'):
            catalog.load_cards(self.root)
        self.card(metadata(related=['example-two']))
        self.card(metadata('example-two'))
        self.assertEqual(2, len(catalog.load_cards(self.root)))

    def test_duplicate_json_keys_are_rejected_not_silently_overwritten(self):
        path = self.card()
        path.write_text(path.read_text().replace('"id": "example-one",', '"id": "example-one", "id": "replacement",'))
        with self.assertRaisesRegex(catalog.CatalogError, 'duplicate JSON key'):
            catalog.load_cards(self.root)

    def test_non_json_constants_and_file_urls_are_rejected(self):
        path = self.card()
        path.write_text(path.read_text().replace('"related": []', '"related": [], "extra": NaN'))
        with self.assertRaisesRegex(catalog.CatalogError, 'non-JSON numeric constant'):
            catalog.load_cards(self.root)
        self.card(body=BODY + '\n[private](file:///private/tmp/private.md)\n')
        with self.assertRaisesRegex(catalog.CatalogError, 'unsupported Markdown link scheme'):
            catalog.load_cards(self.root)

    def test_card_identity_and_filename_agree(self):
        self.card(filename='different-name.md')
        with self.assertRaisesRegex(catalog.CatalogError, 'filename'):
            catalog.load_cards(self.root)

    def test_internal_links_and_symlinks_cannot_escape_portable_package(self):
        outside = self.root.parent / 'private.md'
        outside.write_text('outside package')
        self.card(body=BODY + '\n[private](../../../private.md)\n')
        with self.assertRaisesRegex(catalog.CatalogError, 'escapes package'):
            catalog.load_cards(self.root)
        path = self.card()
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaises(catalog.CatalogError):
            catalog.load_cards(self.root)

    def test_generated_destination_symlink_cannot_overwrite_another_file(self):
        self.card()
        victim = self.root.parent / 'victim.json'
        victim.write_text('unchanged')
        (self.root / 'library/index.json').symlink_to(victim)
        with self.assertRaises(catalog.CatalogError):
            catalog.build(self.root)
        self.assertEqual('unchanged', victim.read_text())

    def test_local_source_is_explicitly_local_only(self):
        m = metadata()
        m['sources'][0]['url'] = 'local:optional-user-reference'
        self.card(m)
        with self.assertRaisesRegex(catalog.CatalogError, 'local-only'):
            catalog.load_cards(self.root)
        m['availability'] = 'local-only'
        self.card(m)
        catalog.build(self.root)
        self.assertIn('local source', (self.root / 'library/index.md').read_text())

    def test_sources_and_evidence_are_searchable_with_explicit_match_fields(self):
        self.card()
        cards = catalog.load_cards(self.root)
        found = catalog.select(cards, self.args(query='example.org historical'))
        self.assertEqual(['sources'], found[0][1]['example.org'])
        self.assertEqual(['evidence'], found[0][1]['historical'])
        found = catalog.select(cards, self.args(query='example.org source-inspected'))
        self.assertEqual(['sources'], found[0][1]['example.org'])
        self.assertEqual(['evidence'], found[0][1]['source-inspected'])

    def test_clean_build_can_bootstrap_internal_links_to_generated_views(self):
        self.card(body=BODY + '\n[Browse related resources](../index.md)\n')
        catalog.build(self.root)
        catalog.build(self.root, check=True)
        self.assertTrue((self.root / 'library/index.md').is_file())

    def test_source_url_cannot_embed_credentials_or_control_characters(self):
        for url in ['https://user:secret@example.org/source', 'https://example.org/\nsource', 'https://[invalid']:
            with self.subTest(url=url):
                m = metadata()
                m['sources'][0]['url'] = url
                self.card(m)
                with self.assertRaises(catalog.CatalogError):
                    catalog.load_cards(self.root)

    def test_filters_use_all_query_terms_and_all_repeated_facet_values(self):
        self.card()
        other = metadata('example-two')
        other['summary'] = 'Explore quiet illustration.'
        other['facets']['tasks'] = ['explore']
        self.card(other, body=BODY.replace('Compare repeated operations', 'Explore unfamiliar material'))
        cards = catalog.load_cards(self.root)
        found = catalog.select(cards, self.args(query='compare correction', task=['compare', 'recover'], platform=['web']))
        self.assertEqual(['example-one'], [c['meta']['id'] for c, _ in found])
        self.assertIn('annotation', found[0][1]['correction'])
        self.assertFalse(catalog.select(cards, self.args(query='compare illustration')))
        self.assertFalse(catalog.select(cards, self.args(task=['compare', 'explore'])))
        self.assertEqual(2, len(catalog.select(cards, self.args(kind=['example', 'tool']))))

    def test_relocated_copy_runs_without_original_repository_or_dependencies(self):
        self.card()
        catalog.build(self.root)
        relocated = self.root.parent / 'relocated'
        shutil.copytree(self.root, relocated)
        shutil.rmtree(self.root)
        result = subprocess.run([sys.executable, '-B', str(relocated / 'scripts/catalog.py'), 'find', 'correction', '--json'],
                                cwd=self.root.parent, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual('example-one', json.loads(result.stdout)[0]['id'])
        shown = subprocess.run([sys.executable, '-B', str(relocated / 'scripts/catalog.py'), 'show', '../private'],
                               capture_output=True, text=True)
        self.assertEqual(1, shown.returncode)
        self.assertIn('not a path', shown.stderr)

    def test_facet_summary_discovers_exact_filter_vocabulary(self):
        self.card()
        self.card(metadata('example-two', status='candidate'))
        result = subprocess.run([sys.executable, '-B', str(self.root / 'scripts/catalog.py'),
                                 'facets', '--status', 'curated', '--json'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(1, summary['resource_count'])
        self.assertEqual({'compare': 1, 'recover': 1}, summary['facets']['tasks'])
        self.assertEqual({}, summary['facets']['character'])

    def test_malformed_metadata_reports_error_instead_of_type_traceback(self):
        m = metadata()
        m['evidence']['freshness'] = ['historical']
        self.card(m)
        result = subprocess.run([sys.executable, '-B', str(self.root / 'scripts/catalog.py'), 'validate'],
                                capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        self.assertIn('freshness', result.stderr)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
