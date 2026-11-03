import pandas as pd


def movie_tv_count(df):
    return df['type'].value_counts()


def top_countries(df):
    return df['country'].str.split(',').explode().value_counts().head(10)


def rating_distribution(df):
    return df['rating'].value_counts()


def top_genres(df):
    return df['listed_in'].str.split(',').explode().value_counts().head(10)


def release_year(df):
    return df['release_year'].value_counts().sort_index()


def yearly_added(df):
    return df.groupby('date_added')['title'].count().sort_index()


def monthly_added(df):
    return df.groupby(df['date_added'].dt.to_period('M'))['title'].count().sort_index()
