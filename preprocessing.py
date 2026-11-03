import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(df):
    df = df.copy()
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    for column in ['country', 'director', 'cast', 'rating']:
        if column in df.columns and df[column].notna().any():
            mode_value = df[column].mode(dropna=True)
            if not mode_value.empty:
                df[column] = df[column].fillna(mode_value.iloc[0])

    if 'duration' in df.columns:
        df['duration'] = df['duration'].astype(str).str.extract(r'(\d+)').astype(float)

    duration_label_col = 'duration_type' if 'duration_type' in df.columns else 'duration_unit'
    if duration_label_col in df.columns:
        df['duration_unit'] = df[duration_label_col].astype(str).str.extract('([a-zA-Z]+)').fillna('min')

    if 'duration_value' in df.columns:
        df['duration_value'] = pd.to_numeric(df['duration_value'], errors='coerce')

    if 'date_added' in df.columns:
        df['year_added'] = df['date_added'].dt.year
        df['month_added'] = df['date_added'].dt.month
        df['day_added'] = df['date_added'].dt.day

    return df