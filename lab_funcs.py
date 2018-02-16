import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
import os
import geocoder

def json_create(acct):
    # https://apps.twitter.com/
    # Create App and get the four strings, put them in hidden.py
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    if (len(acct) < 1):
        return None
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '200'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    with open('data.json', 'w') as outfile:
        json.dump(js, outfile, indent=2)


def get_dict(path):

    res = dict()
    data = json.load(open(path))
    for i in data['users']:
        if i['location'] in res:
            res[i['location']] += [i['name']]
        else:
            res[i['location']] = [i['name']]

    return res


def map_b(data):


    my_map = folium.Map(location=[48.314775, 25.082925], zoom_start=2)
    for location in data:
        if location != '':
            coordinates = get_loc_google(location)
            if coordinates != None:
                tag_names = ""
                for name in data[location]:
                    tag_names += name + ', '
                my_map.add_child(folium.Marker(location=coordinates,
                                       popup=tag_names, icon=folium.Icon()))
    my_map.save("templates/Res_Map.html")


def get_loc_google(name_loc):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyA0iKNhAY6kSCOipNdASgDwx1CQXNVB9M0"
    geo = geocoder.google(name_loc)
    latlong = geo.latlng
    if latlong:
        return latlong
    else:
        print("Location not found: ", name_loc)
        return None
