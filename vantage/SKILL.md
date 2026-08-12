# Vantage Skill

You are running the **Vantage** research skill. When the user asks for recent social / community signal research on a person, company, product, technology, or topic, use this skill.

## When to use

- “What’s the community saying about X lately?”
- “Research [company/product] from the last 30 days”
- “Show me high-engagement posts about Y”
- Competitive or product pulse checks

## How to invoke

Run the CLI tool (must be installed in the environment):

```bash
vantage research "<topic>" --days 30 --sources all
```

Useful flags:
- `--days N`          look-back window
- `--sources reddit|hackernews|github|devto|all`
- `--max N`           results per source
- `-o DIR`            output directory for .md + .html briefs

## Contract

1. Always pass the user’s topic exactly (or a cleaned version of it).
2. Prefer `--days 30` unless the user specifies otherwise.
3. After the command finishes, open the generated `.md` or `.html` file and present the summary + top signals to the user.
4. Do not invent engagement numbers — only report what Vantage returned.
5. If a source fails (e.g. Reddit 403 from a datacenter IP), note it and continue with the other sources.

## Output shape the user expects

- Short summary of what the community is talking about
- Ranked list of high-engagement items with links
- Themes if any
- Paths to the full Markdown and dark-mode HTML briefs

Vantage ranks purely by engagement (upvotes / points / stars). It is not a general web search engine.
