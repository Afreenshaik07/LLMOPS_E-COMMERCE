import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NexaRAG",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp {
    background: #f4f6f9;
}

.block-container {
    max-width: 1380px;
    padding: 0 42px 40px 42px;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

section[data-testid="stSidebar"] .stButton button {
    background: transparent;
    border: 1px solid transparent;
    color: #cbd5e1;
    text-align: left;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #1e293b;
    color: white;
}


/* ==========================================================
   TOP BAR
   ========================================================== */

.topbar {
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 30px;
}

.brand {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
}

.brand span {
    color: #475569;
    font-weight: 500;
}

.status {
    font-size: 12px;
    color: #475569;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 7px 12px;
    border-radius: 20px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    border-radius: 20px;
    padding: 38px 42px;
    margin-bottom: 28px;
}

.hero-small {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 9px;
}

.hero-title {
    color: white;
    font-size: 36px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 10px;
}

.hero-text {
    color: #cbd5e1;
    font-size: 15px;
    max-width: 650px;
    line-height: 1.6;
}


/* ==========================================================
   SEARCH
   ========================================================== */

.search-box {
    background: white;
    border: 1px solid #dbe2ea;
    border-radius: 13px;
    padding: 7px;
    margin-top: -8px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.06);
}

div[data-testid="stTextInput"] input {
    border: none;
    box-shadow: none;
    height: 50px;
    font-size: 15px;
    background: transparent;
}

div[data-testid="stTextInput"] input:focus {
    border: none;
    box-shadow: none;
}


/* ==========================================================
   QUICK ACTIONS
   ========================================================== */

.quick-title {
    color: #64748b;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: 8px;
}

.stButton > button {
    border-radius: 9px;
    border: 1px solid #d7dee8;
    background: white;
    color: #334155;
    font-size: 13px;
    font-weight: 600;
    min-height: 40px;
}

.stButton > button:hover {
    border-color: #475569;
    background: #f8fafc;
}


/* ==========================================================
   SECTION
   ========================================================== */

.section-heading {
    color: #0f172a;
    font-size: 21px;
    font-weight: 750;
    margin-top: 30px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 18px;
}


/* ==========================================================
   PRODUCT CARD
   ========================================================== */

.product-card {
    background: white;
    border: 1px solid #e1e7ef;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.045);
}

.product-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 10px 28px rgba(15,23,42,0.08);
}

.product-category {
    display: inline-block;
    background: #f1f5f9;
    color: #475569;
    border-radius: 6px;
    padding: 5px 9px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .7px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.product-title {
    color: #0f172a;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 4px;
}

.product-brand {
    color: #64748b;
    font-size: 13px;
}

.product-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.55;
    margin-top: 13px;
    max-width: 720px;
}

.product-price {
    color: #0f172a;
    font-size: 24px;
    font-weight: 800;
    text-align: right;
}

.product-id {
    color: #94a3b8;
    font-size: 11px;
    text-align: right;
    margin-top: 5px;
}

.product-meta {
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid #eef2f6;
}

.meta-label {
    color: #94a3b8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .7px;
    text-transform: uppercase;
}

.meta-value {
    color: #334155;
    font-size: 13px;
    font-weight: 650;
    margin-top: 4px;
}

.stock-good {
    color: #166534;
    background: #f0fdf4;
    padding: 5px 9px;
    border-radius: 6px;
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
}

.stock-low {
    color: #a16207;
    background: #fefce8;
    padding: 5px 9px;
    border-radius: 6px;
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
}


/* ==========================================================
   STATS
   ========================================================== */

.stat {
    background: white;
    border: 1px solid #e1e7ef;
    border-radius: 13px;
    padding: 15px 18px;
}

.stat-label {
    color: #64748b;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.stat-value {
    color: #0f172a;
    font-size: 21px;
    font-weight: 750;
    margin-top: 3px;
}


/* ==========================================================
   EMPTY STATE
   ========================================================== */

.empty {
    background: white;
    border: 1px solid #e1e7ef;
    border-radius: 17px;
    padding: 45px;
    text-align: center;
    margin-top: 25px;
}

.empty-title {
    color: #334155;
    font-size: 19px;
    font-weight: 700;
}

.empty-text {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 7px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    color: #94a3b8;
    text-align: center;
    font-size: 11px;
    padding: 30px 0 10px;
}

</style>
""",
unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "raw" / "products.csv"


@st.cache_data
def load_products():
    return pd.read_csv(DATA_PATH)


products = load_products()


# ============================================================
# SEARCH
# ============================================================

def search_products(query):

    query = query.lower().strip()

    exact = products[
        products.apply(
            lambda row:
            str(row["product_name"]).lower() in query
            or str(row["brand"]).lower() in query
            or str(row["category"]).lower() in query,
            axis=1,
        )
    ]

    if not exact.empty:
        return exact

    words = [
        x for x in query.split()
        if len(x) > 2
    ]

    if not words:
        return pd.DataFrame()

    result = products[
        products.apply(
            lambda row: any(
                word in str(row["product_name"]).lower()
                or word in str(row["brand"]).lower()
                or word in str(row["category"]).lower()
                or word in str(row["description"]).lower()
                for word in words
            ),
            axis=1,
        )
    ]

    return result.head(10)


# ============================================================
# PRODUCT CARD
# ============================================================

def show_product(product):

    stock = int(product["stock"])

    if stock <= 10:
        stock_class = "stock-low"
        stock_text = f"Only {stock} left"
    else:
        stock_class = "stock-good"
        stock_text = f"{stock} in stock"

    html = f"""
<div class="product-card">

<div style="display:flex;justify-content:space-between;gap:30px;">

<div style="flex:1;">

<div class="product-category">{product["category"]}</div>

