from ..data.schedule import Section

def get_course_id(section_id):
  """Given a section id, get its course id

  Args:
      section_id (str): section id

  Returns:
      str: course id
  """
  result = section_id[:section_id.index("-")]
  if result.startswith("0"):
    return result[1:]
  return result

  # Builds a list of [Section] objects.
  # 
  # This function works by taking several arguments: 
  # 
  # - courseNames, from [section_reader.course_names]
  # - sectionTeachers, from [section_reader.get_section_faculty_ids]
  # - facultyNames, from [faculty_reader.get_faculty]
  # 
  # These are kept as parameters instead of calling the functions by itself
  # in order to keep the data and logic layers separate.

def get_sections(course_names, section_teachers, faculty_names, zoom_links):
  """Builds a list of [Section] objects

  Args:
      course_names (dict): mapping course ids to course names
      section_teachers (dict): mapping section ids to faculty ids
      faculty_names (dict): mapping faculty ids to [User] objects
      zoom_links (dict): mapping faculty emails to their zoom_link (str)

  Returns:
      list: list of all [Section] objects
  """
  return [
    Section(
      id = key,
      name = course_names[get_course_id(key)],
      teacher = faculty_names[value].name if value in faculty_names else "Missing Teacher",
      # Set's the link to the zoom link attached to a teacher's email
      # If this teacher has different links to different secions, set it 
      # to the link attached to their id.
      # If there is no zoom link attached to an email or a course id, leave it empty.
      zoom_link = zoom_links[faculty_names[value].email] if value in faculty_names and faculty_names[value].email in zoom_links else zoom_links[key] if key in zoom_links else ""
    )
    for key, value in section_teachers.items()
  ]
