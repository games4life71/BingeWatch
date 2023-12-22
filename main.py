from DatabaseConnection import DatabaseConnection
import argparse
import SeriesManager

# connect to database

db_instance = DatabaseConnection("C:\\Users\\stefy\\Desktop\\sqlite-tools-win-x64-3440200\\BingeWatch.db")
connection = db_instance.connect()

cursor = connection.cursor()
series_manager = SeriesManager.SeriesManager(connection)

parser = argparse.ArgumentParser(description='Process the arguments')
# parse arguments

# print(res.fetchall())
#make an insert into the series table
# cursor.execute("INSERT INTO Series (SeriesID,SeriesName,IMDBLink, Score) VALUES (?,?,?,?)",(12,"test","sa",10))
# connection.commit()





parser.add_argument('-A', '--add', nargs=2, type=str, help='Add a new series [link/imdb] [score]')
parser.add_argument('-R', '--remove', type=str, help='Remove a series [name]')
parser.add_argument('-W','--watched',type=str,nargs=3,help='Update number of watched episodes [name] [season] [last_episode]')
parser.add_argument('-S','--snooze',type = str,help='Snooze a series [name]')
parser.add_argument('-L','--list',help='List all series')
parser.add_argument('-s','--unsnooze',type=str,help='Unsnooze a series [name]')
#add help for the arguments


args = parser.parse_args()

if args.add:
    imdb_link = args.add[0]
    series_manager.add(imdb_link, args.add[1])
    # TODO check if the link is valid

if args.remove:
    print("Removing the series: " + args.remove)
