from numpy import array, interp


# simplified version of
# https://stackoverflow.com/questions/63787612/plotly-automatic-zooming-for-mapbox-maps
#
def zoom_center(lons, lats, width_to_height: float = 2.0) -> (float, dict):
    """
    lons:            list of lons`
    lats:            list of lats
    width_to_height: 
    """
    maxlon, minlon = max(lons), min(lons)
    maxlat, minlat = max(lats), min(lats)
    center = {
        "lon": round((maxlon + minlon) / 2, 6),
        "lat": round((maxlat + minlat) / 2, 6),
    }

    # longitudinal range by zoom level (20 to 1)
    # in degrees, if centered at equator
    lon_zoom_range = array(
        [
            0.0007,
            0.0014,
            0.003,
            0.006,
            0.012,
            0.024,
            0.048,
            0.096,
            0.192,
            0.3712,
            0.768,
            1.536,
            3.072,
            6.144,
            11.8784,
            23.7568,
            47.5136,
            98.304,
            190.0544,
            360.0,
        ]
    )

    margin = 1.2
    height = (maxlat - minlat) * margin * width_to_height
    width = (maxlon - minlon) * margin
    lon_zoom = interp(width, lon_zoom_range, range(20, 0, -1))
    lat_zoom = interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)

    return zoom, center
