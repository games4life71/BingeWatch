# this file is used to call the API and get the data from the API

import requests

bearer = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YTI3MWU2MmEyZDUzYjE3NGRkYzk5M2I4ZDhjNWQ3NCIsInN1YiI6IjY1NzM2ZWVkMDA2YjAxMDBjNDM0OTQyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XxK46FWA3Hel7-M71b1G2Pco2QXtS6XUnH0kP_AUT-Y"


def get_by_id_request(id):
    # get the if based on the imdb id
    url = "https://api.themoviedb.org/3/find/"
    url += id
    url += "?external_source=imdb_id"
    api_response = dict()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + bearer
    }
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return "Exception"

    # for each season get the number of episodes and info
    db_id = response.json()["tv_results"][0]["id"]
    series_name = response.json()["tv_results"][0]["name"]
    api_response["series_name"] = series_name
    api_response["series_id"] = db_id
    api_response["episodes"] = []
    # make a call to get the number of seasons

    try:
        url = "https://api.themoviedb.org/3/tv/" + str(db_id)
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return "Exception"
    seasons_number = response.json()["number_of_seasons"]
    # for each season make a call
    for i in range(0, seasons_number):
        try:
            url = "https://api.themoviedb.org/3/tv/" + str(db_id) + "/season/" + str(i + 1)
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return "Exception"
        api_response["episodes"].append(response.json()["episodes"])
    return api_response

