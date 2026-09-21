import re


class AnswerEvaluator:
    """
    Lightweight answer evaluator for RAG grounding.

    Checks whether factual claims in an answer
    are supported by the supplied product context.
    """

    def normalize(self, text):
        text = str(text).lower()
        text = text.replace(",", "")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def extract_context_facts(self, context):
        context = self.normalize(context)

        facts = {
            "product_names": [],
            "brands": [],
            "categories": [],
            "prices": [],
            "ratings": [],
            "stock": [],
            "ram": [],
            "storage": [],
            "descriptions": []
        }

        # Product names
        names = re.findall(
            r"name:\s*(.*?)(?=\s+brand:|\s+category:|\s+description:|\s+price:|\s+rating:|\s+stock:|$)",
            context
        )

        facts["product_names"] = [
            name.strip()
            for name in names
        ]

        # Brands
        brands = re.findall(
            r"brand:\s*(.*?)(?=\s+category:|\s+description:|\s+price:|\s+rating:|\s+stock:|$)",
            context
        )

        facts["brands"] = [
            brand.strip()
            for brand in brands
        ]

        # Categories
        categories = re.findall(
            r"category:\s*(.*?)(?=\s+description:|\s+price:|\s+rating:|\s+stock:|$)",
            context
        )

        facts["categories"] = [
            category.strip()
            for category in categories
        ]

        # Prices
        prices = re.findall(
            r"price:\s*[₹]?\s*([\d,]+)",
            context
        )

        facts["prices"] = [
            price.replace(",", "")
            for price in prices
        ]

        # Ratings
        ratings = re.findall(
            r"rating:\s*([0-9]+(?:\.[0-9]+)?)",
            context
        )

        facts["ratings"] = ratings

        # Stock
        stock = re.findall(
            r"stock:\s*([0-9]+)",
            context
        )

        facts["stock"] = stock

        # RAM
        ram = re.findall(
            r"(\d+)\s*gb\s*ram",
            context
        )

        facts["ram"] = ram

        # Storage
        storage = re.findall(
            r"(\d+)\s*(gb|tb)\s*(?:ssd|storage)",
            context
        )

        facts["storage"] = [
            f"{value}{unit}"
            for value, unit in storage
        ]

        return facts

    def extract_answer_claims(self, answer):
        """
        Extract explicit factual values from the answer.
        """

        normalized = self.normalize(answer)

        claims = {
            "prices": [],
            "ratings": [],
            "stock": [],
            "ram": [],
            "storage": []
        }

        # Prices such as ₹84999, ₹84,999, 84999
        price_matches = re.findall(
            r"(?:₹|rs\.?|inr)?\s*(\d{4,6})",
            normalized
        )

        claims["prices"] = list(
            dict.fromkeys(price_matches)
        )

        # Ratings such as 4.7
        rating_matches = re.findall(
            r"(?:rating|rated|score)\s*(?:of|is|:)?\s*([0-5](?:\.[0-9]+)?)",
            normalized
        )

        claims["ratings"] = list(
            dict.fromkeys(rating_matches)
        )

        # Stock such as 8 units / 8 in stock
        stock_matches = re.findall(
            r"(\d+)\s*(?:units?|items?)?\s*(?:in\s+stock|available|stock)",
            normalized
        )

        claims["stock"] = list(
            dict.fromkeys(stock_matches)
        )

        # RAM
        ram_matches = re.findall(
            r"(\d+)\s*gb\s*ram",
            normalized
        )

        claims["ram"] = list(
            dict.fromkeys(ram_matches)
        )

        # Storage
        storage_matches = re.findall(
            r"(\d+)\s*(gb|tb)\s*(?:ssd|storage)",
            normalized
        )

        claims["storage"] = [
            f"{value}{unit}"
            for value, unit in storage_matches
        ]

        return claims

    def evaluate(self, answer, context):

        normalized_answer = self.normalize(answer)

        context_facts = self.extract_context_facts(
            context
        )

        answer_claims = self.extract_answer_claims(
            answer
        )

        supported_claims = []
        unsupported_claims = []

        # --------------------------------------------------
        # Product names
        # --------------------------------------------------

        for product_name in context_facts["product_names"]:

            if product_name in normalized_answer:

                supported_claims.append(
                    f"Product: {product_name}"
                )

        # --------------------------------------------------
        # Brands
        # --------------------------------------------------

        for brand in context_facts["brands"]:

            if brand in normalized_answer:

                supported_claims.append(
                    f"Brand: {brand}"
                )

        # --------------------------------------------------
        # Categories
        # --------------------------------------------------

        for category in context_facts["categories"]:

            if category in normalized_answer:

                supported_claims.append(
                    f"Category: {category}"
                )

        # --------------------------------------------------
        # Prices
        # --------------------------------------------------

        context_prices = set(
            context_facts["prices"]
        )

        for price in answer_claims["prices"]:

            if price in context_prices:

                supported_claims.append(
                    f"Price: {int(price):,}"
                )

            else:

                unsupported_claims.append(
                    f"Price: {int(price):,}"
                )

        # --------------------------------------------------
        # Ratings
        # --------------------------------------------------

        context_ratings = set(
            context_facts["ratings"]
        )

        for rating in answer_claims["ratings"]:

            if rating in context_ratings:

                supported_claims.append(
                    f"Rating: {rating}"
                )

            else:

                unsupported_claims.append(
                    f"Rating: {rating}"
                )

        # --------------------------------------------------
        # Stock
        # --------------------------------------------------

        context_stock = set(
            context_facts["stock"]
        )

        for stock in answer_claims["stock"]:

            if stock in context_stock:

                supported_claims.append(
                    f"Stock: {stock}"
                )

            else:

                unsupported_claims.append(
                    f"Stock: {stock}"
                )

        # --------------------------------------------------
        # RAM
        # --------------------------------------------------

        context_ram = set(
            context_facts["ram"]
        )

        for ram in answer_claims["ram"]:

            if ram in context_ram:

                supported_claims.append(
                    f"RAM: {ram}GB"
                )

            else:

                unsupported_claims.append(
                    f"RAM: {ram}GB"
                )

        # --------------------------------------------------
        # Storage
        # --------------------------------------------------

        context_storage = set(
            context_facts["storage"]
        )

        for storage in answer_claims["storage"]:

            if storage in context_storage:

                supported_claims.append(
                    f"Storage: {storage}"
                )

            else:

                unsupported_claims.append(
                    f"Storage: {storage}"
                )

        # --------------------------------------------------
        # Grounding score
        # --------------------------------------------------

        total_claims = (
            len(supported_claims)
            + len(unsupported_claims)
        )

        if total_claims > 0:

            grounding_score = (
                len(supported_claims)
                / total_claims
            )

        else:

            grounding_score = 0.0

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        if unsupported_claims:

            if grounding_score >= 0.50:
                status = "PARTIALLY GROUNDED"
            else:
                status = "NOT GROUNDED"

        elif supported_claims:

            status = "GROUNDED"

        else:

            status = "NOT GROUNDED"

        return {
            "answer": answer,
            "grounding_score": grounding_score,
            "supported_claims": supported_claims,
            "unsupported_claims": unsupported_claims,
            "status": status
        }


