import json
import os

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RAG LLMOps Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
<style>

    /* ---------- APP ---------- */

    .stApp {
        background-color: #f8fafc;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* ---------- MAIN HEADINGS ---------- */

    h1 {
        color: #0f172a;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #1e293b;
        font-weight: 750;
    }

    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 800;
    }

    /* ---------- CONTAINERS ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        border-color: #e2e8f0;
        background-color: white;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }

    /* ---------- DATAFRAME ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* ---------- STATUS ---------- */

    .status-active {
        padding: 10px 14px;
        border-radius: 8px;
        background-color: #052e16;
        color: #86efac;
        font-weight: 700;
        text-align: center;
    }

    /* ---------- SMALL TEXT ---------- */

    .muted {
        color: #64748b;
        font-size: 14px;
    }

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CONFIG
# ============================================================

LOG_FILE = "logs/runs.jsonl"


# ============================================================
# LOAD RUNS
# ============================================================

@st.cache_data(ttl=3)
def load_runs():

    if not os.path.exists(LOG_FILE):
        return []

    runs = []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                runs.append(json.loads(line))

            except json.JSONDecodeError:
                continue

    return runs


# ============================================================
# EXTRACT METRICS
# ============================================================

def extract_metrics(runs):

    rows = []

    for run in runs:

        intent = "unknown"
        grounding_score = None
        grounding_status = "UNKNOWN"
        response_length = None

        for event in run.get("events", []):

            event_name = event.get("event")

            if event_name == "router":

                intent = event.get(
                    "intent",
                    "unknown"
                )

            elif event_name == "llm":

                response_length = event.get(
                    "response_length"
                )

            elif event_name == "answer_evaluation":

                grounding_score = event.get(
                    "grounding_score"
                )

                grounding_status = event.get(
                    "status",
                    "UNKNOWN"
                )

        rows.append(
            {
                "Run ID": run.get(
                    "run_id",
                    "N/A"
                ),
                "Timestamp": run.get(
                    "timestamp",
                    ""
                ),
                "Query": run.get(
                    "query",
                    ""
                ),
                "Intent": intent,
                "Latency": run.get(
                    "total_latency_seconds",
                    0
                ),
                "Grounding": grounding_score,
                "Status": grounding_status,
                "Response Length": response_length,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# LOAD DATA
# ============================================================

runs = load_runs()

if not runs:

    st.error(
        "No LLMOps runs found in logs/runs.jsonl."
    )

    st.stop()


df = extract_metrics(runs)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🤖 LLMOps"
    )

    st.caption(
        "RAG E-Commerce Control Center"
    )

    st.divider()

    st.markdown(
        "### System Status"
    )

    st.markdown(
        '<div class="status-active">● SYSTEM ACTIVE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "### Pipeline"
    )

    st.markdown(
        """
        🔀 Agent Router

        🔎 Entity Extraction

        📚 Retrieval

        ⚡ Reranking

        🧩 RAG Context

        🧠 LLM Generation

        🎯 Answer Evaluation

        📡 Persistent Tracing
        """
    )

    st.divider()

    st.markdown(
        "### Data Source"
    )

    st.code(
        "logs/runs.jsonl"
    )

    if st.button(
        "🔄 Refresh Dashboard"
    ):

        st.cache_data.clear()
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 RAG LLMOps Control Center"
)

st.markdown(
    "Advanced RAG E-Commerce Assistant — "
    "Observability, Quality & Runtime Monitoring"
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_runs = len(df)

average_latency = (
    df["Latency"].mean()
    if not df.empty
    else 0
)

minimum_latency = (
    df["Latency"].min()
    if not df.empty
    else 0
)

maximum_latency = (
    df["Latency"].max()
    if not df.empty
    else 0
)


grounding_df = df[
    df["Grounding"].notna()
]


if not grounding_df.empty:

    average_grounding = (
        grounding_df["Grounding"].mean()
    )

    grounded_runs = (
        grounding_df[
            grounding_df["Status"]
            == "GROUNDED"
        ].shape[0]
    )

    partial_runs = (
        grounding_df[
            grounding_df["Status"]
            == "PARTIALLY GROUNDED"
        ].shape[0]
    )

    not_grounded_runs = (
        grounding_df[
            grounding_df["Status"]
            == "NOT GROUNDED"
        ].shape[0]
    )

    grounded_rate = (
        grounded_runs
        / len(grounding_df)
        * 100
    )

else:

    average_grounding = 0
    grounded_runs = 0
    partial_runs = 0
    not_grounded_runs = 0
    grounded_rate = 0


# ============================================================
# SYSTEM OVERVIEW
# ============================================================

st.subheader(
    "📊 System Overview"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        label="Total Runs",
        value=total_runs,
        help="Total recorded pipeline executions."
    )


with c2:

    st.metric(
        label="Average Latency",
        value=f"{average_latency:.4f}s",
        help="Average end-to-end execution latency."
    )


with c3:

    st.metric(
        label="Grounding Score",
        value=f"{average_grounding:.2f}",
        help="Average answer grounding score."
    )


with c4:

    st.metric(
        label="Grounded Rate",
        value=f"{grounded_rate:.1f}%",
        help="Percentage of evaluated responses classified as grounded."
    )


# ============================================================
# PERFORMANCE
# ============================================================

st.subheader(
    "⚡ Runtime Performance"
)

p1, p2, p3 = st.columns(3)


with p1:

    st.metric(
        "Minimum Latency",
        f"{minimum_latency:.4f}s"
    )


with p2:

    st.metric(
        "Average Latency",
        f"{average_latency:.4f}s"
    )


with p3:

    st.metric(
        "Maximum Latency",
        f"{maximum_latency:.4f}s"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Performance",
        "🎯 Answer Quality",
        "🧠 Intent Analytics",
        "📋 Run Explorer",
    ]
)


