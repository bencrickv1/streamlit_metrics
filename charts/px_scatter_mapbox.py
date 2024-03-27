import plotly.express as px
from .field_labels import field_labels


def px_scatter_mapbox(
    display_gdf,
    colour_field,
    colours,
    title,
    size=None,
    showlegend=True,
    legend_title=None,
    y_mod=0,
):

    hover_name = "application_type"
    hover_data = {
        "application_category": False,
        "application_type": False,
        "fee": True,
        "latitude": False,
        "longitude": False,
        "submission_date": True,
        "readable_fee": False,
    }

    fig_map = px.scatter_mapbox(
        data_frame=display_gdf,
        lat="latitude",
        lon="longitude",
        hover_name=hover_name,
        color=colour_field,
        color_discrete_sequence=colours,
        size=size,
        mapbox_style="carto-darkmatter",
        opacity=0.5,
        title=title,
        labels=field_labels,
        hover_data=hover_data,
        height=800,
        width=800,
        center={"lat": 55.36274150310406, "lon": -3.440547563580056},
        zoom=4.5,
    )

    fig_map.update_layout(
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.125 + y_mod, xanchor="center", x=0.5
        ),
        showlegend=showlegend,
    )

    if legend_title:
        fig_map.update_layout(legend_title_text=legend_title)

    return fig_map