def main():

    print("=" * 70)
    print("IMPROVED ANSWER EVALUATION")
    print("=" * 70)

    evaluator = AnswerEvaluator()

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

    test_answers = [

        # ------------------------------------------
        # Test 1 - Fully grounded
        # ------------------------------------------

        (
            "The MacBook Air M2 is an Apple laptop. "
            "It costs ₹84,999 and has a rating of 4.7."
        ),

        # ------------------------------------------
        # Test 2 - Partially grounded
        # ------------------------------------------

        (
            "The MacBook Air M2 costs ₹84,999 "
            "and has 8 units in stock."
        ),

        # ------------------------------------------
        # Test 3 - Hallucinated facts
        # ------------------------------------------

        (
            "The MacBook Air M2 has 16GB RAM "
            "and costs ₹79,999."
        ),

        # ------------------------------------------
        # Test 4 - Correct RAM and storage
        # ------------------------------------------

        (
            "The MacBook Air M2 has 8GB RAM "
            "and 256GB SSD."
        )
    ]

    for index, answer in enumerate(
        test_answers,
        start=1
    ):

        print("\n" + "-" * 70)
        print(f"TEST ANSWER {index}")
        print("-" * 70)

        print("\nAnswer:")
        print(answer)

        result = evaluator.evaluate(
            answer=answer,
            context=context
        )

        print(
            f"\nGrounding Score : "
            f"{result['grounding_score']:.2f}"
        )

        print(
            f"Status          : "
            f"{result['status']}"
        )

        print("\nSupported Claims:")

        if result["supported_claims"]:

            for claim in result["supported_claims"]:
                print(f"  ✓ {claim}")

        else:

            print("  None detected")

        print("\nUnsupported Claims:")

        if result["unsupported_claims"]:

            for claim in result["unsupported_claims"]:
                print(f"  ✗ {claim}")

        else:

            print("  None detected")

    print("\n" + "=" * 70)
    print("IMPROVED ANSWER EVALUATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()