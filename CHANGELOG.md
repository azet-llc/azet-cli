# azet changelog

## 0.3.1 (2026-11-06)
- `azet --help-all` works before you have a key; `azet --version` shows only azet's version.

## 0.3.0 (2026-11-06)
- azet's own build of the agent: azet's name on every screen, and no commands that send your session to outside services (/share, /bug, /login, /logout are gone; /bug links to our GitHub issues).
- Reads skills only from azet's folders (~/.config/azet/agent/skills and a project's .azet/skills), not from other tools' shared folders.
- Says "azet by AZET LLC" when asked who it is.

## 0.2.1 (2026-11-06)
- The azet header on every start, also when a signal ends the session.

## 0.2.0 (2026-11-06)
- Shell commands that delete files, push or publish, send data off the machine, or use sudo ask first (blocked in -p mode).

## 0.1.0 (2026-11-05)
- First release: `brew install azet-llc/tap/azet`, models from AZET AI API.
