import json
from YoutubeSearcher import search_youtube
from APICaller import get_by_id_request

"""
This function parses the imdb link and returns the id of the series,
id that will be used to fetch the series from the api(TMDB)
"""


def parse_imdb_link(imdb_link):
    # https://www.imdb.com/title/tt0068646/?ref_=hm_tpks_tt_i_2_pd_tp1_pbr_ic
    # extract the id from the link
    series_id = imdb_link.split("/")[4]
    # print(series_id)
    return series_id


"""
This class defines the functions that will be used to manage the series in the database
It mostly uses the APICaller to fetch the series from the api and then add it to the database,
update or remove it
"""


class SeriesManager:
    def __init__(self, connection, logger):
        self.connection = connection
        self.logger = logger
        self.cursor = connection.cursor()

    """
    This function adds the series to the database, it uses the APICaller to fetch the series from the api,
    along with the episodes and then adds them to the database with the score given by the user and the imdb link
    """

    def add(self, trimmed_id, score, imdb_link):

        response = get_by_id_request(trimmed_id)
        # TODO check if the response is valid (if the series exists)
        # add it to the database
        try:
            id = response["series_id"]
            series_name = response["series_name"]
            self.cursor.execute("INSERT INTO "
                                "Series(SeriesID,SeriesName,IMDBLink, Score) "
                                "VALUES (?,?,?,?)",
                                (id,
                                 series_name,
                                 imdb_link,
                                 score))
            self.connection.commit()

        except Exception as e:
            # print("Error while adding the series to the database...\n " + str(e))
            self.logger.log("[ERROR]: fetching the response " + str(e))
        for season in response["episodes"]:
            for episode in season:
                # print(episode["name"])
                # add the episode to the database
                try:
                    self.cursor.execute(
                        "INSERT INTO " "Episode(EpisodeID,EpisodeName,SeriesID,EpisodeNumber,SeasonNumber)"
                        "VALUES (?,?,?,?,?)",
                        (episode["id"],
                         episode["name"],
                         id,
                         episode["episode_number"],
                         episode["season_number"]))
                    self.connection.commit()
                except Exception as e:

                    self.logger.log(
                        "[ERROR]: adding a series/episode failed (it's possible it already exists)" + str(e))

        # print the number of episodes in total
        return "succes", id, series_name

    """
    This function updates the watched episodes of the series in the database with the new ones
    """

    def update_watched_episodes(self, name, season, episode):
        # update into series


        try:
            self.cursor.execute("UPDATE Series SET "
                                "LastEpisode = ?, LastSeason = ? ,date = CURRENT_TIMESTAMP "
                                " WHERE SeriesName = ?",
                                (episode, season, name))
            self.connection.commit()


        except Exception as e:
            self.logger.log("[ERROR]: updating the series  didn't work" + str(e))

    """
    This function removes the series from the database along with the episodes from the series
    It search based on the name of the series and then asks the user to choose the series he wants to delete
    """

    def remove(self, name):
        # TODO check if the series is in the database
        # TODO remove the series from the database
        try:
            # get all the matching series from the database
            series = self.cursor.execute("SELECT * FROM Series WHERE SeriesName LIKE ?", (name + "%",))
            series = series.fetchall()
            print("Choose the series you want to delete: ")
            series_selected = None
            for index, serie in enumerate(series):
                # delete all the episodes from the series
                print(serie[1] + " (" + str(index + 1) + ")")
            option = input("Enter the option number:")
            series_selected = series[int(option) - 1]
            self.cursor.execute("DELETE FROM Episode WHERE SeriesID = ?", (series_selected[0],))
            self.cursor.execute("DELETE FROM Series WHERE SeriesID = ?", (series_selected[0],))
            self.connection.commit()
            print("Series deleted successfully")
        except Exception as e:
            self.logger.log("[ERROR]: deleting the series  didn't work" + str(e))

        pass

    """
    This function adds the series to the database without asking the user for input
    <Currently not used>
    """

    def silent_fetch(self, imdb_link, score):
        try:
            self.add(imdb_link, score)
        except Exception as e:
            self.logger.log("[ERROR]: silent fetch failed" + str(e))
            pass

    """
    This function gets all the series from the database along with the episodes
    """

    def get_all(self):
        # TODO get all the series from the database
        try:
            self.cursor.execute("SELECT * FROM Series")
            return self.cursor.fetchall()
        except Exception as e:
            # print("Error while getting all the series...\n " + str(e))
            # return "Exception"
            self.logger.log("[ERROR]: getting all the series failed" + str(e))

    """
    This pretty much does the same thing as get_all, but it gets the series by name xD
    """

    def get_by_name(self, name):
        # TODO get the series by name
        try:
            self.cursor.execute("SELECT * FROM Series WHERE SeriesName LIKE ?", (name + "%",))
            return self.cursor.fetchall()
        except Exception as e:
            # print("Error while getting the series by name...\n " + str(e))
            # return "Exception"
            self.logger.log("[ERROR]: getting the series by name failed" + str(e))

    """
    This function snoozes the series, it sets the snoozed field to 1 
    """

    def snooze(self, name, snooze):
        try:

            self.connection.execute("UPDATE Series "
                                    "SET Snoozed = ? WHERE SeriesID = ?", (snooze, name))
            self.connection.commit()
        except Exception as e:
            # print("Error while snoozing the series...\n " + str(e))
            # return "Exception"
            self.logger.log("[ERROR]: snoozing the series failed" + str(e))

    """
    This function lists all the unwatched episodes from all the series
    Before displaying the unwatched episodes, it fetches the new episodes from the api
    It also searches on youtube for the new updates trailer on youtube with search_youtube(query)
    """

    def list_unwatched(self):
        try:
            # fetch the updates

            self.cursor.execute("SELECT * FROM Series WHERE Snoozed = 0 ORDER BY Score DESC ")
            series_unsnoozed = self.cursor.fetchall()

            for series in series_unsnoozed:
                print("Updates from " + series[1] + ":")
                print("Last episode watched: " + str(series[5]) + " from season " + str(series[6]))
                parsed_id = parse_imdb_link(str(series[2]))

                # update the series with the new episodes
                self.add(parsed_id, series[3],
                         series[2])  # this will update the series with the new episodes if there are any

                new_episodes = self.cursor.execute("SELECT * FROM Episode WHERE SeriesID = ? AND SeasonNumber >= ? "
                                                   "AND EpisodeNumber > ?",
                                                   (series[0], series[6], series[5]))

                for episode in new_episodes:
                    print("New episode: " + episode[1] + "(ep:" + str(episode[4]) + ")" + " from season " + str(
                        episode[5]))
                # TODO update the search on youtube query
                query = "trailer " + series[1]
                results = search_youtube(query)
                for result in results:
                    print("Youtube link: " + result)
                print("\n")
            # search on youtube for the series

        except Exception as e:
            # print("Error while getting all the series...\n " + str(e))
            # return "Exception"
            self.logger.log("[ERROR]: listing the unwatched episodes failed..." + str(e))

    def update_score(self, name, score):
        try:
            self.cursor.execute("UPDATE Series SET Score = ? WHERE SeriesName = ?", (score, name))
            self.connection.commit()
        except Exception as e:
            self.logger.log("[ERROR]: updating the score failed..." + str(e))

    def show_updates(self, series):
        print("IMDB link is " + str(series[2]))
        parsed_id = parse_imdb_link(str(series[2]))

        # update the series with the new episodes
        self.add(parsed_id, series[3], series[2])
        new_episodes = self.cursor.execute("SELECT * FROM Episode WHERE SeriesID = ? AND SeasonNumber >= ? "
                                           "AND EpisodeNumber > ?",
                                           (series[0], series[6], series[5]))
        print("Updates from " + series[1] + ":")
        for episode in new_episodes:
            print("New episode: " + episode[1] + "(ep:" + str(episode[4]) + ")" + " from season " + str(episode[5]))
        # TODO update the search on youtube query
        query = "trailer " + series[1]
        results = search_youtube(query)
        for result in results:
            print("Youtube link: " + result)

    """
    Searches for updates of a series episode on youtube
    """
    def get_trailer(self,seriesName,season, episode):
        return  search_youtube(seriesName + " season " + str(season) + " episode " + str(episode))



