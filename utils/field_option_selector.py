
import streamlit as st
import pandas as pd

def field_option_multiselect(df: pd.DataFrame, field_name: str, label: str) -> list[str]:

    options = st.sidebar.multiselect(
        label=label,
        options=sorted(list(set(df[field_name])))
    )

    return options

def field_option_checkboxes(df: pd.DataFrame, field_name: str, preselected) -> list[str]:

    options_active = {
        value: st.sidebar.checkbox(
            label=value,
            value=True if value in preselected else False
        )
    for value in sorted(list(set(df[field_name])))}

    use_options = [type for type in options_active if options_active[type]]

    return use_options