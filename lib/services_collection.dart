import "package:flutter/foundation.dart" show required;

import "package:ramaz/services.dart";
import "package:ramaz/models.dart";
import "package:ramaz/data.dart";

DateTime now = DateTime.now();

class ServicesCollection {
	final Reader reader;
	final Preferences prefs;

	Reminders reminders;
	Schedule schedule;

	ServicesCollection({
		@required this.reader,
		@required this.prefs,
	});

	/// This function is a safety!
	/// In the event a file is unavailable, the try, catch in main will catch it
	/// After the files are verifiably available, this function is called. 
	///
	/// Use this function to initialize anything that requires a file.
	void init() {
		reminders = Reminders (reader);
		schedule = Schedule(
			reader, 
			reminders: reminders,
		);
		verify();
	}

	/// Since [init] cannot be enforced, this function does null checks.
	/// Put any variables that aren't final in here
	void verify() {
		final List properties = [reminders, schedule];

		for (final property in properties) {
			assert (
				property != null,
				"ServicesCollection.init was not called"
			);
		}
	}

	Future<void> initOnLogin(String email, {bool first = true}) async {
		// Save and initialize the student to get the subjects
		final Map<String, dynamic> studentData = await Firestore.student;
		final Student student = Student.fromJson(studentData);		

		// save the data
		reader
			..studentData = studentData
			..subjectData = await Firestore.getClasses(student)
			..calendarData =  await Firestore.month
			..remindersData = await Firestore.reminders;

		if (first) {
			init();
		}
	}
}

