def build_user_story_prompt(query: str, context_text: str) -> str:
    return f"""
You are an expert Product Owner assistant. Follow these steps carefully:

1. Extract only the information strictly relevant to the query from the given context.
2. Using only the extracted information, write a detailed user story following the INVEST criteria:
   - Independent
   - Negotiable
   - Valuable
   - Estimable
   - Small
   - Testable
3. Provide clear acceptance criteria as bullet points, strictly based on the context—do NOT add or assume anything not present.
4. Suggest any missing critical information or improvements without fabricating details.

Context:
{context_text}

User Query:
{query}

Format your output EXACTLY like this:

User Story:
As [role], I want to [action] so that [benefit].

Acceptance Criteria:
- ...

Suggestions:
- ...
"""

def build_extract_relevant_info_prompt(query: str, docs_text: str) -> str:
    return f"""
You are a precise assistant helping a product manager.

From the following documentation, extract **only** the information that is strictly relevant to the query. Do NOT include any explanation, opinions, or formatting.

Query:
"{query}"

Documentation:
{docs_text}

Return ONLY the relevant content as plain text.
"""

def build_ai_score_prompt(query: str, user_story_text: str) -> str:
    return f"""
You are an AI reviewer scoring a user story from 1 to 10, where 10 means perfectly aligns with the query and is specific, complete, testable, and relevant.

Query:
"{query}"

User Story:
{user_story_text}

Return ONLY the numeric score (1 to 10), without any additional text.
"""

def build_ai_feedback_prompt(query: str, original_output: str, relevant_info: str) -> str:
    return f"""
You are an AI reviewer. The following user story may be incomplete or unclear.

Query:
{query}

Original User Story:
{original_output}

Relevant Context:
{relevant_info}

Identify weaknesses and suggest improvements. Then regenerate the user story following INVEST criteria, strictly based on the relevant context. Do NOT invent any features or details.

Return only the improved user story with acceptance criteria and suggestions.
"""
