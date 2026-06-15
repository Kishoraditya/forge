# Turn Files

This folder stores crash-recovery notes for agent sessions.

Use one zero-padded turn number per response:
- `Turn-00-start.md`
- `Turn-00-stop.md`
- `Turn-01-start.md`
- `Turn-01-stop.md`

The start file is the first repo action in a response. The stop file is the last
repo action in a response. When resuming after a crash, read the newest file in
this folder first.
