library pages;

export "src/pages/admin.dart";
export "src/pages/builders/day_builder.dart";
export "src/pages/builders/reminder_builder.dart";
export "src/pages/builders/special_builder.dart";
export "src/pages/builders/sports_builder.dart";
export "src/pages/calendar.dart";
export "src/pages/drawer.dart";
export "src/pages/feedback.dart";
export "src/pages/new_home.dart";
export "src/pages/home.dart";
export "src/pages/login.dart";
export "src/pages/reminders.dart";
export "src/pages/route_initializer.dart";
export "src/pages/schedule.dart";
export "src/pages/specials.dart";
export "src/pages/sports.dart";

/// Route names for each page in the app.
/// 
/// These would be enums, but Flutter requires Strings. 
class Routes {
	/// The route name for the home page.
	static const String home = "home";

	/// The route name for the schedule page.
	static const String schedule = "schedule";

	/// The route name for the reminders page.
	static const String reminders = "reminders";

	/// The route name for the login page.
	static const String login = "login";

	/// The route name for the feedback page.
	static const String feedback = "feedback";

	/// The route name for the calendar page. 
	static const String calendar = "calendar";

	/// The route name for the specials manager page. 
	static const String specials = "specials";

	/// The route name for the admin home page. 
	static const String admin = "admin";

	/// The route name for the sports games page.
	static const String sports = "sports";
}
