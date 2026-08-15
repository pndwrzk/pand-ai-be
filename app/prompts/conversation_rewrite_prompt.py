QUERY_REWRITE_PROMPT = """
Given the conversation history and the user's latest message, rewrite the latest message into a standalone question that can be understood without the conversation history.

Rules:
- If the latest message already stands on its own, return it unchanged.
- Resolve pronouns and references using the conversation history.
- Do NOT answer the question. Only rewrite it.
- Keep the same language as the user's message.
- Return ONLY the rewritten question, nothing else.

Conversation history:
{conversation_history}

Latest message:
{message}

Rewritten standalone question:
"""