class Feedback:
	def __init__(self, message, email, name, is_anonymous, timestamp):
		"""
		Args:
			message (str): the message
			email (str): the user's email
			name (str): the user's name
			is_anonymous (bool): if the user is anonymous
			timestamp (DatetimeWithNanoseconds): exact timestamp of message
		"""
		self.message = message
		self.email = email
		self.name = name
		self.is_anonymous = is_anonymous
		self.timestamp = timestamp

	def from_json(json): return Feedback(
		message = json["message"],
		email=json.get("email"),
		name=json["name"],
		is_anonymous=json.get("anonymous") or not json.get("responseConsent"),
		timestamp=json["timestamp"]
	)

	def __repr__(self): 
		result = ""
		if not self.is_anonymous:
			result += f"{self.name}, {self.email}: "
		result += f"{self.message} -- {self.timestamp}"
		return result

	def __lt__(self, other): 
		return self.timestamp < other.timestamp