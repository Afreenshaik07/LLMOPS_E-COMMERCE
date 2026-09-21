from app.agent.state import AgentState
from app.agent_router import AgentRouter
from app.llm.generator import MockLLM
from app.context_builder import build_context
from app.rag_prompt import build_rag_prompt
from app.monitoring.tracer import LLMOpsTracer
from app.evaluation.answer_eval import AnswerEvaluator


router = AgentRouter()
llm = MockLLM()
tracer = LLMOpsTracer()
answer_evaluator = AnswerEvaluator()


def router_node(state: AgentState):
    query = state["query"]

    tracer.start_trace(query)

    intent = router.detect_intent(query)

    print("\n[ROUTER NODE]")
    print(f"Query  : {query}")
    print(f"Intent : {intent}")

    tracer.record_event(
        "router",
        intent=intent
    )

    return {"intent": intent}


def product_search_node(state: AgentState):
    query = state["query"]

    print("\n[PRODUCT SEARCH NODE]")

    result = router.search_tool.search(query)

    tracer.record_event(
        "product_search",
        results_count=len(result)
        if isinstance(result, list)
        else 0
    )

    return {"tool_result": result}


def product_details_node(state: AgentState):
    product_name = state["product_name"]

    print("\n[PRODUCT DETAILS NODE]")
    print(f"Product : {product_name}")

    result = router.details_tool.get_details(
        product_name
    )

    tracer.record_event(
        "product_details",
        product=product_name,
        found=result is not None
    )

    return {"tool_result": result}


def inventory_node(state: AgentState):
    product_name = state["product_name"]

    print("\n[INVENTORY NODE]")
    print(f"Product : {product_name}")

    result = router.inventory_tool.check_stock(
        product_name
    )

    tracer.record_event(
        "inventory",
        product=product_name,
        found=result is not None
    )

    return {"tool_result": result}


def comparison_node(state: AgentState):
    product1 = state["product_name"]
    product2 = state["product_name_2"]

    print("\n[COMPARISON NODE]")
    print(f"Product 1 : {product1}")
    print(f"Product 2 : {product2}")

    result = router.comparison_tool.compare(
        product1,
        product2
    )

    tracer.record_event(
        "comparison",
        product1=product1,
        product2=product2
    )

    return {"tool_result": result}


def response_node(state: AgentState):
    print("\n[LLM RESPONSE NODE]")

    result = state.get("tool_result")
    intent = state.get("intent")

    if not result:

        response = (
            "I could not find the requested information."
        )

        tracer.record_event(
            "response",
            status="no_result"
        )

        trace = tracer.end_trace()
        tracer.print_trace(trace)

        return {
            "response": response
        }

    # --------------------------------------------------
    # Build product list
    # --------------------------------------------------

    if intent == "inventory":

        product_name = state.get(
            "product_name"
        )

        print(
            "\n[INVENTORY CONTEXT ENRICHMENT]"
        )

        print(
            f"Fetching complete details for: "
            f"{product_name}"
        )

        full_product = (
            router.details_tool.get_details(
                product_name
            )
        )

        if full_product:
            products = [full_product]
        else:
            products = [result]

    elif isinstance(result, list):

        products = result

    elif isinstance(result, dict):

        products = []

        if "product1" in result:
            products.append(
                result["product1"]
            )

        if "product2" in result:
            products.append(
                result["product2"]
            )

        if not products:
            products.append(result)

    else:

        products = []

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    tracer.record_event(
        "context_builder",
        products_count=len(products)
    )

    context = build_context(products)

    print("\n[CONTEXT]")
    print(context)

    # --------------------------------------------------
    # RAG Prompt
    # --------------------------------------------------

    prompt = build_rag_prompt(
        query=state["query"],
        context=context
    )

    print("\n[GENERATED PROMPT]")
    print(prompt)

    tracer.record_event(
        "rag_prompt",
        context_length=len(context),
        prompt_length=len(prompt)
    )

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------

    response = llm.generate(prompt)

    print("\n[LLM OUTPUT]")
    print(response)

    tracer.record_event(
        "llm",
        provider="MockLLM",
        response_length=len(response)
    )

    # --------------------------------------------------
    # Answer Evaluation
    # --------------------------------------------------

    evaluation = answer_evaluator.evaluate(
        answer=response,
        context=context
    )

    print("\n[ANSWER EVALUATION]")
    print(
        f"Grounding Score : "
        f"{evaluation['grounding_score']:.2f}"
    )

    print(
        f"Status          : "
        f"{evaluation['status']}"
    )

    print("\nSupported Claims:")

    if evaluation["supported_claims"]:

        for claim in evaluation[
            "supported_claims"
        ]:
            print(f"  ✓ {claim}")

    else:

        print("  None detected")

    print("\nUnsupported Claims:")

    if evaluation["unsupported_claims"]:

        for claim in evaluation[
            "unsupported_claims"
        ]:
            print(f"  ✗ {claim}")

    else:

        print("  None detected")

    # --------------------------------------------------
    # Add evaluation to trace
    # --------------------------------------------------

    tracer.record_event(
        "answer_evaluation",
        grounding_score=round(
            evaluation["grounding_score"],
            4
        ),
        status=evaluation["status"],
        supported_claims=len(
            evaluation["supported_claims"]
        ),
        unsupported_claims=len(
            evaluation["unsupported_claims"]
        )
    )

    # --------------------------------------------------
    # End Trace
    # --------------------------------------------------

    trace = tracer.end_trace()

    tracer.print_trace(trace)

    return {
        "response": response
    }