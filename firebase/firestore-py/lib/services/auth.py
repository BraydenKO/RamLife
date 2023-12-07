from .firebase import app
from firebase_admin import auth
from firebase_admin.exceptions import NotFoundError

def create_user(email): 
	"""creates user account with this email

	Args:
		email (str): the user's email

	Returns:
		UserRecord: user record for new user
	"""
	return auth.create_user(email=email)

def get_user(email): 
	"""gets the user with the associated email

	Args:
		email (str): user's email

	Returns:
		UserRecord: user record instance
	"""
	try: return auth.get_user_by_email(email)
	except NotFoundError: return create_user(email)

def get_claims(email):
	"""get the claims for the user with this email

	Args:
		email (str): user's email

	Returns:
		custom_claims: A dictionary or a JSON string containing the custom claims
	"""
	return get_user(email).custom_claims

def set_scopes(email, scopes): 
	"""sets these scopes to the user with the specified email. These scopes are used
		to grant the user permissions within the app.

	Args:
		email (str): user's email
		scopes (list): list of user's scopes
	"""
	auth.set_custom_user_claims(
		get_user(email).uid,
		{"isAdmin": bool(scopes), "scopes": scopes},
	)

def list_users():
	"""creates a [UserIterator] for all users 

	Returns:
		UserIterator: iterator of all user accounts
	"""
	return auth.list_users().iterate_all()

def revoke_token(user):
	"""revokes refresh tokens for specific user

	Args:
		user (UserRecord): [UserRecord] see get_user(email) function
	"""
	auth.revoke_refresh_tokens(user.uid)
