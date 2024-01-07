import sys

from DatabaseConnection import DatabaseConnection
import argparse
import SeriesManager
import argparse_range

from ErrorLogger import ErrorLogger

# connect to database

db_instance = DatabaseConnection("C:\\Users\\stefy\\Desktop\\sqlite-tools-win-x64-3440200\\BingeWatch.db")
connection = db_instance.connect()

# define the helper classes/objects
cursor = connection.cursor()
logger = ErrorLogger()
series_manager = SeriesManager.SeriesManager(connection, logger)

parser = argparse.ArgumentParser(description='BingeWatch')

# define the arguments for the program
parser.add_argument('-A', '--add', nargs=2, type=str, help='Add a new series [link/imdb] [score]')
parser.add_argument('-R', '--remove', type=str, help='Remove a series [name]')
parser.add_argument('-W', '--watched', type=str, nargs=3,
                    help='Update number of watched episodes [name] [season] [last_episode]')
parser.add_argument('-S', '--snooze', type=str, help='Snooze a series [name]')
parser.add_argument('-L', '--list', action='store_true', help='List all updates from all series series')
parser.add_argument('-X', '--unsnooze', type=str, help='Unsnooze a series [name]')
parser.add_argument('-U', '--updates', type=str, help='Show news from a series [name]')
parser.add_argument('-SC', '--score', nargs=2, type=str, help='Update the score of a series [name] [score]')
parser.add_argument('-T', '--trailer', nargs=3, type=str, help='Get a trailer for a series [name] [season] [episode]')
# add help for the arguments


args = parser.parse_args()
# if no arguments are given, show the help
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# parse each argument and call the corresponding function
if args.add:
    imdb_link = args.add[0]
    parsed_id = SeriesManager.parse_imdb_link(imdb_link)
    print("Adding the series: " + imdb_link)
    if int(args.add[1]) > 10 or int(args.add[1]) < 0:
        print("Invalid score ... the score must be between 0 and 10")
        # end the program
        exit(1)
    info = series_manager.add(parsed_id, args.add[1], imdb_link)

    # ask for prompt to set the viewed episodes
    option = input("Do you want to set the viewed episodes? (y/n)")
    if option == 'y':
        episode, season = input("Enter the season and episode number [episode] [season]: ").split()
        series_manager.update_watched_episodes(info[2], season, episode)
    else:
        series_manager.update_watched_episodes(info[2], 0, 0)

if args.list:
    print("List all the updates from all series")
    series_manager.list_unwatched()

if args.remove:
    print("Removing the series: " + args.remove)
    series_manager.remove(args.remove)

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

if args.watched:
    try:
        series_manager.update_watched_episodes(args.watched[0], args.watched[1], args.watched[2])
    except Exception as e:
        logger.log("Error while updating the watched episodes" + str(e))
        exit(1)

if args.updates:
    # show if there are new episodes coming out for a series
    series = series_manager.get_by_name(args.updates)
    for serie in series:
        option = input("Do you want to show the updates for " + serie[1] + "? (y/n)")
        if option != 'y':
            continue
        series_manager.show_updates(serie)
    pass

if args.score:
    # update the score of a series
    if int(args.score[1]) > 10 or int(args.score[1]) < 0:
        print("Invalid score ... the score must be between 0 and 10")
        # end the program
        exit(1)

    series = series_manager.get_by_name(args.score[0])
    for serie in series:
        option = input("Do you want to update the score of " + serie[1] + " to " + str(args.score[1]) + " ? (y/n)")
        if option != 'y':
            continue
        series_manager.update_score(serie[1], str(args.score[1]))

if args.trailer:
    # get a trailer for a series
    series = series_manager.get_by_name(args.trailer[0])
    for serie in series:
        option = input(
            "Do you want to get a trailer for " + serie[1] + " season " + str(args.trailer[1]) + " episode " +
            args.trailer[2] + " ? (y/n)")
        if option != 'y':
            continue
        results = series_manager.get_trailer(serie[1], args.trailer[1], args.trailer[2])
        for result in results:
            print(result)
logger.log_to_file()
