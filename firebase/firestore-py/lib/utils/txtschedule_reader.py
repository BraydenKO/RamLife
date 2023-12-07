"""These functions should hopefully be forever deprecated.
These functions are used to take a pdf of a student's schedule and convert
it into a dictionary that will be uploaded to the database. It may be hard to read
or grasp exactly why each line is necessary. 
"""
from ..data.schedule import Period
from .dir import data_dir
import os
import PyPDF2

schedules_dir = data_dir / "new student schedules"
days = ["Friday", "Thursday", "Wednesday", "Tuesday", "Monday"]

def get_files():
  """get list of files in "new student schedules" folder

  Returns:
      list: list of paths to these schedules
  """
  return os.listdir(schedules_dir)

def read_pdf(file):
  """reads pdf to a list of lines of text.
  
  Note:
    Can be very finnicky and sensitive to slight changes in pdf.

  Args:
      file (str): file path

  Returns:
      list: line of text for this pdf
  """
  # Open the PDF file
  with open(schedules_dir / file, 'rb') as file:
      # Create a PDF reader object
      reader = PyPDF2.PdfReader(file)

      # Read the number of pages in the PDF
      num_pages = len(reader.pages)

      # Holds the lines of texts
      all_lines = []

      # Iterate through all the pages
      for i in range(num_pages):
          # Get the page object
          page = reader.pages[i]

          # Extract the text from the page
          text = page.extract_text()
          print(text)
          lines = text.split("\n")
          all_lines = all_lines + lines
      
      return all_lines

def get_name(lines):
  """get name of the student

  Args:
      lines (list): list of lines of text

  Returns:
      str: student's name
  """
  for line in lines:
    if line.startswith("GRADE"):
      return line

  return "Error in finding student details"

def get_periods(schedule, period, day_num = None, classes = None):
  """extract periods from text

  Args:
      schedule (list): list of lines of text for the schedule
      period (int): int in range(1,11) referring to which period
      day_num (int, optional): index of day of the week in reverse. Defaults to None.
      classes (list, optional): list of [Period] objects to add this period to. Defaults to None.

  Returns:
      list: list of [Period] objects both initialized with (see Args) and extracted.
  """
  if day_num is None:
    day_num = 0 if period <= 6 else 1
  if classes is None:
    classes = []
  
  period = str(period)
  read= False
  skip = False
  add_free = False
  num_frees = 0
  
  for idx, line in enumerate(schedule):
    if skip:
      skip = False
      continue

    if line.startswith(period + ":"):
      if len(period.split(" ")) > 1:
        period = period.split(" ")[0]
        
      read = True

      id = line.split("  ")[-1]
      room_line = schedule[idx + 1]

      if "HR" not in room_line:
        
        if ":" in room_line:
          room = room_line[0:room_line.index(":")-len(period)]
        else:
          room = room_line[:-len(period)]
          add_free = True
          num_frees = 1
      else:
        room = room_line[0:room_line.index("H")]
        skip = True

      room, add_free, num_frees = has_free(room, period,add_free,num_frees)

      classes.append(Period(room,id, days[day_num], period))
      continue
    if read and day_num != 4:
      if add_free:
        for _ in range(num_frees):
          day_num += 1
          classes.append(None)
          #classes.append(Period(room=None,id=None, day=days[day_num], period=period))
        add_free = False
        num_frees = 0

      if day_num==4:
        break
      day_num += 1
      if day_num > 4:
        break
      id = line.split("  ")[-1]
      room_line = schedule[idx + 1]
      
      if day_num != 4:
        if ":" in room_line:
          room = room_line[0:room_line.index(":")-len(period)]
        else:
          room = room_line[:-len(period)]
          add_free = True
          num_frees = 1
      else:
        room = room_line

      room, add_free, num_frees = has_free(room, period, add_free, num_frees)

      classes.append(Period(room,id, days[day_num], period))
    
    if day_num == 4:
      break

    # Friday 3rd period is a free
    if line.startswith(period + " HR"):
      read = True
      #print("YOOOOOO")
      #print(Period(room=None,id=None, day=days[day_num], period=period))
      classes.append(None)
      #classes.append(Period(room=None,id=None, day=days[day_num], period=period))

  else:
    classes.append(None)
    #classes.append(Period(room=None,id=None, day=days[day_num], period=period.split(" ")[0]))
    day_num += 1
    period = period + " " + period.split(" ")[0]

    classes = classes + get_periods(schedule,period,day_num)

  return classes

def has_free(room, period, num_frees = 0):
  """extracts room and checks whether to add a free to
    the students schedule. Frees look pretty different that normal
    periods when reading text from a converted pdf and they may affect data around them. 
    Hence why they get a special recursive (frees can happen multiple times in a row) function. 

  Args:
      room (str): room of period
      period (str): period
      num_frees (int, optional): number of frees user has. Defaults to 0.

  Returns:
      str: room
      bool: whether to add a free
      int: number of frees to add
  """
  if " " in room:
    num_frees += 1
    room, add_free, num_frees = has_free(room[:-(1+len(period))], period, add_free=True, num_frees=num_frees)
    return room, add_free, num_frees
  else:

    try: 
      int(room[1])
      if len(room) > 4:
        room = room[:4]
        add_free = True
        num_frees += 1
    except:
      add_free = False
    return room, add_free, num_frees 

def build_schedule(lines):
  """given the lines, build the schedule.

  Args:
      lines (list): list of lines of text from pdf

  Returns:
      dict: mapping day names to period in that day for a specific user
  """
  classes = []
  for period in range(1,11):
    classes = classes + get_periods(lines, period)
  schedule = {day: [] for day in days}
  day_num = 0
  period = 1
  for section in classes:
    schedule[days[day_num]].append(section)
    
    if day_num == 4 and period >= 6:
      day_num = 1
      period += 1
    elif day_num == 4 and period < 6:
      day_num = 0
      period += 1
    else:
      day_num += 1
  
  return schedule
