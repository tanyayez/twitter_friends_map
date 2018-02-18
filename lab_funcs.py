import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
import os
import geocoder


def json_create(acct):
    '''
    str -> None
    This program creates a json file with infon about given account`s friends
    :param acct: string a name of twitter account
    :return: None
    '''

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


def get_dict(lst):
    '''(list) ->  dict
    This function from the given list of lists where every list consists of two
    items creates a dictionary
    with keys as first item and value as list of second items for the same key
    :param lst: a list that consists of lists of two items
    :return: dictionary with first items of the contained lists as keys and
    list of second items as values
    '''

    res = dict()
    for i in lst:
        if i[1] in res:
            res[i[1]] += [i[0]]
        else:
            res[i[1]] = [i[0]]
    return res


def map_b(data):
    '''
    dict -> None
    This fuction creates a map with marked people`s(names) locations
    :param data: dictionary with names(str) as keys and lists of
    locations(strings) as value
    :return: None
    '''

    my_map = folium.Map(location=[48.314775, 25.082925], zoom_start=2)
    folium.TileLayer('stamenterrain').add_to(my_map)
    for location in data:
        if location != '':
            coordinates = get_loc_google(location)
            if coordinates is not None:
                tag_names = ""
                for name in data[location]:
                    tag_names += name + ', '
                my_map.add_child(folium.Marker(location=coordinates,
                                               popup=tag_names,
                                               icon=folium.Icon()))
    my_map.save("templates/Res_Map.html")


def get_loc_google(name_loc):
    '''
    str -> list
    This function returns list of two integer that represent coordinates gotten
    from Google
    :param name_loc: string representing location
    :return: list of two coordinates represented by integers
    '''

    os.environ["GOOGLE_API_KEY"] = "AIzaSyA0iKNhAY6kSCOipNdASgDwx1CQXNVB9M0"
    geo = geocoder.google(name_loc)
    latlong = geo.latlng
    if latlong:
        return latlong
    else:
        print("Location not found: ", name_loc)
        return None


def json_read_new(path, lst):
    '''
    (str, list) -> list
    This function from  given json file forms a list of lists where each list
    include values by given key
    :param path: a path to the json file to be read
    :param lst: list that consist of key words(keys of dictionaries of the list
    that is value from key users) in json file, info from which
    should be returned
    :return: a list of lists that include info by given keys
    prediction: keys in list should be among the elements of variable keys
    in this function
    '''

    res = []
    data = json.load(open(path))
    keys = ["id", "id_str", "name", "screen_name", "location", "description",
            "url", "entities",  "protected", "followers_count",
            "listed_count", "created_at", "favourites_count", "utc_offset",
            "time_zone", "geo_enabled", "verified", "statuses_count", "lang",
            "contributors_enabled", "is_translator", "is_translation_enabled",
            "profile_background_color", "profile_background_image_url",
            "profile_background_image_url_https", "profile_background_tile",
            "profile_image_url", "profile_image_url_https",
            "profile_banner_url", "profile_link_color",
            "profile_sidebar_border_color", "profile_sidebar_fill_color",
            "profile_text_color", "profile_use_background_image",
            "has_extended_profile", "default_profile", "default_profile_image",
            "following", "live_following", "follow_request_sent",
            "notifications", "muting", "blocking", "blocked_by",
            "translator_type", "friends_count"]
    for key in lst:
        if key not in keys:
            print("Wrong key name: ", key)
            return None

    for i in data['users']:
        a = []
        for key in lst:
            a.append(i[key])
        res.append(a)
    return res
