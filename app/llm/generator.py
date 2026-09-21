import os
import re
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class MockLLM(BaseLLM):
    """
    Local deterministic LLM simulator.

    Uses the RAG context to generate a grounded
    product response without calling an API.
    """

    def generate(self, prompt: str) -> str:

        context_match = re.search(
            r"Product Context:\s*(.*?)(?:\nInstructions:|\nAnswer:)",
            prompt,
            re.DOTALL
        )

        query_match = re.search(
            r"User Query:\s*(.*?)(?:\n\nProduct Context:)",
            prompt,
            re.DOTALL
        )

        if not context_match:
            return (
                "I could not find sufficient product "
                "information in the provided context."
            )

        context = context_match.group(1).strip()

        query = (
            query_match.group(1).strip()
            if query_match
            else ""
        )

        products = self._parse_products(context)

        if not products:
            return (
                "I could not find sufficient product "
                "information in the provided context."
            )

        return self._generate_answer(
            query=query,
            products=products
        )

    def _parse_products(self, context):

        blocks = re.split(
            r"\n\s*Product \d+:\s*",
            context
        )

        products = []

        for block in blocks:

            if not block.strip():
                continue

            def get_field(field):

                match = re.search(
                    rf"{field}:\s*(.*)",
                    block
                )

                if match:
                    return match.group(1).strip()

                return ""

            products.append({
                "name": get_field("Name"),
                "brand": get_field("Brand"),
                "category": get_field("Category"),
                "description": get_field("Description"),
                "price": get_field("Price"),
                "rating": get_field("Rating"),
                "stock": get_field("Stock")
            })

        return products

    def _generate_answer(self, query, products):

        query_lower = query.lower()

        # ---------------------------------------------
        # Comparison
        # ---------------------------------------------

        if (
            "compare" in query_lower
            and len(products) >= 2
        ):

            p1 = products[0]
            p2 = products[1]

            return (
                f"{p1['name']} is a {p1['brand']} "
                f"{p1['category']} priced at "
                f"{p1['price']}, with a rating of "
                f"{p1['rating']} and stock of "
                f"{p1['stock']}. "
                f"{p1['description']}\n\n"

                f"{p2['name']} is a {p2['brand']} "
                f"{p2['category']} priced at "
                f"{p2['price']}, with a rating of "
                f"{p2['rating']} and stock of "
                f"{p2['stock']}. "
                f"{p2['description']}"
            )

        product = products[0]

        # ---------------------------------------------
        # Inventory
        # ---------------------------------------------

        if (
            "stock" in query_lower
            or "available" in query_lower
            or "in stock" in query_lower
        ):

            return (
                f"{product['name']} currently has "
                f"{product['stock']} units in stock."
            )

        # ---------------------------------------------
        # Product details
        # ---------------------------------------------

        if (
            "details" in query_lower
            or "detail" in query_lower
            or "specification" in query_lower
            or "specifications" in query_lower
        ):

            return (
                f"{product['name']} is a "
                f"{product['brand']} "
                f"{product['category']}. "
                f"{product['description']} "
                f"It costs {product['price']} and has "
                f"a rating of {product['rating']}."
            )

        # ---------------------------------------------
        # Default product search
        # ---------------------------------------------

        return (
            f"{product['name']} is a "
            f"{product['brand']} "
            f"{product['category']} priced at "
            f"{product['price']}. "
            f"It has a rating of "
            f"{product['rating']} and "
            f"{product['stock']} units in stock. "
            f"{product['description']}"
        )


class OpenAILLM(BaseLLM):

    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set "
                "in the .env file."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = "gpt-5.6-luna"

    def generate(self, prompt: str) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text


if __name__ == "__main__":

    print("=" * 60)
    print("LOCAL MOCK LLM TEST")
    print("=" * 60)

    llm = MockLLM()

    test_prompt = """
You are an e-commerce product assistant.

User Query:
I need an Apple laptop under 90000

Product Context:

Product 1:

Product ID: P005
Name: MacBook Air M2
Brand: Apple
Category: Laptop
Description: Lightweight laptop with Apple M2 chip, 8GB RAM and 256GB SSD
Price: ₹84999
Rating: 4.7
Stock: 8

Instructions:
- Be concise and helpful.
- Do not invent specifications.

Answer:
"""

    print("\nResponse:")
    print(llm.generate(test_prompt))