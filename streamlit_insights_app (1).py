
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Insights Dashboard", layout="wide")

# Title
st.title("Streamlit Insights Application")
st.write("Upload a CSV file to explore data and gain insights.")

# Upload
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Cleaning
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # Basic EDA
    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Column selection for visualizations
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # Insight 1: Histogram of a selected numeric column
    if numeric_cols:
        st.subheader("Distribution of a Numeric Column")
        col = st.selectbox("Choose a column", numeric_cols, key="hist_col")
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        st.pyplot(fig)

    # Insight 2: Correlation Heatmap
    if len(numeric_cols) > 1:
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # Insight 3: Bar plot of a categorical column
    if categorical_cols:
        st.subheader("Value Counts of a Categorical Column")
        col = st.selectbox("Choose a column", categorical_cols, key="bar_col")
        fig, ax = plt.subplots()
        df[col].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    # Insight 4: Time series line chart (if a date column exists)
    date_cols = df.select_dtypes(include='datetime').columns.tolist()
    if not date_cols:
        for col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col])
                date_cols.append(col)
            except Exception:
                continue

    if date_cols and numeric_cols:
        st.subheader("Time Series Analysis")
        date_col = st.selectbox("Date Column", date_cols)
        val_col = st.selectbox("Value Column", numeric_cols, key="line_col")
        df_sorted = df[[date_col, val_col]].dropna().sort_values(date_col)
        st.line_chart(df_sorted.set_index(date_col))

else:
    st.info("Awaiting CSV file upload.")

# Footer
st.markdown("---")
st.caption("Developed as part of Backend/Data Engineering assignment.")
