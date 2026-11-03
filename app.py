import sys
from pathlib import Path

import pandas as pd
import streamlit as st

base_dir = Path(__file__).resolve().parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from analysis import (
    movie_tv_count,
    rating_distribution,
    release_year,
    top_countries,
    top_genres,
    yearly_added,
)
from charts import bar_chart, line_chart, pie_chart
from preprocessing import clean_data

st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")


@st.cache_data
def load_dataset():
    csv_path = base_dir / "cleaned_data.csv"
    if not csv_path.exists():
        csv_path = base_dir / "netflix_titles.csv"

    if not csv_path.exists():
        raise FileNotFoundError("No dataset file found in the project folder.")

    df = pd.read_csv(csv_path)
    if "date_added" in df.columns:
        df = clean_data(df)

    if "type" not in df.columns:
        df["type"] = "Unknown"

    if "duration" not in df.columns and "duration_value" in df.columns:
        df["duration"] = pd.to_numeric(df["duration_value"], errors="coerce")

    df["country"] = df["country"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Unknown")
    return df


def filter_dataframe(df):
    if df.empty:
        return df

    type_options = sorted(df["type"].dropna().unique().tolist())
    selected_types = st.sidebar.multiselect("Content type", type_options, default=type_options)

    country_options = sorted(
        df["country"].fillna("Unknown").str.split(",").explode().str.strip().dropna().unique().tolist()
    )
    selected_countries = st.sidebar.multiselect("Country", country_options, default=[])

    rating_options = sorted(df["rating"].dropna().unique().tolist())
    selected_ratings = st.sidebar.multiselect("Rating", rating_options, default=[])

    mask = df["type"].isin(selected_types)

    if selected_countries:
        country_mask = df["country"].fillna("Unknown").str.split(",").apply(
            lambda values: any(value.strip() in selected_countries for value in values)
        )
        mask &= country_mask

    if selected_ratings:
        mask &= df["rating"].isin(selected_ratings)

    return df[mask].copy()


df = load_dataset()
filtered_df = filter_dataframe(df)

st.title("Netflix EDA Dashboard")
st.caption("Interactive insights into the Netflix catalog")

if filtered_df.empty:
    st.warning("No data matches the current filters. Please adjust the sidebar selections.")
    st.stop()

avg_duration = filtered_df["duration"].dropna().mean() if "duration" in filtered_df.columns else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total titles", len(filtered_df))
col2.metric("Movies", int((filtered_df["type"] == "Movie").sum()))
col3.metric("TV shows", int((filtered_df["type"] == "TV Show").sum()))
col4.metric("Avg. duration (min)", f"{avg_duration:,.0f}" if pd.notna(avg_duration) else "N/A")

st.subheader("Content mix")
count = movie_tv_count(filtered_df)
fig = bar_chart(count, "Number of Movies and TV Shows", "Type", "Count")
st.pyplot(fig)

st.subheader("Catalog overview")
col_left, col_right = st.columns(2)
with col_left:
    top_countries_series = top_countries(filtered_df)
    if not top_countries_series.empty:
        country_fig = bar_chart(top_countries_series.head(10), "Top Countries", "Country", "Count")
        st.pyplot(country_fig)
with col_right:
    rating_series = rating_distribution(filtered_df)
    if not rating_series.empty:
        rating_fig = pie_chart(rating_series.head(10), "Rating Distribution")
        st.pyplot(rating_fig)

st.subheader("Release trends")
col_a, col_b = st.columns(2)
with col_a:
    year_series = release_year(filtered_df)
    if not year_series.empty:
        year_fig = line_chart(year_series.sort_index(), "Release Year Trend", "Release Year", "Titles")
        st.pyplot(year_fig)
with col_b:
    genre_series = top_genres(filtered_df)
    if not genre_series.empty:
        genre_fig = bar_chart(genre_series.head(10), "Top Genres", "Genre", "Count")
        st.pyplot(genre_fig)

st.subheader("Recent additions")
if "date_added" in filtered_df.columns:
    added_series = yearly_added(filtered_df)
    if not added_series.empty:
        added_fig = line_chart(added_series, "Titles Added by Year", "Year", "Titles")
        st.pyplot(added_fig)

st.subheader("Data table")
st.dataframe(filtered_df.head(50), use_container_width=True)

