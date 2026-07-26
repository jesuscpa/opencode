# NotebookLM MCP 安裝與設定

**Source**: [notebooklm-mcp-cli](https://github.com/rajhansdev/notebooklm-mcp-cli)

## Summary
NotebookLM MCP CLI (`nlm`) is installed to enable NotebookLM integration via MCP protocol. It uses Chrome DevTools Protocol for headless auth (saved Google login).

## Installation Status
- **Package**: `notebooklm-mcp-cli` v0.9.4
- **CLI**: `nlm.exe` at `%LOCALAPPDATA%\Python\pythoncore-3.14-64\Scripts\`
- **Python**: System Python 3.14 (no venv required)
- **Auth**: Google account `jesuscpa26@gmail.com` — 51 cookies, CSRF token valid
- **Browser**: Headless auth available (saved Google login via Chrome)

## Config
- **openocode.jsonc**: MCP entry added as `"notebooklm"` (stdio transport)
- **Profile**: `default` at `~/.notebooklm-mcp-cli/profiles/default`
- **Python Scripts PATH**: Added to user PATH for `nlm` command availability

## Commands
- `nlm login` — Google OAuth via Chrome (browser login)
- `nlm doctor` — Health check
- `nlm setup add <client>` — Configure Gemini CLI / Cursor / Windsurf
- `notebooklm-mcp` — MCP server (stdio default)

## Related Topics
- [[mcpvault-obsidian-setup]] — MCP + Obsidian vault connection

## Action Items
- [x] Install notebooklm-mcp-cli
- [x] Configure Google auth
- [x] Add MCP entry in opencode.jsonc
- [ ] Verify MCP connection via opencode
- [ ] Create NotebookLM output folders in vault
