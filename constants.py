# Values constant between everything

VERSION = "v1.0.1"

INPUT_TEAMS_FILE = 1
INPUT_STUDENT_FILE = 2
OUTPUT_XLSX = 3
VALID_EXTENSIONS = ["xlsx", "xls", "csv"]

# Frame names
INPUT_TEAMS_FRAME = "frame_grade_csv"
INPUT_STUDENT_FRAME = "frame_student_xlsx"
OUTPUT_XLSX_FRAME = "frame_output_xlsx"

# File Information
# Student Logins description:
#   * Saved as an Excel 2007 Workbook (.xlsx), columns B:L are used.
#   * Rows 1:3 are unused or "metadata"
#   * Only columns of interest are E (student IDs) and H (usernames - email addresses)
#   * Other columns:    B - Line
#                       C - Teacher
#                       D - Period
#                       F - Grade level
#                       G - Student name (Last, First Suffix)
#                       I - Password (unless reset)
#                       J - Password reset by
#                       K - None
#                       L - Date password was reset
STUDENT_LOGINS = {"header": 3, "usecols": ["StuID", "Username"]}
# Teams grades description:
#   * Saved as CSV, 6 columns
#   * First row contains headers, and every other row is just text by default
#   * Column 4 (D) header is the assignment name
#   * Other columns:    0 (A) - First Name
#                       1 (B) - Last Name
#                       2 (C) - Email Address
#                       3 (D) - Points earned
#                       4 (E) - Total point for the assignment
#                       5 (F) - Feedback, if present
#   * Example row: "Dylan","Armitage","dylanjarmitage@gmail.com","18","20","=""Feedback is here only"""
#   * Yes, that is a messed up way of storing CSV data
#   * First name and last name aren't necessarily the student's actual first and last name,
#       especially if they have more than one
#   * If the file is an export of all the grades, then the number of columns is unknown but should be a multiple of 3:
#       columns 3,4,5 repeat for each assignment, with the most recent assignment being the "first" one.
#       * Example row (header):
#           "First Name","Last Name","Email Address","Unit 2 Quiz","Points","Feedback","Unit 1 Quiz","Points","Feedback"
#       * TODO: May need to create some sort of structure/class/etc. to load multiple assignments properly.
TEAMS_CSV = {"usecols": [2, 3]}
