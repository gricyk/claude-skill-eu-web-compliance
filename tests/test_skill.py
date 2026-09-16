import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class SkillManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read("SKILL.md")
        match = re.match(r"^---\n(.*?)\n---\n", cls.text, re.DOTALL)
        assert match, "SKILL.md must start with YAML frontmatter"
        cls.frontmatter = dict(
            (k.strip(), v.strip().strip('"')) for k, v in
            (line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
        )

    def test_name(self):
        name = self.frontmatter.get("name", "")
        self.assertRegex(name, r"^[a-z0-9-]{1,64}$")
        self.assertEqual(name, "eu-web-compliance")

    def test_description_within_limit(self):
        description = self.frontmatter.get("description", "")
        self.assertTrue(description)
        self.assertLessEqual(len(description), 1024)
        self.assertNotIn("<", description)

    def test_referenced_files_exist(self):
        corpus = self.text + read("README.md")
        paths = set(re.findall(r"`((?:references|scripts)/[\w./-]+\.(?:md|py))`", corpus))
        self.assertTrue(paths)
        for rel in paths:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, rel)), f"missing: {rel}")

    def test_every_template_is_listed_in_readme(self):
        readme = read("README.md")
        for fn in os.listdir(os.path.join(ROOT, "references", "templates")):
            self.assertIn(fn, readme)


if __name__ == "__main__":
    unittest.main()
