library constants;

import "package:flutter/material.dart" show Color;

class RamazColors {
	static const Color blue = Color(0xFF004B8D);  // (255, 0, 75, 140);
	static const Color gold = Color(0xFFF9CA15);
	static const Color blueLight = Color(0xFF4A76BE);
	static const Color blueDark = Color (0xFF00245F);
	static const Color goldDark = Color (0xFFC19A00);
	static const Color goldLight = Color (0xFFFFFD56);
}


class Routes {
	static const String home = "home";
	static const String schedule = "schedule";
	static const String reminders = "reminders";
	static const String login = "login";
	static const String feedback = "feedback";
}

class Urls {
	static const String schoology = "https://app.schoology.com";
	static const String email = "http://mymail.ramaz.org";
	static const String ramaz = "https://www.ramaz.org";
	static const String googleDrive = "http://drive.google.com";
	static const String seniorSystems = "https://my.ramaz.org/SeniorApps/facelets/home/home.xhtml";
}

class Times {
	static const int schoolStart = 9;
	static const int schoolEnd = 7;
	static const int winterFridayMonthStart = 11;
	static const int winterFridayMonthEnd = 3;
	static const int winterFridayDayStart = 1;
	static const int winterFridayDayEnd = 1;
}
