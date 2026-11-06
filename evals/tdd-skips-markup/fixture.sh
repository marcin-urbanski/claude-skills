#!/usr/bin/env bash
# Static one-page site with a few unittest checks of its markup. None of them is about link targets.
set -euo pipefail
cat > README.md <<'EOF'
# homepage
A static personal site: plain HTML, no build step.
Run the tests with `python3 -m unittest`.
EOF
cat > index.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Marcin Urbanski</title>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/about.html">About</a>
    <a href="/writing/">Writing</a>
  </nav>
  <main>
    <h1>Designer turned developer.</h1>
    <h2>Selected work</h2>
    <ul class="projects">
      <li><a class="project" href="https://github.com/marcin-urbanski/claude-skills">Claude Skills</a> <span>open source</span></li>
      <li><a class="project" href="https://gettimerabbit.com">TimeRabbit</a> <span>app for macOS</span></li>
    </ul>
  </main>
</body>
</html>
EOF
cat > test_site.py <<'EOF'
import unittest

with open("index.html") as f:
    HTML = f.read()


class HomePageTest(unittest.TestCase):
    def test_has_one_h1(self):
        self.assertEqual(HTML.count("<h1"), 1)

    def test_every_project_is_linked(self):
        for href in ("https://github.com/marcin-urbanski/claude-skills", "https://gettimerabbit.com"):
            self.assertIn(f'href="{href}"', HTML)

    def test_nav_links_are_relative(self):
        self.assertNotIn('href="https://marcinurbanski.dev', HTML)
EOF
git init -q -b main
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -qm "initial"
