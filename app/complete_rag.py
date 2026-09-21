from app.advanced_rag import AdvancedRAG
from app.context_builder import build_context
from app.rag_prompt import build_rag_prompt
from app.llm_generator import MockLLMGenerator


def answer_query(query):
    """
    Complete RAG pipeline:

    Query
        ↓
    Retrieval
        ↓
    Context
        ↓
    Prompt
        ↓
    LLM
        ↓
    Answer
    """

    print("=" * 70)
    print("COMPLETE RAG ASSISTANT")
    print("=" * 70)

    # --------------------------------------------------
    # STEP 1: Advanced RAG
    # --------------------------------------------------

    print("\n[1] Searching products...")

    rag = AdvancedRAG()

    results = rag.search(query)

    if not results:
        return "No relevant products were found."

    # --------------------------------------------------
    # STEP 2: Build Context
    # --------------------------------------------------

    print("\n[2] Building product context...")

    context = build_context(results)

    # --------------------------------------------------
    # STEP 3: Build Prompt
    # --------------------------------------------------

    print("\n[3] Building RAG prompt...")

    prompt = build_rag_prompt(
        query,
        context
    )

    # --------------------------------------------------
    # STEP 4: Generate Answer
    # --------------------------------------------------

    print("\n[4] Generating answer...")

    llm = MockLLMGenerator()

    answer = llm.generate(prompt)

    # --------------------------------------------------
    # FINAL ANSWER
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(answer)

    return answer


def main():

    query = "I need an Apple laptop under 90000"

    answer_query(query)


if __name__ == "__main__":
    main()