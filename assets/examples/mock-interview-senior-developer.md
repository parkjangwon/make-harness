# Mock Interview: senior developer

This example shows how the same `make-harness` one-time setup can stay precise for a senior developer without changing the underlying philosophy.

Goal:
- confirm durable rules quickly
- allow explicit overrides instead of forcing defaults
- keep the interview compact while preserving precision

Context:
- existing repository
- package scripts and code structure already exist
- the developer wants precise control over approval and definition of done
- this follows the repo-first path, where the agent confirms only what code cannot settle

## Transcript

Agent: This is a one-time setup. I inspected the repo first, so I’ll mostly confirm the durable rules that are not obvious from code.

Agent: From the current structure, would it make sense to treat this project as a web app?
User: Yes, but note that the admin dashboard and public site live together.

Agent: Got it. I’ll keep `webapp` as the main type and add a note instead of inventing a new category.

Agent: From the README and config, `pnpm test` looks like the default verification command. Should I use that?
User: Yes. For lint use `pnpm lint`, and please override the default build command to `pnpm build:prod`.

Agent: Great. I’ll keep those exact commands.

Agent: Would it be okay to treat passing tests and lint as the default definition of done?
User: Not always. For content-only changes, a manual check is enough. For code changes, tests and lint are required.

Agent: Understood. I’ll store the default definition of done conservatively and add a note about the content-change override.

Agent: For larger changes, should I check with you first, while safe edits can go through directly? If you're unsure, I can default to confirming only risky changes first.
User: Keep approval explicit for risky changes. Safe fixes can go through directly.

Agent: Perfect. I’ll keep that approval default and preserve your override notes.

## Why this is good for seniors

- it respects repo-first inference
- it keeps defaults visible but easy to override
- it allows precise approval and definition of done rules
- it preserves exact commands like `pnpm test`
- it does not force a simplistic wizard when the developer already knows what they want

## Important note

This is the same one-time setup skill as the junior example.
The difference is that the senior path uses more precise overrides, not a different harness philosophy.
