import "package:firestore/data.dart";
import "package:firestore/helpers.dart";

/// A collection of functions to read student data.
/// 
/// No function in this class actually performs logic on said data, just returns
/// it. This helps keep the program modular, by separating the data sources from
/// the data indexing.
/// 
/// NOTE: [homeroomLocations] is filled by [getPeriods]. Until that function is
/// called, its value is null and [Map.[]] cannot be used. 
class StudentReader {
	/// Maps student IDs to their respective [Student] objects.
	static Future<Map<String, Student>> getStudents() async => {
		await for (final Map<String, String> entry in csvReader(DataFiles.students)) 
			entry ["ID"]: Student(
				first: entry ["First Name"],
				last: entry ["Last Name"],
				email: entry ["Student E-mail"],
				id: entry ["ID"],
			)
	};

	/// Maps homeroom section IDs to their respective rooms.
	/// 
	/// This value is filled by [getPeriods]. Do not try to access it beforehand.
	static Map<String, String> homeroomLocations;

	/// Maps section IDs to their respective [Period] objects.
	/// 
	/// This also detects homeroom sections and places them in [homeroomLocations],
	/// which cannot be accessed without calling this function.
	static Future<Map<String, List<Period>>> getPeriods() async {
		homeroomLocations = {};  // allow it to be accessed
		final Map<String, List<Period>> result = DefaultMap((_) => []);
			await for (
				final Map<String, String> entry in 
				csvReader(DataFiles.sectionSchedule)
			) {
				final String sectionID = entry ["SECTION_ID"];
				final String day = entry ["WEEKDAY_NAME"];
				final Letter letter = stringToLetter [day];
				final String periodString = entry ["BLOCK_NAME"];
				final String room = entry ["ROOM"];
				final int periodNumber = int.tryParse(periodString);
				if (periodNumber == null) {
					if (periodString == "HOMEROOM") {
						homeroomLocations [sectionID] = room;
					}
					continue;
				} 
				final Period period = Period(
					day: letter,
					room: room,
					id: sectionID,
					period: periodNumber,
				);
				result [sectionID].add(period);
			}
		return result;
	}

	/// Maps student IDs to a list of section IDs they're enrolled in.
	static Future<Map<String, List<String>>> getStudentClasses() async {
		final Map<String, List<String>> result = DefaultMap((_) => []);
		await for (final Map<String, String> entry in csvReader(DataFiles.schedule)) {
			result [entry ["STUDENT_ID"]].add(entry ["SECTION_ID"]);
		}
		return result;
	}

	/// Maps section IDs to their respective [Semesters] objects. 
	static Future<Map<String, Semesters>> getSemesters() async => {
		await for (final Map<String, String> entry in csvReader(DataFiles.section))
			entry ["SECTION_ID"]: Semesters(
				semester1: entry ["TERM1"] == "Y",
				semester2: entry ["TERM2"] == "Y",
				sectionID: entry ["SECTION_ID"]  // for debugging
			)
	};
}