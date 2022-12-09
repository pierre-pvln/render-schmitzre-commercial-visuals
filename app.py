# v44 
# ===
# - changed the name of global vars to glb_
# - removed var ref_in_fname 
# v45
# ===
# - removed var municipality_text; replaced by o_glb_selected_municipality_name
# - cleanup actions when callback is triggered
# v46
# - cleaned up version of v45

app_version = "v47"
# put the name of this python file in txt file for processing by other scripts
with open("_current_app_version.txt", "w") as version_file:
    version_file.write(app_version + "\n")

# TODO
# - ZOOM IN / OUT REMOVES POLYGONS
# - Add data set when selecting municipality

import json
import os
import sys
import socket
from datetime import datetime

# Visualization modules
import dash
import plotly
from dash import Dash
import dash_bootstrap_components as dbc

# data wrangling modules
import numpy as np
import pandas as pd

from dash import dcc, html
from dash.dash_table.Format import Align, Format, Group
from dash.dependencies import Input, Output, State
from numpy import cos, pi, sin

# geo stuff
# https://stackoverflow.com/questions/43892459/check-if-geo-point-is-inside-or-outside-of-polygon
from shapely.geometry import Point, shape

# local settings from subfolders of this app
from config import strings
from html_layouts import footer, header, rows, debug
from utils.geo_mapbox import zoom_center
from utils.geojsons import boundingbox_and_geojson, circle_and_geojson, isochrone_and_geojson
from dcc_graphs.configs.modebars import mapbox_modebar
from dcc_graphs.figures.data_list_of_dicts.update import *
from dcc_graphs.figures.initial_figures import empty_map

run_environment = "production"
print("[INFO   ] ==== START ===")
print("[INFO   ] Run environment:",run_environment)

####################################################
# DEFINE GENERICALLY USED VARS
####################################################
# initialize some globally used vars

if run_environment=="test":
    glb_verbose = True  # True
    glb_fxn_verbose = 3  # 3
    # 0 = Don't output any text
    # 1 = Show only function name
    # 2 = Show function input values
    # 3 = Show additional info
    glb_hide_debug_text = False
else:
    glb_verbose = False
    glb_fxn_verbose = 0
    # 0 = Don't output any text
    # 1 = Show only function name
    # 2 = Show function input values
    # 3 = Show additional info
    glb_hide_debug_text = True


o_glb_selected_municipality_name = strings.HEADER_SUBTITLE  # the value of the municipality name in the selectionbox

glb_mapbox_access_token = os.getenv("MAPBOX_ACCESS_TOKEN", default=None)

# SYSTEM AND APP INFO
# =============================================
the_hostname = socket.gethostname()
run_on = os.getenv("RUN_LOCATION", "local")
if run_on.lower() in ["heroku"]:
    glb_verbose = False
python_version = sys.version.split()[0]
dash_version = dash.__version__
plotly_version = plotly.__version__

# folders for output
input_dir = "./data/final/"

# datasets
company_subset = "Company"
municipality_subset = "Municipality"
netzknoten_subset = "Netzknoten"
prediction_subset_10Km = "10Km_combined_prediction_df"
prediction_subset_20Km = "20Km_combined_prediction_df"
selected_municipality_subset = "SelectedMunicipality"
baseline = "Baseline"

# Company
# ==================================================
# read company data from file
df_company = pd.read_csv(input_dir + company_subset + ".csv")
df_company = df_company.rename(
    columns={"latitude": "lat", "longitude": "lon"}
)
# remove any empty values
df_company.dropna(subset=["uniform_city_name"], inplace=True)
df_company_filtered = pd.DataFrame(columns=df_company.columns)
if glb_verbose:
    print("[INFO   ] len(df_company) :", len(df_company))
    print("[INFO   ]", df_company.columns)

# dropdown selection options
enterprise_options = [
    {"label": i, "value": i} for i in df_company["enterprise"].unique()
]
all_enterprise_values = df_company["enterprise"].unique().tolist()


# Municipality
# ==================================================
# read municipality data from file
df_municipality = pd.read_csv(input_dir + municipality_subset + ".csv")
df_municipality = df_municipality.rename(
    columns={"breitengrad": "lat", "längengrad": "lon"}
)
# remove any empty values
df_municipality.dropna(subset=["uniform_city_name"], inplace=True)
glb_df_municipality_filtered = pd.DataFrame(columns=df_municipality.columns)
if glb_verbose:
    print("[INFO   ] len(df_municipality) :", len(df_municipality))
    print("[INFO   ]", df_municipality.columns)

# create an empty dataframe for selected municipality
df_selected_municipality = pd.DataFrame(columns=df_municipality.columns)  # df for selected municipality in dropdownbox
df_point_on_map_filtered = pd.DataFrame(columns=df_municipality.columns)  #

municipality_options = [
    {"label": i, "value": i} for i in df_municipality["grad_der_verstädterung"].unique()
]
all_municipality_values = df_municipality["grad_der_verstädterung"].unique().tolist()

# sort the municipality names also
all_municipality_names = sorted(df_municipality["uniform_city_name"].unique().tolist())
municipality_names = [{"label": i, "value": i} for i in all_municipality_names]

# read baseline data from file
# TODO wat is verschil tussen baseline en municiplaity bestand?
# TODO en moet municiplaity bestand niet vervangen worden door baseline?
input_filename = input_dir + baseline
df_baseline = pd.read_csv(input_filename + ".csv")
df_baseline.dropna(subset=["uniform_city_name"], inplace=True)
if glb_verbose:
    print("[INFO   ] len(" + baseline + ") :", len(df_baseline))
    print("[INFO   ]", df_baseline.columns)


# Netzknoten
# ==================================================
# read netzknoten data from file
glb_df_netzknoten = pd.read_csv(input_dir + netzknoten_subset + ".csv")
# initialize df with filtered data
glb_df_netzknoten_filtered = pd.DataFrame(columns=glb_df_netzknoten.columns)
if glb_verbose:
    print("[INFO   ] len(glb_df_netzknoten) :", len(glb_df_netzknoten))
    print("[INFO   ]", glb_df_netzknoten.columns)

netzknoten_options = [{"label": i, "value": i} for i in glb_df_netzknoten["NK_GeoStrKls"].unique()]
all_netzknoten_values = glb_df_netzknoten["NK_GeoStrKls"].unique().tolist()


# Prediction 10 km
# ==================================================
# read prediction data from file
df_prediction_10Km = pd.read_csv(input_dir + prediction_subset_10Km + ".csv")
# initialize df with filtered data
df_prediction_10Km_filtered = pd.DataFrame(columns=df_prediction_10Km.columns)
if glb_verbose:
    print("[INFO   ] len(df_prediction_10Km) :", len(df_prediction_10Km))
    print("[INFO   ]", df_prediction_10Km.columns)

