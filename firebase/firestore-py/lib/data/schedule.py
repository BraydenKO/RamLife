class Semesters: 
	def __init__(self, semester1, semester2, section_id): 
		"""
		Args:
			semester1 (bool): is this section in semester 1
			semester2 (bool): is this section in semester 2
			section_id (str): id of section

		Raises:
			AssertionError: If both semester 1 and 2 and None
		"""
		self.semester1 = semester1
		self.semester2 = semester2
		self.section_id = section_id
		assert semester1 is not None and semester2 is not None, f"Could not read semester data for {section_id}"

	def __str__(self): return f"Semesters({self.semester1}, {self.semester2})"
	def __repr__(self): return f"Semesters({int(self.semester1)}, {int(self.semester2)})"

class Section: 
	def __init__(self, name, id, teacher, zoom_link): 
		"""Creates a Section object

		Args:
			name (str): name of section
			id (str): id of section
			teacher (str): name of teacher for section
			zoom_link (str): zoom link of section
		"""
		self.name = name
		self.id = id
		self.teacher = teacher
		self.zoom_link = zoom_link

	def __repr__(self): return f"{self.name} ({self.id})"

	def to_json(self): return {
		"name": self.name, 
		"teacher": self.teacher, 
		"id": self.id, 
		"virtualLink": self.zoom_link,
	}

class Period: 
	PERIODS_IN_DAY = {
		"Monday": 10,
		"Tuesday": 10,
		"Wednesday": 10,
		"Thursday": 10,
		"Friday": 6,
	}

	def __init__(self, room, id, day, period): 
		"""Creates a Period object

		Args:
			room (str): room for this period
			id (str): id of class
			day (str): day of week
			period (int): period num
		"""
		assert day is not None and period is not None, f"Could not read period data for {id}"
		assert (id is None) == (room is None), f"If ID is None, room must be too (and vice versa): {day}, {period}, {id}"
		self.room = room
		self.id = id
		self.day = day
		self.period = period

	def __repr__(self): return f"{self.day}_{self.period}({self.id})"

	def to_json(self): return {
		"room": self.room,
		"id": self.id,
		"dayName": self.day,
		"name": str(self.period),
	}
