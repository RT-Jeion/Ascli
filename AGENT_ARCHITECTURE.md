# Agent architecture notes for Ascli

This project is best approached as a set of small subsystems instead of one large prompt loop.

## Suggested folder layout

```text
ascli/
  app.py
  agent/
    runtime.py
    prompts.py
    schemas.py
  tools/
    registry.py
    web_search.py
    file_io.py
    directory.py
  memory/
    session_store.py
    summary_store.py
    long_term_store.py
  rag/
    ingest.py
    chunking.py
    embed.py
    retrieve.py
  web/
    search.py
    cache.py
  storage/
    mongodb.py
    vector_store.py
  utils/
    time.py
    logging.py
```

Keep the current simple scripts while learning, then move functionality into these modules one piece at a time.

## How the current files map

- `agent.py` -> future `agent/runtime.py`
- `llm.py` -> future `agent/runtime.py` + `tools/registry.py`
- `web.py` -> future `tools/web_search.py` or `web/search.py`
- `file_handle.py` -> future `tools/file_io.py`
- `mongodb.py` -> future `storage/mongodb.py`
- `chat_session.py` -> future `memory/session_store.py`
- `get_time.py` -> future `utils/time.py`
- `essentials.py` -> future `agent/prompts.py` and `agent/schemas.py`

## Beginner definitions

- **Agent runtime**: the control loop that decides when to ask the model, when to call tools, and when to stop.
- **Tool**: a callable action the agent can use to do something outside the model, like search or file I/O.
- **Memory**: saved chat context or important facts the agent should remember across turns.
- **RAG**: retrieval from your own document store so the model can answer with project-specific knowledge.
- **Web search**: external search for fresh information that is not already in your local data.
- **Storage**: the database or files that keep sessions, memory, documents, and cached results.

## 1. Agent runtime

The runtime should own the conversation loop:

- send user input to the model
- read tool calls
- execute tools
- feed tool output back to the model
- repeat until the model returns a final answer

Keep recursion controlled with:

- max tool-call depth
- max total tool calls per request
- per-tool timeout
- safe retry rules only for idempotent tools

## 2. Tool system

Use a tool registry instead of hardcoding tool behavior in the loop.

Each tool should expose:

- name
- input schema
- execution function
- optional metadata like timeout or side effects

This makes it easier to add new tools without rewriting the agent core.

## 3. Conversation memory

Conversation memory should have three layers:

- **Short-term memory**: recent turns that stay in the prompt
- **Summary memory**: compressed older conversation
- **Long-term memory**: important facts, preferences, and past tasks

Do not keep every turn in the prompt forever. Summarize older context and retrieve only what is needed.

## 4. RAG system

RAG should be separate from chat memory.

Suggested flow:

1. ingest documents
2. chunk them
3. embed the chunks
4. store them in a vector store with metadata
5. retrieve top matches for a query
6. rerank if needed
7. send only the best chunks to the model

Use metadata such as source, file name, section, and timestamp.

## 5. Web search system

Treat web search as temporary external context.

Recommended behavior:

- search only when needed
- cache results for a short time
- summarize useful facts
- keep citations or source links
- avoid storing raw search output as permanent memory

## 6. Storage design

Use separate stores for separate jobs:

- session store for chat runs and usage
- memory store for summaries and important facts
- retrieval store for RAG documents
- cache store for web results

## 7. Practical build order

Build in this order:

1. clean agent runtime
2. tool registry
3. session storage
4. conversation summary memory
5. vector retrieval
6. web search cache
7. safety and limits

## 8. Main design rule

If a feature changes often, keep it modular.
If a feature is core to reasoning, keep it visible and easy to inspect.

That way the project stays good for learning while still moving toward a real agent.
