# https://plotly.com/python/graph-objects/
# https://plotly.com/python/figure-structure/


def default_modebar(save_to_filename):
    return dict(
        # https://plotly.com/javascript/configuration-options/#never-display-the-modebar
        displayModeBar="hover",
        # True : always show mode bar
        # False: never show mode bar
        # "hover": only show mode bar when hovering over graph
        # https://plotly.com/javascript/configuration-options/#remove-modebar-buttons
        modeBarButtonsToRemove=["lasso2d", "select2d"],
        # https://plotly.com/javascript/configuration-options/#customize-download-plot-options
        toImageButtonOptions=dict(
            format="png",  # one of 'png', 'svg', 'jpeg', 'webp'
            filename=save_to_filename,
            # height=500,
            # width=700,
            scale=1,  # Multiply title / legend / axis / canvas sizes by this factor
        ),
        # https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar
        displaylogo=True,  # Either True or False
    )


def graph_modebar(save_to_filename):
    return dict(
        # https://plotly.com/javascript/configuration-options/#never-display-the-modebar
        displayModeBar="hover",
        # True : always show modebar
        # False: never show mode bar
        # "hover": only show modebar when hovering over graph
        # https://plotly.com/javascript/configuration-options/#remove-modebar-buttons
        modeBarButtonsToRemove=[
            "lasso2d",
            "select2d",
            "pan2d",
            "toggleSpikelines",
            "toggleHover",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "hoverClosestGl2d",
        ],
        # https://plotly.com/javascript/configuration-options/#customize-download-plot-options
        toImageButtonOptions=dict(
            format="png",  # one of 'png', 'svg', 'jpeg', 'webp'
            filename=save_to_filename,
            height=500,
            width=700,
            scale=1,  # Multiply title / legend / axis / canvas sizes by this factor
        ),
        # https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar
        displaylogo=True,  # Either True or False
    )


def mapbox_modebar(save_to_filename):
    return dict(
        # https://plotly.com/javascript/configuration-options/#never-display-the-modebar
        displayModeBar="hover",
        # True : always show mode bar
        # False: never show mode bar
        # "hover": only show mode bar when hovering over graph
        # https://plotly.com/javascript/configuration-options/#remove-modebar-buttons
        modeBarButtonsToRemove=[
            "lasso2d",
            "select2d",
            "pan2d",
            "zoom2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
        ],
        # https://plotly.com/javascript/configuration-options/#customize-download-plot-options
        toImageButtonOptions=dict(
            format="png",  # one of 'png', 'svg', 'jpeg', 'webp'
            filename=save_to_filename,
            # height=500,
            # width=700,
            scale=1,  # Multiply title / legend / axis / canvas sizes by this factor
        ),
        # https://plotly.com/javascript/configuration-options/#hide-the-plotly-logo-on-the-modebar
        displaylogo=True,  # Either True or False
    )
