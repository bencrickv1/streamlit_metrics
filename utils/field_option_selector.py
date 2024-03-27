import streamlit as st
import pandas as pd


def field_option_multiselect(
    df: pd.DataFrame,
    field_name: str,
    label: str,
    pre_toggle,
    preselected,
    key,
    toggle_key,
) -> list[str]:

    st.sidebar.markdown(f"<small>{label}</small>", unsafe_allow_html=True)

    with open("./utils/multiselect.css") as fi:
        css = fi.read()

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    all_options = sorted(list(set(df[field_name])))

    def toggle_all():
        toggle_state = st.session_state[toggle_key]
        if toggle_state:
            st.session_state[key] = all_options
        else:
            st.session_state[key] = []
        st.session_state[toggle_key] = toggle_state

    toggle = st.sidebar.toggle(
        label="Select / deselect all",
        value=pre_toggle,
        on_change=toggle_all,
        key=toggle_key,
    )

    options = st.sidebar.multiselect(
        label=label,
        options=all_options,
        default=preselected,
        label_visibility="collapsed",
        key=key,
    )

    return toggle, options


def field_option_checkboxes(
    df: pd.DataFrame, field_name: str, preselected
) -> list[str]:

    st.sidebar.markdown("<small>Application Category</small>", unsafe_allow_html=True)

    options_active = {
        value: st.sidebar.checkbox(
            label=value, value=True if value in preselected else False
        )
        for value in sorted(list(set(df[field_name])))
    }

    use_options = [type for type in options_active if options_active[type]]

    return use_options
