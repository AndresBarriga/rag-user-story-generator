from data_loader import load_all_docs_from_data
from splitter import split_documents
from vectorstore import create_vectorstore, get_retriever
from prompt_builder import build_user_story_prompt
from scoring import generate_feedback
from evaluator import ai_score_output, evaluate_with_ragas
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sys
from llm_tools import extract_relevant_info, generate_full_context_story
from cost_estimator import  estimate_cost




def main(query: str):
    load_dotenv()

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost_usd = 0

    # Initialize two LLM instances:
    #  - llm_rag: smaller, cheaper model for retrieval-augmented generation (RAG)
    #  - llm_full: larger, more powerful model for fallback with full context
    llm_rag = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_full = ChatOpenAI(model="gpt-4o", temperature=0)

    try:
        # 1. Load all source documents from the 'data' folder
        docs = load_all_docs_from_data("data")
        if not docs:
            print("No documents found in 'data' folder.")
            return

        # 2. Split documents into smaller chunks for indexing/search
        chunks = split_documents(docs)
        if not chunks:
            print("Could not split documents into chunks.")
            return

        # 3. Create a vectorstore from chunks and get a retriever for semantic search
        vectorstore = create_vectorstore(chunks)
        retriever = get_retriever(vectorstore)

        # 4. Use retriever to get documents relevant to the query
        relevant_docs = retriever.get_relevant_documents(query)
        if not relevant_docs:
            print(f"No relevant documents found for query: {query}")
            return

        # 5. Explicitly extract only the relevant information from those documents using the smaller LLM
        relevant_text = extract_relevant_info(llm_rag, query, relevant_docs)

        # 6. Build a user story generation prompt based on the extracted relevant text
        prompt = build_user_story_prompt(query, relevant_text)
        response = llm_rag.invoke(prompt)
        rag_output = response.content

        print("\n--- User Story Generated (RAG Context) ---")
        print(rag_output)

        # 7. Score the generated user story using the smaller LLM (scale 0-10)
        score = ai_score_output(llm_rag, query, rag_output)
        print(f"\nAI Score: {score}/10")

        # 8. Count tokens and estimate cost for this prompt + output
        token_info = estimate_cost(prompt, rag_output, model="gpt-4o-mini")
        print(f"\nToken usage and estimated cost: {token_info}")
           # Accumulate tokens and cost
        total_input_tokens += token_info["input_tokens"]
        total_output_tokens += token_info["output_tokens"]
        total_cost_usd += token_info["total_cost_usd"]

        # 9. If score is below threshold, generate feedback and improved output
        if score < 6.5:
            print("\nScore below threshold, generating improved output with feedback...")
            improved_output = generate_feedback(query, rag_output, relevant_text)

            print("\n--- Improved Output After Feedback ---")
            print(improved_output)

            # 10. Full context fallback generation using the larger LLM
            print("\n--- Full Context Fallback with larger LLM ---")
            full_context_output = generate_full_context_story(llm_full, query, docs)
            print(full_context_output)

            # 11. Count tokens and estimate cost for fallback generation
            full_prompt = build_user_story_prompt(query, "\n\n".join([doc.page_content for doc in docs]))
            fallback_token_info = estimate_cost(full_prompt, full_context_output, model="gpt-4o")
            print(f"\nFull context fallback token usage and cost estimate: {fallback_token_info}")

            # Accumulate tokens and cost from fallback
            total_input_tokens += fallback_token_info["input_tokens"]
            total_output_tokens += fallback_token_info["output_tokens"]
            total_cost_usd += fallback_token_info["total_cost_usd"]


        else:
            print("\nOutput accepted without improvements.")

        # 12. Perform detailed evaluation with advanced metrics and print results
        metrics = evaluate_with_ragas(llm_rag, query, rag_output, relevant_docs)
        print("\n--- Detailed Metrics ---")
        print(metrics)

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    query_input = sys.argv[1] if len(sys.argv) > 1 else "Stripe Integration"
    main(query_input)
