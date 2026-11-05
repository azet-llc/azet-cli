# azet-agent build

azet-agent is Pi v1.5.0 (MIT, https://github.com/earendil-works/pi) with three small patches, built the same way Pi builds its release binaries.

```sh
git clone --depth 1 --branch v1.5.0 https://github.com/earendil-works/pi.git && cd pi
python3 ../agent-build/patch-1-commands.py packages/coding-agent/src   # drop /share /bug /login /logout and two easter eggs
python3 ../agent-build/patch-2-skills.py packages/coding-agent/src     # do not read ~/.agents/skills or .agents/skills
sed -i 's#or \.pi/mcp\.json\.#or .azet/mcp.json.#g' packages/coding-agent/src/extensions/mcp/index.ts packages/coding-agent/src/extensions/mcp/cli.ts
bash scripts/build-binaries.sh --platform darwin-arm64            # bun 1.4.4; also darwin-x64
```

Then in the release folder: rename `pi` to `azet-agent`, set `"piConfig": {"name": "azet", "configDir": ".azet"}` in `package.json`, replace `CHANGELOG.md` with azet's, and add `LICENSE-pi` and `THIRD_PARTY_NOTICES.md` (made by `python3 agent-build/notices.py <pi> <bun LICENSE.md> THIRD_PARTY_NOTICES.md`; texts for packages that ship no license file are in `agent-build/upstream-licenses/`).
