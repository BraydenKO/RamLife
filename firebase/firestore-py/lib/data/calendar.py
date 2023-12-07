"""Defines ways to create and validate a calendar"""
from datetime import date
import calendar as calendar_model
from datetime import datetime

from .. import utils

SPECIAL_NAMES = {
	"rosh chodesh": "Rosh Chodesh",
	"friday r.c.": "Friday Rosh Chodesh",
	"early dismissal": "Early Dismissal",
	"modified": "Modified",
}

current_year = date.today().year
current_month = date.today().month
cal = calendar_model.Calendar(firstweekday=6)

def get_default_calendar(month): 
	"""Creates a list of [Day] objects for each day
 		in the given month

	Args:
		month (int): index of month (1-based)

	Returns:
		list: A list of [Day] objects for each day that month
	"""
	result = []
	year = get_year(month)
	for date in cal.itermonthdates(year, month): 
		if date.month != month: continue
		weekday = calendar_model.day_name[date.weekday()]
		if weekday in {"Saturday", "Sunday"}: 
			result.append(None)
		elif weekday == "Friday": 
			result.append(Day(date=date, name=weekday, special="Friday"))
		else: 
			result.append(Day(date=date, name=weekday, special="Weekday"))
	return result

def get_year(month): 
	"""Get the year this month is in.


	Args:
		month (int): index of month (1-based).

	Returns:
		int: the year this month is in.
  
	Examples:
		Run this function in the year 2023, in Dec.
  		then again in 2024 in Jan.
  
		>>> get_year(2)
		2024
		>>> get_year(12)
		2023
	"""
	if current_month > 7:
		return current_year if month > 7 else current_year + 1
	else: 
		return current_year - 1 if month > 7 else current_year

def get_empty_calendar(month): 
	"""Create empty month of 31 days

	Note:
		This function is only run for the months
		July and August as of now (31 days each).
		If one wants to use this function for other
		months, the function should be modified.

	Args:
		month (int): index of month. Not currently used,
			but maybe be used if more months use this
			function.

	Returns:
		list: list of 31 NoneType elements
	"""
	return [None] * 31

class Day: 
	def get_list(date_line, name_line, special_line, month): 
		"""create a list of [Day] objects given dates, names, specials,
			and the month.

		Todo:
			Justify why we have this function

		Args:
			date_line (list): dates
			name_line (list): names
			special_line (list): specials
			month (int): index of month (1-based)

		Returns:
			list: list of [Day] objects
		"""
		return [
			Day.raw(date=date, name=name, special=special, month=month)
			for date, name, special in zip(date_line, name_line, special_line)
			if date
		]

	def verify_calendar(month, calendar): 
		"""Verifies that a given month in a calendar
			is valid.

		Todo:
			Make this function handle leap years
			by using get_year(month) instead of current_year
  
		Args:
			month (int): index of the month (1-based)
			calendar (list): data of days in the month

		Returns:
			bool: whether the calendar is valid
		"""
		_, days_in_month = calendar_model.monthrange(current_year, month)
		days = set(range(1, days_in_month + 1))
		is_valid = len(calendar) == days_in_month
		if not is_valid: utils.logger.warning(f"Calendar for {month} is invalid. Missing entries for {days}.")
		return is_valid

	def raw(date, name, special, month): 
		print(date,name,special,month)
		"""Create a Day object using these args

		Todo:
			Justify why we have this function

		Args:
			date (str): day of month
			name (str): name of day
			special (str): special schedule
			month (int): index of month (1-based)

		Returns:
			Day: Day object for this data
		"""
		year = get_year(month)
		day = int(date)
		date = datetime(year, month, day)
		name = name.split() [0]
		special = special.lower()
		if special.endswith(" Schedule"): 
			special = special[:special.find(" Schedule")]
		if special.startswith("modified"):
			special = "Modified" 
		elif not special or special not in SPECIAL_NAMES: 
			special = None
		else: special = SPECIAL_NAMES[special]
		return Day(date = date, name = name, special = special)

	def __init__(self, date, name, special): 
		"""initializes Day object

		Args:
			date (datatime.date): date of Day
			name (str): name of Day
			special (str): special schedule
   
		Raises:
			AssertionError: If there is a special but no name
		"""
  
		self.date = date
		self.name = name
		self.special = special
		assert name is not None or special is None, f"Cannot have a special without a name: {date}"

	def __str__(self): 
		if self.name is None: return f"{self.date}: No school"
		else: return f"{self.date}: {self.name} {self.special}"

	def __repr__(self): return str(self)

	def to_json(self): return {
		"name": self.name,
		"schedule": self.special
	}

