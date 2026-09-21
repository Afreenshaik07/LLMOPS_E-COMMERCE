from app.advanced_rag import AdvancedRAG
from app.context_builder import build_context
from app.rag_prompt import build_rag_prompt


def run_rag(query):
    """
    Complete RAG pipeline:

    Query
        ↓
    Advanced Retrieval
        ↓
    Context Building
        ↓
    Prompt Construction
    """

    print("=" * 70)
    print("END-TO-END RAG PIPELINE")
    print("=" * 70)

    # --------------------------------------------------
    # STEP 1: Advanced Retrieval
    # --------------------------------------------------

    print("\n[1] Running Advanced RAG...")

    rag = AdvancedRAG()

    results = rag.search(query)

    print(f"Retrieved products: {len(results)}")

    # --------------------------------------------------
    # STEP 2: Build Context
    # --------------------------------------------------

    print("\n[2] Building Context...")

    context = build_context(results)

    # --------------------------------------------------
    # STEP 3: Build RAG Prompt
    # --------------------------------------------------

    print("\n[3] Building RAG Prompt...")

    prompt = build_rag_prompt(
        query,
        context
    )

    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL LLM PROMPT")
    print("=" * 70)

    print(prompt)

    return prompt


def main():

    query = "I need an Apple laptop under 90000"

    run_rag(query)


if __name__ == "__main__":
    main()