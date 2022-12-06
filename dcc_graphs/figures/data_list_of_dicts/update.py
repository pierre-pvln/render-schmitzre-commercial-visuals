def point_on_map_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    point_on_map = dict(
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
        type="scattermapbox",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
        name=subset_name,
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
        showlegend=False,  # do not show this dataset in legend
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
        # where to show the markers
        lat=inputdf["lat"],
        lon=inputdf["lon"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
        # show markers + text on the map
        mode="markers+text",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
        # show hovertext if not defined
        # show the text
        hovertext=inputdf["grad_der_verstädterung"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
        # customdata=inputdf["city"],
        customdata=inputdf["uniform_city_name"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
        hoverinfo="name+text",
        # hoverinfo="name",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
        hovertemplate="<b>%{customdata}</b><br><br>"
        + "%{hovertext}<br>"
        + "<extra>Selected Location</extra>",
        marker=dict(
            symbol="circle",  # name of icon in icon set or "circle"
            size=15,
            color="darkred",
            #line=dict(width=6, color="green"),
            opacity=1,  # show marker
        ),
    )
    return [point_on_map]

def municipality_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    data_dict_list = []

    # for name in inputdf['grad_der_verstädterung'].unique().tolist():
    #    print(name)
    data_dict_list = data_dict_list + [
        dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            # @@ name=municipality_subset,
            name=subset_name,
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-legendgroup
            # legendgroup=municipality_subset,
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
            # where to show the markers
            lat=inputdf["lat"],
            lon=inputdf["lon"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
            # show markers + text on the map
            mode="markers+text",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
            # show hovertext if not defined
            # show the text
            hovertext=inputdf["grad_der_verstädterung"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            # customdata=inputdf["city"],
            customdata=inputdf["uniform_city_name"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
            hovertemplate="<b>%{hovertext}</b><br><br>"
            + "City: %{customdata}<br>"
            + "<extra>Municipality</extra>",
            # Set marker colors based on values
            # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
            # https://plotly.com/python/marker-style/
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                size=[
                    16
                    if (x == "dicht besiedelt") or (x == "dicht besiedelt-Kreissitz")
                    else 8
                    if (x == "mittlere Besiedlungsdichte")
                    or (x == "mittlere Besiedlungsdichte-Kreissitz")
                    else 4
                    if (x == "gering besiedelt") or (x == "gering besiedelt-Kreissitz")
                    else 2
                    for x in list(inputdf["grad_der_verstädterung"])
                ],
                color=[
                    "black"
                    if x == "dicht besiedelt"
                    else "black"
                    if x == "mittlere Besiedlungsdichte"
                    else "grey"
                    if x == "gering besiedelt"
                    else "purple"
                    if x == "dicht besiedelt-Kreissitz"
                    else "purple"
                    if x == "mittlere Besiedlungsdichte-Kreissitz"
                    else "blueviolet"
                    if x == "gering besiedelt-Kreissitz"
                    else "lavender"
                    for x in list(inputdf["grad_der_verstädterung"])
                ],
                opacity=0.5,
            ),
        )
    ]

    return data_dict_list


def company_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    company_data_dict = dict(
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
        type="scattermapbox",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
        name=subset_name,
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
        showlegend=False,  # do not show this dataset in legend
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
        # where to show the markers
        lat=inputdf["lat"],
        lon=inputdf["lon"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
        # show markers + text on the map
        mode="markers+text",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
        # show hovertext if not defined
        # show the text
        hovertext=inputdf["enterprise"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
        # customdata=inputdf["city"],
        customdata=inputdf["uniform_city_name"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
        hoverinfo="name+text",
        # hoverinfo="name",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
        hovertemplate="<b>%{hovertext}</b><br><br>"
        + "City: %{customdata}<br>"
        + "<extra>Company</extra>",
        # Set marker colors based on values
        # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
        marker=dict(
            symbol="circle",  # name of icon in icon set or "circle"
            size=10,
            color=[
                "blue"
                if x == "BurgerKing"
                else "red"
                if x == "McDonalds"
                else "green"
                if x == "KentuckyFriedChicken"
                else "orange"
                if x == "McFIT"
                else "yellow"
                for x in list(inputdf["enterprise"])
            ],
            opacity=0.5,
        ),
    )
    return [company_data_dict]


def netzknoten_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    nk_data_dict = dict(
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
        type="scattermapbox",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
        name=subset_name,
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
        showlegend=False,  # do not show this dataset in legend
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
        # where to show the markers
        lat=inputdf["lat"],
        lon=inputdf["lon"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
        # show markers + text on the map
        mode="markers+text",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
        # show hovertext if not defined
        # show the text
        hovertext=inputdf["NK_Name"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
        customdata=inputdf["NK_GeoStrKls"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
        hoverinfo="name+text",
        # hoverinfo="name",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
        hovertemplate="<b>%{hovertext}</b><br><br>"
        + "GeoStrKls: %{customdata}<br>"
        + "<extra>Netzknoten</extra>",
        # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
        marker=dict(
            symbol="circle",  # name of icon in icon set or "circle"
            size=8,
            color="violet",
            opacity=0.5,
        ),
    )
    return [nk_data_dict]


def prediction_10km_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    data_10Km_dict = dict(
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
        type="scattermapbox",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
        name=subset_name,
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
        showlegend=False,  # do not show this dataset in legend
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
        # where to show the markers
        lat=inputdf["lat"],
        lon=inputdf["lon"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
        # show markers + text on the map
        mode="markers+text",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
        # show hovertext if not defined
        # show the text
        hovertext=inputdf["meaningfull_text_10km"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
        customdata=inputdf["uniform_city_name"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
        hoverinfo="name+text",
        # hoverinfo="name",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
        hovertemplate="<b>%{hovertext}</b><br><br>"
        + "Municipality: %{customdata}<br>"
        + "<extra>Prediction 10Km</extra>",
        # Set marker colors based on values
        # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
        marker=dict(
            symbol="circle",  # name of icon in icon set or "circle"
            size=8,
            color=[
                "cyan" if x else "white"
                for x in list(inputdf["select_this_location_prediction"])
            ],
            opacity=0.5,
        ),
    )
    return [data_10Km_dict]


def prediction_20km_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    data_20Km_dict = dict(
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
        type="scattermapbox",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
        name=subset_name,
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
        showlegend=False,  # do not show this dataset in legend
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
        # where to show the markers
        lat=inputdf["lat"],
        lon=inputdf["lon"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
        # show markers + text on the map
        mode="markers+text",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
        # show hovertext if not defined
        # show the text
        hovertext=inputdf["meaningfull_text_totals"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
        customdata=inputdf["uniform_city_name"],
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
        hoverinfo="name+text",
        # hoverinfo="name",
        # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
        hovertemplate="<b>%{hovertext}</b><br><br>"
        + "Municipality: %{customdata}<br>"
        + "<extra>Prediction 20Km</extra>",
        # Set marker colors based on values
        # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
        marker=dict(
            symbol="circle",  # name of icon in icon set or "circle"
            size=8,
            color=[
                "fuchsia" if x else "white"
                for x in list(inputdf["select_this_location_prediction"])
            ],
            opacity=0.5,
        ),
    )
    return [data_20Km_dict]


def selected_municipality_data_dict_list(inputdf, subset_name, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] point_on_map_data_dict_list")
    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("subset_name    :", subset_name)

    # shows only the point of the selected municipality on the map
    if len(inputdf) == 1:
        # print(inputdf.columns)
        selected_municipality_dict = dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            name=subset_name,
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-showlegend
            showlegend=False,  # do not show this dataset in legend
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lat
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-lon
            # where to show the markers
            lat=inputdf["lat"],
            lon=inputdf["lon"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-mode
            # show markers + text on the map
            mode="markers+text",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertext
            # show hovertext if not defined
            # show the text
            # hovertext=inputdf["meaningfull_text_totals"],
            hovertext=inputdf["uniform_city_name"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            customdata=inputdf["uniform_city_name"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hovertemplate
            hovertemplate="<b>%{hovertext}</b><br><br>"
            + "Municipality: %{customdata}<br>"
            + "<extra>Selected Municipality</extra>",
            # https://plotly.com/python/reference/scattermapbox/#scattermapbox-textposition
            # textposition='top left',
            # Set marker colors based on values
            # https://stackoverflow.com/questions/61686382/change-the-text-color-of-cells-in-plotly-table-based-on-value-string
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                size=15,
                color="white",
                opacity=0.5,
            ),
        )

    else:
        selected_municipality_dict = {}

    return [selected_municipality_dict]