<div class="product-title">{product["product_name"]}</div>

<div class="product-brand">
{product["brand"]} · {product["category"]}
</div>

<div class="product-description">
{product["description"]}
</div>

</div>

<div style="min-width:145px;">

<div class="product-price">
₹{product["price"]:,.0f}
</div>

<div class="product-id">
{product["product_id"]}
</div>

</div>

</div>

<div class="product-meta">

<div style="display:flex;gap:55px;align-items:center;">

<div>
<div class="meta-label">Rating</div>
<div class="meta-value">★ {product["rating"]} / 5</div>
</div>

<div>
<div class="meta-label">Availability</div>
<div class="{stock_class}">{stock_text}</div>
</div>

<div>
<div class="meta-label">Brand</div>
<div class="meta-value">{product["brand"]}</div>
</div>

</div>

</div>

</div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:25px;
            font-weight:800;
            color:white;
            margin-top:8px;
        ">
        NexaRAG
        </div>

        <div style="
            color:#94a3b8;
            font-size:12px;
            margin-top:5px;
        ">
        E-Commerce Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.divider()

    st.markdown("**PLATFORM**")

    st.caption("Product Discovery")
    st.caption("Inventory Intelligence")
    st.caption("Product Comparison")

    st.write("")

    st.markdown("**KNOWLEDGE BASE**")

    st.info(
        f"{len(products)} products"
    )

    st.write("")

    st.markdown("**SYSTEM**")

    st.success("Online")

    st.caption("Docker Runtime")


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
<div class="topbar">

<div class="brand">
NexaRAG <span>/ E-Commerce Assistant</span>
</div>

<div class="status">
● System Online
</div>

</div>
""",
unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-small">
Intelligent Product Discovery
</div>

<div class="hero-title">
Find the right product.
</div>

<div class="hero-text">
Search products, explore specifications, check inventory
and compare products through one intelligent interface.
</div>

</div>
""",
unsafe_allow_html=True,
)


# ============================================================
# SEARCH
# ============================================================

query = st.text_input(
    "Search",
    placeholder="Search for a product, brand, category or inventory...",
    label_visibility="collapsed",
)


# ============================================================
# QUICK SEARCH
# ============================================================

st.markdown(
    '<div class="quick-title">Quick Search</div>',
    unsafe_allow_html=True,
)

q1, q2, q3, q4 = st.columns(4)

quick_queries = [
    "MacBook Air M2",
    "Galaxy Tab S9",
    "WH-CH520",
    "Compare MacBook Air M2 and Galaxy Tab S9",
]

for col, value in zip(
    [q1, q2, q3, q4],
    quick_queries,
):

    with col:

        if st.button(
            value,
            width="stretch",
        ):

            st.session_state["query"] = value
            st.rerun()


if (
    "query" in st.session_state
    and not query
):

    query = st.session_state["query"]


# ============================================================
# PLATFORM STATS
# ============================================================

st.write("")

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        f"""
<div class="stat">
<div class="stat-label">Products</div>
<div class="stat-value">{len(products)}</div>
</div>
""",
        unsafe_allow_html=True,
    )

with s2:

    st.markdown(
        f"""
<div class="stat">
<div class="stat-label">Categories</div>
<div class="stat-value">{products["category"].nunique()}</div>
</div>
""",
        unsafe_allow_html=True,
    )

with s3:

    st.markdown(
        f"""
<div class="stat">
<div class="stat-label">Available Units</div>
<div class="stat-value">{int(products["stock"].sum())}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# RESULTS
# ============================================================

if query:

    query_lower = query.lower()

    st.markdown(
        '<div class="section-heading">Search Results</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # COMPARISON
    # ========================================================

    if "compare" in query_lower:

        matched = [
            name
            for name in products["product_name"]
            if name.lower() in query_lower
        ]

        if len(matched) >= 2:

            p1 = products[
                products["product_name"] == matched[0]
            ].iloc[0]

            p2 = products[
                products["product_name"] == matched[1]
            ].iloc[0]

            st.markdown(
                f"""
<div class="section-subtitle">
Comparing {matched[0]} and {matched[1]}
</div>
""",
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)

            with c1:
                show_product(p1)

            with c2:
                show_product(p2)

        else:

            st.warning(
                "Please provide two product names."
            )


    # ========================================================
    # INVENTORY
    # ========================================================

    elif any(
        word in query_lower
        for word in [
            "stock",
            "inventory",
            "units",
            "available",
        ]
    ):

        matched = [
            name
            for name in products["product_name"]
            if name.lower() in query_lower
        ]

        if matched:

            product = products[
                products["product_name"] == matched[0]
            ].iloc[0]

            st.markdown(
                f"""
<div class="section-subtitle">
Current availability for {product["product_name"]}
</div>
""",
                unsafe_allow_html=True,
            )

            show_product(product)

        else:

            st.warning(
                "Product not found."
            )


    # ========================================================
    # NORMAL SEARCH
    # ========================================================

    else:

        results = search_products(query)

        if results.empty:

            st.markdown(
                """
<div class="empty">

<div class="empty-title">
No products found
</div>

<div class="empty-text">
Try searching by product name, brand or category.
</div>

</div>
""",
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
<div class="section-subtitle">
{len(results)} product(s) found
</div>
""",
                unsafe_allow_html=True,
            )

            for _, product in results.iterrows():

                show_product(product)


# ============================================================
# LANDING PAGE
# ============================================================

else:

    st.markdown(
        """
<div class="empty">

<div class="empty-title">
What are you looking for?
</div>

<div class="empty-text">
Search the product catalog or use one of the quick searches above.
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
NexaRAG · E-Commerce Intelligence Platform · Docker
</div>
""",
    unsafe_allow_html=True,
)