# azet

An AI coding agent in your terminal. One brew command installs it.

```sh
brew install azet-llc/tap/azet
cd your-project && azet
```

Free credit on the first run is opening soon. Until then, add credit at https://api.azet.io/#credits and run `AZET_API_KEY=azk_... azet` (the key is saved to `~/.config/azet` by `npx azet-ai login azk_...`).

![azet demo: brew install to first result in 44.6s on a clean Mac account](docs/azet-demo.gif)

- Models: DeepSeek V4.1 Flash (default), Kimi K2.6, DeepSeek V4 Pro. Switch with `/model`.
- One-shot: `azet -p "fix the failing test"`.
- Shell commands that delete files, push or publish, send data off your machine, or use sudo ask before they run (blocked in `-p` mode).
- Sandbox on by default (macOS `sandbox-exec`): the agent and its commands can write only inside the folder you started in, `~/.config/azet`, temp folders and package caches, and cannot read secrets (~/.ssh, ~/.aws and other logins, the keychain, `.env` files). Off: `azet --no-sandbox` or `AZET_SANDBOX=0`.
- Started in your home folder or `/`, azet asks for a work folder first.
- Config lives in `~/.config/azet` and never touches other tools' settings.

The agent is our build of [Pi](https://github.com/earendil-works/pi) by Mario Zechner (MIT, see `LICENSE-pi`; patches in `agent-build/`; bundled packages and the Bun runtime in `THIRD_PARTY_NOTICES.md`); `azet` is a small launcher that wires it to AZET AI API.

MIT © AZET LLC
