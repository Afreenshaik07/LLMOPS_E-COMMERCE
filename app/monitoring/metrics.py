import json
import os
from collections import Counter


class LLMOpsMetrics:

    def __init__(self, log_file="logs/runs.jsonl"):
        self.log_file = log_file

    def load_runs(self):

        if not os.path.exists(self.log_file):
            return []

        runs = []

        with open(self.log_file, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:
                    runs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return runs

    def calculate(self):

        runs = self.load_runs()

        latencies = []
        context_sizes = []
        prompt_sizes = []
        response_sizes = []
        intents = []

        grounding_scores = []
        grounding_statuses = []

        for run in runs:

            latency = run.get("total_latency_seconds")

            if isinstance(latency, (int, float)):
                latencies.append(latency)

            for event in run.get("events", []):

                event_name = event.get("event")

                if event_name == "router":

                    intent = event.get("intent")

                    if intent:
                        intents.append(intent)

                elif event_name == "rag_prompt":

                    context = event.get("context_length")
                    prompt = event.get("prompt_length")

                    if isinstance(context, (int, float)):
                        context_sizes.append(context)

                    if isinstance(prompt, (int, float)):
                        prompt_sizes.append(prompt)

                elif event_name == "llm":

                    response = event.get("response_length")

                    if isinstance(response, (int, float)):
                        response_sizes.append(response)

                elif event_name == "answer_evaluation":

                    score = event.get("grounding_score")
                    status = event.get("status")

                    if isinstance(score, (int, float)):
                        grounding_scores.append(score)

                    if status:
                        grounding_statuses.append(status)

        grounded_count = grounding_statuses.count("GROUNDED")

        grounded_rate = (
            grounded_count / len(grounding_statuses)
            if grounding_statuses
            else 0.0
        )

        return {

            "total_runs": len(runs),

            "average_latency": (
                sum(latencies) / len(latencies)
                if latencies else 0.0
            ),

            "minimum_latency": (
                min(latencies)
                if latencies else 0.0
            ),

            "maximum_latency": (
                max(latencies)
                if latencies else 0.0
            ),

            "intent_distribution": dict(
                Counter(intents)
            ),

            "average_context_size": (
                sum(context_sizes) / len(context_sizes)
                if context_sizes else 0.0
            ),

            "average_prompt_size": (
                sum(prompt_sizes) / len(prompt_sizes)
                if prompt_sizes else 0.0
            ),

            "average_response_size": (
                sum(response_sizes) / len(response_sizes)
                if response_sizes else 0.0
            ),

            "average_grounding_score": (
                sum(grounding_scores) / len(grounding_scores)
                if grounding_scores else 0.0
            ),

            "grounding_status_distribution": dict(
                Counter(grounding_statuses)
            ),

            "grounded_rate": grounded_rate,
        }

    def print_metrics(self, metrics):

        print("\n" + "=" * 70)
        print("LLMOPS METRICS")
        print("=" * 70)

        print(
            f"Total Runs          : "
            f"{metrics['total_runs']}"
        )

        print(
            f"Average Latency     : "
            f"{metrics['average_latency']:.4f} seconds"
        )

        print(
            f"Minimum Latency     : "
            f"{metrics['minimum_latency']:.4f} seconds"
        )

        print(
            f"Maximum Latency     : "
            f"{metrics['maximum_latency']:.4f} seconds"
        )

        print("\nIntent Distribution:")

        for intent, count in metrics[
            "intent_distribution"
        ].items():

            print(
                f"  {intent}: {count}"
            )

        print(
            "\nAverage Context Size : "
            f"{metrics['average_context_size']:.2f} characters"
        )

        print(
            "Average Prompt Size  : "
            f"{metrics['average_prompt_size']:.2f} characters"
        )

        print(
            "Average Response Size: "
            f"{metrics['average_response_size']:.2f} characters"
        )

        print("\nGrounding Metrics:")

        print(
            f"  Average Grounding Score : "
            f"{metrics['average_grounding_score']:.2f}"
        )

        print(
            f"  Grounded Rate           : "
            f"{metrics['grounded_rate'] * 100:.2f}%"
        )

        print("\n  Grounding Status:")

        for status, count in metrics[
            "grounding_status_distribution"
        ].items():

            print(
                f"    {status}: {count}"
            )

        print("=" * 70)


def main():

    print("=" * 70)
    print("LLMOPS METRICS ANALYSIS")
    print("=" * 70)

    evaluator = LLMOpsMetrics()

    metrics = evaluator.calculate()

    evaluator.print_metrics(metrics)


if __name__ == "__main__":
    main()
    