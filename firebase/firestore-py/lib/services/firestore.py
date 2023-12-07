from firebase_admin import _DEFAULT_APP_NAME, firestore
from .. import data
from datetime import date

_firestore = firestore.client()

students = _firestore.collection("students")
calendar = _firestore.collection("calendar")
courses = _firestore.collection("classes")
feedback = _firestore.collection("feedback")
dataRefresh = _firestore.collection("dataRefresh")
sports = _firestore.collection("sports2")

def upload_users(users): 
  """upload list of users to firestore

  Args:
      users (list): list of [User] objects
  """   
  batch = _firestore.batch()
  for user in users:
    batch.set(students.document(user.email), user.to_json())
  batch.commit()

def upload_month(month, data):
  """uploads a month to firestore

  Args:
      month (int): index of month (1-based)
      data (list): list of [Day] objects for each day in month
  """   
  calendar.document(str(month)).update({
    "month": month,
    "calendar": [(day.to_json() if day is not None else None) for day in data]
  })

def upload_sections(sections):
  """uploads class sections to firestore

  Args:
      sections (list): list of [Section] objects
  """
  if len(sections) > 500:
    upload_sections(sections[:500])
    upload_sections(sections[500:])
    return
  batch = _firestore.batch()
  for section in sections:
    batch.set(courses.document(section.id), section.to_json())
  batch.commit()

def get_month(month):
  """get data for specific month

  Args:
      month (int): index of month (1-based)

  Returns:
      dict: dict of month data
  """   
  return calendar.document(str(month)).get().to_dict()

def get_feedback(): 
  """get list of feedback from firestore

  Returns:
      list: list of [Feedback] objects
  """
  return [
    data.Feedback.from_json(document.to_dict())
    for document in feedback.stream()
  ]

def upload_userdate(date):
  """update the date user were last updated

  Args:
      date (str): the date
  """
  dataRefresh.document("dataRefresh").update({
    "user": date
  }) 

def upload_caldate(date):
  """_summary_

  Args:
      date (_type_): _description_
  """
  dataRefresh.document("dataRefresh").update({
    "calendar": date
  })

def update_user(users, section_id, meetings):
  """updates user data for given section and meetings

  Args:
      users (list): list of user emails
      section_id (str): section id
      meetings (list): list of [day of week, period, room] elements
  """
  if len(users) > 10: 
    update_user(users[10:], section_id, meetings)
    users = users[:10]
  query = students.where("email", "in", users).stream()
  batch = _firestore.batch()
  for user in query:
    user_dict = user.to_dict()
    for day, period, room in meetings:
      user_dict[day][int(period)-1] = {
        "id": section_id,
        "name": period,
        "room": room,
        "dayName": day
      }
    batch.set(students.document(user_dict["email"]), user_dict)
  
  batch.commit()

def upload_sports(sports_games):
  """uploads sports data to firestore

  Args:
      sports_games (list): list of [SportsGame] objects
  """
  from datetime import date
  year = date.today().strftime("%Y")
  month = int(date.today().strftime("%m"))

  # In the academic year 22' - 23', use 2022 not 2023
  if month < 7:
    year = str(int(year) - 1)

  sports.document(year).set({"games": sports_games})

def update_user_beta(users, schedules):
  """
  Updates users in firestore by reading the whole schedule from a pdf (this part is just the updating part)
  Precondition: users is a list of emails
                schedules is a list of dictioniaries that map weekdays to a list of Period objects.
                Each index of users corresponds to a schedule in schedules.
  
  Note: Reads the user's data first because not all of their data can be obtained from the PDF
        Ex: Homeroom info
  
  Args:
      users (list): list of emails
      schedules (list): list of dicts containing user schedules
  """
  if len(users) > 10: 
    update_user_beta(users[10:], schedules[10:])
    users = users[:10]
    schedules = schedules[:10]

  user_to_sched = {users[i]:schedules[i] for i in range(len(users))}

  query = students.where("email", "in", users).stream()
  batch = _firestore.batch()

  for user in query:
    user_dict = user.to_dict()
    email = user_dict['email']
    schedule = user_to_sched[email]
 
    for day, sched in schedule.items():
      for p_num,period in enumerate(sched):
        if period is not None:
          user_dict[day][p_num] = {
            'room': period.room,
            'dayName': day,
            'id': period.id,
            'name': period.period
          }
        else:
          user_dict[day][p_num] = None
    batch.set(students.document(user_dict['email']), user_dict)
  batch.commit()
