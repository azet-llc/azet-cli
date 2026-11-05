# azet

An AI coding agent in your terminal. No account and no key needed to start.

```sh
brew install azet-llc/tap/azet
cd your-project && azet
```

The first run gets a small free trial credit from [AZET AI API](https://api.azet.io). When it runs out, add credit at https://api.azet.io/#credits, or bring your own key: `AZET_API_KEY=azk_... azet`.

- Models: DeepSeek V4.1 Flash (default), Kimi K2.6, DeepSeek V4 Pro. Switch with `/model`.
- One-shot: `azet -p "fix the failing test"`.
- Config lives in `~/.config/azet` and never touches other tools' settings.

The agent is [Pi](https://github.com/earendil-works/pi) by Mario Zechner (MIT, see `LICENSE-pi`); `azet` is a small launcher that wires it to AZET AI API.

MIT © AZET LLC
