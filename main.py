from DatabaseConnection import DatabaseConnection
import argparse
import SeriesManager
import argparse_range

# connect to database

db_instance = DatabaseConnection("C:\\Users\\stefy\\Desktop\\sqlite-tools-win-x64-3440200\\BingeWatch.db")
connection = db_instance.connect()

cursor = connection.cursor()
series_manager = SeriesManager.SeriesManager(connection)

parser = argparse.ArgumentParser(description='BingeWatch')
# parse arguments

parser.add_argument('-A', '--add', nargs=2, type=str, help='Add a new series [link/imdb] [score]')
parser.add_argument('-R', '--remove', type=str, help='Remove a series [name]')
parser.add_argument('-W', '--watched', type=str, nargs=3,
                    help='Update number of watched episodes [name] [season] [last_episode]')
parser.add_argument('-S', '--snooze', type=str, help='Snooze a series [name]')
parser.add_argument('-L', '--list',action='store_true', help='List all updates from all series series')
parser.add_argument('-X', '--unsnooze', type=str, help='Unsnooze a series [name]')
parser.add_argument('-U', '--updates', type=str, help='Show new from a series [name]')

# add help for the arguments


args = parser.parse_args()

if args.add:
    imdb_link = args.add[0]
    parsed_id = series_manager.parse_imdb_link(imdb_link)
    if int(args.add[1]) > 10 or int(args.add[1]) < 0:
        print("Invalid score ... the score must be between 0 and 10")
        # end the program
        exit(1)
    info = series_manager.add(parsed_id, args.add[1])

    # ask for prompt to set the viewed episodes
    option = input("Do you want to set the viewed episodes? (y/n)")
    if option == 'y':
        episode, season = input("Enter the season and episode number [episode] [season]: ").split()
        series_manager.update_watched_episodes(info[2], season, episode)

        pass

    # TODO check if the series is already in the database
    # TODO add options to set view all episodes or only the ones that are not watched

if args.list:
    print("List all the updates from all series")
    series_manager.list_unwatched()

if args.remove:
    print("Removing the series: " + args.remove)

if args.snooze:
    results = series_manager.get_by_name(args.snooze)
    if results != "Exception":
        for result in results:
            option = input("Do you want to snooze the series " + result[1] + "? (y/n)")
            if option != 'y':
                continue
            series_manager.snooze(result[0], 1)

    else:
        print("Error while getting the series by name")
        exit(1)

if args.unsnooze:
    results = series_manager.get_by_name(args.unsnooze)
    if results != "Exception":
        for result in results:
            option = input("Do you want to unsnooze the series " + result[1] + "? (y/n)")
            if option != 'y':
                continue
            series_manager.snooze(result[0], 0)

    else:
        print("Error while getting the series by name")
        exit(1)

