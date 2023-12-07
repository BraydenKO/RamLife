import yaml
from datetime import date

from . import dir

day_names = None 
corrupted_students = None
is_semester1 = date.today().month > 7
testers = None
ignored_students = None
ignored_sections = None

def init():
	"""initializes these constants from constants.yaml:

		day_names (list): list of names for non-weekend days in week 
		corrupted_students (list): list of student ids that are corrupted
		testers (list): list of dicts containin the email, first name and last name
			of each tester.
		ignored_students (list): list of student ids to ignore for any reason
		ignored_sections (list): list of section ids to ignore for any reason
	"""     
	global day_names, corrupted_students, testers, ignored_students, ignored_sections
	with open(dir.constants) as file: 
		contents = yaml.safe_load(file)

	day_names = contents["dayNames"]
	corrupted_students = contents["corruptStudents"]
	testers = [
		{"email": tester, "first": contents["testers"][tester]["first"], "last": contents["testers"][tester]["last"]}
		for tester in contents["testers"]
	]
	ignored_students = contents["ignoredStudents"]
	ignored_sections = contents["ignoredSections"]
