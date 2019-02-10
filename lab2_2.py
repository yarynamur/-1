import folium
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


def sort_movies(file):
    """
    () -> lst
    Makes list of movies, years and locations from file 'locations.list'
    e.g.
    [['2006', 'Los Angeles, California, USA']]
    """
    with open(file, encoding='utf-8', errors='ignore') as f:
        lines = f.read().split('\n')[14:-2]
    lst = []
    for line in lines:
        line = line.split('\t')
        line[0] = line[0].split(' (')
        if '(' not in line[-1]:
            new_line = [line[0][1][:4], line[-1]]
            lst.append(new_line)
        else:
            new_line = [line[0][1][:4], line[-2]]
            lst.append(new_line)
    return lst


def sort_year(year):
    """
    (int) -> lst
    Creates a list of locations made in given year
    >>> sort_year(1890)
    (["Trafalgar Square, St James's, London, England, UK"], [51.508037], [-0.128049410707247])
    """
    location_list = []
    latitude_list = []
    longitude_list = []
    geolocator = Nominatim(user_agent="name", timeout=None, scheme='http')
    geocode = RateLimiter(geolocator.geocode, error_wait_seconds=5.0,
                          max_retries=0, swallow_exceptions=False, return_value_on_exception=True)
    for movie in sort_movies('locations.list.txt'):
        if movie[0] == str(year):
            location = geolocator.geocode(movie[1])
            if location != None:
                location_list.append(movie[1])
                latitude_list.append(location.latitude)
                longitude_list.append(location.longitude)
    return location_list, latitude_list, longitude_list


def create_map(year):
    """
    Creates map with location of movies of given year and colors of countries population
    >>> create_map(2015)
    """
    movies = sort_year(year)[0]
    lat = sort_year(year)[1]
    lon = sort_year(year)[2]

    map = folium.Map(zoom_start=10)
    fg_hc = folium.FeatureGroup(name="Movies Locations")
    for lt, ln, mv in zip(lat, lon, movies):
        fg_hc.add_child(folium.CircleMarker(location=[
                        lt, ln], radius=5, popup=mv, fill_color='red', color='red', fill_opacity=1))
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                   style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                             else 'red'}))
    map.add_child(fg_hc)
    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())
    map.save('Map.html')


if __name__ == '__main__':
    year = int(input())
    create_map(year)
