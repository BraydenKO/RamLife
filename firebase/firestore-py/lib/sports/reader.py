import lib.utils as utils
from lib.data.sports import SportsGame
import csv
from datetime import date
year = date.today().strftime("%Y")

def read_sports():
    """reads sports data from sports.csv

    Returns:
        list: list of [SportsGame] objects
    """
    with open(utils.dir.sports_schedule) as f:
        games = []
        for row in csv.DictReader(f):
            opponent = row["Opponent"]
            if opponent == "": continue

            date = get_date(year, row["Date"])
            livestream_url = None
            scores = None
            start = row["Time"].split(" ")[0] # The split(" ")[0] gets rid of " PM" if it's in the time

            games.append(SportsGame(
                opponent=opponent, 
                location=row["Location"], 
                date=date, 
                livestream_url=livestream_url, 
                scores=scores, 
                team=row["Team"], 
                start=start)
                )
        
        return games

def get_date(year, date):
    """properly formats date from the date in sports.csv

    Args:
        year (str): string for current year
        date (str): string for date as in sports.csv

    Returns:
        str: properly formatted date
    """
    #2022-02-08 00:00:00.000
    date = date.split("-")[0] # If the date is 11/6 - 11/8, just use 11/6

    month = date[:date.index("/")]
    if len(month) == 1: # If the month has only 1 digit
        month = "0" + month # Make it 2 digits
    if int(month) <= 7:
        year = int(year) + 1
    day = date[date.index("/") +1:]
    if len(day) == 1:
        day = "0" + day
    return f"{year}-{month}-{day} 00:00:00.000"
