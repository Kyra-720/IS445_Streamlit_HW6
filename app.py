
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Illinois Building Inventory", layout="wide")

st.title("Illinois Building Inventory Dashboard")

st.write(
    "This dashboard explores building construction years "
    "and building sizes in Illinois."
)

# Load dataset
url = (
    "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(url, low_memory=False)

df = load_data()

df["Year Constructed"] = pd.to_numeric(
    df["Year Constructed"], errors="coerce"
)
df["Square Footage"] = pd.to_numeric(
    df["Square Footage"], errors="coerce"
)

# Visualization 1
st.header("Visualization 1: Buildings by Construction Year")

year_range = st.slider(
    "Select construction year range",
    1850, 2026, (1950, 2020)
)

df_year = df[
    df["Year Constructed"].between(
        year_range[0], year_range[1]
    )
].copy()

df_year["Decade"] = (
    df_year["Year Constructed"] // 10 * 10
).astype(int)

counts = (
    df_year.groupby("Decade")
    .size()
    .reset_index(name="Number of Buildings")
)

chart1 = (
    alt.Chart(counts)
    .mark_bar(color="steelblue")
    .encode(
        x=alt.X("Decade:O", title="Construction Decade"),
        y=alt.Y("Number of Buildings:Q"),
        tooltip=["Decade", "Number of Buildings"]
    )
    .properties(height=400)
)

st.altair_chart(chart1, use_container_width=True)

st.write(
    "This chart shows how the number of buildings varies "
    "by construction decade. I used bars because they make "
    "it easy to compare counts across decades. The blue "
    "color keeps the design simple, and the slider allows "
    "users to explore different construction periods. "
    "With more time, I would add filters for building location."
)

# Visualization 2
st.header("Visualization 2: Building Size by Usage")

df_size = df[
    (df["Square Footage"] > 0) &
    (df["Square Footage"] < 1000000) &
    df["Usage Description"].notna()
].copy()

usage_counts = df_size["Usage Description"].value_counts()
usage_options = usage_counts.head(10).index.tolist()

selected_usage = st.selectbox(
    "Select building usage",
    usage_options
)

filtered = df_size[
    df_size["Usage Description"] == selected_usage
]

chart2 = (
    alt.Chart(filtered)
    .mark_bar(color="orange")
    .encode(
        x=alt.X(
            "Square Footage:Q",
            bin=alt.Bin(maxbins=30),
            title="Square Footage"
        ),
        y=alt.Y(
            "count():Q",
            title="Number of Buildings (Log Scale)",
            scale=alt.Scale(type="log")
        ),
        tooltip=[alt.Tooltip("count():Q", title="Count")]
    )
    .properties(height=400)
)

st.altair_chart(chart2, use_container_width=True)


st.write(
    "This histogram shows the distribution of building sizes for "
    "different usage categories. I used bars and bins to show how "
    "many buildings fall into each size range. The orange color "
    "helps distinguish this chart from the first visualization. "
    "I also used a logarithmic scale on the y-axis because most "
    "buildings are relatively small, while a few are much larger. "
    "The dropdown allows users to explore different building "
    "usage categories. If I had more time, I would add more "
    "filters and summary statistics to help users compare "
    "building sizes."
)


st.header("Changes from Homework 5")

st.write(
    "I reused the Building Inventory dataset from Homework 5, "
    "but created two different visualizations for this assignment. "
    "Instead of the building status chart and the scatter plot "
    "from Homework 5, I created a construction-decade bar chart "
    "and a building-size histogram. I also added Streamlit "
    "widgets to allow users to filter the data."
)
