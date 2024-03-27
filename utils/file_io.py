import streamlit as st


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")
