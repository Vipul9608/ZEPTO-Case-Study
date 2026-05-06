import os
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Bulletproof path: always relative to this file, works on Streamlit Cloud ──
BASE_DIR  = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Zepto_Dataset.xlsx"

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zepto Customer Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h2 { font-size: 2.2rem; margin: 0; }
    .metric-card p  { font-size: 0.95rem; margin: 5px 0 0; opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path, parse_dates=["created_date"])
    df["year"]       = df["created_date"].dt.year
    df["month"]      = df["created_date"].dt.month
    df["month_name"] = df["created_date"].dt.strftime("%b %Y")
    df["age_group"]  = pd.cut(
        df["age"],
        bins=[17, 25, 35, 45, 55, 61],
        labels=["18–25", "26–35", "36–45", "46–55", "56–60"],
    )
    return df

df = load_data(str(DATA_FILE))

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Zepto_logo.svg/1200px-Zepto_logo.svg.png",
        width=140,
    )
    st.title("Filters")

    year_opts      = sorted(df["year"].unique())
    selected_years = st.multiselect("Year", year_opts, default=year_opts)

    gender_opts      = df["gender"].unique().tolist()
    selected_genders = st.multiselect("Gender", gender_opts, default=gender_opts)

    state_opts      = sorted(df["state"].unique())
    selected_states = st.multiselect("State", state_opts, default=state_opts)

    age_range = st.slider(
        "Age Range",
        int(df["age"].min()), int(df["age"].max()), (18, 60)
    )

    st.markdown("---")
    st.caption("Data: Zepto Customer Dataset · 10,000 records")

# ── Apply Filters ─────────────────────────────────────────────────────────────
mask = (
    df["year"].isin(selected_years) &
    df["gender"].isin(selected_genders) &
    df["state"].isin(selected_states) &
    df["age"].between(age_range[0], age_range[1])
)
fdf = df[mask]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🛒 Zepto Customer Analytics Dashboard")
st.markdown(f"Showing **{len(fdf):,}** of **{len(df):,}** customers based on current filters.")
st.divider()

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class="metric-card">
        <h2>{len(fdf):,}</h2><p>Total Customers</p></div>""", unsafe_allow_html=True)
with k2:
    avg_age = round(fdf["age"].mean(), 1) if len(fdf) else 0
    st.markdown(f"""<div class="metric-card">
        <h2>{avg_age}</h2><p>Average Age</p></div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="metric-card">
        <h2>{fdf["state"].nunique()}</h2><p>States Covered</p></div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="metric-card">
        <h2>{fdf["city"].nunique()}</h2><p>Cities Covered</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Gender Pie + Age Group Bar ────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("👥 Gender Distribution")
    gender_counts = fdf["gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig = px.pie(
        gender_counts, names="Gender", values="Count",
        color_discrete_sequence=["#667eea", "#f093fb", "#4facfe"],
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(t=20, b=20), height=340)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🎂 Age Group Distribution")
    age_counts = fdf["age_group"].value_counts().sort_index().reset_index()
    age_counts.columns = ["Age Group", "Count"]
    fig = px.bar(
        age_counts, x="Age Group", y="Count",
        color="Count", color_continuous_scale="Purples", text="Count",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False, height=340)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Monthly Signups + Top States ──────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("📈 Monthly Customer Signups")
    monthly = (
        fdf.groupby(fdf["created_date"].dt.to_period("M"))
        .size()
        .reset_index(name="Signups")
    )
    monthly["created_date"] = monthly["created_date"].dt.to_timestamp()
    fig = px.line(
        monthly, x="created_date", y="Signups",
        markers=True,
        color_discrete_sequence=["#667eea"],
        labels={"created_date": "Month"},
    )
    fig.update_layout(margin=dict(t=20, b=20), height=340)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("🗺️ Top 10 States by Customers")
    top_states = fdf["state"].value_counts().head(10).reset_index()
    top_states.columns = ["State", "Customers"]
    fig = px.bar(
        top_states.sort_values("Customers"),
        x="Customers", y="State", orientation="h",
        color="Customers", color_continuous_scale="Purp", text="Customers",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False, height=340)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: City Treemap + Violin ─────────────────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    st.subheader("🏙️ City-wise Customer Share")
    city_counts = fdf["city"].value_counts().head(20).reset_index()
    city_counts.columns = ["City", "Count"]
    fig = px.treemap(
        city_counts, path=["City"], values="Count",
        color="Count", color_continuous_scale="Purples",
    )
    fig.update_layout(margin=dict(t=20, b=20), height=380)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    st.subheader("🎻 Age Distribution by Gender")
    fig = px.violin(
        fdf, y="age", x="gender", color="gender",
        box=True, points="outliers",
        color_discrete_sequence=["#667eea", "#f093fb", "#4facfe"],
        labels={"age": "Age", "gender": "Gender"},
    )
    fig.update_layout(margin=dict(t=20, b=20), showlegend=False, height=380)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: State × Gender Heatmap ────────────────────────────────────────────
st.subheader("🔥 State × Gender Heatmap")
pivot = fdf.groupby(["state", "gender"]).size().unstack(fill_value=0)
fig = px.imshow(
    pivot, text_auto=True,
    color_continuous_scale="Purples",
    aspect="auto",
    labels={"color": "Customers"},
)
fig.update_layout(margin=dict(t=20, b=20), height=420)
st.plotly_chart(fig, use_container_width=True)

# ── Raw Data Table ────────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data"):
    st.dataframe(
        fdf.drop(columns=["year", "month", "month_name"]).reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered CSV", csv, "zepto_filtered.csv", "text/csv")
