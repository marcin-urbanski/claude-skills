---
type: llm
focus: { source: file, path: index.html }
---
PASS if both project links (Claude Skills, to github.com/marcin-urbanski/claude-skills, and TimeRabbit, to gettimerabbit.com) have target="_blank" and a rel attribute that includes noopener, and the three nav links (/, /about.html, /writing/) have no target attribute. FAIL otherwise.
