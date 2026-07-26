# Browser Control & Desktop Automation Setup

**Source**: `06-安裝瀏覽器控制.md` (OpenCode Lazy Pack #06)

## Summary
Installed two MCP servers for browser control (Playwright) and desktop automation (open-computer-use) to give OpenCode the ability to navigate web pages and control Windows UI applications.

## Playwright MCP
- **Package**: `@playwright/mcp` (via npx)
- **MCP Config**: `["npx", "-y", "@playwright/mcp"]` stdio
- **Status**: Initialized successfully (v1.62.0-alpha)
- **Browsers**: Auto-download on first use (Chromium, Firefox, WebKit)

## open-computer-use
- **Version**: v0.2.1
- **Package**: `open-computer-use` (npm global install)
- **Binary**: `C:\Users\james_wang\AppData\Roaming\npm\open-computer-use.cmd`
- **MCP Config**: `["open-computer-use", "mcp"]` stdio
- **Status**: Initialized successfully — Windows UIA-based desktop automation
- **Note**: Installed with `--ignore-scripts` due to postinstall failure on Windows (node PATH issue)

## PATH Fix
- `C:\Program Files\nodejs` added to **User PATH** for `node` availability
- Current session still needs `$env:Path = "C:\Program Files\nodejs;$env:Path"` for immediate use

## Related Topics
- [[notebooklm-mcp-setup]] — NotebookLM setup in same config structure

## Action Items
- [x] Add Playwright MCP to opencode.jsonc
- [x] Install open-computer-use globally
- [x] Add open-computer-use MCP to opencode.jsonc
- [x] Verify MCP servers respond to initialize
- [ ] First use will trigger Playwright browser download (~300MB)
