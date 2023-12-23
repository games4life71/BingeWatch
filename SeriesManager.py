import json
from YoutubeSearcher import search_youtube
from APICaller import get_by_id_request


class SeriesManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, imdb_link, score):
        # TODO check if the link is valid
        # TODO check if the score is valid
        # TODO check if the series is already in the database
        # TODO add the series to the database
        print("Adding the series: " + imdb_link)
        response = get_by_id_request(imdb_link)
        # TODO check if the response is valid (if the series exists)
        # add it to the database
        try:
            id = response["series_id"]
            series_name = response["series_name"]
            # save the response in a json file

            with open("episode1.json", "w") as f:
                json.dump(response["episodes"][0], f)

            self.cursor.execute("INSERT INTO "
                                "Series(SeriesID,SeriesName,IMDBLink, Score) "
                                "VALUES (?,?,?,?)",
                                (id,
                                 series_name,
                                 imdb_link,
                                 score))

            self.connection.commit()



        except Exception as e:
            print("Error while adding the series to the database...\n " + str(e))
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
                    print("Error while adding the episode to the database...\n " + str(e))

        # print the number of episodes in total
        return "succes", id, series_name

    def update_watched_episodes(self, name, season, episode):
        # update into series
        # TODO check if the series is in the database

        try:
            self.cursor.execute("UPDATE Series SET "
                                "LastEpisode = ?, LastSeason = ?"
                                " WHERE SeriesName = ?",
                                (episode, season, name))
            self.connection.commit()


        except Exception as e:
            print("Error while updating the series...\n " + str(e))
            return "Exception"

    def remove(self, name):
        # TODO check if the series is in the database
        # TODO remove the series from the database
        pass

    def update(self, name, score):
        # TODO check if the series is in the database
        # TODO check if the score is valid
        # TODO update the score of the series
        pass

    def get_all(self):
        # TODO get all the series from the database
        try:
            self.cursor.execute("SELECT * FROM Series")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error while getting all the series...\n " + str(e))
            return "Exception"

    def get_by_name(self, name):
        # TODO get the series by name
        try:
            self.cursor.execute("SELECT * FROM Series WHERE SeriesName LIKE ?", (name + "%",))
            return self.cursor.fetchall()
        except Exception as e:
            print("Error while getting the series by name...\n " + str(e))
            return "Exception"

    def parse_imdb_link(self, imdb_link):
        # TODO parse the imdb link and get the id
        # https://www.imdb.com/title/tt0068646/?ref_=hm_tpks_tt_i_2_pd_tp1_pbr_ic
        # extract the id from the link
        series_id = imdb_link.split("/")[4]
        print(series_id)
        return series_id

    def snooze(self, name, snooze):
        # TODO check if the series is in the database
        # TODO snooze the series
        try:

            self.connection.execute("UPDATE Series "
                                    "SET Snoozed = ? WHERE SeriesID = ?", (snooze, name))
            self.connection.commit()
        except Exception as e:
            print("Error while snoozing the series...\n " + str(e))
            return "Exception"

    def list_unwatched(self):
        #TODO update the episodes for each series(check if there are new episodes)

        try:
            self.cursor.execute("SELECT * FROM Series WHERE Snoozed = 0 ORDER BY Score DESC ")
            series_unsnoozed = self.cursor.fetchall()

            for series in series_unsnoozed:
                print("Updates from" + series[1] + ":" )
                print("Last episode watched: " + str(series[5]) + " from season " + str(series[6]))
                #check if there are new episodes
                new_episodes = self.cursor.execute("SELECT * FROM Episode WHERE SeriesID = ? AND SeasonNumber >= ? "
                                                   "AND EpisodeNumber > ?",
                                    (series[0], series[6], series[5]))
                for episode in new_episodes:
                    print("New episode: " + episode[1]+"(ep:"+str(episode[4])+")" + " from season " + str(episode[5]))
                #TODO update the search on youtube query
                query = "trailer " + series[1]
                results = search_youtube(query)
                for result in results:
                    print("Youtube link: " + result)
            #search on youtube for the series

        except Exception as e:
            print("Error while getting all the series...\n " + str(e))
            return "Exception"
