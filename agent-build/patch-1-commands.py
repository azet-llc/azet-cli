# azet 판 Pi 패치(v1.5.0, MIT): Pi 이름·Pi 회사 서비스로 가는 내장 명령을 뺀다. 빠진 명령은 azet 확장(input 훅)이 대신 답한다.
import re, sys
root = sys.argv[1]  # ~/pi-src/packages/coding-agent/src

def edit(path, pairs):
    p = f"{root}/{path}"; s = open(p).read()
    for a, b in pairs:
        n = s.count(a)
        assert n == 1, f"{path}: expected 1 match, got {n}: {a[:70]!r}"
        s = s.replace(a, b)
    open(p, "w").write(s)

# 1) / 메뉴 표에서 Pi 서비스로 가는 명령 4개 제거(share=Radius·gist 업로드, bug=Pi 개발자에게 전송, login/logout=Radius 로그인 화면)
edit("core/slash-commands.ts", [
    ('\t{ name: "share", description: "Share session via a Radius artifact or a GitHub gist" },\n', ""),
    ('\t{ name: "bug", description: "Report a bug to the Pi developers", argumentHint: "<description>" },\n', ""),
    ('\t{ name: "login", description: "Configure provider authentication", argumentHint: "<provider>" },\n', ""),
    ('\t{ name: "logout", description: "Remove provider authentication" },\n', ""),
])

# 2) 입력 처리에서 같은 명령 + 숨은 이스터에그(/arminsayshi, /dementedelves = 「pi has joined Earendil」) 분기 제거 → 확장 input 훅으로 넘어간다
im = "modes/interactive/interactive-mode.ts"
blocks = [
    '\t\t\tif (text === "/share") {\n\t\t\t\tawait this.handleShareCommand();\n\t\t\t\tthis.editor.setText("");\n\t\t\t\treturn;\n\t\t\t}\n',
    '\t\t\tif (text === "/bug" || text.startsWith("/bug ")) {\n\t\t\t\tconst hint = text.slice("/bug".length).trim();\n\t\t\t\tthis.editor.setText("");\n\t\t\t\tawait this.handleBugCommand(hint ? hint : undefined);\n\t\t\t\treturn;\n\t\t\t}\n',
    '\t\t\tif (text === "/login" || text.startsWith("/login ")) {\n\t\t\t\tconst providerRef = text.startsWith("/login ") ? text.slice(7).trim() : undefined;\n\t\t\t\tthis.editor.setText("");\n\t\t\t\tawait this.handleLoginCommand(providerRef);\n\t\t\t\treturn;\n\t\t\t}\n',
    '\t\t\tif (text === "/logout") {\n\t\t\t\tthis.showOAuthSelector("logout");\n\t\t\t\tthis.editor.setText("");\n\t\t\t\treturn;\n\t\t\t}\n',
    '\t\t\tif (text === "/arminsayshi") {\n\t\t\t\tthis.handleArminSaysHi();\n\t\t\t\tthis.editor.setText("");\n\t\t\t\treturn;\n\t\t\t}\n',
    '\t\t\tif (text === "/dementedelves") {\n\t\t\t\tthis.handleDementedDelves();\n\t\t\t\tthis.editor.setText("");\n\t\t\t\treturn;\n\t\t\t}\n',
]
edit(im, [(b, "") for b in blocks] + [
    ("`Pi can explain its own features and look up its docs. Ask it how to use or extend Pi.`",
     "`Ask ${APP_NAME} what it can do in this folder.`"),
])
print("patched")
