import streamlit as st
import pandas as pd
import os

# PAGE CONFIG
st.set_page_config(
    page_title="Haryana Tender Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TITLE
st.title("🚜 Haryana Tender Intelligence System")
st.caption("CEO Level Government Tender Dashboard")

# LOAD DATA
@st.cache_data
def load_data():

    if not os.path.exists("haryana_tenders_master.csv"):
        return pd.DataFrame()

    try:
        df = pd.read_csv("haryana_tenders_master.csv")

        required_cols = {
            "Tender_ID": "N/A",
            "Department": "N/A",
            "District": "N/A",
            "Category": "General",
            "Work_Type": "N/A",
            "Value": 0,
            "Status": "LIVE",
            "Priority_Score": "LOW",
            "Last_Date": "N/A",
            "Source": "Haryana Portal"
        }

        for col, default_value in required_cols.items():

            if col not in df.columns:
                df[col] = default_value

        df["Value"] = pd.to_numeric(
            df["Value"],
            errors="coerce"
        ).fillna(0)

        return df

    except Exception as e:
        st.error(f"CSV Error: {e}")
        return pd.DataFrame()

df = load_data()

# NO DATA
if df.empty:

    st.warning("⚠️ Tender data not found.")
    st.stop()

# SIDEBAR
st.sidebar.title("🎯 Smart Tender Filters")

districts = st.sidebar.multiselect(
    "District Select",
    sorted(df["District"].dropna().unique())
)

departments = st.sidebar.multiselect(
    "Department Select",
    sorted(df["Department"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Tender Category",
    sorted(df["Category"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Tender Status",
    sorted(df["Status"].dropna().unique()),
    default=sorted(df["Status"].dropna().unique())
)

budget_range = st.sidebar.slider(
    "Budget Range (₹)",
    min_value=0,
    max_value=100000000,
    value=(0, 100000000),
    step=1000
)

search_query = st.sidebar.text_input(
    "🔍 Search",
    placeholder="Bolero, Scorpio, JCB..."
)

# FILTER LOGIC
filtered_df = df.copy()

if districts:
    filtered_df = filtered_df[
        filtered_df["District"].isin(districts)
    ]

if departments:
    filtered_df = filtered_df[
        filtered_df["Department"].isin(departments)
    ]

if categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(categories)
    ]

if status_filter:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(status_filter)
    ]

filtered_df = filtered_df[
    (filtered_df["Value"] >= budget_range[0]) &
    (filtered_df["Value"] <= budget_range[1])
]

if search_query:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row:
            search_query.lower() in str(row).lower(),
            axis=1
        )
    ]

# METRICS
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📋 Total Tenders",
    len(df)
)

col2.metric(
    "🎯 Matching Tenders",
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

highest_value = int(filtered_df["Value"].max()) \
    if not filtered_df.empty else 0

col4.metric(
    "💰 Highest Value",
    f"₹{highest_value:,}"
)

# MAIN TABLE
st.subheader("📊 Haryana Tender Master Table")

display_cols = [
    "Tender_ID",
    "Department",
    "District",
    "Category",
    "Work_Type",
    "Value",
    "Status",
    "Priority_Score",
    "Last_Date",
    "Source"
]

st.dataframe(
    filtered_df[display_cols],
    use_container_width=True
)

# VEHICLE SECTION
st.markdown("---")
st.subheader("🚘 Vehicle Hiring Tenders")

vehicle_df = filtered_df[
    filtered_df["Category"].str.contains(
        "Vehicle",
        case=False,
        na=False
    )
]

st.dataframe(
    vehicle_df,
    use_container_width=True
)

# MANPOWER SECTION
st.markdown("---")
st.subheader("👷 Manpower Tenders")

manpower_df = filtered_df[
    filtered_df["Category"].str.contains(
        "Manpower",
        case=False,
        na=False
    )
]

st.dataframe(
    manpower_df,
    use_container_width=True
)

# HIGH PRIORITY
st.markdown("---")
st.subheader("🔥 AI High Priority Tenders")

high_df = filtered_df[
    filtered_df["Priority_Score"] == "HIGH"
]

st.dataframe(
    high_df,
    use_container_width=True
)

# DOWNLOAD
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "filtered_tenders.csv",
    "text/csv"
)

# FOOTER
st.markdown("---")

st.caption(
    "Haryana Tender Intelligence • Enterprise Dashboard"
)