# Prediction 20 km
# ==================================================
# read prediction data from file
df_prediction_20Km = pd.read_csv(input_dir + prediction_subset_20Km + ".csv")
# initialize df with filtered data
df_prediction_20Km_filtered = pd.DataFrame(columns=df_prediction_20Km.columns)
if glb_verbose:
    print("[INFO   ] len(df_prediction_20Km) :", len(df_prediction_20Km))
    print("[INFO   ]", df_prediction_20Km.columns)

# dropdown selection options
prediction_options = [
    {"label": "LogReg", "value": "LogReg"},  # Logistic Regression
    {"label": "LinReg", "value": "LinReg"},  # Linear Regression
    {"label": "BstGs", "value": "BstGs"},  # Best Guess
    {"label": "Reccom", "value": "Reccom"},  # Recommender system
]

# Other selection options
# ==================================================
datatable_radio_options = [
    {"label": "Keine Daten zeigen", "value": "empty"},
    {"label": "Box 20Km", "value": "bbox20"},
    {"label": "Box 10Km", "value": "bbox10"},
    {"label": "Circle 20Km", "value": "circle20"},
    {"label": "Circle 10Km", "value": "circle10"},
    {"label": "Car 30min", "value": "car-iso30"},
    {"label": "Car 20min", "value": "car-iso20"},
    {"label": "Car 10min", "value": "car-iso10"},
    {"label": "Bike 20min", "value": "bike-iso20"},
    {"label": "Bike 10min", "value": "bike-iso10"},
    {"label": "Walk 10min", "value": "walk-iso10"},
]

default_radio_item_selection = "empty"

# ===================================
#
# Initializing global default values
#
# ===================================
# set the zoom level to show all points on the map
glb_init_calc_zoom, glb_init_calc_center = zoom_center(lons=df_company["lon"], lats=df_company["lat"])
glb_calc_zoom = glb_init_calc_zoom
glb_calc_center = glb_init_calc_center

# these hold the latest value of last selected municipality and its lon/lat values
glb_latest_municipality = ""
glb_latest_lon = glb_calc_center["lon"]
glb_latest_lat = glb_calc_center["lat"]

# start values to create an empty datatable
datatable_lon = None
datatable_lat = None
datatable_mun = ""
datatable_typ = default_radio_item_selection
glb_datatable_geojson = {}  # geojson holding the contours on the map with the data in the datatable


municipality_type_selection_text = "municipality-type"
company_selection_text = "company"
netzknoten_selection_text = "netzknoten"
prediction_selection_text = "prediction"

# create empty layers list for geojson polygons on map
glb_geojson_layers_list = []


# ===================================
#
# FUNTIONS FOR HANDLING DATATABLE
#
# ===================================
def select_datatable_subset(
    inputdf, lon, lat, geojson, municipality, selectiontype=default_radio_item_selection, fxn_verbose=0
):
    """
    inputdf:       dataframe with the info of all places
    lon:           longitude van middelpunt van de locatie
    lat:           latitude van middelpunt van de locatie
    geojson:       geojson holding the contour outerbounds (municipalities in the geojson get another color).
    municipality:  name of the municipality in which the point that was clicked is located
    selectiontype: one of
                   bbox10: bounding box round circle with 10 km radius
                   bbox20: bounding box round circle with 20 km radius
                   #circle10: within circle with 10km radius
                   #circle20: within circle with 10km radius
                   #circle10: circle with radius 10 km
                   #circle20: circle with radius 20 km
    fxn_verbose    boolean; wether or not to verbose output from this function
    """

    if fxn_verbose > 0:
        print("[FUNCTION] select_datatable_subset")

    if fxn_verbose > 1:
        print("len inputdf    :", len(inputdf))
        print("columns inputdf:", inputdf.columns)
        print("lon            :", str(lon))
        print("lat            :", str(lat))
        print("geojson        :", geojson)
        print("municipality   :", municipality)
        print("selectiontype  :", selectiontype)

    columns_list = [
        "uniform_city_name",
        "lon",
        "lat",
        "insgesamt",
        "count_BK",
        "count_McD",
        "count_KFC",
        "count_MFT",
    ]
    subset_df = pd.DataFrame(columns=columns_list)
    subset_df_total = pd.DataFrame(columns=columns_list)

    # geojson has precedence
    # TODO why does geojson have precendence?

    # work with geojson
    if geojson is not None:
        if fxn_verbose > 2:
            print("Working with geojson")

        geometry = geojson.get("geometry")
        if geometry is not None:
            if fxn_verbose > 2:
                print("geometry is not None")

            # define the polygon
            poly = shape(geometry)
            # get boundaries of polygon
            lon_min, lat_min, lon_max, lat_max = poly.bounds

            # bepaal welke plaatsen in de boundary
            subset_df = inputdf.loc[
                (inputdf["lon"] >= lon_min)
                & (inputdf["lon"] <= lon_max)
                & (inputdf["lat"] >= lat_min)
                & (inputdf["lat"] <= lat_max)
            ].copy()

            # select only the relevant columns (which are in columns_list)
            subset_df = subset_df[columns_list]
            subset_df["not_in_polygon"] = True

            # Nu bepalen welke punten uit die lijst in de polygon zijn (de geojson).
            subset_df["not_in_polygon"] = subset_df.apply(
                lambda x: not poly.contains(Point(x["lon"], x["lat"])), axis=1
            )

            # verwijder onderdelen die niet in polygon zitten
            if fxn_verbose > 2:
                print(len(subset_df))

            subset_df.drop(subset_df[subset_df["not_in_polygon"]].index, inplace=True)

            if fxn_verbose > 2:
                print("Polygon contains:", len(subset_df), "municipalities")

            # and sort on einwohner and name
            subset_df.sort_values(by=["insgesamt", "uniform_city_name"], ascending=[False, True], inplace=True)

        else:
            if fxn_verbose > 2:
                print("geometry is None")
                print("now what?")

    else:
        # geojson was none
        # work with coordinates
        if lon is not None and lat is not None and selectiontype != "empty":
            if fxn_verbose > 2:
                print("KOMT DIT NOG WEL VOOR??")
                print("Working with coordinates")
                print("radio selection type :" + selectiontype)

            if selectiontype == "bbox20":
                # bepaal de buitenranden van de cirkel
                r = 0.1
                r_factor = 2
                #    r = 0.75
                #    r = 0.1  # r = 100 meters
                t = np.linspace(0, 2 * pi, 100)
                circle_lon = lon + r * r_factor * cos(t)
                circle_lat = lat + r * r_factor * sin(t)

                coords = []
                for lo, la in zip(list(circle_lon), list(circle_lat)):
                    coords.append([lo, la])

                bbox = [
                    circle_lon.min(),
                    circle_lon.max(),
                    circle_lat.min(),
                    circle_lat.max(),
                ]

                # bepaal welke plaatsen in de boudingbox
                subset_df = inputdf.loc[
                    (df_baseline["lon"] >= bbox[0])
                    & (df_baseline["lon"] <= bbox[1])
                    & (df_baseline["lat"] >= bbox[2])
                    & (df_baseline["lat"] <= bbox[3])
                ].copy()

                # select only the relevant columns (which are in columns_list)
                subset_df = subset_df[columns_list]
                # and sort on einwohner and name
                subset_df.sort_values(
                    by=["insgesamt", "uniform_city_name"],
                    ascending=[False, True],
                    inplace=True,
                )

                # # add totals to totals df
                # subset_df_total = subset_df_total.append(subset_df.sum(numeric_only=True), ignore_index=True)
                # subset_df_total['uniform_city_name'] = "Total bbox 20km " + str(municipality)

            elif selectiontype == "bbox10":
                # bepaal de buitenranden van de cirkel
                r = 0.1
                r_factor = 1
                #    r = 0.75
                #    r = 0.1  # r = 100 meters
                t = np.linspace(0, 2 * pi, 100)
                circle_lon = lon + r * r_factor * cos(t)
                circle_lat = lat + r * r_factor * sin(t)

                coords = []
                for lo, la in zip(list(circle_lon), list(circle_lat)):
                    coords.append([lo, la])

                bbox = [
                    circle_lon.min(),
                    circle_lon.max(),
                    circle_lat.min(),
                    circle_lat.max(),
                ]

                # bepaal welke plaatsen in de boudingbox
                subset_df = inputdf.loc[
                    (df_baseline["lon"] >= bbox[0])
                    & (df_baseline["lon"] <= bbox[1])
                    & (df_baseline["lat"] >= bbox[2])
                    & (df_baseline["lat"] <= bbox[3])
                ].copy()

                # select only the relevant columns (which are in columns_list)
                subset_df = subset_df[columns_list]
                # and sort on einwohner and name
                subset_df.sort_values(
                    by=["insgesamt", "uniform_city_name"],
                    ascending=[False, True],
                    inplace=True,
                )

                # add totals to totals df
                # ##subset_df_total = subset_df_total.append(subset_df.sum(numeric_only=True), ignore_index=True)
                # ##subset_df_total['uniform_city_name'] = "Total bbox 10km " + str(municipality)

    subset_df_total = subset_df_total.append(
        subset_df.sum(numeric_only=True), ignore_index=True
    )
    subset_df_total["uniform_city_name"] = "Insgesamt im Bereich " + str(municipality)

    return subset_df, subset_df_total


