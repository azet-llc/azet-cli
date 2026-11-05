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
- Config lives in `~/.config/azet` and never touches other tools' settings.

The agent is [Pi](https://github.com/earendil-works/pi) by Mario Zechner (MIT, see `LICENSE-pi`); `azet` is a small launcher that wires it to AZET AI API.

MIT © AZET LLC