# ============================================================
# TAB 1 — PERFORMANCE
# ============================================================

with tab1:

    st.subheader(
        "Latency Monitoring"
    )

    latency_data = df[
        ["Latency"]
    ].copy()

    latency_data.index = range(
        1,
        len(latency_data) + 1
    )

    st.line_chart(
        latency_data,
        width="stretch",
        height=350
    )

    st.caption(
        "End-to-end latency recorded for each pipeline execution."
    )

    st.subheader(
        "Response Size"
    )

    response_df = df[
        ["Response Length"]
    ].dropna()

    if not response_df.empty:

        response_df.index = range(
            1,
            len(response_df) + 1
        )

        st.area_chart(
            response_df,
            width="stretch",
            height=300
        )


# ============================================================
# TAB 2 — ANSWER QUALITY
# ============================================================

with tab2:

    st.subheader(
        "🎯 Grounding Quality"
    )

    if not grounding_df.empty:

        grounding_chart = grounding_df[
            ["Grounding"]
        ].copy()

        grounding_chart.index = range(
            1,
            len(grounding_chart) + 1
        )

        st.line_chart(
            grounding_chart,
            width="stretch",
            height=350
        )

    else:

        st.info(
            "No grounding evaluation data available."
        )

    st.subheader(
        "Grounding Status"
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        st.metric(
            "✅ Grounded",
            grounded_runs
        )

    with q2:

        st.metric(
            "⚠️ Partially Grounded",
            partial_runs
        )

    with q3:

        st.metric(
            "❌ Not Grounded",
            not_grounded_runs
        )

    status_counts = (
        grounding_df["Status"]
        .value_counts()
    )

    if not status_counts.empty:

        st.bar_chart(
            status_counts,
            width="stretch",
            height=300
        )


# ============================================================
# TAB 3 — INTENT ANALYTICS
# ============================================================

with tab3:

    st.subheader(
        "🔀 Query Intent Distribution"
    )

    intent_counts = (
        df["Intent"]
        .value_counts()
    )

    st.bar_chart(
        intent_counts,
        width="stretch",
        height=350
    )

    st.subheader(
        "Intent Summary"
    )

    intent_table = (
        df["Intent"]
        .value_counts()
        .rename_axis("Intent")
        .reset_index(
            name="Requests"
        )
    )

    st.dataframe(
        intent_table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# TAB 4 — RUN EXPLORER
# ============================================================

with tab4:

    st.subheader(
        "📋 Run Explorer"
    )

    # Filters

    f1, f2 = st.columns(2)

    with f1:

        intent_options = [
            "All"
        ] + sorted(
            df["Intent"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_intent = st.selectbox(
            "Filter by Intent",
            intent_options
        )

    with f2:

        status_options = [
            "All"
        ] + sorted(
            df["Status"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_status = st.selectbox(
            "Filter by Status",
            status_options
        )


    filtered = df.copy()


    if selected_intent != "All":

        filtered = filtered[
            filtered["Intent"]
            == selected_intent
        ]


    if selected_status != "All":

        filtered = filtered[
            filtered["Status"]
            == selected_status
        ]


    display_df = filtered.copy()


    display_df["Timestamp"] = pd.to_datetime(
        display_df["Timestamp"],
        errors="coerce"
    )


    display_df["Timestamp"] = (
        display_df["Timestamp"]
        .dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    display_df = display_df[
        [
            "Timestamp",
            "Intent",
            "Latency",
            "Grounding",
            "Status",
            "Query",
        ]
    ]


    display_df = display_df.rename(
        columns={
            "Latency": "Latency (s)",
            "Grounding": "Grounding Score",
        }
    )


    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Latency (s)": st.column_config.NumberColumn(
                format="%.4f"
            ),
            "Grounding Score": st.column_config.NumberColumn(
                format="%.2f"
            ),
        },
    )


    st.caption(
        f"Showing {len(filtered)} of {len(df)} recorded runs."
    )


# ============================================================
# PIPELINE ARCHITECTURE
# ============================================================

st.divider()

st.subheader(
    "🔗 Observed Pipeline"
)

pipeline = (
    "User Query  →  Agent Router  →  Entity Extraction  →  "
    "Retrieval  →  Reranking  →  RAG Context  →  "
    "LLM  →  Answer Evaluation  →  Trace  →  Metrics"
)

st.info(
    pipeline
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RAG LLMOps Control Center • "
    "Advanced RAG E-Commerce Assistant • "
    "Local Observability"
)