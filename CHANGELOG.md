# azet changelog

## 0.5.0 (2026-11-06)
- Started in your home folder or /, azet asks for a work folder first (Enter = ~/azet-work); without a terminal it stops with a message.
- The sandbox also blocks reading secrets: ~/.ssh, ~/.gnupg, ~/.aws, ~/.azure, ~/.kube, gcloud and gh logins, ~/.docker/config.json, ~/.netrc, ~/.git-credentials, azet's key file, the keychain, and .env files anywhere (.env.example and similar templates stay readable).
- Upstream license texts for the bundled packages that ship none are kept in agent-build/upstream-licenses, including the MIT text for standardwebhooks.

## 0.4.0 (2026-11-06)
- Sandbox on by default (macOS): the agent and every command it runs can write only inside the folder you started in, ~/.config/azet, temp folders and package caches. `azet --no-sandbox` or `AZET_SANDBOX=0` turns it off.
- THIRD_PARTY_NOTICES.md: license texts for every package bundled in the agent and for the Bun runtime, in the repo and next to the agent.

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
