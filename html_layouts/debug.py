# ############################################################################
#
# GEEN FUNCTIES/LOGICA UITVOEREN IN DIT BESTAND.
# ENKEL BEDOELD OM EEN LAYOUT ELEMENT TE DEFINIEREN
# AANPASSINGEN VIA CALLBACK OUTPUTS
#
# @version    v0.0.2  2022-12-02
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
from dash import html


# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
def build_header(dbg_str, hide_it=True):
    """
    Returns HTML Header element for the applications debugging header.

    :return: HTML Header
    """
    return html.Header(
        children=[header_row_top(), header_row_center(dbg_str), header_row_bottom()],
        hidden=hide_it,
    )


def header_row_top():
    return dbc.Row(children=[], id="dbg_header-row-top")


def header_row_center(debug_text):
    return dbc.Row(
        children=[
            dbc.Col([]),
            dbc.Col(
                [
                    html.P(
                        [debug_text],
                        id="debug_header-row-center-text",
                        style={"textAlign": "center", "color": "#263473"},
                    ),
                ],
                width=8,
            ),
            dbc.Col([]),
        ],
        id="debug_header-row-center",
        style={
            "background": "#D5E8F5",
            "borderBottom": "solid",
            "borderColor": "#9BC552",
        },
    )


def header_row_bottom():
    return dbc.Row(
        children=[],
        id="debug_header-row-bottom",
        style={"background": "#D5E8F5", "paddingTop": "10px"},
    )
