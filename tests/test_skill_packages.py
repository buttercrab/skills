"""Check discovery and resource integrity; behavior is evaluated with real agent trials."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
EXPECTED = {
    'audit-technical-work', 'refactor-by-invariant', 'propagate-contract-changes',
    'write-task-handoff', 'research-with-evidence', 'responsive-coordinator',
}

class SkillPackageTests(unittest.TestCase):
    def test_only_six_installable_skills(self):
        self.assertEqual({p.parent.name for p in SKILLS.glob('*/SKILL.md')}, EXPECTED)
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, EXPECTED)

    def test_metadata_and_explicit_coordinator_policy(self):
        for name in EXPECTED:
            with self.subTest(skill=name):
                directory = SKILLS / name
                text = (directory / 'SKILL.md').read_text()
                match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
                self.assertIsNotNone(match)
                metadata = yaml.safe_load(match.group(1))
                self.assertEqual(metadata['name'], name)
                self.assertTrue(metadata['description'].strip())
                agent = yaml.safe_load((directory / 'agents/openai.yaml').read_text())
                interface = agent['interface']
                self.assertTrue(interface['display_name'])
                self.assertTrue(25 <= len(interface['short_description']) <= 64)
                self.assertIn(f'${name}', interface['default_prompt'])
                implicit = agent.get('policy', {}).get('allow_implicit_invocation', True)
                self.assertIs(implicit, name != 'responsive-coordinator')

    def test_linked_local_resources_resolve(self):
        for name in EXPECTED:
            directory = SKILLS / name
            for path in directory.rglob('*.md'):
                for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if '://' in target or target.startswith('#'):
                        continue
                    with self.subTest(file=str(path), target=target):
                        resource = (path.parent / target.split('#', 1)[0]).resolve()
                        self.assertTrue(resource.is_file())
                        self.assertTrue(resource.is_relative_to(directory.resolve()))

    def test_retired_tools_are_not_discoverable_skills(self):
        for directory in ('integrations', 'legacy', 'tools'):
            self.assertFalse(list((ROOT / directory).rglob('SKILL.md')))

if __name__ == '__main__':
    unittest.main()
