# Claude Code skills

Skills for [Claude Code](https://claude.com/claude-code), mostly for embedded
systems and electronics work.

| Skill | What it does |
|-------|--------------|
| [esp32](skills/esp32) | ESP32-family firmware (ESP32, S3, C3, C6, P4) with ESP-IDF / Arduino-ESP32: target detection, per-chip pin rules, IDF 5.x drivers, build/flash/crash decoding, GPIO checker |

## Installing a skill

Each folder under `skills/` is a self-contained skill. Copy the one you want
into your skills folder:

```bash
git clone https://github.com/giltal/claude-skills
cp -r claude-skills/skills/esp32 ~/.claude/skills/          # personal, all projects
cp -r claude-skills/skills/esp32 <project>/.claude/skills/  # one project, shared via its repo
```

On Windows, the personal skills folder is `%USERPROFILE%\.claude\skills\`.

To keep up to date, symlink (Linux/macOS: `ln -s`) or junction
(Windows: `mklink /J`) the skill folder instead of copying it, then
`git pull` the repo.

## Local settings

A skill may read an optional `local.md` next to its `SKILL.md`, for
machine-specific details such as tool install paths. These files are
git-ignored.

## Contributing

Corrections and new chips or skills are welcome. Open an issue or a pull request.
