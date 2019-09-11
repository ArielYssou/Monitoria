# Monitoria

 Parses grades imported from moodle (seeks for files in the directory ~/Downloads by default) and arranges then for easy exportation and storage. Can take account of the attendance of a given class inputted by the user using a interactive menu. Can also establish new group formations based on grades and average attendance of each student.

##Synopsis
        monitoria.sh [-h] [-f <class number>] [-q <class number>] [-a <class number>] [-l <list number>] [-e <exam number>] [-m mid-exam number ] [-t (f|q|a|l|e|m|g)] [-g] [-s] [-r]

##Options
	-h|     This help text
	-f|     Attendance of a class. Prompts the user with  interactive menu where he/her can enter the attendance of each student (i.e. the group the student was in the given class). Hitting 0 will assign a vacancy for the student and <Enter> will assign the student current group automatically. Use the directional keys <Up> <Down> to move around the menu and make any changes necessary. <Esc> escapes. After execution, prompts the attendances in alphabetical order for exportation.
	-q|     QPrevs. Parsers the QPrev activity for a given class.
	-a|     ATCs. Parses the ATC activity for a given class considering the attendance (Vacant students will not receive grades). Take the average grade for each group considering all parts of the ATC, and then assign grades by group for each student.
	-l|     Lists. Parses the grades of a list. Inputs like 1a or 2b will assume a list that has different parts (like "1 (parte a)").
        -e|     Exams. Passes the grades of a exam. ***The file is expected to have a header line containing 'nusp,nota'***.
        -m|     Mid-Exams (provinhas). Parses the grades for a mid exam. Also expects the header 'nusp,nota'.
	-g|     Composes a new attendance list based on the average grade of each student and his/hers attendance up to the most recent class. Prompts the user until he/her is satisfied or wishes to exit. Changes only take place when a new list is explicitly accepted.
        -t|     Run a test between {q,a,l,e,m,g} for each functionality mentioned above (with the same char characterizing it). Uses a "dummy" class and removes any new files upon completion.
