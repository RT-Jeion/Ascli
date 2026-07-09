# Ascli

Ascli is a learning project for building an AI agent in Python from scratch.

## Current state

- CLI-based chat agent
- Groq-powered LLM loop
- Basic tool calling for:
  - web search
  - file reading/writing
  - directory listing
- MongoDB-backed session storage

## Overall direction

The goal is to grow this into a proper modular agent system while keeping the code simple enough to learn from.

Planned systems:

- **Agent runtime**: controls recursive and multi-step tool calling
- **Tool registry**: keeps tools separate from the main loop
- **Conversation memory**: recent chat, summaries, long-term recall
- **RAG system**: indexed knowledge base for documents and notes
- **Web search system**: external information lookup with caching and citations
- **Storage layer**: sessions, history, retrieved data, and agent state

## Learning focus

This project is mainly for understanding:

- how agents decide what to do next
- how tool calling works
- how memory differs from retrieval
- how to structure a system so parts can grow independently

## What these parts mean

- **Agent runtime**: the part that talks to the model, sees its next action, runs tools, and keeps the conversation moving.
- **Tools**: small functions the agent can use, like searching the web, reading a file, or writing output.
- **Memory**: saved conversation context so the agent can remember recent chat and important facts.
- **RAG**: a way to look up useful information from your own documents before answering.
- **Web search**: a way to fetch fresh information from the internet when the agent needs it.
- **Storage**: where chat sessions, summaries, and retrieved data are kept.

## Suggested roadmap

1. Separate the agent loop into clear modules.
2. Build a unified tool interface.
3. Add short-term and long-term memory handling.
4. Add RAG indexing and retrieval.
5. Add web search caching and result formatting.
6. Add limits for recursion, retries, and tool usage.

## Suggested project structure

```text
ascli/
  agent/
  tools/
  memory/
  rag/
  web/
  storage/
  utils/
```

Start by moving the current scripts into `agent/`, `tools/`, and `storage/`, then add `memory/` and `rag/` as the project grows.
