# MCPVault Obsidian Connection

**Source**: OpenCode Lazy Pack #03 — 建立第二大腦 Obsidian

## Summary
MCPVault (@bitbonsai/mcpvault) bridges OpenCode with Obsidian vault, enabling AI agents to read and write notes directly.

## Key Details
- **Vault Path**: `D:\AI angent course download file\Obsidian\JWObsidianvault`
- **MCP Tool**: `@bitbonsai/mcpvault` v0.12.4
- **Config**: Registered in `~/.config/opencode/opencode.jsonc` under `mcp.obsidian`
- **Install**: `npm install -g @bitbonsai/mcpvault`

## Related Topics
- [[handoff-template]] — Cross-device handoff uses Obsidian for detailed logs (L3)
- [[startup-skill]] — Reads handoff.md, lists Obsidian notes on request
- [[shutdown-skill]] — Writes detailed logs to Obsidian

## Action Items
- [ ] Test read: ask Agent to list vault root
- [ ] Test write: ask Agent to create a test note
