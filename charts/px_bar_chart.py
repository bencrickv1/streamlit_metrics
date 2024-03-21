
import plotly.express as px
from .field_labels import field_labels

def px_bar_chart(display_df, colour_field, colours, x_field, y_field, text_field, title, showlegend=True, legend_title=None):

    base_height = 800
    base_width = 800

    fig_bar = px.bar(
        display_df,
        x=x_field,
        y=y_field,
        color=colour_field,
        color_discrete_sequence=colours,
        width=base_width,
        height=base_height,
        title=title,
        text=text_field,
        labels=field_labels,
        opacity=0.75
    )

    fig_bar.update_layout(
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1.02,
        #     xanchor="center",
        #     x=1
        # ),
        showlegend=showlegend
    )


    fig_bar.update_traces(textposition='outside')

    if legend_title:
        fig_bar.update_layout(legend_title_text=legend_title)

    return fig_bar