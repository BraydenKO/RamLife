from ..data.schedule import Section

'''
A collection of functions to index course data.

No function in this class reads data from the data files, just works on them. 
This helps keep the program modular by seperating the data from 
the data indexing
'''

# Converts a section ID to a course ID.
def get_course_id(section_id):
  result = section_id[0:section_id.index("-")]
  if result.startswith("0"):
    return result[1:]
  else:
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
  return [
    Section(
      id = key,
      name = course_names[get_course_id(key)],
      teacher = faculty_names[value].name if value in faculty_names else "missing teacher",
      # Set's the link to the zoom link attached to a teacher's email
      # If this teacher has different links to different secions, set it 
      # to the link attached to their id.
      # If there is no zoom link attached to an email or a course id, leave it empty.
      zoom_link = zoom_links[key] if key in zoom_links else zoom_links[faculty_names[value].email]
        if value in faculty_names and faculty_names[value].email in zoom_links else ""
    )
    for key, value in section_teachers.items()
  ]
