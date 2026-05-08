import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Haryana Tender Intelligence",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS (Mobile + CEO UI)
# ---------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

div[data-testid="metric-container"] {
    border: 1px solid #333;
    padding: 10px;
    border-radius: 12px;
    background-color: #111111;
}

.stDataFrame {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🚜 Haryana Tender Intelligence System")
st.caption("AI Powered Government Tender Tracking Dashboard")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data(ttl=300)
def load_data():

    if not os.path.exists("haryana_tenders_master.csv"):
        return pd.DataFrame()

    try:
        df = pd.read_csv("haryana_tenders_master.csv")

        # ---------------------------------------------------
        # REQUIRED COLUMNS
        # ---------------------------------------------------
        required_cols = {
            "Tender_ID": "N/A",
            "Department": "N/A",
            "District": "N/A",
            "Value": 0,
            "Work_Type": "N/A",
            "Status": "LIVE",
            "Priority_Score": "LOW",
            "Last_Date": "N/A"
        }

        for col, default_val in required_cols.items():
            if col not in df.columns:
                df[col] = default_val

        # ---------------------------------------------------
        # CLEANING
        # ---------------------------------------------------
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)

        df["Department"] = df["Department"].astype(str)
        df["District"] = df["District"].astype(str)
        df["Status"] = df["Status"].astype(str)
        df["Priority_Score"] = df["Priority_Score"].astype(str)

        return df

    except Exception as e:
        st.error(f"CSV Error: {e}")
        return pd.DataFrame()

# ---------------------------------------------------
# LOAD CSV
# ---------------------------------------------------
df = load_data()

# ---------------------------------------------------
# EMPTY DATA CONDITION
# ---------------------------------------------------
if df.empty:
    st.warning("⚠️ अभी डेटा उपलब्ध नहीं है। पहले scraper.py चलाएँ।")
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🎯 Smart Filters")

# District Filter
districts = st.sidebar.multiselect(
    "District चुनें",
    sorted(df["District"].dropna().unique())
)

# Department Filter
departments = st.sidebar.multiselect(
    "Department चुनें",
    sorted(df["Department"].dropna().unique())
)

# Status Filter
status_filter = st.sidebar.multiselect(
    "Status चुनें",
    sorted(df["Status"].dropna().unique()),
    default=sorted(df["Status"].dropna().unique())
)

# Budget Filter
max_budget = int(df["Value"].max()) if len(df) > 0 else 1000000

budget_range = st.sidebar.slider(
    "Budget Range (₹)",
    min_value=0,
    max_value=max_budget,
    value=(0, max_budget),
    step=50000
)

# Search
search_query = st.sidebar.text_input(
    "🔍 Search",
    placeholder="Bolero, JCB, Cleaning..."
)

# ---------------------------------------------------
# FILTER LOGIC
# ---------------------------------------------------
filtered_df = df.copy()

if districts:
    filtered_df = filtered_df[
        filtered_df["District"].isin(districts)
    ]

if departments:
    filtered_df = filtered_df[
        filtered_df["Department"].isin(departments)
    ]

if status_filter:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(status_filter)
    ]

filtered_df = filtered_df[
    (filtered_df["Value"] >= budget_range[0]) &
    (filtered_df["Value"] <= budget_range[1])
]

# Search Logic
if search_query:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: search_query.lower() in str(row).lower(),
            axis=1
        )
    ]

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
st.markdown("## 📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📋 Total Tenders",
    len(df)
)

col2.metric(
    "🎯 Matching",
    len(filtered_df)
)

high_priority = len(
    filtered_df[
        filtered_df["Priority_Score"] == "HIGH"
    ]
)

col3.metric(
    "🔥 High Priority",
    high_priority
)

highest_value = int(filtered_df["Value"].max()) if not filtered_df.empty else 0

col4.metric(
    "💰 Highest Value",
    f"₹{highest_value:,}"
)

# ---------------------------------------------------
# MAIN TABLE
# ---------------------------------------------------
st.markdown("---")
st.subheader("📑 Tender Master Table")

display_cols = [
    "Tender_ID",
    "Department",
    "District",
    "Work_Type",
    "Value",
    "Status",
    "Priority_Score",
    "Last_Date"
]

st.dataframe(
    filtered_df[display_cols],
    use_container_width=True,
    height=500
)

# ---------------------------------------------------
# HIGH PRIORITY SECTION
# ---------------------------------------------------
st.markdown("---")
st.subheader("🔥 High Priority Opportunities")

high_prio = filtered_df[
    filtered_df["Priority_Score"] == "HIGH"
]

if not high_prio.empty:

    st.table(
        high_prio[
            [
                "Tender_ID",
                "Department",
                "District",
                "Work_Type",
                "Value"
            ]
        ]
    )

else:
    st.info("कोई High Priority Tender नहीं मिला।")

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------
st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_tenders.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("🚀 Haryana Tender AI Dashboard • CEO Level Intelligence System") 
