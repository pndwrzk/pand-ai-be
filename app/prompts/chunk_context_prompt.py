CHUNK_CONTEXT_PROMPT = """
You are given a full document and one specific chunk extracted from that document.

Your task: write a short context (1-2 sentences, in the same language as the document) that situates this chunk within the overall document, so it can be understood on its own without reading the rest of the document.

Rules:
- Do NOT summarize the whole document.
- Do NOT repeat the chunk content itself.
- Only add context that helps disambiguate who/what/when this chunk refers to (subject names, dates, topic of the document).
- Output ONLY the context sentence(s), nothing else.

Full document:
{document}

Chunk:
{chunk}

Context:
"""