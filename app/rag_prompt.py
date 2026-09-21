def build_rag_prompt(query, context):
    """Create a grounded RAG prompt."""

    prompt = f"""
You are an e-commerce product assistant.

Answer the user's question using ONLY
the product information provided in the context.

Do not invent product details.

If the answer cannot be found in the
context, say that the information is
not available.

User Query:
{query}

Product Context:
{context}

Instructions:
- Be concise and helpful.
- Mention relevant product names.
- Include prices when relevant.
- Include ratings when relevant.
- Do not invent specifications.
- Do not recommend products that are
  not present in the context.

Answer:
"""

    return prompt.strip()


def main():

    print("=" * 60)
    print("RAG PROMPT BUILDER")
    print("=" * 60)

    query = "I need an Apple laptop under 90000"

    context = """
Product 1:

Product ID: P005
Name: MacBook Air M2
Brand: Apple
Category: Laptop
Description: Lightweight laptop with Apple M2 chip,
8GB RAM and 256GB SSD
Price: ₹84999
Rating: 4.7
Stock: 8
"""

    prompt = build_rag_prompt(
        query,
        context
    )

    print("\nGenerated RAG Prompt:")
    print("-" * 60)
    print(prompt)


if __name__ == "__main__":
    main()