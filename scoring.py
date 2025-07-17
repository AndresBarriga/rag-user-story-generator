# scoring.py
from langchain_openai import ChatOpenAI
from prompt_builder import (
    build_ai_score_prompt,
    build_ai_feedback_prompt,
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def score_user_story(query: str, user_story_text: str) -> float:
    prompt = build_ai_score_prompt(query, user_story_text)
    response = llm.invoke(prompt)
    try:
        score = float(response.content.strip().split()[0])
    except (ValueError, IndexError):
        score = 0.0  # fallback si no parsea bien
    return score

def generate_feedback(query: str, original_output: str, relevant_info: str) -> str:
    prompt = build_ai_feedback_prompt(query, original_output, relevant_info)
    response = llm.invoke(prompt)
    return response.content
