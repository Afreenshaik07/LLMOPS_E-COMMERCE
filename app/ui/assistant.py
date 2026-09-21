import streamlit as st
import pandas as pd
from pathlib import Path

from app.agent_router import AgentRouter


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #f4f7fb;
}

[data-testid="stSidebar"] {
    background-color: #07111f;
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* HERO */

.hero-box {
    background: linear-gradient(
        135deg,
        #111936 0%,
        #1e3a8a 55%,
        #2563eb 100%
    );
    padding: 42px;
    border-radius: 25px;
    margin-bottom: 30px;
    box-shadow: 0 15px 40px rgba(15, 23, 42, 0.18);
}

.hero-label {
    color: #bfdbfe;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-top: 12px;
}

.hero-text {
    color: #dbeafe;
    font-size: 17px;
    line-height: 1.7;
    margin-top: 12px;
    max-width: 850px;
}

/* PRODUCT CARD */

.product-card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    margin: 12px 0;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
}

.product-title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
}

.product-meta {
    color: #64748b;
    margin: 5px 0 15px 0;
}

.product-description {
    color: #334155;
    line-height: 1.6;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748b;
    padding: 35px 0 10px 0;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD ROUTER
# ============================================================

@st.cache_resource
def load_router():
    return AgentRouter()


router = load_router()


# ============================================================
# LOAD PRODUCT DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "products.csv"
)

try:
    products_df = pd.read_csv(CSV_PATH)
except Exception:
    products_df = pd.DataFrame()


# ============================================================
# FIND PRODUCTS IN QUERY
# ============================================================

def find_products_in_query(query):

    if products_df.empty:
        return []

    query_lower = query.lower()

    matches = []

    for product_name in products_df["product_name"]:

        product_lower = str(
            product_name
        ).lower()

        if product_lower in query_lower:
            matches.append(
                str(product_name)
            )

    return matches


# ============================================================
# DISPLAY PRODUCT
# ============================================================

