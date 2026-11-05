# azet-agent 바이너리에 묶이는 서드파티 고지 모음: coding-agent 의 런타임 의존 트리(npm ls --omit=dev) + 소스에 들어온 사본(LICENSES 폴더) + Bun 런타임.
# 사용: python3 notices.py <pi-src> <bun LICENSE 파일> <출력.md> [upstream-licenses 폴더]
import json, os, subprocess, sys
root, bun_license, out = sys.argv[1:4]
upl = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "upstream-licenses")
# --parseable = every installed package path in the production tree (the --json walk missed deduped branches)
paths = subprocess.run(["npm", "ls", "--omit=dev", "--all", "--parseable", "-w", "packages/coding-agent"],
                       cwd=root, capture_output=True, text=True).stdout.split()
pkgs = {}
for path in paths:
    try:
        pj = json.load(open(os.path.join(path, "package.json")))
    except (OSError, ValueError):
        continue
    lic = pj.get("license") or ""
    if isinstance(lic, dict):
        lic = lic.get("type", "")
    pkgs.setdefault((pj.get("name", os.path.basename(path)), pj.get("version", "")), (lic, os.path.realpath(path)))
def license_text(path):
    # every LICENSE / COPYING / NOTICE file (Apache-2.0 requires passing NOTICE on)
    texts = [open(os.path.join(path, f), errors="replace").read().strip() for f in sorted(os.listdir(path))
             if f.upper().startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE")) and os.path.isfile(os.path.join(path, f))]
    return "\n\n".join(texts) or None
lines = ["# Third-party notices for azet-agent", "",
         "azet-agent is a build of Pi (MIT, Copyright (c) 2025 Mario Zechner, see LICENSE-pi) compiled with Bun.",
         "It includes the software listed below. Each is used under its license, reproduced here.", "",
         "## Source and rebuilding", "",
         "Everything in this executable can be rebuilt from public source, including with a modified JavaScriptCore (LGPL-2, see the Bun section):",
         "- Pi v1.5.0: https://github.com/earendil-works/pi/tree/v1.5.0",
         "- azet's patches and build steps: https://github.com/azet-llc/azet-cli/tree/main/agent-build",
         "- Bun bun-v1.4.4: https://github.com/oven-sh/bun/tree/bun-v1.4.4 (its JavaScriptCore build: https://github.com/oven-sh/WebKit)",
         "Build Bun from source with your changes, then run the steps in agent-build/README.md with that bun.", ""]
first_party = ("@earendil-works/", "pi-monorepo")
# packages whose npm tarball ships no license file: the upstream repository's text
UPSTREAM = {  # files in agent-build/upstream-licenses (see its README for sources)
    "@aws-sdk/credential-provider-http": (["aws-sdk-js-v3-Apache-2.0.txt"], "https://github.com/aws/aws-sdk-js-v3/blob/main/LICENSE"),
    "@aws-sdk/credential-provider-login": (["aws-sdk-js-v3-Apache-2.0.txt"], "https://github.com/aws/aws-sdk-js-v3/blob/main/LICENSE"),
    "@aws-sdk/nested-clients": (["aws-sdk-js-v3-Apache-2.0.txt"], "https://github.com/aws/aws-sdk-js-v3/blob/main/LICENSE"),
    "data-uri-to-buffer": (["data-uri-to-buffer-MIT.txt"], "https://github.com/TooTallNate/proxy-agents/blob/main/packages/data-uri-to-buffer/LICENSE"),
    "proxy-agent-negotiate": (["proxy-agent-negotiate-MIT.txt"], "MIT per package.json (author Nathan Rajlich); upstream has no license file, standard MIT text"),
    "standardwebhooks": (["standardwebhooks-MIT.txt", "standard-webhooks-Apache-2.0.txt"], "package.json says MIT, the repository LICENSE says Apache-2.0; both texts"),
}
missing, licenses = [], {}
for (name, ver), (lic, path) in sorted(pkgs.items()):
    if name.startswith(first_party):
        continue  # Pi's own packages: covered by LICENSE-pi
    text = license_text(path)
    licenses[lic or "UNKNOWN"] = licenses.get(lic or "UNKNOWN", 0) + 1
    lines += [f"## {name} {ver} ({lic or 'license field missing'})", ""]
    if text:
        lines += ["```", text, "```", ""]
    else:
        if name not in UPSTREAM:
            missing.append(f"{name}@{ver}")
            lines += [f"No license file shipped in the package; package.json license: {lic or 'none'}.", ""]
            continue
        f, src = UPSTREAM[name]
        lines += [f"No license file in the npm package. Text from upstream ({src}):", "", "```", "\n\n".join(open(os.path.join(upl, x)).read().strip() for x in f), "```", ""]
for vend in ["packages/schema/LICENSES", "packages/mcp/LICENSES"]:
    for f in sorted(os.listdir(os.path.join(root, vend))):
        lines += [f"## Vendored in Pi: {f}", "", "```", open(os.path.join(root, vend, f)).read().strip(), "```", ""]
lines += ["## Bun runtime (embedded in the executable)", "", "```", open(bun_license).read().strip(), "```", ""]
open(out, "w").write("\n".join(lines) + "\n")
print("packages:", sum(licenses.values()), "licenses:", dict(sorted(licenses.items(), key=lambda x: -x[1])))
print("no license file:", missing)
