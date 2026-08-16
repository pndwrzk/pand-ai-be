QUERY_REWRITE_PROMPT = """
Rewrite the user's latest message into a standalone search query optimized for retrieving facts from a knowledge base.

Rules:
- Resolve pronouns/references using conversation history.
- If the question asks for something that is likely DERIVED from a stored fact (age, duration, time elapsed, count, comparison), rewrite it toward the underlying stored fact instead of the derived value. Example: "berapa umur X" -> "tanggal lahir X"; "sudah berapa lama X bekerja di Y" -> "kapan X mulai bekerja di Y".
- Do NOT answer the question. Only produce the search query.
- Keep the same language as the user's message.

Conversation history:
{conversation_history}

Latest message:
{message}

Rewritten standalone question:
"""