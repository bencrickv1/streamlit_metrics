import streamlit as st
import geopandas as gpd


@st.cache_data
def gpd_load_cached(input_file):
    gdf = gpd.read_file(input_file)
    gdf.to_crs("EPSG:4326", inplace=True)
    return gdf
