from app.retriever import ProductRetriever


class RetrievalEvaluator:
    """
    Evaluates the quality of the product retrieval system.

    Metrics:
    - Recall@K
    - Precision@K
    - Hit Rate
    """

    def __init__(self):
        self.retriever = ProductRetriever()

    def evaluate(self, query, expected_products, top_k=5):
        """
        Evaluate retrieval quality.

        Parameters:
            query: User search query
            expected_products: Products expected to be retrieved
            top_k: Number of products to retrieve
        """

        # -------------------------------------------------
        # RUN RETRIEVAL
        # -------------------------------------------------

        results = self.retriever.search(
            query,
            top_k=top_k
        )

        # Extract retrieved product names
        retrieved_products = [
            product["product_name"]
            for product in results
        ]

        # Convert to sets for comparison
        expected_set = set(expected_products)
        retrieved_set = set(retrieved_products)

        # -------------------------------------------------
        # FIND RELEVANT RETRIEVED PRODUCTS
        # -------------------------------------------------

        relevant_retrieved = (
            expected_set.intersection(retrieved_set)
        )

        # -------------------------------------------------
        # RECALL@K
        # -------------------------------------------------
        #
        # Recall = Relevant retrieved products
        #          ----------------------------
        #          Expected relevant products
        #
        # -------------------------------------------------

        if expected_set:
            recall_at_k = (
                len(relevant_retrieved)
                / len(expected_set)
            )
        else:
            recall_at_k = 0.0

        # -------------------------------------------------
        # PRECISION@K
        # -------------------------------------------------
        #
        # Precision = Relevant retrieved products
        #             ----------------------------
        #             Retrieved products
        #
        # -------------------------------------------------

        if retrieved_set:
            precision_at_k = (
                len(relevant_retrieved)
                / len(retrieved_set)
            )
        else:
            precision_at_k = 0.0

        # -------------------------------------------------
        # HIT RATE
        # -------------------------------------------------

        hit_rate = (
            1.0
            if relevant_retrieved
            else 0.0
        )

        # -------------------------------------------------
        # RETURN EVALUATION RESULT
        # -------------------------------------------------

        return {
            "query": query,
            "expected_products": expected_products,
            "retrieved_products": retrieved_products,
            "relevant_retrieved": list(
                relevant_retrieved
            ),
            "recall_at_k": recall_at_k,
            "precision_at_k": precision_at_k,
            "hit_rate": hit_rate,
            "top_k": top_k,
        }


def main():

    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    evaluator = RetrievalEvaluator()

    # -----------------------------------------------------
    # EVALUATION DATASET
    # -----------------------------------------------------

    test_cases = [
        {
            "query": "I need an Apple laptop",
            "expected_products": [
                "MacBook Air M2"
            ],
        },
        {
            "query": "wireless headphones",
            "expected_products": [
                "WH-CH520",
                "AirPods 4",
                "Galaxy Buds FE",
            ],
        },
        {
            "query": "wireless mouse",
            "expected_products": [
                "MX Master 3S",
                "Magic Mouse",
            ],
        },
    ]

    # -----------------------------------------------------
    # METRIC ACCUMULATORS
    # -----------------------------------------------------

    total_recall = 0.0
    total_precision = 0.0
    total_hit_rate = 0.0

    # -----------------------------------------------------
    # RUN TEST CASES
    # -----------------------------------------------------

    for index, test_case in enumerate(
        test_cases,
        start=1
    ):

        print("\n" + "-" * 70)
        print(f"TEST CASE {index}")
        print("-" * 70)

        result = evaluator.evaluate(
            query=test_case["query"],
            expected_products=test_case["expected_products"],
            top_k=5,
        )

        # -------------------------------------------------
        # DISPLAY RESULTS
        # -------------------------------------------------

        print(
            f"Query       : "
            f"{result['query']}"
        )

        print(
            f"Expected    : "
            f"{result['expected_products']}"
        )

        print(
            f"Retrieved   : "
            f"{result['retrieved_products']}"
        )

        print(
            f"Relevant    : "
            f"{result['relevant_retrieved']}"
        )

        print(
            f"Recall@5    : "
            f"{result['recall_at_k']:.2f}"
        )

        print(
            f"Precision@5 : "
            f"{result['precision_at_k']:.2f}"
        )

        print(
            f"Hit Rate    : "
            f"{result['hit_rate']:.2f}"
        )

        # -------------------------------------------------
        # ADD TO TOTALS
        # -------------------------------------------------

        total_recall += result["recall_at_k"]

        total_precision += result["precision_at_k"]

        total_hit_rate += result["hit_rate"]

    # -----------------------------------------------------
    # CALCULATE AVERAGES
    # -----------------------------------------------------

    number_of_tests = len(test_cases)

    average_recall = (
        total_recall
        / number_of_tests
    )

    average_precision = (
        total_precision
        / number_of_tests
    )

    average_hit_rate = (
        total_hit_rate
        / number_of_tests
    )

    # -----------------------------------------------------
    # FINAL REPORT
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("OVERALL RETRIEVAL PERFORMANCE")
    print("=" * 70)

    print(
        f"Average Recall@5    : "
        f"{average_recall:.2f}"
    )

    print(
        f"Average Precision@5 : "
        f"{average_precision:.2f}"
    )

    print(
        f"Average Hit Rate    : "
        f"{average_hit_rate:.2f}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()