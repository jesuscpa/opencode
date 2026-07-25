# Project Context

This is an AI Agent Process Knowledge Database Hub - a structured knowledge vault built from YouTube transcripts, tutorials, and agent-generated content.

## Quick Start

```bash
pip install yt-dlp
python extract_videos.py    # Extract filtered video URLs from channel
python download_all_subs.py # Download subtitles and clean to Markdown
```

## Vault Structure

| Directory | Purpose | Agent Editable |
|-----------|---------|:---:|
| `Clipping/` | Raw external transcripts | No |
| `創作庫/` | Original creations/scripts | No |
| `知識庫/` | Structured knowledge base | Yes |
| `subtitles/` | Raw VTT downloads | No |

## Agent Instructions

Read `AGENTS.md` for the full system prompt on weekly vault maintenance, knowledge restructuring, and note formatting.

## Key Scripts

- `extract_videos.py` - Fetches YouTube channel videos, filters by AI keywords, exports URLs
- `download_all_subs.py` - Downloads VTT subtitles, cleans timestamps/tags, writes Markdown to Clipping/

## Knowledge Base Domains

- AI Workflows (AI工作流)
- Teaching Trends (教學趨勢)
- Agent Frameworks (Agent框架)
- Tool Development (工具開發)

## Weekly Maintenance

Every Sunday, run the restructure workflow defined in AGENTS.md:
1. Scan Clipping/ and 創作庫/ for new files
2. Digest and extract key info
3. Write structured notes to 知識庫/
4. Health check and link verification
5. Update Index and Log
