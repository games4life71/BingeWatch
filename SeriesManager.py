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
        response = get_by_id_request(imdb_link)
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
            print("Error while adding the series to the database...\n " + str(e))
        for season in response["episodes"]:
            for episode in season:

                print(episode["name"])
        #print the number of episodes in total
        print("Number of episodes: " + str(len(response["episodes"])))
        return 1
        pass

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

        pass
