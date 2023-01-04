def empty_map(token, center_value, zoom_value):
    initial_data_dict_list = [
        dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
        )
    ]

    return {
        "data": initial_data_dict_list,
        "layout": dict(
            autosize=True,
            hovermode="closest",
            margin=dict(l=0, r=0, t=0, b=0),
            clickmode="event+select",
            mapbox=dict(
                accesstoken=token,
                bearing=0,
                #                 center={"lon": 5.764278, "lat": 50.986729}, Stein
                center=center_value,  # {"lon": 5.764278, "lat": 50.986729},
                style="outdoors",
                pitch=0,
                #                zoom=13.97,
                zoom=zoom_value  # 13.97,
                #            layers=update_layers_list(glb_geozone_list)
            ),
        ),
    }
