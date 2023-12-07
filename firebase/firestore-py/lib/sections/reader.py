import csv
from ..utils import dir, logger

def fix_id(id):
  """fixes ids of the form "90070.0" to look like "90070"

  Args:
      id (str): an id, for example "90070","90070.0", 
        or "CADV"

  Returns:
      str: correct(ed) id
  """
  try:
    return str(int(float(id)))
  except ValueError:
    return id
    
def get_course_names():
  """ Reads courses data from courses.csv
  
  Returns:
      dict: mapping course ids to course names
  """
  with open(dir.courses) as file:
    return {
      fix_id(row["Course ID"]): row["Course Name"]
      for row in csv.DictReader(file) 
      if row["School ID"] == "Upper"}
  
def get_section_faculty_ids():
  """Reads sections data from section.csv
  
  Returns:
      dict: mapping section ids to faculty ids
  """
  with open(dir.section) as file: 
    return {
      row["SECTION_ID"]: row["FACULTY_ID"]
      for row in csv.DictReader(file)
      if row["SCHOOL_ID"] == "Upper" and row["FACULTY_ID"]}
  

def get_zoom_links():
  """Reads zoom_links data from zoom_links.csv

  Returns:
      dict: mapping teacher emails to zoom links
  """
  Links = {}
  try:
    with open(dir.zoom_links) as file:
      for row in csv.DictReader(file):
        if row["LINK"]:
          Links[row["EMAIL"]] = row["LINK"]

  except FileNotFoundError:
    logger.warning("zoom_links.csv doesn't exist. Cannot grab data. Using an empty dictionary instead")

  try:
    with open(dir.special_zoom_links) as file:
      for row in csv.DictReader(file):
        Links[row["ID"]] = row["LINK"]

  except FileNotFoundError:
    logger.warning("No special zoom links")
  
  return Links

