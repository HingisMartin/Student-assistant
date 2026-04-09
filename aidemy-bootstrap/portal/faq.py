import os
from pathlib import Path

from langchain_google_vertexai import ChatVertexAI


MODEL_NAME = os.environ.get("FAQ_MODEL", "gemini-2.0-flash")
TEMPERATURE = float(os.environ.get("FAQ_TEMPERATURE", "0.2"))
TEACHING_PLAN_PATH = Path(os.environ.get("TEACHING_PLAN_PATH", "teaching_plan.txt"))


# def _load_teaching_context() -> str:
#     if not TEACHING_PLAN_PATH.exists():
#         return "No teaching plan is currently available."

#     content = TEACHING_PLAN_PATH.read_text(encoding="utf-8").strip()
#     return content or "No teaching plan is currently available."


def answer_faq_question(question: str) -> str:
    cleaned_question = (question or "").strip()
    if not cleaned_question:
        raise ValueError("Question is required.")

    llm = ChatVertexAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    
    prompt = f"""
You are Aidemy's student FAQ assistant.
Answer the student's question clearly and concisely.
If the answer is not grounded in the provided context, say that explicitly and give the safest helpful guidance.


Student question:
{cleaned_question}
""".strip()

    response = llm.invoke(prompt)
    return getattr(response, "content", str(response)).strip()
