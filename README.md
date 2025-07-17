# AI-Powered User Story Generator with RAG and Full Context Fallback

## Overview

This project is an AI-driven system designed to generate detailed product management user stories from natural language queries. It leverages Retrieval-Augmented Generation (RAG) to extract relevant context from technical documents and uses large language models (LLMs) to produce, evaluate, and improve user stories automatically.

## Features

- Loads documents from the `/data` folder
- Splits documents into semantic chunks
- Indexes them using a vectorstore
- Retrieves relevant chunks based on a user query
- Uses LLMs to:
  - Extract relevant information
  - Generate a user story
  - Evaluate and score the story
  - Generate feedback or fallback if needed
- Calculates token usage and cost

## Architecture & Workflow

The architecture is modular and consists of the following components:

- **Data Loading & Splitting:** Loads markdown or text documents, then splits them into smaller chunks for efficient retrieval.
- **Vector Store & Retriever:** Embeds document chunks and indexes them in a vector database to perform similarity search.
- **Prompt Builder:** Constructs detailed prompts for various stages: extracting relevant context, generating user stories, scoring, and feedback.
- **LLM Interaction:** Two LLM instances are used:
  - A smaller model (`gpt-4o-mini`) for retrieval-augmented generation (RAG) and scoring.
  - A larger model (`gpt-4o`) for fallback with full context when RAG output is insufficient.
- **Evaluation & Feedback:** Automatically scores the generated story, provides feedback, and can trigger a regeneration cycle.
- **Cost & Token Estimation:** Counts tokens for prompts and completions and estimates associated API costs.

## How to Run

```bash
python main.py "Your feature request or topic here"
```

## Requirements

- Python 3.8+
- `.env` file with your OpenAI API key
- Install dependencies via:

```bash
pip install -r requirements.txt
```

## Folder Structure

- `main.py`: Main entry point
- `data/`: Markdown and source documents
- `splitter.py`: Splits docs into chunks
- `vectorstore.py`: Handles embedding & retrieval
- `prompt_builder.py`: Builds prompts for generation, scoring, and feedback
- `scoring.py`: LLM-based evaluation and feedback
- `evaluator.py`: Additional scoring metrics
- `cost_estimator.py`: Token counting and cost estimation
- `llm_tools.py`: Helper functions for LLM tasks

---

# 🔍 Workflow Comparison: RAG vs Full Context

## 1. Retrieval-Augmented Generation (RAG)

### Overview

- Fast and cheap
- Uses only relevant parts of documents
- Uses `gpt-4o-mini` for speed and efficiency

### Sample Output

- **AI Score:** 8.0/10
- **Tokens:** 156 input, 139 output
- **Estimated Cost:** $0.000287

### Pros

- Low latency and cost
- High precision for scoped questions

### Cons

- May miss important details if retrieval is incomplete

---

## 2. Full Context Fallback

### Overview

- Triggered only when RAG output score < 6.5
- Uses entire document corpus
- Powered by `gpt-4o` for depth and completeness

### Sample Output

- **Tokens:** 18,273 input, 516 output
- **Estimated Cost:** $0.099105

### Pros

- Most complete and thorough output
- Captures global document context

### Cons

- High cost and slower performance

---

## 3. Workflow Summary Table

| Workflow              | Tokens (In + Out) | Cost (USD) | AI Score | Speed | Best Use Case                              |
| --------------------- | ----------------- | ---------- | -------- | ----- | ------------------------------------------ |
| RAG (gpt-4o-mini)     | ~295              | ~$0.0003   | ~7–9     | Fast  | General use, low-cost environments         |
| Full Context (gpt-4o) | ~18,789           | ~$0.099    | N/A      | Slow  | Detailed coverage, fallback only if needed |

---

## 4. Recommendations

- Use **RAG** as the default path
- Trigger **fallback** only when quality is insufficient
- Track **token usage** to manage costs
- Watch for deprecation warnings (e.g., LangChain `get_relevant_documents`)

---

Happy Story Generating!
