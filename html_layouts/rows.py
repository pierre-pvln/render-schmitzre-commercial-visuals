# ############################################################################
#
# GEEN FUNCTIES/LOGICA UITVOEREN IN DIT BESTAND.
# ENKEL BEDOELD OM EEN LAYOUT ELEMENT TE DEFINIEREN
# AANPASSINGEN VIA CALLBACK OUTPUTS
#
# @version    v0.0.6  2023-01-04
# @author     pierre@ipheion.eu
# @copyright  (C) 2020-2022 Pierre Veelen
#
# ############################################################################
#
# - styling in .\assets\styles.css
#                 python <-> css
#                tagname <-> tagname
#             id=some-id <-> #some-id
#   className=some-class <-> .some-class
#
# ############################################################################

# Visualization modules
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dash_table, dcc, html


def MAP_ROW(id_name, settings, a_figure):
    return dbc.Row(
        # row with the map
        [
            # https://dash.plotly.com/dash-core-components/graph
            dcc.Graph(
                id=id_name,
                style={"height": "800px", "width": "90%"},
                figure=a_figure,
                config=settings,
            ),
        ],
    )


def MUNICIPALITY_NAME_SELECTION_ROW(SelectionText, DropDownOptions):
    return dbc.Row(  # Municipality
        [
            dbc.Col(
                [html.P([SelectionText],)],
                style={
                    # "border-style": "solid"
                    "marginLeft": "10px",
                },
                width=3),
            dbc.Col(
                [
                    # https://dash.plotly.com/dash-core-components/dropdown
                    dcc.Dropdown(
                        id="locate-municipality",
                        options=DropDownOptions,
                        # value=enterprise_options[0]['value'],  # start with one value is selectionbox
                        value="",  # all_municipality_names,  # start with all values in selectionbox
                        placeholder="Start typing the name of the municipality to go to on the map",
                        searchable=True,
                        multi=False,
                        disabled=False,
                    ),
                ],
                width=8,
            ),
        ]
    )


def SWITCH_AND_SELECTION_ROW(
    SelectionName, SelectionText, DropDownPlaceholderText, DropDownOptions, DropDownOptionTitle="Options"
):
    return dbc.Row(  # Netzknoten
        [
            dbc.Col(
                [
                    html.P([SelectionText],),
                    daq.BooleanSwitch(id=SelectionName + "-switch", on=True,),
                ],
                id=SelectionName + "-switch-column",
                style={
                    # "border-style": "solid"
                    "marginLeft": "10px",
                },
                width=3,
            ),
            dbc.Col(
                # create a dropdown selection for the netzknoten
                [
                    html.P([DropDownOptionTitle],),
                    # https://dash.plotly.com/dash-core-components/dropdown
                    dcc.Dropdown(
                        id=SelectionName + "-selection",
                        options=DropDownOptions,
                        # value=enterprise_options[0]['value'],  # start with one value is selectionbox
                        value=[],  # start with empty selection
                        # value=all_enterprise_values,  # start with all values in selectionbox
                        placeholder=DropDownPlaceholderText,
                        searchable=True,
                        multi=True,
                        disabled=False,
                    ),
                ],
                id=SelectionName + "-dropdown-column",
                width=8,
                # style={"borderStyle": "solid"}
            ),
        ],
    )


def DATATABLE_RESULTS_ROW(RadioItemOptions, RadioItemValue, TableColumnSettings):

    return dbc.Row(  # datatabel overzicht
        [
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P(
                                ["Show data based on which selection criterium:"],
                                id="datatable-pre-text",
                                style={"marginLeft": "-20px"},
                            ),
                            dcc.RadioItems(
                                options=RadioItemOptions,
                                id="radio-item-selection",
                                value=RadioItemValue,
                                labelStyle={
                                    "display": "inline-block",
                                    "marginRight": "50px",
                                },
                            ),
                        ],
                        id="div-radio-items",
                        style={
                            "marginLeft": "20px",
                            "marginTop": "10px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dash_table.DataTable(
                                id="the-datatable-total",
                                columns=TableColumnSettings,
                                # data=datatable_df.to_dict('records'),
                                page_size=2,  # max number of rows per "page" in this case only header and total row
                                style_table={"overflowY": "auto"},  # 'height': '300px',
                                # keep heading on 1 line, wrap the data
                                style_data={"whiteSpace": "normal", "height": "auto"},
                                style_cell_conditional=[
                                    {
                                        "if": {"column_id": "uniform_city_name"},
                                        "width": "200px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "insgesamt"},
                                        "width": "30px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_BK"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_McD"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_KFC"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_MFT"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                ],
                            ),
                            html.Br([],),
                            dash_table.DataTable(
                                id="the-datatable",
                                columns=TableColumnSettings,
                                # data=datatable_df.to_dict('records'),
                                page_size=6,  # max number of rows per "page"
                                style_table={"overflowY": "auto"},  # 'height': '300px',
                                # keep heading on 1 line, wrap the data
                                style_data={"whiteSpace": "normal", "height": "auto"},
                                style_cell_conditional=[
                                    {
                                        "if": {"column_id": "uniform_city_name"},
                                        "width": "200px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "insgesamt"},
                                        "width": "30px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_BK"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_McD"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_KFC"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                    {
                                        "if": {"column_id": "count_MFT"},
                                        "width": "25px",
                                        "fontSize": "12px",
                                    },
                                ],
                            ),
                            html.Br([],),
                        ],
                        # styling used to show / not show the table
                        # default setting is hidden
                        style={
                            # "borderStyle": "solid",
                            # "borderWidth": "1px",
                            "visibility": "hidden"
                        },
                        id="div-datatable",
                    ),
                ],
                id="datatable-col",
                style={},
            ),
        ],
        id="data-overview",
        style={  # "borderStyle": "solid",
            # "borderWidth": "1px",
            "height": "400px",
            "marginLeft": "20px",
            "marginTop": "20px",
        },
    )


def LEGEND_ROW():
    return dbc.Row(
        [
            dbc.Col(
                [
                    # Start with empty legend text
                    # html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
                    # html.Div(["-* legend updated when selected *-"]),
                ],
                id="isochrone-legend-col",
                width=12,
            ),
            dbc.Col(
                [
                    # Start with empty legend text
                    # html.Div(["COMMERCIAL POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
                    # html.Div(["Mc Donalds"], style={"color": "red", "marginRight": "10px"}),
                    # html.Div(["Burger King"], style={"color": "blue", "marginRight": "10px"}),
                    # html.Div(["KFC"], style={"color": "green", "marginRight": "10px"}),
                    # html.Div(["Expansion"], style={"color": "orange", "marginRight": "10px"}),
                ],
                id="company-legend-col",
                width=4,
            ),
            dbc.Col(
                [
                    # Start with empty legend text
                    # html.Div(["PREDICTION POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
                    # html.Div(["10 Km / Min Zone"], style={"color": "cyan", "marginRight": "10px"}),
                    # html.Div(["20 Km / Min Zone"], style={"color": "fuchsia", "marginRight": "10px"}),
                ],
                id="prediction-legend-col",
                width=4,
            ),
            dbc.Col(
                [
                    # Start with empty legend text
                    # html.Div(["MUNICIPALITY POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
                    # html.Div(["Gemeinde"], style={"color": "black", "marginRight": "10px"}),
                    # html.Div(["Kreissitz gemeinde"], style={"color": "purple", "marginRight": "10px"}),
                ],
                id="municipality-legend-col",
                width=4,
            ),
        ],
        style={  # "borderStyle": "solid",
            # "borderWidth": "1px",
            "height": "250px",
        },
    )
