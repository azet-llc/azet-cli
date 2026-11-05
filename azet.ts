// azet extension for Pi: our header instead of Pi's logo, and a confirm step before risky shell commands.
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// Three kinds of shell command ask first, like Codex and Claude Code: deleting, pushing, sending data out.
// shortcut: pattern match, not a sandbox; a determined model can still disguise a command. Upgrade = OS sandbox (Codex seatbelt).
export const RISKY: [string, RegExp][] = [
  ["deletes files", /(^|[\s;&|(])(rm|rmdir|unlink|shred|truncate)\s|\bfind\b.*\s-delete\b|\bgit\s+(clean|reset\s+--hard|checkout\s+--\s|restore\s)|\bdd\s+.*of=|\bmkfs\b/],
  ["pushes or publishes", /\bgit\s+push\b|\b(npm|pnpm|yarn|bun)\s+publish\b|\bdocker\s+push\b|\bgh\s+(release|repo\s+delete|pr\s+merge)\b|\bterraform\s+apply\b|\bwrangler\s+deploy\b|\bvercel\b.*--prod/],
  ["sends data off this machine", /\bcurl\b.*\s(-d|--data[\w-]*|-F|--form|-T|--upload-file|-X\s*(POST|PUT|PATCH|DELETE))\b|\bwget\b.*--post|\b(scp|sftp|rsync|nc|ncat|ssh|ftp|sendmail|mail)\s/],
  ["runs as root", /(^|[\s;&|(])sudo\s/],
];
export const risk = (cmd: string) => RISKY.find(([, re]) => re.test(cmd))?.[0];

// Our build of Pi drops /share, /bug, /login and /logout (they went to Pi's own services).
// /bug comes back as ours; the other three answer people who type them out of habit.
const REPO = "https://github.com/azet-llc/azet-cli";
export const REPLIES: Record<string, string> = {
  share: "azet does not upload sessions. Use /export to save this session to a local file.",
  login: "azet signs in with your AZET key: AZET_API_KEY or ~/.config/azet/key. Credit: https://api.azet.io/#credits",
  logout: "To sign out, delete ~/.config/azet/key.",
};
// our reply for a typed /share, /login or /logout, else undefined
export const takeOver = (text: string) => REPLIES[text.trim().match(/^\/([a-z-]+)(\s|$)/)?.[1] ?? ""];

export default function (pi: ExtensionAPI) {
  pi.registerCommand("bug", {
    description: "Report an azet bug on GitHub",
    handler: async (_args, ctx) => ctx.ui.notify(`Report bugs at ${REPO}/issues. Nothing is sent from here.`, "info"),
  });

  pi.on("input", async (event, ctx) => {
    if (event.source === "extension") return { action: "continue" };
    const reply = takeOver(event.text);
    if (!reply) return { action: "continue" };
    ctx.ui.notify(reply, "info");
    return { action: "handled" };
  });

  pi.on("session_start", async (_e, ctx) => {
    if (ctx.mode !== "tui") return;
    ctx.ui.setTitle?.(`azet · ${process.cwd().split("/").pop()}`);
    ctx.ui.setHeader((_tui, theme) => ({
      render: () => [
        "",
        theme.fg("accent", " ▄▀█ ▀█ █▀▀ ▀█▀"),
        theme.fg("accent", " █▀█ █▄ ██▄  █ ") + theme.fg("muted", "  AI coding agent by AZET LLC") + theme.fg("dim", `  v${process.env.AZET_VERSION || "dev"}`),
        theme.fg("dim", ` esc stop · ctrl+l model · ctrl+c twice quit · risky shell commands ask first · sandbox ${process.env.AZET_SANDBOX === "0" ? "off" : "on: writes stay in this folder"}`),
        "",
      ],
      invalidate() {},
    }));
  });

  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName !== "bash") return undefined;
    const cmd = String((event.input as { command?: string }).command ?? "");
    const why = risk(cmd);
    if (!why) return undefined;
    if (!ctx.hasUI) return { block: true, reason: `azet blocked a command that ${why}. Run azet interactively to approve it: ${cmd}` };
    const ok = await ctx.ui.confirm(`This command ${why}. Run it?`, cmd);
    return ok ? undefined : { block: true, reason: `The user declined a command that ${why}.` };
  });
}