def settings_table_columns():
    # https://dash.plotly.com/datatable/data-formatting
    table_column_settings = [
        dict(
            id="uniform_city_name",
            name="Gemeinde",
            type="text",
            format=Format(align=Align.right, padding_width=50),
        ),
        dict(
            id="insgesamt",
            name="Anzahl Einwohner",
            type="numeric",
            format=Format(group_delimiter=".", group=Group.yes, groups=[3]),
        ),
        dict(
            id="count_BK",
            name="Anzahl BK",
            type="numeric",
            format=Format(group_delimiter=".", group=Group.yes, groups=[3]),
        ),
        dict(
            id="count_McD",
            name="Anzahl McD",
            type="numeric",
            format=Format(group_delimiter=".", group=Group.yes, groups=[3]),
        ),
        dict(
            id="count_KFC",
            name="Anzahl KFC",
            type="numeric",
            format=Format(group_delimiter=".", group=Group.yes, groups=[3]),
        ),
        dict(
            id="count_MFT",
            name="Anzahl MFT",
            type="numeric",
            format=Format(group_delimiter=".", group=Group.yes, groups=[3]),
        ),

    ]

    return table_column_settings


def update_municipalities_in_table_data_dict_list(inputdf, fxn_verbose=0):
    # shows all the municipalities that are present in the data table on the map
    if fxn_verbose > 0:
        print("[FUNCTION] update_municipalities_in_table_data_dict_list")

    if fxn_verbose > 1:
        print("len inputdf:"+str(len(inputdf)))
        print(inputdf.columns)

    toprow   = "<b>" + inputdf["uniform_city_name"] + "</b><br>"
    inwoners = "<br>" + "Einwohner    : " + inputdf["insgesamt"].astype(int).astype(str)
    cnt_bk   = "<br>" + "# Burgerking : " + inputdf["count_BK"].astype(int).astype(str)
    cnt_mcd  = "<br>" + "# Mc Donalds : " + inputdf["count_McD"].astype(int).astype(str)
    cnt_kfc  = "<br>" + "# KFC        : " + inputdf["count_KFC"].astype(int).astype(str)
    cnt_mft  = "<br>" + "# MacFIT     : " + inputdf["count_MFT"].astype(int).astype(str)

    # create column with specific hovertext
    inputdf["hovertext"] = toprow + inwoners + cnt_bk + cnt_mcd + cnt_kfc + cnt_mft

    if len(inputdf) >= 1:
        # print(inputdf.columns)
        municipalities_in_table_dict = dict(
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-type
            type="scattermapbox",
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-name
            name="in-contour",
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
            hovertext=inputdf["hovertext"],
            # # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-customdata
            # customdata=inputdf["uniform_city_name"],
            # https://plotly.com/javascript/reference/scattermapbox/#scattermapbox-hoverinfo
            hoverinfo="name+text",
            # hoverinfo="name",
            # Set marker
            marker=dict(
                symbol="circle",  # name of icon in icon set or "circle"
                size=10,
                color="teal",  # polygon_color, # "black",
                opacity=1,
            ),
        )

    else:
        municipalities_in_table_dict = {}

    return [municipalities_in_table_dict]


# ===================================
#
# GENERIC GRAPH/MAP UTILITY FUNCTIONS
#
# ===================================

# update the map
# ===================
def update_overall_map(the_zoom, the_center, fxn_verbose=0):
    if fxn_verbose > 0:
        print("[FUNCTION] update_overall_map")

    return {
        "data": prediction_10km_data_dict_list(df_prediction_10Km_filtered, prediction_subset_10Km, fxn_verbose)
        + prediction_20km_data_dict_list(df_prediction_20Km_filtered, prediction_subset_20Km, fxn_verbose)
        + netzknoten_data_dict_list(glb_df_netzknoten_filtered, netzknoten_subset, fxn_verbose)
        + company_data_dict_list(df_company_filtered, company_subset, fxn_verbose)
        + municipality_data_dict_list(glb_df_municipality_filtered, municipality_subset, fxn_verbose)
        + selected_municipality_data_dict_list(df_selected_municipality, selected_municipality_subset, fxn_verbose)
        + update_municipalities_in_table_data_dict_list(glb_updated_tabledata, fxn_verbose)
        + point_on_map_data_dict_list(df_point_on_map_filtered, "selected Location", fxn_verbose),
        "layout": dict(
            autosize=True,
            hovermode="closest",
            margin=dict(l=0, r=0, t=0, b=0),
            mapbox=dict(
                accesstoken=glb_mapbox_access_token,
                bearing=0,
                #                    center=dict(lat=lat_center, lon=lon_center),
                center=the_center,
                style="outdoors",
                pitch=0,
                #                    zoom=zoom_value,
                zoom=the_zoom,
                layers=glb_geojson_layers_list,
            ),
        ),
    }


