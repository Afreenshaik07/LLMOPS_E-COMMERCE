import json
import os
import time
import uuid
from datetime import datetime


class LLMOpsTracer:
    """
    Lightweight LLMOps tracer.

    Responsibilities:
    - Track execution events
    - Measure total latency
    - Generate a unique run ID
    - Persist completed traces to logs/runs.jsonl
    """

    def __init__(self, log_file="logs/runs.jsonl"):
        self.start_time = None
        self.events = []
        self.run_id = None
        self.query = None
        self.log_file = log_file

    def start_trace(self, query):
        self.start_time = time.perf_counter()
        self.events = []
        self.run_id = str(uuid.uuid4())
        self.query = query

        self.events.append({
            "event": "trace_started",
            "timestamp": datetime.now().isoformat(),
            "query": query
        })

    def record_event(self, event_name, **metadata):
        event = {
            "event": event_name,
            "timestamp": datetime.now().isoformat(),
            **metadata
        }

        self.events.append(event)

    def end_trace(self):
        if self.start_time is None:
            return None

        total_latency = time.perf_counter() - self.start_time

        trace = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "query": self.query,
            "total_latency_seconds": round(total_latency, 4),
            "events": self.events
        }

        self._save_trace(trace)

        self.start_time = None

        return trace

    def _save_trace(self, trace):
        """
        Append the completed trace to JSON Lines log.
        """

        log_directory = os.path.dirname(self.log_file)

        if log_directory:
            os.makedirs(log_directory, exist_ok=True)

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(
                    trace,
                    ensure_ascii=False
                )
                + "\n"
            )

    def print_trace(self, trace):
        print("\n" + "=" * 70)
        print("LLMOPS TRACE")
        print("=" * 70)

        if not trace:
            print("No trace available.")
            return

        print(f"Run ID        : {trace['run_id']}")
        print(f"Query         : {trace['query']}")
        print(
            f"Total Latency : "
            f"{trace['total_latency_seconds']:.4f} seconds"
        )

        print("\nEvents:")

        for index, event in enumerate(
            trace["events"],
            start=1
        ):

            print(
                f"\n{index}. {event['event']}"
            )

            for key, value in event.items():

                if key not in [
                    "event",
                    "timestamp"
                ]:
                    print(
                        f"   {key}: {value}"
                    )

        print("\n" + "=" * 70)


def main():

    print("=" * 70)
    print("LLMOPS PERSISTENT TRACER TEST")
    print("=" * 70)

    tracer = LLMOpsTracer()

    tracer.start_trace(
        "I need an Apple laptop under 90000"
    )

    tracer.record_event(
        "router",
        intent="product_search"
    )

    tracer.record_event(
        "retrieval",
        documents_retrieved=5
    )

    tracer.record_event(
        "reranking",
        documents_reranked=5
    )

    tracer.record_event(
        "llm",
        provider="MockLLM"
    )

    trace = tracer.end_trace()

    tracer.print_trace(trace)

    print("\nTrace saved to:")
    print("logs/runs.jsonl")


if __name__ == "__main__":
    main()