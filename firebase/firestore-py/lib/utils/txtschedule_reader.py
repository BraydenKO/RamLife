from ..data.schedule import Period
from .dir import data_dir
import os
import PyPDF2

schedules_dir = data_dir / "new student schedules"
days = ["Friday", "Thursday", "Wednesday", "Tuesday", "Monday"]

def get_files():
  return os.listdir(schedules_dir)

def read_pdf(file):
  # Open the PDF file
  with open(schedules_dir / file, 'rb') as file:
      # Create a PDF reader object
      reader = PyPDF2.PdfFileReader(file)

      # Read the number of pages in the PDF
      num_pages = reader.numPages

      # Holds the lines of texts
      all_lines = []

      # Iterate through all the pages
      for i in range(num_pages):
          # Get the page object
          page = reader.getPage(i)

          # Extract the text from the page
          text = page.extractText()
          lines = text.split("\n")
          all_lines = all_lines + lines
      
      return all_lines

def get_name(lines):
  for line in lines:
    if line.startswith("GRADE"):
      return line

  return "Error in finding student details"

def get_periods(schedule, period, day_num = None):
  if day_num is None:
    day_num = 0 if period <= 6 else 1
  period = str(period)
  classes = []
  read= False
  skip = False
  add_free = False
  num_frees = 0

  for idx, line in enumerate(schedule):
    if skip:
      skip = False
      continue

    if line.startswith(period + ":"):
      read = True

      id = line.split("  ")[-1]
      room_line = schedule[idx + 1]
      if "HR" not in room_line:
        room = room_line[0:room_line.index(":")-len(period)]
      else:
        room = room_line[0:room_line.index("H")]
        skip = True

      room, add_free, num_frees = has_free(room, period)

      classes.append(Period(room,id, days[day_num], period))
      continue
    if read and day_num != 4:
      if add_free:
        for _ in range(num_frees):
          day_num += 1
          classes.append(Period(room=None,id=None, day=days[day_num], period=period))
        add_free = False

      day_num += 1
      id = line.split("  ")[-1]
      room_line = schedule[idx + 1]

      if day_num != 4:
        room = room_line[0:room_line.index(":")-len(period)]
      else:
        room = room_line

      room, add_free, num_frees = has_free(room, period)

      classes.append(Period(room,id, days[day_num], period))
    
    if day_num == 4:
      break
  
  else:
    classes.append(Period(room=None,id=None, day=days[day_num], period=period))
    day_num += 1
    period = period + " " + period + ":"
    classes = get_periods(schedule,period,day_num)

  
  return classes

def has_free(room, period, add_free = False, num_frees = 0):
  if " " in room:
    num_frees += 1
    room, add_free, num_frees = has_free(room[:-(1+len(period))], period, add_free=True, num_frees=num_frees)
    return room, add_free, num_frees
  else:
    return room, add_free, num_frees 

def build_schedule(lines):
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

if __name__ == "__main__":
  files = get_files()
  lines = read_pdf(files[0])
  schedule = build_schedule(lines)