def contour_graph(contour_type, lon, lat, contour_color="black", fxn_verbose=0):
    if fxn_verbose > 0:
        print("[INFO   ] Start function contour_graph")
        
    if fxn_verbose > 1:
        print("== INPUT ====================")
        print("contour_type :", contour_type)
        print("lon          :", lon)
        print("lat          :", lat)
        print("contour_color:", contour_color)
        print("== DONE =====================")

    geojson_layers_list = []
    datatable_geojson = {}
    # reset isochrone legend text
    isochrone_legend = []

    # create a new layers list everytime a point is clicked based on selection of radiobutton
    if contour_type == "empty":
        geojson_layers_list = []
        datatable_geojson = {}
        # reset isochrone legend text
        isochrone_legend = []

    if contour_type == "circle10":
        # if "marker.color" in i_graph_clickdata["points"][0]:
        #     contour_color = i_graph_clickdata["points"][0]["marker.color"]
        # else:
        #     contour_color = "black"
        geojson_layers_list, datatable_geojson = circle_and_geojson(
            center_lon=lon,
            center_lat=lat,
            r=0.1,  # r = 0.1 ongeveer 10 km radius
            color=contour_color,
        )
        # reset isochrone legend text
        isochrone_legend = []

    if contour_type == "circle20":
        # if "marker.color" in i_graph_clickdata["points"][0]:
        #     contour_color = i_graph_clickdata["points"][0]["marker.color"]
        # else:
        #     contour_color = "black"
        geojson_layers_list, datatable_geojson = circle_and_geojson(
            center_lon=lon,
            center_lat=lat,
            r=0.2,  # r = 0.2 ongeveer 20 km radius
            color=contour_color,
        )
        # reset isochrone legend text
        isochrone_legend = []

    if contour_type == "bbox10":
        # if "marker.color" in i_graph_clickdata["points"][0]:
        #     contour_color = i_graph_clickdata["points"][0]["marker.color"]
        # else:
        #     contour_color = "black"
        geojson_layers_list, datatable_geojson = boundingbox_and_geojson(
            center_lon=lon,
            center_lat=lat,
            r=0.1,  # r = 0.1 ongeveer 10 km radius
            bboxcolor=contour_color,
        )
        # reset isochrone legend text
        isochrone_legend = []

    if contour_type == "bbox20":
        # if "marker.color" in i_graph_clickdata["points"][0]:
        #     contour_color = i_graph_clickdata["points"][0]["marker.color"]
        # else:
        #     contour_color = "black"
        geojson_layers_list, datatable_geojson = boundingbox_and_geojson(
            center_lon=lon,
            center_lat=lat,
            r=0.2,  # r = 0.2 ongeveer 20 km radius
            bboxcolor=contour_color,
        )
        # reset isochrone legend text
        isochrone_legend = []

    if contour_type == "car-iso10":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="5",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, datatable_geojson = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="10",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 5 minutes drive by car"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 10 minutes drive by car"], style={"color": "orange", "marginRight": "10px"}),
        ]

    if contour_type == "car-iso20":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="5",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="10",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        a_layer, datatable_geojson = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="line",
            profile_str = "car",
            minutes_str="20",
            hex_colors_str="ff0000",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 5 minutes drive by car"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 10 minutes drive by car"], style={"color": "orange", "marginRight": "10px"}),
            html.Div(["Red zone: within 20 minutes drive by car"], style={"color": "red", "marginRight": "10px"}),
        ]

    if contour_type == "car-iso30":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="10",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str = "car",
            minutes_str="20",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        a_layer, datatable_geojson = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="line",
            profile_str = "car",
            minutes_str="30",
            hex_colors_str="ff0000",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 10 minutes drive by car"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 20 minutes drive by car"], style={"color": "orange", "marginRight": "10px"}),
            html.Div(["Red zone: within 30 minutes drive by car"], style={"color": "red", "marginRight": "10px"}),
        ]

    if contour_type == "bike-iso10":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="bike",
            minutes_str="5",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, datatable_geojson = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="bike",
            minutes_str="10",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 5 minutes cycling"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 10 minutes cycling"], style={"color": "orange", "marginRight": "10px"}),
        ]

    if contour_type == "bike-iso20":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="bike",
            minutes_str="5",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="bike",
            minutes_str="10",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        a_layer, datatable_geojson = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="line",
            profile_str="bike",
            minutes_str="20",
            hex_colors_str="ff0000",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 5 minutes cycling"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 10 minutes cycling"], style={"color": "orange", "marginRight": "10px"}),
            html.Div(["Red zone: within 20 minutes cycling"], style={"color": "red", "marginRight": "10px"}),
        ]

    if contour_type == "walk-iso10":
        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="walk",
            minutes_str="5",
            hex_colors_str="00ff00",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = a_layer

        a_layer, geojson_not_used = isochrone_and_geojson(
            lon_point=lon,
            lat_point=lat,
            polygontype_str="fill",
            profile_str="walk",
            minutes_str="10",
            hex_colors_str="ffa500",
            mapbox_access_token=glb_mapbox_access_token
        )
        geojson_layers_list = geojson_layers_list + a_layer

        # set isochrone legend text
        isochrone_legend = [
            html.Div(["ISOCHRONE LINES:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Green zone: within 5 minutes walking"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["Orange zone: within 10 minutes walking"], style={"color": "orange", "marginRight": "10px"}),
        ]

    return datatable_geojson, geojson_layers_list, isochrone_legend


####################################################
# APP DEFINITIONS
####################################################
external_stylesheets = [
    # https://bootswatch.com/zephyr/
    dbc.themes.ZEPHYR,
    # For Bootstrap Icons...
    dbc.icons.BOOTSTRAP
]

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
)
app.title = "Ipheion Demo Dashboard"
app.config['update_title'] = '.. Renewing ..'
# ToDo html page title to location that is viewed
# https://dash.plotly.com/external-resources -> Update the Document Title Dynamically Based on the URL or Tab


