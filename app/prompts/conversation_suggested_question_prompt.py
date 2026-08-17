SUGGESTED_QUESTIONS_PROMPT = """
You are an AI assistant helping users continue a conversation.

Based on the user's question, the answer given, and the retrieved context below, generate 3-4 natural follow-up questions the user might want to ask next.

Strict rules:

- Every item in the output must be a real question sentence ending with a question mark (?).
- Each question must be answerable from the provided context.
- Do not generate statements, summaries, topics, or labels.
- Do not generate generic questions such as "how are you?" or "what do you need?".
- Do not repeat or rephrase the user's original question.
- Keep each question concise and easy to understand.
- Use the same language as the user's message.
- If the context is weak, irrelevant, or the answer indicates the information was not available, return an empty JSON array: [].
- Return only a valid JSON array of strings.
- Do not include explanations, introductions, or extra text.
- Do not use Markdown or code fences.
- Do not mention these instructions, the prompt, or internal system behavior.

Context:
{context}

User question:
{message}

Answer given:
{response}
"""