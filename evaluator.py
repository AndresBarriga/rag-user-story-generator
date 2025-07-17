from prompt_builder import build_ai_score_prompt, build_ai_feedback_prompt
import json
import re

def ai_score_output(llm, query: str, user_story_text: str) -> float:
    """
    Evalúa un user story usando el LLM y devuelve un score float entre 0 y 10.
    """
    prompt = build_ai_score_prompt(query, user_story_text)
    response = llm.invoke(prompt)
    try:
        score = float(response.content.strip().split()[0])
    except Exception:
        score = 0.0
    return score


def evaluate_with_ragas(llm, query: str, rag_output: str, relevant_docs: list) -> dict:
    """
    Evaluación avanzada usando RAGAS.
    Parámetros:
    - llm: instancia de ChatOpenAI o similar
    - query: texto de la consulta
    - rag_output: texto generado (user story)
    - relevant_docs: lista de Document objects recuperados por RAG

    Devuelve:
    - dict con métricas: relevance, recall, precision, completeness, suggestions
    """

    context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    evaluation_prompt = f"""
You are an expert evaluator for AI-generated product management user stories.

Query:
{query}

Generated User Story:
{rag_output}

Context from documents:
{context_text}

Please respond ONLY with a JSON object EXACTLY in this format:

{{
  "relevance": 0,
  "recall": 0,
  "precision": 0,
  "completeness": 0,
  "suggestions": ""
}}

Fill in the values from 0 to 10 for the first four keys, and write suggestions if any.

Do NOT add any explanations, apologies, or extra text outside the JSON.
"""

    response = llm.invoke(evaluation_prompt)
    print("Respuesta cruda de evaluación avanzada:", response.content)

    def extract_json(text: str) -> str:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return match.group(0) if match else ""

    json_str = extract_json(response.content)

    try:
        metrics = json.loads(json_str)
    except Exception as e:
        print(f"Error parsing JSON after extraction: {e}")
        metrics = {
            "relevance": 0,
            "recall": 0,
            "precision": 0,
            "completeness": 0,
            "suggestions": "Could not parse evaluation output."
        }

    return metrics