# app.config["suppress_callback_exceptions"] = True  # default is False
# suppress_callback_exceptions: check callbacks to ensure referenced IDs exist and props are valid.
# Set to True if your layout is dynamic, to bypass these checks.

if the_hostname not in ["LEGION-2020"]:
    server = app.server  # required for Heroku

app.layout = html.Div(
        [
            # TOP ROW / HEADER ROW
            # ====================
            # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
            header.build_header(
                title_str=strings.HEADER_TITLE,
                subtitle_str=o_glb_selected_municipality_name,
                version_str=app_version
            ),

            debug.build_header(
                dbg_str="-* debug text here *-",  # start with empty debug text
                hide_it=glb_hide_debug_text
            ),

            # CENTER ROW
            # ==========
            dbc.Row(
                [

                    # LEFT COLUMN
                    # ============
                    dbc.Col(
                        [
                            rows.MUNICIPALITY_NAME_SELECTION_ROW(
                                "Select Municipality", municipality_names
                            ),
                            html.Br(),
                            rows.SWITCH_AND_SELECTION_ROW(
                                SelectionName=company_selection_text,
                                SelectionText="Show Company locations",
                                DropDownPlaceholderText="Select 1 or more enterprises",
                                DropDownOptions=enterprise_options,
                            ),
                            html.Br(),
                            rows.SWITCH_AND_SELECTION_ROW(
                                SelectionName=municipality_type_selection_text,
                                SelectionText="Show municipality types",
                                DropDownPlaceholderText="Select 1 or more municipality types",
                                DropDownOptions=municipality_options,
                            ),
                            html.Br(),
                            rows.SWITCH_AND_SELECTION_ROW(
                                SelectionName=netzknoten_selection_text,
                                SelectionText="Show Netzknoten locations",
                                DropDownPlaceholderText="Select 1 or more netzknoten",
                                DropDownOptions=netzknoten_options,
                            ),
                            html.Br(),
                            rows.SWITCH_AND_SELECTION_ROW(
                                SelectionName=prediction_selection_text,
                                SelectionText="Show Predicted locations",
                                DropDownPlaceholderText="Select 1 or more predictions",
                                DropDownOptions=prediction_options,
                            ),
                            html.Br(),
                            rows.DATATABLE_RESULTS_ROW(
                                datatable_radio_options,
                                default_radio_item_selection,
                                settings_table_columns(),
                            ),
                        ],
                        width=6,
                        # style={"height": "400px"},
                    ),

                    # RIGHT COLUMN
                    # ============
                    dbc.Col(
                        [
                            # Adding Loading animation before map is shown
                            dcc.Loading(
                                id="loading-map",
                                type="default",
                                children=[
                                    rows.MAP_ROW(
                                        "mapbox",
                                        mapbox_modebar("company_overview"),
                                        empty_map(glb_mapbox_access_token, glb_calc_center, glb_calc_zoom),
                                    ),
                                ],
                            ),
                            html.Br(),
                            rows.LEGEND_ROW(),
                        ],
                        width=6,
                        # style={"height": "400px"},
                    ),
                ],
                style={"paddingTop": "10px"},
            ),

            # BELOW THE MAP AND SELECTIONS
            # ============================
            html.Br(),
            footer.build_footer(),
        ],
        id="data-screen",
        # style={
        #     "border-style": "solid",
        #     "height": "98vh"
        # }
    )


####################################################
# Define callbacks for the app
# https://dash.plotly.com/basic-callbacks
# https://dash.plotly.com/advanced-callbacks
####################################################