def display_product(product):

    name = product.get(
        "product_name",
        "Unknown Product",
    )

    brand = product.get(
        "brand",
        "Unknown",
    )

    category = product.get(
        "category",
        "Unknown",
    )

    price = product.get(
        "price",
        "N/A",
    )

    rating = product.get(
        "rating",
        "N/A",
    )

    stock = product.get(
        "stock",
        "N/A",
    )

    description = product.get(
        "description",
        "No description available.",
    )

    try:
        formatted_price = f"₹{float(price):,.0f}"
    except (ValueError, TypeError):
        formatted_price = str(price)

    st.markdown(
        f"""
<div class="product-card">

<div class="product-title">
{name}
</div>

<div class="product-meta">
{brand} • {category}
</div>

<b>Price:</b> {formatted_price}<br>
<b>Rating:</b> {rating}<br>
<b>Stock:</b> {stock} units

<div class="product-description">
<br>
{description}
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## RAG Assistant"
    )

    st.markdown(
        "AI E-Commerce Product Intelligence"
    )

    st.success(
        "SYSTEM ACTIVE"
    )

    st.markdown("---")

    st.subheader(
        "Capabilities"
    )

    st.markdown(
        "Product Search"
    )

    st.markdown(
        "Product Details"
    )

    st.markdown(
        "Inventory Checking"
    )

    st.markdown(
        "Product Comparison"
    )

    st.markdown(
        "Grounded Answers"
    )

    st.markdown(
        "RAG Evaluation"
    )

    st.markdown(
        "LangGraph Routing"
    )

    st.markdown(
        "LLMOps Monitoring"
    )

    st.markdown("---")

    st.caption(
        "Advanced RAG E-Commerce Assistant"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero-box">

<div class="hero-label">
LLMOPS • RAG • LANGGRAPH
</div>

<div class="hero-title">
Intelligent E-Commerce Assistant
</div>

<div class="hero-text">
Advanced Retrieval-Augmented Generation system for
product discovery, product intelligence, inventory checking,
product comparison and grounded answer generation.
</div>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.subheader(
    "System Overview"
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Products Indexed",
        "15",
    )

with m2:
    st.metric(
        "Embedding Dimensions",
        "384",
    )

with m3:
    st.metric(
        "Agent Routes",
        "4",
    )

with m4:
    st.metric(
        "Architecture",
        "RAG",
    )


# ============================================================
# QUERY SECTION
# ============================================================

st.subheader(
    "Ask the E-Commerce Assistant"
)

query = st.text_input(
    "Product Query",
    placeholder=(
        "Example: I need an Apple laptop under 90000"
    ),
    label_visibility="collapsed",
)


# ============================================================
# EXAMPLE QUERIES
# ============================================================

st.caption(
    "Try an example"
)

b1, b2, b3, b4 = st.columns(4)

with b1:

    if st.button(
        "Apple laptop under ₹90K",
        width="stretch",
    ):

        query = (
            "I need an Apple laptop under 90000"
        )

with b2:

    if st.button(
        "MacBook details",
        width="stretch",
    ):

        query = (
            "Tell me about MacBook Air M2"
        )

with b3:

    if st.button(
        "MacBook inventory",
        width="stretch",
    ):

        query = (
            "How many MacBook Air M2 are in stock?"
        )

with b4:

    if st.button(
        "Compare laptops",
        width="stretch",
    ):

        query = (
            "Compare MacBook Air M2 and Galaxy Tab S9"
        )


# ============================================================
# PROCESS QUERY
# ============================================================

if query:

    st.subheader(
        "Assistant Response"
    )

    with st.spinner(
        "Running RAG pipeline..."
    ):

        try:

            # ------------------------------------------------
            # DETECT INTENT
            # ------------------------------------------------

            intent = router.detect_intent(
                query
            )

            # ------------------------------------------------
            # FIND PRODUCT NAMES
            # ------------------------------------------------

            product_names = (
                find_products_in_query(
                    query
                )
            )

            # ------------------------------------------------
            # EXECUTE TOOL
            # ------------------------------------------------

            result = None

            # =================================================
            # COMPARISON
            # =================================================

            if intent == "comparison":

                if len(product_names) >= 2:

                    result = (
                        router.comparison_tool.compare(
                            product_names[0],
                            product_names[1],
                        )
                    )

                else:

                    st.warning(
                        "Please mention two product names to compare."
                    )

            # =================================================
            # PRODUCT DETAILS
            # =================================================

            elif intent == "product_details":

                if product_names:

                    result = (
                        router.details_tool.get_details(
                            product_names[0]
                        )
                    )

                else:

                    st.warning(
                        "Please mention the product name."
                    )

            # =================================================
            # INVENTORY
            # =================================================

            elif intent == "inventory":

                if product_names:

                    result = (
                        router.inventory_tool.check_stock(
                            product_names[0]
                        )
                    )

                else:

                    st.warning(
                        "Please mention the product name."
                    )

            # =================================================
            # PRODUCT SEARCH
            # =================================================

            else:

                result = (
                    router.search_tool.search(
                        query
                    )
                )

            # ------------------------------------------------
            # NORMALIZE RESULTS
            # ------------------------------------------------

            products = []

            if isinstance(
                result,
                list,
            ):

                products = result

            elif isinstance(
                result,
                dict,
            ):

                if "product1" in result:

                    products.append(
                        result["product1"]
                    )

                if "product2" in result:

                    products.append(
                        result["product2"]
                    )

                if not products:

                    product_name = result.get(
                        "product_name"
                    )

                    if product_name:

                        full_product = (
                            router.details_tool.get_details(
                                product_name
                            )
                        )

                        if full_product:

                            products.append(
                                full_product
                            )

                        else:

                            products.append(
                                result
                            )

            # =================================================
            # NO RESULT
            # =================================================

            if not products:

                st.error(
                    "No matching product information was found."
                )

            else:

                # =================================================
                # COMPARISON
                # =================================================

                if (
                    intent == "comparison"
                    and len(products) >= 2
                ):

                    st.success(
                        "Product comparison completed."
                    )

                    p1 = products[0]
                    p2 = products[1]

                    display_product(
                        p1
                    )

                    display_product(
                        p2
                    )

                    st.subheader(
                        "Comparison Table"
                    )

                    # Convert every cell to STRING.
                    # This prevents PyArrow mixed-type errors.

                    product1_name = str(
                        p1.get(
                            "product_name",
                            "Product 1",
                        )
                    )

                    product2_name = str(
                        p2.get(
                            "product_name",
                            "Product 2",
                        )
                    )

                    comparison_df = pd.DataFrame(
                        {
                            "Feature": [
                                "Brand",
                                "Category",
                                "Price",
                                "Rating",
                                "Stock",
                            ],

                            product1_name: [
                                str(
                                    p1.get(
                                        "brand",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p1.get(
                                        "category",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p1.get(
                                        "price",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p1.get(
                                        "rating",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p1.get(
                                        "stock",
                                        "N/A",
                                    )
                                ),
                            ],

                            product2_name: [
                                str(
                                    p2.get(
                                        "brand",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p2.get(
                                        "category",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p2.get(
                                        "price",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p2.get(
                                        "rating",
                                        "N/A",
                                    )
                                ),

                                str(
                                    p2.get(
                                        "stock",
                                        "N/A",
                                    )
                                ),
                            ],
                        }
                    )

                    # Force complete DataFrame to strings.
                    comparison_df = (
                        comparison_df.astype(str)
                    )

                    st.dataframe(
                        comparison_df,
                        width="stretch",
                        hide_index=True,
                    )

                    st.info(
                        "Comparison generated from retrieved "
                        "product information."
                    )

                # =================================================
                # INVENTORY
                # =================================================

                elif intent == "inventory":

                    product = products[0]

                    display_product(
                        product
                    )

                    stock = product.get(
                        "stock",
                        0,
                    )

                    try:

                        stock = int(
                            float(stock)
                        )

                    except (
                        ValueError,
                        TypeError,
                    ):

                        stock = 0

                    if stock > 10:

                        st.success(
                            f"{stock} units are currently in stock."
                        )

                    elif stock > 0:

                        st.warning(
                            f"Only {stock} units are currently in stock."
                        )

                    else:

                        st.error(
                            "Product is currently out of stock."
                        )

                # =================================================
                # PRODUCT DETAILS
                # =================================================

                elif intent == "product_details":

                    product = products[0]

                    display_product(
                        product
                    )

                    st.success(
                        "Complete product details retrieved."
                    )

                # =================================================
                # PRODUCT SEARCH
                # =================================================

                else:

                    st.success(
                        f"Found {len(products)} matching product(s)."
                    )

                    for product in products:

                        display_product(
                            product
                        )

                # =================================================
                # PIPELINE INFORMATION
                # =================================================

                st.subheader(
                    "Pipeline Information"
                )

                p1, p2, p3, p4 = st.columns(4)

                with p1:

                    st.info(
                        f"Intent\n\n{intent}"
                    )

                with p2:

                    st.info(
                        f"Retrieved\n\n{len(products)} products"
                    )

                with p3:

                    st.info(
                        "Retriever\n\n"
                        "Sentence Transformers"
                    )

                with p4:

                    st.info(
                        "Router\n\n"
                        "LangGraph"
                    )

        except Exception as error:

            st.error(
                "An error occurred while processing the request."
            )

            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "---"
)

st.caption(
    "Advanced RAG E-Commerce Assistant | "
    "Retrieval | Reranking | LangGraph | LLMOps"
)