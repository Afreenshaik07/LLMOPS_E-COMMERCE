class LLMGenerator:
    """
    LLM generation interface.

    The actual LLM provider will be connected later.
    """

    def generate(self, prompt):
        """
        Generate an answer from the provided prompt.
        """

        raise NotImplementedError(
            "LLM provider has not been connected yet."
        )


class MockLLMGenerator(LLMGenerator):
    """
    Temporary LLM used for testing the pipeline.
    """

    def generate(self, prompt):

        return (
            "The MacBook Air M2 is an Apple laptop available "
            "under ₹90,000. It costs ₹84,999 and has a "
            "4.7 rating."
        )


def main():

    print("=" * 60)
    print("LLM GENERATOR TEST")
    print("=" * 60)

    generator = MockLLMGenerator()

    prompt = "I need an Apple laptop under 90000."

    answer = generator.generate(prompt)

    print("\nGenerated Answer:")
    print("-" * 60)
    print(answer)


if __name__ == "__main__":
    main()