####################################################
# UPDATE FUNCTIONS GRAPHS
####################################################
# if switch is off no locations from that dataset are shown on the map
# if switch in on show locations on the map
#
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output("mapbox", "figure"),  # update the graph in mapbox section
    Output("the-datatable", "data"),  # details datatable
    Output("the-datatable-total", "data"),  # totals datatable
    Output("datatable-pre-text", "children"),  # text above datatable
    Output("isochrone-legend-col", "children"),  # add or remove / update the isochrone legend
    Output("header-subtitle", "children"),  # set value in the headers subtitle
    Output("locate-municipality", "value"),  # set value in the Select Municipality dropdown box
    Output("radio-item-selection", "value"),  # set value in the radio item of the data table
    Output("debug_header-row-center-text", "children"),  # text to show in debug row

    # Changes in (one of) these fires this callback
    # =============================================
    Input(company_selection_text + "-switch", "on"),  # use value from switch
    Input(company_selection_text + "-selection", "value"),  # use value from dropdown
    Input(municipality_type_selection_text + "-switch", "on"),  # use value from switch
    Input(municipality_type_selection_text + "-selection", "value"),  # use value from dropdown
    Input(netzknoten_selection_text + "-switch", "on"),  # use value from switch
    Input(netzknoten_selection_text + "-selection", "value"),  # use value from dropdown
    Input(prediction_selection_text + "-switch", "on"),  # use value from switch
    Input(prediction_selection_text + "-selection", "value"),  # use value from dropdown
    Input("mapbox", "clickData"),  # use data from click event
    Input("mapbox", "relayoutData"),  # use zoom value and center from mapbox update
    # https://dash.plotly.com/dash-core-components/graph
    Input("locate-municipality", "value"),
    Input("radio-item-selection", "value"),
    Input("isochrone-legend-col", "children"),  # current isochrone legend

    # Values passed without firing callback
    # =============================================
    State("mapbox", "figure"),

    # Remarks
    # =============================================
    # Input vars in function should start with i_
    # State vars in function should start with s_
    # Output vars from function should start with o_
    #
)
def update_overview(
    # Input()
    i_company_active,
    i_enterprise_list,
    i_municipality_active,
    i_municipality_list,
    i_netzknoten_active,
    i_netzknoten_list,
    i_prediction_active,
    i_prediction_list,
    i_graph_clickdata,
    i_graph_relayoutdata,
    i_selected_municipality_name,  # the name of the municipality in the selection box
    i_radio_item_selection,
    i_updated_isochrone_legend,
    # State()
    s_figure,
):

    # create as globals to store these var values
    # they should be available/updated even when this function is not executed

    # map settings
    global glb_init_calc_zoom  # initial value of map zoom
    global glb_calc_zoom  # current value of map zoom 
    global glb_init_calc_center  # initial value of map center
    global glb_calc_center  # current value of map center

    global glb_latest_municipality
    global glb_latest_lon
    global glb_latest_lat

    global glb_datatable_geojson
    # base dataframes
    global df_company, df_company_filtered
    global glb_df_netzknoten, glb_df_netzknoten_filtered
    global df_municipality, glb_df_municipality_filtered
    global df_point_on_map_filtered

    # prediction dataframes
    global df_prediction_10Km, df_prediction_20Km
    global df_prediction_10Km_filtered, df_prediction_20Km_filtered

    global glb_geojson_layers_list
    global df_selected_municipality
    global datatable_lon, datatable_lat, datatable_mun, datatable_typ

    # TODO kan weg?
    # global polygon_color

    global glb_updated_tabledata

    global glb_verbose  # generic verbose setting
    global glb_fxn_verbose  # verbose for functions

    global o_glb_selected_municipality_name  # the selected municipality name in the selection box

    if glb_fxn_verbose > 0:
        print("[INFO   ] Start function update_overview")
        
    if glb_fxn_verbose > 1:
        print("== INPUT ====================")
        print("i_company_active            :", i_company_active)
        print("i_enterprise_list           :", i_enterprise_list)
        print("i_municipality_active       :", i_municipality_active)
        print("i_municipality_list         :", i_municipality_list)
        print("i_netzknoten_active         :", i_netzknoten_active)
        print("i_netzknoten_list           :", i_netzknoten_list)
        print("i_prediction_active         :", i_prediction_active)
        print("i_prediction_list           :", i_prediction_list)
        print("i_graph_clickdata           :", i_graph_clickdata)
        print("i_graph_relayoutdata:       :", i_graph_relayoutdata)
        print("i_selected_municipality_name:", '"' + str(i_selected_municipality_name) + '"')
        print("i_radio_item_selection      :", i_radio_item_selection)
        print("i_updated_isochrone_legend  :", i_updated_isochrone_legend)
        print("== STATE ====================")
        # print("s_figure                    :", s_figure)
        print("== DONE =====================")

    o_debug_text = "[DEBUG ] Callback Triggered by: " + json.dumps(dash.callback_context.triggered) + str(i_selected_municipality_name)

    # these output vars have to have a value, so we set it to the input value
    # and if needed change it further on
    o_glb_selected_municipality_name = i_selected_municipality_name

    # o_radio_item_selection has to have a value, so we set it to the input value
    # and if needed change it further on
    o_radio_item_selection = i_radio_item_selection

    # o_updated_isochrone_legend has to have a value, so we set it to the input value
    # and if needed change it further on
    o_updated_isochrone_legend = i_updated_isochrone_legend

    # create a list of property's that changed and triggered this callback function
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered]
    if glb_fxn_verbose > 2:
        print("\nchanged_id start")
        print(changed_id)
        print("changed_id end\n")

    # zoom or move action on the map
    # then change the global vars for zoom and center
    # ==============================
    if "mapbox.relayoutData" in changed_id:
        if glb_fxn_verbose > 2:
            print(datetime.now(), "[INFO   ] Zoom or move action")
        # new center point clicked on map
        if "mapbox.center" in i_graph_relayoutdata:
            if glb_fxn_verbose > 2:
                print(datetime.now(), "[INFO   ] center changed")
                # print('mapbox.relayoutData in changed_id')
            glb_calc_center = i_graph_relayoutdata["mapbox.center"]

        # new centerpoint clicked on map or if zoom function clicked in mode bar
        if "mapbox.zoom" in i_graph_relayoutdata:
            if glb_fxn_verbose > 2:
                print(datetime.now(), "[INFO   ] zoom changed")
            glb_calc_zoom = i_graph_relayoutdata["mapbox.zoom"]

    # the municipality name in the selection box has changed
    # ======================================================
    if "locate-municipality.value" in changed_id:
        if i_selected_municipality_name is not None:  # a municipality name is selected from selection box
            if glb_fxn_verbose > 2:
                print("[INFO   ] Municipality_selection is not None")
                print("[INFO   ]", i_selected_municipality_name)

            glb_latest_municipality = i_selected_municipality_name
            # get lat and lon values for the municipality that was selected in the selection box
            glb_latest_lon = df_municipality.loc[df_municipality["uniform_city_name"] == i_selected_municipality_name]["lon"].values[0]
            glb_latest_lat = df_municipality.loc[df_municipality["uniform_city_name"] == i_selected_municipality_name]["lat"].values[0]
            if glb_fxn_verbose > 2:
                print("[INFO   ] lon:", glb_latest_lon)
                print("[INFO   ] lat:", glb_latest_lat)

            # zoom in to municipality that was selected
            glb_calc_zoom = 10  # zoom in to that point
            glb_calc_center = {  # and use that point as center of the map
                "lon": glb_latest_lon,
                "lat": glb_latest_lat,
            }

            # update the selected municipality name
            o_glb_selected_municipality_name = i_selected_municipality_name

            datatable_mun = i_selected_municipality_name
            datatable_lon = glb_latest_lon
            datatable_lat = glb_latest_lat

            # show a point on the map with only this city
            df_selected_municipality = df_baseline[
                df_baseline["uniform_city_name"].isin([i_selected_municipality_name])
            ].copy()

            # create a contour based on the radiobutton selection
            glb_datatable_geojson, glb_geojson_layers_list, o_updated_isochrone_legend = contour_graph(
                contour_type=i_radio_item_selection,
                lon=glb_latest_lon,
                lat=glb_latest_lat,
                contour_color="black",
                fxn_verbose=glb_fxn_verbose)

        else:  # locate-municipality value deselected
            # reset map to initial status / reset view
            if glb_fxn_verbose > 2:
                print("[INFO   ] Municipality_selection is None")

            glb_latest_municipality = ""
            glb_latest_lon = glb_calc_center["lon"]
            glb_latest_lat = glb_calc_center["lat"]

            datatable_lon = None
            datatable_lat = None

            glb_calc_zoom = glb_init_calc_zoom
            glb_calc_center = glb_init_calc_center
            o_glb_selected_municipality_name = ""
            o_radio_item_selection = "empty"
            datatable_mun = ""

            # don't show a point on the map
            df_selected_municipality = df_baseline[
                df_baseline["uniform_city_name"].isin([])
            ].copy()

            # reset the radiobutton for data selection
            datatable_typ = "empty"

            glb_datatable_geojson = {}  # reset the geojeson contour because no municipality selected
            glb_geojson_layers_list = []
            o_updated_isochrone_legend = []  # remove the isochrone legend

    # Value in dropdown box with companies changed
    # ======================================================
    if "company-selection.value" in changed_id:
        # filter which datapoints to show on map based on status of company switch and dropdownbox
        if i_company_active:
            # show all datapoints that are visible in i_enterprise_list
            df_company_filtered = df_company[
                df_company["enterprise"].isin(i_enterprise_list)
            ].copy()
        else:
            df_company_filtered = df_company[
                df_company["enterprise"].isin([])
            ].copy()

    # Value in dropdown box with municipality types changed
    # ======================================================
    if "municipality-type-selection.value" in changed_id:
        # filter which datapoints to show on map to show based on status of municipality switch and dropdownbox
        if i_municipality_active:
            # show all datapoints that are visible i_municipality_list
            glb_df_municipality_filtered = df_municipality[
                df_municipality["grad_der_verstädterung"].isin(i_municipality_list)
            ].copy()
        else:
            glb_df_municipality_filtered = df_municipality[
                df_municipality["grad_der_verstädterung"].isin([])
            ].copy()

    # Value in dropdown box with netzknoten changed
    # ======================================================
    if "netzknoten-selection.value" in changed_id:
        # filter which datapoints to show on map to show based on status of municipality switch and dropdownbox
        if i_netzknoten_active:
            # show all datapoints that are visible i_netknoten_list
            glb_df_netzknoten_filtered = glb_df_netzknoten[
                glb_df_netzknoten["NK_GeoStrKls"].isin(i_netzknoten_list)
            ].copy()
        else:
            glb_df_netzknoten_filtered = glb_df_netzknoten[
                glb_df_netzknoten["NK_GeoStrKls"].isin([])
            ].copy()

    # Value in dropdown box with prediction changed
    # ======================================================
    if "prediction-selection.value" in changed_id:
        # filter which datapoints to show on map to show based on status of prediction switch and dropdownbox
        if i_prediction_active:
            # filter only the predicted locations and the selections from the list
            df_prediction_10Km_filtered = df_prediction_10Km[
                (df_prediction_10Km["select_this_location_prediction"])
            ].copy()
            df_prediction_10Km_filtered = df_prediction_10Km_filtered[
                (df_prediction_10Km_filtered["prediction_type"].isin(i_prediction_list))
            ].copy()

            df_prediction_20Km_filtered = df_prediction_20Km[
                (df_prediction_20Km["select_this_location_prediction"])
            ].copy()
            df_prediction_20Km_filtered = df_prediction_20Km_filtered[
                (df_prediction_20Km_filtered["prediction_type"].isin(i_prediction_list))
            ].copy()
        else:
            df_prediction_10Km_filtered = df_prediction_10Km[
                (df_prediction_10Km["select_this_location_prediction"])
            ].copy()
            df_prediction_10Km_filtered = df_prediction_10Km_filtered[
                (df_prediction_10Km_filtered["prediction_type"].isin([]))
            ].copy()

            df_prediction_20Km_filtered = df_prediction_20Km[
                (df_prediction_20Km["select_this_location_prediction"])
            ].copy()
            df_prediction_20Km_filtered = df_prediction_20Km_filtered[
                (df_prediction_20Km_filtered["prediction_type"].isin([]))
            ].copy()

    # Value of radio button changed
    # ======================================================
    if "radio-item-selection.value" in changed_id:
        if glb_fxn_verbose > 2:
            print("radio-item-selection.value in changed_id")
        datatable_typ = i_radio_item_selection

        # zoom in to point that was clicked
        glb_calc_zoom = 10  # zoom in to that point
        if glb_fxn_verbose > 2:
            print(datatable_typ)
        # zoom out a little bit
        if datatable_typ in ["iso30", "iso20", "bbox20", "circle20"]:
            if glb_fxn_verbose > 2:
                print("changing glb_calc_zoom")
            glb_calc_zoom = 9

        if i_selected_municipality_name is not None and i_selected_municipality_name != "":
            # create a contour based on the radiobutton selection
            glb_datatable_geojson, glb_geojson_layers_list, o_updated_isochrone_legend = contour_graph(
                contour_type=i_radio_item_selection,
                lon=glb_latest_lon,   # I have to check if there is always a value
                lat=glb_latest_lat,
                contour_color="black",
                fxn_verbose=glb_fxn_verbose)
        else:
            glb_calc_zoom = glb_init_calc_zoom

    # Clicked somewhere om the map
    # ======================================================
    if 'mapbox.clickData' in changed_id:
        if glb_fxn_verbose > 2:
            print("mapbox.clickData in changed_id")

        glb_latest_lon = i_graph_clickdata["points"][0]["lon"]
        glb_latest_lat = i_graph_clickdata["points"][0]["lat"]

        # zoom in to point that was clicked
        glb_calc_zoom = 10  # zoom in to that point
        if datatable_typ in ["iso30", "iso20", "bbox20", "circle20"]:
            if glb_verbose:
                print("changing calc zoom")
            glb_calc_zoom = 9

        glb_calc_center = {  # and use that point as center of the map
            "lon": glb_latest_lon,
            "lat": glb_latest_lat,
        }

        # find which curve was clicked we
        # https://community.plotly.com/t/get-trace-name-from-clickdata/18406/3
        #
        curve_number = i_graph_clickdata["points"][0]["curveNumber"]
        curve_name = s_figure["data"][curve_number]["name"]

        if glb_fxn_verbose > 2:
            print("Point on curve: " + str(curve_number))
            print("Point on curve: " + curve_name)

        # check if location was clicked in one of the relevant curves
        # if so, create the polygon that was selected by the radio button
        if curve_name in [
            "Municipality",
            "SelectedMunicipality",
            "in-contour",
            "dicht besiedelt",
            "dicht besiedelt-Kreissitz",
            "mittlere Besiedlungsdichte",
            "mittlere Besiedlungsdichte-Kreissitz",
            "gering besiedelt",
            "gering besiedelt-Kreissitz",
            "Company",
            "_10Km_combined_prediction_df",
            "_20Km_combined_prediction_df",
            "selected location"
        ]:
            glb_datatable_geojson, glb_geojson_layers_list, o_updated_isochrone_legend = contour_graph(
                contour_type=i_radio_item_selection,
                lon=glb_latest_lon,   # I have to check if there is always a value
                lat=glb_latest_lat,
                contour_color="black",
                fxn_verbose=glb_fxn_verbose)

        # When point clicked is on Municipality Curves
        if curve_name in [
            "Municipality",
            "SelectedMunicipality",
            "dicht besiedelt",
            "dicht besiedelt-Kreissitz",
            "mittlere Besiedlungsdichte",
            "mittlere Besiedlungsdichte-Kreissitz",
            "gering besiedelt",
            "gering besiedelt-Kreissitz",
        ]:
            glb_latest_municipality = i_graph_clickdata["points"][0]["customdata"]

        # When point clicked is on Company Curves
        if curve_name in ["Company"]:
            glb_latest_municipality = i_graph_clickdata["points"][0]["customdata"]

        # When point clicked is on Prediction Curves
        if curve_name in [
            "_10Km_combined_prediction_df",
            "_20Km_combined_prediction_df",
        ]:
            glb_latest_municipality = i_graph_clickdata["points"][0]["customdata"]

        datatable_lon = glb_latest_lon
        datatable_lat = glb_latest_lat
        datatable_mun = glb_latest_municipality
        o_glb_selected_municipality_name = glb_latest_municipality

    # select the point data for the point on the map that is currently selected
    df_point_on_map_filtered = df_municipality[
        df_municipality["uniform_city_name"].isin([o_glb_selected_municipality_name])
    ].copy()

    # update the datatable
    o_updated_tabledata, o_updated_tabledata_total = select_datatable_subset(
        df_baseline,
        datatable_lon,
        datatable_lat,
        glb_datatable_geojson,
        datatable_mun,
        datatable_typ,
        glb_fxn_verbose
    )
    glb_updated_tabledata = o_updated_tabledata.copy()

    if glb_verbose:
        print(o_updated_tabledata)
        print("UPDATED_GEO_FIG")

    if o_glb_selected_municipality_name != "":
        o_datatable_pre_text = "Showing data in table below for " + o_glb_selected_municipality_name
    else:
        o_datatable_pre_text = "Show data for selected municipality in table"

    return (
        update_overall_map(
            the_zoom=glb_calc_zoom,
            the_center=glb_calc_center,
            fxn_verbose=glb_fxn_verbose
        ),
        o_updated_tabledata.to_dict("records"),
        o_updated_tabledata_total.to_dict("records"),
        o_datatable_pre_text,
        o_updated_isochrone_legend,
        o_glb_selected_municipality_name,
        o_glb_selected_municipality_name,
        o_radio_item_selection,
        o_debug_text
    )


