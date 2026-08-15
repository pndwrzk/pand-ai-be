import json

from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.constants.conversation_role import ConversationRole
from app.models.conversation_message import ConversationMessage
from app.prompts.conversation_first_response_prompt import CONVERSATION_FIRST_RESPONSE_PROMPT
from app.prompts.conversation_response_prompt import CONVERSATION_RESPONSE_PROMPT
from app.prompts.conversation_suggested_question_prompt import SUGGESTED_QUESTIONS_PROMPT
from app.prompts.conversation_title_prompt import CONVERSATION_TITLE_PROMPT
from app.core.config import settings


class LLMService:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.llm = ChatGroq(
            model=model_name,
            temperature=0.3,
            max_tokens=1024,
            api_key=settings.GROQ_API_KEY,
        )

    def _build_history_text(self, history: list[ConversationMessage]) -> str:
        return "\n".join(
            f"{'You' if msg.role == ConversationRole.SYSTEM else 'User'}: {msg.content}"
            for msg in history
        )

    def _build_context_text(self, contexts: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in contexts) or "No relevant context was found."

    def _stream_llm(self, prompt: str):
        for chunk in self.llm.stream([HumanMessage(content=prompt)]):
            content = getattr(chunk, "content", "")
            if isinstance(content, str):
                yield content
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, str):
                        yield item

    def generate_title(self, message_content: str) -> str:
        prompt = CONVERSATION_TITLE_PROMPT.replace("{message}", message_content)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return str(response.content).strip()

    def generate_first_response_stream(self, message_content: str, contexts: list[Document]):
        prompt = CONVERSATION_FIRST_RESPONSE_PROMPT.format(
            context=self._build_context_text(contexts),
            message=message_content,
        )
        yield from self._stream_llm(prompt)

    def generate_response_stream(
        self,
        message_content: str,
        history: list[ConversationMessage],
        contexts: list[Document],
    ):
        prompt = CONVERSATION_RESPONSE_PROMPT.format(
            conversation_history=self._build_history_text(history),
            context=self._build_context_text(contexts),
            message=message_content,
        )
        yield from self._stream_llm(prompt)

    def generate_suggested_questions(self, message_content: str) -> list[str]:
        prompt = SUGGESTED_QUESTIONS_PROMPT.format(message=message_content)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        content = response.content

        if not isinstance(content, str):
            raise ValueError("Unexpected LLM response format")

        questions = json.loads(content)
        if not isinstance(questions, list):
            raise ValueError("Suggested questions must be a list")

        return [q for q in questions if isinstance(q, str)]