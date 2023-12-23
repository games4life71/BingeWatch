import json

from youtube_search import YoutubeSearch


def search_youtube(query):
    results = YoutubeSearch(query+"trailer", max_results=3).to_dict()
    links = []
    for result in results:
        links.append("https://www.youtube.com" + result["url_suffix"])

    return links