####################################################
# enabling company selection dropdown based on status switch
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output(company_selection_text + "-selection", "disabled"),  # enable/disable dropdownbox functionality
    Output("company-legend-col", "children"),

    # Changes in (one of) these fires this callback
    # =============================================
    Input(company_selection_text + "-switch", "on"),  # use value from switch
    Input(company_selection_text + "-selection", "value")

    # Remarks
    # =============================================
    # Input vars in function should start with i_
    # State vars in function should start with s_
    # Output vars from function should start with o_
    #
)
def status_company_selection(
        # Input()
        i_switch_val,
        i_selection_val
        # State()
):
    if not i_switch_val:  # disabled the selection options trough switch
        o_switch_set = True
    else:  # enabled the selection options
        o_switch_set = False

    if len(i_selection_val) == 0:  # empty selection text
        o_legend_text = []
    else:  # some selections made
        o_legend_text = [
            html.Div(["COMMERCIAL POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Mc Donalds"], style={"color": "red", "marginRight": "10px"}),
            html.Div(["Burger King"], style={"color": "blue", "marginRight": "10px"}),
            html.Div(["KFC"], style={"color": "green", "marginRight": "10px"}),
            html.Div(["McFIT"], style={"color": "orange", "marginRight": "10px"}),
        ]

    return o_switch_set, o_legend_text


