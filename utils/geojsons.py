# basic modules
import json

import certifi
# https modules
import urllib3
# data wrangling modules
from numpy import cos, linspace, pi, sin


def boundingbox_and_geojson(
    center_lon, center_lat, r=0.1, bboxcolor="purple", verbose=False
):
    """
    lon:       lon of center of bbox
    lat:       lat of center of bbox
    r:         baseline distance (10km = 0.1)
    bboxcolor: color of line
    """

    lon_min = center_lon + r * -1
    lon_max = center_lon + r * 1
    lat_min = center_lat + r * -1
    lat_max = center_lat + r * 1

    coords_list = [
        [lon_min, lat_min],  # top left
        [lon_min, lat_max],  # bottom left
        [lon_max, lat_max],  # bottom right
        [lon_max, lat_min],  # top right
        [lon_min, lat_min],  # top left
    ]

    geojson = {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords_list]},
    }

    bbox_dict = dict(
        sourcetype="geojson",
        source=geojson,
        color=bboxcolor,
        opacity=0.8,
        #            type='fill',
        type="line",
        below="mapbox",
    )

    if verbose:
        print(bbox_dict)

    bbox_list = [bbox_dict]
    return bbox_list, geojson


def circle_and_geojson(center_lon, center_lat, r=0.1, color="red", verbose=False):
    """
    center_lon: lon of center of bbox
    center_lat: lat of center of bbox
    r:          baseline distance (10km = 0.1)
    color: color of line
    """

    #    r = 0.75
    #    r = 0.1  # r = 100 meters
    t = linspace(0, 2 * pi, 100)
    circle_lon = center_lon + r * cos(t)
    circle_lat = center_lat + r * sin(t)

    coords = []
    for lo, la in zip(list(circle_lon), list(circle_lat)):
        coords.append([lo, la])

    geojson = {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
    }

    if verbose:
        print("geojson_dict")
        print(geojson)

    circle_layer_dict = dict(
        sourcetype="geojson",
        source=geojson,
        color=color,
        opacity=0.8,
        # type='fill',
        type="line",
        below="mapbox",
    )
    if verbose:
        print(circle_layer_dict)

    circle_layer_list = [circle_layer_dict]
    return circle_layer_list, geojson


def isochrone_and_geojson(
    lon_point,
    lat_point,
    polygontype_str,
    profile_str,
    minutes_str,
    hex_colors_str,
    mapbox_access_token,
    verbose=False,
):
    # https://api.mapbox.com/isochrone/v1/mapbox/driving/-118.22258,33.99038?contours_minutes=5,10,15&contours_colors=6706ce,04e813,4286f4&polygons=true&access_token=pk.eyJ1IjoicGllcnJldmVlbGVuIiwiYSI6ImNra3V6Z2JhNTFjeXUycHBjdWVkOXUxdDMifQ.tzOHbTKha9Co8-s_AarPJg
    if polygontype_str == "fill":
        opacity = 0.3
    else:
        opacity = 0.5

    # either 'driving' 'cycling' 'walking'
    if profile_str == "car":
        profile = "driving"
    elif profile_str == "bike":
        profile = "cycling"
    elif profile_str == "walk":
        profile = "walking"
    else:
        profile = "driving"

    url = (
        "https://api.mapbox.com/isochrone/v1/mapbox/"
        + profile
        + "/"
        + str(lon_point)
        + ","
        + str(lat_point)
    )
    contours_minutes = minutes_str

    polygons = "true"
    access_token = mapbox_access_token
    contours_colors = hex_colors_str

    payload = {
        "contours_minutes": contours_minutes,
        "contours_colors": contours_colors,
        "polygons": polygons,
        "access_token": access_token,
    }

    if verbose:
        print(url)
        print(payload)

    https = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    response = https.request(
        "GET",
        url,
        fields=payload,
        retries=urllib3.Retry(total=40, status=40, redirect=40),
    )

    if verbose:
        print(dir(response))
        print("geturl")
        print(response.geturl())
        print("header")
        print(response.getheaders())
        print("get_redirect_location")
        print(response.get_redirect_location())
        print(json.loads(response.data.decode()))

    features_dict = json.loads(response.data.decode())

    if verbose:
        print("============ features_dict ===============")
        print(features_dict)
        print("============ features_dict ===============")

    contours_list = []
    featurecount = 0

    if verbose:
        print(len(features_dict["features"]))
    for feature in features_dict["features"]:
        geojson = {
            "type": "Feature",
            "geometry": feature["geometry"],
        }
        # https://plotly.com/python/reference/layout/mapbox/#layout-mapbox-layers
        contours_list = contours_list + [
            dict(
                sourcetype="geojson",
                source=geojson,
                color=feature["properties"]["color"],
                #                opacity=feature['properties']['opacity'],
                opacity=opacity,
                # https://plotly.com/python/reference/layout/mapbox/#layout-mapbox-layers-items-layer-type
                # polygontype is "fill" or "line"
                type=polygontype_str,
                line={"width": 2},
                # below="mapbox",
                below="",
            )
        ]
        featurecount = featurecount + 1

        if verbose:
            print("number of features : " + str(featurecount))

    if verbose:
        print(contours_list)

    # output should be a list
    return contours_list, geojson
