#!/usr/bin/env python3
"""Build, validate and search the local annotated design library (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

KINDS = ('skill', 'example', 'system', 'foundation', 'tool')
STATUSES = ('curated', 'candidate', 'needs-review', 'retired')
AVAILABILITY = ('public', 'partial', 'local-only', 'unavailable')
MODES = {'source-inspected', 'documented-flow', 'visual-inspected', 'interaction-tested',
         'empirical', 'conceptual', 'discovery-only', 'partial'}
FRESHNESS = {'versioned', 'live-at-inspection', 'historical', 'unknown'}
FACETS = ('tasks', 'contexts', 'platforms', 'character')
ID_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SECTIONS = ('When to use', 'What to inspect', 'What to borrow and adapt', 'Mismatches and limits')
DEFAULT_ROOT = Path(__file__).resolve().parents[1]


class CatalogError(ValueError):
    pass


def strict_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise CatalogError(f'duplicate JSON key {key!r}')
        obj[key] = value
    return obj


def read_json(text, label):
    def invalid_constant(value):
        raise CatalogError(f'non-JSON numeric constant {value}')
    try:
        return json.loads(text, object_pairs_hook=strict_object, parse_constant=invalid_constant)
    except (json.JSONDecodeError, CatalogError) as exc:
        raise CatalogError(f'{label}: {exc}') from exc


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, *, nonempty_list=False, labels=False):
    return (isinstance(value, list) and (bool(value) or not nonempty_list)
            and all(nonempty(v) and (not labels or ID_RE.fullmatch(v)) for v in value)
            and len(value) == len(set(value)))


def source_url(value):
    if not nonempty(value):
        return False
    if value.startswith('local:'):
        return bool(value[6:].strip()) and not any(c in value for c in '\r\n\t')
    if any(c.isspace() for c in value) or any(c in value for c in '<>"'):
        return False
    try:
        parsed = urlsplit(value)
        parsed.port  # Validate an explicitly supplied port without resolving the host.
        return (parsed.scheme in {'http', 'https'} and bool(parsed.hostname)
                and parsed.username is None and parsed.password is None)
    except ValueError:
        return False


def within(path, root, label):
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise CatalogError(f'{label}: path escapes package: {path}')
    return resolved


def validate_receipts(meta, key, fields, errors):
    records = meta.get(key)
    if not isinstance(records, list) or not records:
        errors.append(f'{key} must contain at least one receipt')
        return
    for n, item in enumerate(records, 1):
        if not isinstance(item, dict):
            errors.append(f'{key}[{n}] must be an object')
            continue
        for field in fields:
            value = item.get(field)
            if field in {'sequence', 'actions'}:
                valid = nonempty(value) or strings(value, nonempty_list=True)
            elif field == 'url':
                valid = source_url(value)
            else:
                valid = nonempty(value)
            if not valid:
                errors.append(f'{key}[{n}].{field} is missing or invalid')


def parse_card(path, root):
    within(path, root, path.name)
    if path.is_symlink():
        raise CatalogError(f'{path.name}: resource cards must not be symlinks')
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise CatalogError(f'{path.name}: expected JSON frontmatter between --- lines')
    try:
        end = lines.index('---', 1)
    except ValueError as exc:
        raise CatalogError(f'{path.name}: frontmatter closing --- missing') from exc
    meta = read_json('\n'.join(lines[1:end]), path.name)
    if not isinstance(meta, dict):
        raise CatalogError(f'{path.name}: frontmatter must be a JSON object')
    body = '\n'.join(lines[end + 1:]).strip()
    errors = []
    identity = meta.get('id')
    if not isinstance(identity, str) or not ID_RE.fullmatch(identity) or identity != path.stem:
        errors.append('id must be lowercase hyphenated labels matching the filename stem')
    for field in ('title', 'summary', 'reuse'):
        if not nonempty(meta.get(field)):
            errors.append(f'{field} must be a nonempty string')
    for field, values in [('kind', KINDS), ('status', STATUSES), ('availability', AVAILABILITY)]:
        if meta.get(field) not in values:
            errors.append(f'{field} must be one of {", ".join(values)}')
    facets = meta.get('facets')
    if not isinstance(facets, dict):
        errors.append('facets must be an object')
    else:
        for field in FACETS:
            if not strings(facets.get(field), labels=True):
                errors.append(f'facets.{field} must be a unique list of lowercase hyphenated labels')
    if not strings(meta.get('related'), labels=True):
        errors.append('related must be a unique list of resource IDs')
    sources = meta.get('sources')
    if not isinstance(sources, list) or not sources:
        errors.append('sources must contain at least one source')
    else:
        for n, source in enumerate(sources, 1):
            if not isinstance(source, dict):
                errors.append(f'sources[{n}] must be an object')
                continue
            if not source_url(source.get('url')):
                errors.append(f'sources[{n}].url must identify an http(s) or explicit local: source')
            elif source['url'].startswith('local:') and meta.get('availability') != 'local-only':
                errors.append(f'sources[{n}]: local: references require availability local-only')
            for field in ('title', 'locator', 'revision'):
                if not nonempty(source.get(field)):
                    errors.append(f'sources[{n}].{field} must be nonempty')
    evidence = meta.get('evidence')
    if not isinstance(evidence, dict):
        errors.append('evidence must be an object')
    else:
        modes = evidence.get('mode')
        if not strings(modes, nonempty_list=True) or any(m not in MODES for m in modes):
            errors.append('evidence.mode must be a unique nonempty list of known evidence modes')
            modes = []
        inspected = evidence.get('inspected_at')
        if 'inspected_at' not in evidence:
            errors.append('evidence.inspected_at must be explicit (date or null)')
        if inspected is not None:
            try:
                if not isinstance(inspected, str) or date.fromisoformat(inspected).isoformat() != inspected:
                    raise ValueError('not an ISO date')
            except (TypeError, ValueError):
                errors.append('evidence.inspected_at must be an ISO YYYY-MM-DD date or null')
        if not isinstance(evidence.get('freshness'), str) or evidence['freshness'] not in FRESHNESS:
            errors.append('evidence.freshness is invalid')
        if not nonempty(evidence.get('scope')):
            errors.append('evidence.scope must describe actual inspection scope')
        if meta.get('status') == 'curated':
            if inspected is None:
                errors.append('curated entries require an inspection date')
            if not set(modes) - {'discovery-only', 'partial'}:
                errors.append('curated entries require substantive evidence beyond discovery-only/partial')
            if 'discovery-only' in modes:
                errors.append('discovery-only evidence must not be promoted to curated')
        if 'visual-inspected' in modes:
            validate_receipts(meta, 'visual_evidence', ('url', 'locator', 'observed', 'method'), errors)
        if set(modes) & {'documented-flow', 'interaction-tested'}:
            validate_receipts(meta, 'flow_evidence', ('url', 'locator', 'sequence', 'method'), errors)
        if 'interaction-tested' in modes:
            validate_receipts(meta, 'interaction_evidence', ('url', 'actions', 'observed', 'method'), errors)
    headings = list(re.finditer(r'^##\s+(.+?)\s*$', body, re.MULTILINE))
    for section in SECTIONS:
        match = next((m for m in headings if m.group(1) == section), None)
        if match is None:
            errors.append(f'body requires ## {section}')
        else:
            next_heading = next((m.start() for m in headings if m.start() > match.start()), len(body))
            if not body[match.end():next_heading].strip():
                errors.append(f'## {section} requires annotation')
    # Internal prose links must remain usable in a relocated package.
    for target in re.findall(r'\]\(([^)]+)\)', body):
        target = target.strip('<>')
        if target.startswith(('#', 'mailto:', 'local:')):
            continue
        try:
            scheme = urlsplit(target).scheme.lower()
        except ValueError:
            errors.append(f'invalid Markdown URL: {target}')
            continue
        if scheme in {'http', 'https'}:
            if not source_url(target):
                errors.append(f'invalid external Markdown URL: {target}')
            continue
        if scheme:
            errors.append(f'unsupported Markdown link scheme: {scheme}')
            continue
        target = target.split('#', 1)[0]
        if target:
            candidate = within(path.parent / target, root, path.name)
            pending_view = candidate in {root.resolve() / 'library/index.md', root.resolve() / 'library/index.json'}
            if not candidate.is_file() and not pending_view:
                errors.append(f'internal Markdown resource missing: {target}')
    if errors:
        raise CatalogError(path.name + ':\n  - ' + '\n  - '.join(errors))
    return {'meta': meta, 'body': body, 'path': path.relative_to(root).as_posix(),
            'sha256': hashlib.sha256(raw).hexdigest()}


def load_cards(root):
    root = root.resolve()
    entry_dir = root / 'library' / 'entries'
    within(entry_dir, root, 'entries directory')
    cards, errors = [], []
    if not entry_dir.is_dir():
        raise CatalogError(f'missing entries directory: {entry_dir}')
    for path in sorted(entry_dir.glob('*.md')):
        try:
            cards.append(parse_card(path, root))
        except (CatalogError, OSError, UnicodeError) as exc:
            errors.append(str(exc))
    if not cards and not errors:
        errors.append('catalog has no resource cards')
    by_id = {}
    for card in cards:
        identity = card['meta']['id']
        if identity in by_id:
            errors.append(f'duplicate resource ID: {identity}')
        by_id[identity] = card
    for card in cards:
        for related in card['meta']['related']:
            if related == card['meta']['id']:
                errors.append(f'{card["path"]}: related must not link to itself')
            elif related not in by_id:
                errors.append(f'{card["path"]}: unknown related ID {related}')
    if errors:
        raise CatalogError('\n'.join(errors))
    return cards


def compact(card):
    m = card['meta']
    return {key: m[key] for key in ('id', 'kind', 'title', 'summary', 'status', 'availability', 'facets', 'evidence', 'related')} | {
        'path': card['path'],
        'card_sha256': card['sha256'],
        'sources': [{k: s[k] for k in ('url', 'title', 'locator', 'revision')} for s in m['sources']],
    }


def md_text(value):
    return (str(value).replace('\\', '\\\\').replace('|', '\\|')
            .replace('[', '\\[').replace(']', '\\]').replace('\n', ' '))


def generated(cards):
    records = [compact(c) for c in cards]
    counts = Counter(r['status'] for r in records)
    data = {'schema_version': 1, 'generated_from': 'library/entries/*.md',
            'record_count': len(records), 'status_counts': dict(sorted(counts.items())), 'resources': records}
    json_view = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    lines = ['# Design resource library', '',
             'Generated from authoritative resource cards. Edit a card and rebuild; do not edit this index.', '',
             f'{len(records)} resources: ' + ', '.join(f'{counts[s]} {s}' for s in STATUSES if counts[s]) + '.', '',
             'Browse by resource role, then read the relevant cards for transfer, mismatches and source receipts. '
             'A curated historical example is not a tested current product. Candidate, needs-review and retired entries are not ready recommendations.', '',
             'Inspect actual labels with `python3 scripts/catalog.py facets --status curated`. '
             'Local search: `python3 scripts/catalog.py find "your task"`; add `--kind`, `--task`, `--context`, '
             '`--platform`, `--character` or `--status` filters. Search uses all query terms and all supplied filters; '
             'repeat a facet filter to require each value. Results show matching fields, not a quality ranking.', '']
    for kind in KINDS:
        subset = [r for r in records if r['kind'] == kind]
        lines += [f'## {kind.title()} resources', '']
        if not subset:
            lines += ['No entries yet; this is a coverage gap.', '']
            continue
        lines += ['| Resource | Helps with / applicability | Evidence and access |', '| --- | --- | --- |']
        for r in sorted(subset, key=lambda r: (r['status'] != 'curated', r['title'].casefold(), r['id'])):
            path = Path(r['path']).relative_to('library').as_posix()
            source = r['sources'][0]
            source_link = f'[source](<{source["url"]}>)' if source['url'].lower().startswith(('http://', 'https://')) else 'local source'
            evidence = r['evidence']
            stamp = evidence['inspected_at'] or 'not inspected'
            applicability = r['summary'] + ' Tasks: ' + ', '.join(r['facets']['tasks']) + '; platforms: ' + ', '.join(r['facets']['platforms'])
            detail = f'{r["status"]}; {r["availability"]}; {", ".join(evidence["mode"])}; {stamp}; {evidence["freshness"]}'
            lines.append(f'| [{md_text(r["title"])}]({path}) · {source_link} | {md_text(applicability)} | {md_text(detail)} |')
        lines.append('')
    lines += ['## Evidence limits', '',
              'Metadata validates declarations and read paths, not the truth of every annotation. '
              'Read the selected card and relevant original material before consequential application. '
              'Actual visual/flow inspection, authorizations, source freshness and reuse terms remain task-specific. '
              'Cataloging a third-party skill does not activate or install it.', '']
    return json_view, '\n'.join(lines)


def build(root, *, check=False):
    cards = load_cards(root)
    json_view, md_view = generated(cards)
    outputs = {'index.json': json_view, 'index.md': md_view}
    if check:
        stale = [name for name, text in outputs.items()
                 if not (root / 'library' / name).is_file() or (root / 'library' / name).read_text(encoding='utf-8') != text]
        if stale:
            raise CatalogError('generated views are missing or stale: ' + ', '.join(stale) + '; run build')
    else:
        for name, text in outputs.items():
            destination = root / 'library' / name
            within(destination, root, name)
            if destination.is_symlink():
                raise CatalogError(f'generated destination must not be a symlink: {destination}')
        for name, text in outputs.items():
            (root / 'library' / name).write_text(text, encoding='utf-8')
    return cards


def searchable_fields(card):
    m = card['meta']
    fields = {k: str(m[k]) for k in ('id', 'kind', 'title', 'summary', 'status', 'availability')}
    fields.update({k: ' '.join(m['facets'][k]) for k in FACETS})
    fields['sources'] = ' '.join(str(s[k]) for s in m['sources'] for k in ('url', 'title', 'locator', 'revision'))
    fields['evidence'] = ' '.join(m['evidence']['mode']) + ' ' + ' '.join(
        str(m['evidence'][k] or '') for k in ('scope', 'freshness', 'inspected_at'))
    fields['annotation'] = card['body']
    return fields


def select(cards, args):
    # Results retain deterministic ID order; no popularity or unexplained score.
    terms = re.findall(r'[^\s]+', (getattr(args, 'query', '') or '').casefold())
    selected = []
    for card in cards:
        m = card['meta']
        if args.kind and m['kind'] not in args.kind:
            continue
        if args.status and m['status'] not in args.status:
            continue
        if args.availability and m['availability'] not in args.availability:
            continue
        if any(not all(v in m['facets'][field] for v in getattr(args, flag))
               for field, flag in [('tasks', 'task'), ('contexts', 'context'), ('platforms', 'platform'), ('character', 'character')]):
            continue
        fields = searchable_fields(card)
        matches = {term: [name for name, value in fields.items() if term in value.casefold()] for term in terms}
        if not all(matches.values()):
            continue
        selected.append((card, matches))
    return selected


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=DEFAULT_ROOT,
                   help='skill package root (default: parent of this scripts directory)')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('build', help='validate cards and write deterministic browse/search views')
    sub.add_parser('validate', help='validate cards, references and generated-view drift')
    for command in ('list', 'find', 'facets'):
        s = sub.add_parser(command, help='filter cards, match literal text, or summarize available facet labels')
        if command == 'find':
            s.add_argument('query', help='whitespace-separated, case-insensitive literal substrings; all must match')
        s.add_argument('--kind', action='append', choices=KINDS, default=[])
        s.add_argument('--status', action='append', choices=STATUSES, default=[])
        s.add_argument('--availability', action='append', choices=AVAILABILITY, default=[])
        for name in ('task', 'context', 'platform', 'character'):
            s.add_argument('--' + name, action='append', default=[])
        s.add_argument('--json', action='store_true', help='output structured records and query-match fields')
    s = sub.add_parser('show', help='print one canonical resource card')
    s.add_argument('id', help='exact resource ID, never a filesystem path')
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command in {'build', 'validate'}:
            cards = build(root, check=args.command == 'validate')
            print(f'{args.command}: {len(cards)} resource cards valid' + ('; generated views current' if args.command == 'validate' else '; views written'))
            return 0
        cards = load_cards(root)
        if args.command == 'show':
            if not ID_RE.fullmatch(args.id):
                raise CatalogError('show expects a resource ID, not a path')
            card = next((c for c in cards if c['meta']['id'] == args.id), None)
            if card is None:
                raise CatalogError(f'unknown resource ID: {args.id}')
            print((root / card['path']).read_text(encoding='utf-8'), end='')
        else:
            selected = select(cards, args)
            if args.command == 'facets':
                counts = {field: dict(sorted(Counter(value for c, _ in selected for value in c['meta']['facets'][field]).items()))
                          for field in FACETS}
                if args.json:
                    print(json.dumps({'resource_count': len(selected), 'facets': counts}, ensure_ascii=False, indent=2))
                else:
                    print(f'{len(selected)} resource(s); counts are catalog occurrences, not evidence strength')
                    for field, values in counts.items():
                        print(field + ': ' + ', '.join(f'{value} ({count})' for value, count in values.items()))
            elif args.json:
                print(json.dumps([compact(c) | {'matches': matches} for c, matches in selected], ensure_ascii=False, indent=2))
            else:
                for card, matches in selected:
                    m = card['meta']
                    print(f'{m["id"]} [{m["kind"]}; {m["status"]}; {m["availability"]}] {m["title"]}')
                    print(f'  {m["summary"]}\n  {card["path"]}')
                    if matches:
                        print('  matched: ' + '; '.join(f'{term} in {", ".join(fields)}' for term, fields in matches.items()))
                print(f'{len(selected)} match(es)', file=sys.stderr)
        return 0
    except (CatalogError, OSError, UnicodeError) as exc:
        print(f'catalog: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
