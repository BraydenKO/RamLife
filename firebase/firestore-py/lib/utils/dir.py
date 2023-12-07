from pathlib import Path

project_dir = Path.cwd()
data_dir = project_dir.parent.parent / "data"

# The path to the admin certificate file. 
certificate = project_dir / "admin.json"

# The courses database. 

# Contains the names of every course, but requires a course ID, not 
# a section ID. 
courses = data_dir / "courses.csv"

# The faculty database.
# 
# Contains the names, emails, and IDs of every faculty member. 
faculty = data_dir / "faculty.csv"

# The schedule database. 
# 
# Contains a list pairing each student ID to multiple section IDs. 
schedule = data_dir / "schedule.csv"

# The sections database.
# 
# Contains the teachers of every section, along with other useful data.
section = data_dir / "section.csv"

# The periods database.
# 
# Contains each period every section meets. 
section_schedule = data_dir / "section_schedule.csv"

# The students database. 
# 
# Contains the names, emails, and IDs of every student.
students = data_dir / "students.csv"

# The virtual class links connecting a zoom link to a teacher's email.
zoom_links = data_dir / "zoom_links.csv"

# The virtual class links connecting a zoom link to a section Id.
special_zoom_links = data_dir / "special_zoom_links.csv"


# The list of admins.
# 
# Each row should be the name of the admin, followed by a list of scopes.
admins = data_dir / "admins.csv"

# Options for this tool
constants = project_dir / "constants.yaml"

# Constants such as dayNames, corruptStudents, and testers
constants = project_dir / "constants.yaml"

# List of future Ramaz sports games
sports_schedule = data_dir / "sports.csv"

def get_month(month): 
    """returns path for specific month in calendar

    Args:
        month (int): index of month (1-based)

    Returns:
        Path: path to month specified
    """
    return data_dir / "calendar" / f"{month}.csv"