####################################################
# enabling municipality selection dropdown based on status switch
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output(municipality_type_selection_text + "-selection", "disabled"),  # enable/disable dropdownbox functionality
    Output("municipality-legend-col", "children"),

    # Changes in (one of) these fires this callback
    # =============================================
    Input(municipality_type_selection_text + "-switch", "on"),  # use value from switch
    Input(municipality_type_selection_text + "-selection", "value")

    # Remarks
    # =============================================
    # Input vars in function should start with i_
    # State vars in function should start with s_
    # Output vars from function should start with o_
    #
)
def status_municipality_selection(
        # Input()
        i_switch_val,
        i_selection_val
        # State()
):
    if not i_switch_val:  # disabled the selection options trough switch
        o_switch_set = True
    else:  # enabled the selection options
        o_switch_set = False

    if len(i_selection_val) == 0:  # empty selection text
        o_legend_text = []
    else:  # some selections made
        o_legend_text = [
            html.Div(["MUNICIPALITY POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["Gemeinde"], style={"color": "black", "marginRight": "10px"}),
            html.Div(["Kreissitz gemeinde"], style={"color": "purple", "marginRight": "10px"}),
        ]

    return o_switch_set, o_legend_text


####################################################
# enabling netzknoten selection dropdown based on status switch
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output(netzknoten_selection_text + "-selection", "disabled"),  # enable/disable dropdownbox functionality

    # Changes in (one of) these fires this callback
    # =============================================
    Input(netzknoten_selection_text + "-switch", "on"),  # use value from switch

    # Remarks
    # =============================================
    # Input vars in function should start with i_
    # State vars in function should start with s_
    # Output vars from function should start with o_
    #
)
def status_netzknoten_selection(
        # Input()
        i_switch_val
        # State()
):
    if not i_switch_val:  # disabled the selection options trough switch
        o_switch_set = True
    else:  # enabled the selection options
        o_switch_set = False

    return o_switch_set


####################################################
# enabling prediction selection dropdown based on status switch
####################################################
@app.callback(
    # Where the results of the function end up
    # =======================================
    Output("prediction-selection", "disabled"),  # enable/disable dropdownbox functionality
    Output("prediction-legend-col", "children"),

    # Changes in (one of) these fires this callback
    # =============================================
    Input("prediction-switch", "on"),  # use value from switch
    Input("prediction-selection", "value")

    # Remarks
    # =============================================
    # Input vars in function should start with i_
    # State vars in function should start with s_
    # Output vars from function should start with o_
    #
)
def status_prediction_selection(
        # Input()
        i_switch_val,
        i_selection_val
        # State()
):
    if not i_switch_val:  # disabled the selection options trough switch
        o_switch_set = True
    else:  # enabled the selection options
        o_switch_set = False

    if len(i_selection_val) == 0:  # empty selection text
        o_legend_text = []
    else:  # some selections made
        o_legend_text = [
            html.Div(["PREDICTION POINTS:"], style={"fontWeight": "bold", "color": "black", "marginRight": "10px"}),
            html.Div(["10 Km / Min Zone"], style={"color": "cyan", "marginRight": "10px"}),
            html.Div(["20 Km / Min Zone"], style={"color": "fuchsia", "marginRight": "10px"}),
        ]

    return o_switch_set, o_legend_text


####################################################
# START THE APP
####################################################
if __name__ == "__main__":
    print("Running on     : " + the_hostname)
    print("Run on env var : " + run_on)
    print("App version    : " + app_version)
    print("Python version : " + python_version)
    print("dash version   : " + dash_version)
    print("plotly version : " + plotly_version)

    # #################################
    # depending on where code is running
    # should be optimized in final version
    # #################################

    # Raspberry Pi on Local network
    if the_hostname == "rpi4-18 ":
        app.run_server(host="192.168.2.18", port=8050, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

    # EC2 instance on AWS
    elif the_hostname == "ip-10-0-1-5":
        app.run_server(host="10.0.1.5", port=8050, debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

    # local development machine
    elif the_hostname == "LEGION-2020":
        app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

    # on Heroku
    else:
        app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
