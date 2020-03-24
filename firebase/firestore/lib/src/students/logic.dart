import "package:firestore/data.dart";
import "package:firestore/helpers.dart";

import "reader.dart";  // for doc comments, can be removed if necessary.

/// A collection of functions to index student data. 
/// 
/// No function in this class reads data from the data files, just works logic
/// on them. This helps keep the program modular, by separating the data sources
/// from the data indexing.
/// 
/// NOTE: [homerooms] and [seniors] are filled by [getSchedules]. Until that 
/// function is called, their values will be null and [Map.[]] and 
/// [Set.contains] cannot be used on them.
class StudentLogic {
	/// A list of expelled students. 
	static const Set<String> expelled = {};

	/// Maps a [Letter] to the number of periods in that day.
	/// 
	/// Not all periods will be shown in the app. `Special.periods.length` will
	/// dictate that, and `Special.periods.skips` dictates which periods will 
	/// be skipped.
	static Map<Letter, int> periodsInDay = {
		Letter.A: 11, 
		Letter.B: 11,
		Letter.C: 11,
		Letter.M: 11,
		Letter.R: 11, 
		Letter.E: 7,
		Letter.F: 7,
	};

	/// Maps students to their homeroom section IDs.
	/// 
	/// This map is populated by [getSchedules].
	static Map<Student, String> homerooms;

	/// A collection of all seniors. 
	/// 
	/// Seniors do not have regular homerooms, so if they are present in this set, 
	/// their homerooms will be ignored. 
	/// 
	/// This set is populated by [getSchedules].
	static Set<Student> seniors;

	/// Builds a student's schedule.
	/// 
	/// This function works by taking several arguments: 
	/// 
	/// - students, from [StudentReader.getStudents]
	/// - periods, from [StudentReader.getPeriods]
	/// - studentClasses, from [StudentReader.getStudentClasses]
	/// - semesters, from [StudentReader.getSemesters]
	/// 
	/// These are kept as parameters instead of calling the functions by itself
	/// in order to keep the data and logic layers separate. 
	/// 
	/// Additionally, this function populates [seniors] and [homerooms].
	static Map<Student, Map<Letter, List<Period>>> getSchedules({
		@required Map<String, Student> students,
		@required Map<String, List<Period>> periods,
		@required Map<String, List<String>> studentClasses, 
		@required Map<String, Semesters> semesters,
	}) {
		homerooms = {};
		seniors = {};
		final Map<Student, Map<Letter, List<Period>>> result = DefaultMap(
			(_) => DefaultMap((Letter letter) => 
				List.filled(periodsInDay[letter], null))
		);
		for (final MapEntry<String, List<String>> entry in studentClasses.entries) {
			final Student student = students [entry.key];
			for (final String sectionId in entry.value) {
				if (sectionId.contains("UADV")) {
					homerooms [student] = sectionId;
					continue;
				}

				if (!semesters [sectionId].semester2) {
					continue;
				} else if (sectionId.startsWith("12")) {
					seniors.add(student);
				}

				assert(
					periods [sectionId] != null, 
					"Could not find $sectionId in the schedule."
				);

				for (final Period period in periods [sectionId]) {
					result [student] [period.day] [period.period - 1] = period;
				}
			}
		}
		return result;
	}

	/// Returns complete [Student] objects.
	/// 
	/// This function returns [Student] objects with more properties than before.
	/// See [Student.addSchedule] for which properties are added. 
	/// 
	/// This function works by taking several arguments: 
	/// 
	/// - schedules, from [getSchedules] 
	/// - homerooms, from [homerooms]
	/// - homeroomLocations, from [StudentReader.homeroomLocations]
	/// 
	/// These are kept as parameters instead of calling the functions by itself
	/// in order to keep the data and logic layers separate. 
	static List<Student> getStudentsWithSchedules({
		@required Map<Student, Map<Letter, List<Period>>> schedules, 
		@required Map<Student, String> homerooms,
		@required Map<String, String> homeroomLocations,
	}) => [
		for (
			final MapEntry<Student, Map<Letter, List<Period>>> entry in 
			schedules.entries
		)
			if (!expelled.contains(entry.key.id))
				entry.key.addSchedule(
					schedule: entry.value, 
					homeroom: seniors.contains(entry.key) 
						? "SENIOR_HOMEROOM"
						: homerooms [entry.key],
					homeroomLocation: homeroomLocations [homerooms [entry.key]],
				)
	];
}
