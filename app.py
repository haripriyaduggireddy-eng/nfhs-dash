import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

# Title
st.title("📊 National Family Health Survey (NFHS) Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("/mnt/data/All India National Family Health Survey1.xlsx")
    return df

df = load_data()

# Show raw data
st.subheader("📄 Raw Data Preview")
st.dataframe(df.head())

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Select column for analysis
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
selected_col = st.sidebar.selectbox("Select a numeric indicator", numeric_cols)

# Optional state filter (if present)
if "State" in df.columns:
    states = df["State"].unique()
    selected_state = st.sidebar.multiselect("Select State(s)", states, default=states)

    filtered_df = df[df["State"].isin(selected_state)]
else:
    filtered_df = df

# KPI section
st.subheader("📌 Key Statistics")
col1, col2, col3 = st.columns(3)

col1.metric("Mean", round(filtered_df[selected_col].mean(), 2))
col2.metric("Maximum", round(filtered_df[selected_col].max(), 2))
col3.metric("Minimum", round(filtered_df[selected_col].min(), 2))

# Chart section
st.subheader(f"📈 Distribution of {selected_col}")

fig, ax = plt.subplots()
sns.histplot(filtered_df[selected_col].dropna(), kde=True, ax=ax)
st.pyplot(fig)

# Bar chart (State-wise if available)
if "State" in df.columns:
    st.subheader(f"🏙️ State-wise {selected_col}")

    state_avg = filtered_df.groupby("State")[selected_col].mean().sort_values(ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    state_avg.plot(kind="bar", ax=ax2)
    ax2.set_ylabel(selected_col)
    st.pyplot(fig2)
