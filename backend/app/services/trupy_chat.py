from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from openai import OpenAI, OpenAIError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.utils.logger import setup_logger

settings = get_settings()

LOGS_DIR = settings.LOGS_DIR
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "trupy_chat.log"
logger = setup_logger(name="trupy_chat", log_file=LOG_FILE)

CRISIS_KEYWORDS = [
    "suicid", "kill myself", "self-harm", "self harm", "hurt myself",
    "end my life", "want to die", "harm others", "hurt someone",
]

SAFETY_MESSAGE = (
    "Thank you for sharing that with me. It sounds like you are going through a lot right "
    "now, and it's brave of you to talk about it. Please know that help is available, and "
    "you don't have to go through this alone. I strongly encourage you to connect with a "
    "professional who can offer the support you deserve. Here are some resources:\n\n"
    "- [Email the University Psychologist](mailto:psicologia@upy.edu.mx)\n"
    "- [Schedule a Confidential Appointment](https://upy.edu.mx/appointment)\n"
    "- [Report a Concern](https://upy.edu.mx/report)"
)


class TrupyOpenAI:
    def __init__(self, user_profile: Optional[Dict[str, str]] = None):
        self.client = OpenAI(
            base_url=settings.BASE_URL or None,
            api_key=settings.LLM_API_KEY,
        )
        self.user_profile = user_profile
        self.messages: List[Dict[str, str]] = []
        self.crisis_detected: bool = False
        self.is_concluded: bool = False

        system_prompt = self._build_system_prompt()
        self.messages.append({"role": "system", "content": system_prompt})



    def _build_system_prompt(self) -> str:
        profile_context = ""
        if self.user_profile:
            profile_context = (
                f"\nThe student has already identified themselves:\n"
                f"  - Name: {self.user_profile.get('name')}\n"
                f"  - Major: {self.user_profile.get('major')}\n"
                f"  - Quarter: {self.user_profile.get('quarter')}\n"
                "Use this information to personalize the conversation. Do NOT ask for name, major, or quarter again."
            )
        else:
            profile_context = "\nThe student has chosen to remain anonymous. Do NOT ask for personal details."

        return f"""
                Persona: You are a virtual assistant, called Trupy AI, for the Department of Psychology at UPY University. Your personality is that of a kind, respectful, and professional companion. Always maintain this character.
                Core Objective:
                Your main purpose is to be a supportive figure for students to talk with about psychology and their mental well-being.
                Operational Guidelines:
                1.  Conversation Scope: You must only engage in conversations related to psychology and mental well-being.
                2.  Information Boundaries: You are not equipped to handle academic inquiries (e.g., courses, grades, university policies). If asked, politely state that you do not have that information.
                3.  Off-Topic Queries: For any requests outside your core objective, simply state that the topic is outside your scope of knowledge.
                4.  Response Length: Keep your responses brief and to the point. Only elaborate if the user specifically asks for more detail.
                5.  Formatting: All output must be plain text. Do not use markdown or any rich text formatting.
                6.  Student Identity: {profile_context}
                Safety Protocol:
                    - If the student expresses any sign of self-harm or intent to harm others, politely recommend to contact a professional or the university's psychological support team.
                """

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_profile": self.user_profile,
            "messages": self.messages,
            "crisis_detected": self.crisis_detected,
            "is_concluded": self.is_concluded,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TrupyOpenAI":
        instance = cls.__new__(cls)
        instance.client = OpenAI(
            base_url=settings.BASE_URL or None,
            api_key=settings.LLM_API_KEY,
        )
        instance.user_profile = data.get("user_profile")
        instance.messages = data.get("messages", [])
        instance.crisis_detected = data.get("crisis_detected", False)
        instance.is_concluded = data.get("is_concluded", False)

        return instance

    @retry(
        retry=retry_if_exception_type(OpenAIError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def _call_openai_api(self, messages: List[Dict[str, str]]) -> Any:
        try:
            return self.client.chat.completions.create(
                model=settings.MODEL,
                messages=messages,
            )
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _contains_crisis_keywords(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in CRISIS_KEYWORDS)

    def start_conversation(self) -> str:
        trigger = "Please greet the student and ask how you can help them today."
        self.messages.append({"role": "user", "content": trigger})
        try:
            response = self._call_openai_api(self.messages)
            message = response.choices[0].message
            if message.content:
                self.messages.append({"role": "assistant", "content": message.content})
                return message.content
        except Exception as e:
            logger.error(f"Error starting conversation: {e}")
        return "Hello! I'm Trupy AI, the assistant for the Psychology Department at UPY. How can I help you today?"

    def get_response(self, user_input: str) -> Union[str, Dict[str, Any]]:
        if self._contains_crisis_keywords(user_input):
            self.crisis_detected = True
            self.is_concluded = True
            logger.warning("Crisis keywords detected in user input.")
            return {
                "type": "crisis",
                "message": SAFETY_MESSAGE,
                "crisis_detected": True,
            }

        self.messages.append({"role": "user", "content": user_input})

        try:
            response = self._call_openai_api(self.messages)
            message = response.choices[0].message

            if message.content:
                if self._contains_crisis_keywords(message.content):
                    self.crisis_detected = True
                    self.is_concluded = True
                    return {
                        "type": "crisis",
                        "message": SAFETY_MESSAGE,
                        "crisis_detected": True,
                    }
                self.messages.append({"role": "assistant", "content": message.content})
                return message.content

            return "I'm having trouble understanding. Could you please repeat that?"

        except Exception as e:
            logger.error(f"Unexpected error in get_response: {e}")
            return "I apologize, but I'm currently experiencing technical difficulties. Please try again later."

    def generate_summary(self) -> str:
        summary_prompt = (
            "Based on the conversation so far, generate a concise, non-identifiable summary "
            "of the main topics discussed. Focus on themes, not personal details. Keep it under 100 words."
        )
        summary_messages = [
            *self.messages,
            {"role": "user", "content": summary_prompt},
        ]
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL,
                messages=summary_messages,
            )
            return response.choices[0].message.content or "No summary available."
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Summary could not be generated."

    def get_history(self) -> List[Dict[str, str]]:
        return [m for m in self.messages if m["role"] != "system"]
