CONVERSATION_TITLE_PROMPT = """
Generate a concise title for this conversation.

Rules:
- Maximum 6 words
- Use the same language as the user's message
- Describe the main topic
- Return only the title

User message:
{message}
"""