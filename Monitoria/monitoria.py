from sys import argv
from modules.common import Turma, load_turma

def helper():
    print(
	'''
        monitoria.sh 
Description:
	monirotia.sh: Parses grades imported from moodle (seeks for files in the directory ~/Downloads by default) and arranges then for easy exportation and storage. Can take account of the attendance of a given class inputted by the user using a interactive menu. Also establishes new group formations based on grades and mean attendance of each student.

Synopsis
        monitoria.sh [-h] [-f <class number>] [-q <class number>] [-a <class number>] [-l <list number>] [-e <exam number>] [-m mid-exam number ] [-t (f|q|a|l|e|m|g)] [-g] [-s] [-d] [-r]

Options
	-h|     This help text
	-f|     Attendance of a class. Prompts the user with  interactive menu where he/her can enter the attendance of each student (i.e. the group the student was in the given class). Hitting 0 will assign a vacancy for the student and <Enter> will assign the student current group automatically. Use the directional keys <Up> <Down> to move around the menu and make any changes necessary. <Esc> escapes. After execution, prompts the attendances in alphabetical order for exportation.
	-q|     QPrevs. Parsers the QPrev activity for a given class.
	-a|     ATCs. Parses the ATC activity for a given class considering the attendance (Vacant students will not receive grades). Take the average grade for each group considering all parts of the ATC, and then assign grades by group for each student.
	-l|     Lists. Parses the grades of a list. Inputs like 1a or 2b will assume a list that has different parts (like "1 (parte a)").
        -e|     Exams. Passes the grades of a exam. ***The file is expected to have a header line containing 'nusp,nota'***.
        -m|     Mid-Exams (provinhas). Parses the grades for a mid exam. Also expects the header 'nusp,nota'.
	-g|     Composes a new attendance list based on the average grade of each student and his/hers attendance up to the most recent class. Prompts the user until he/her is satisfied or wishes to exit. Changes only take place when a new list is explicitly accepted.
        -t|     Run a test between {q,a,l,e,m,g} for each functionality mentioned above (with the same char characterizing it). Uses a "dummy" class and removes any new files upon completion.
        -s|     [WIP] Setup. Checks if modules and directories are in place, checks all dependencies
        -d|     [WIP] Prints all dependencies.
        -r|     [WIP] Data analysis and visualization for: Grades evolution, correlations between activities, evolution of average attendance. Connectivity graph between students.

Author
	Ariel Yssou arielyssou@gmail.com

Bugs
	In the modules.parsers.attendance the menu was supposed to go tot he next empty field after a valid input, but it only goes down.
       ''' 
        )
    
if __name__ == '__main__':
    aulas = list(filter(lambda x : x.isnumeric(), argv))
    if '-f' in argv:
        from modules.parsers import attendance
        turma = load_turma()
        for aula in aulas:
            attendance(turma, aula)

    elif '-q' in argv:
        from modules.parsers import parse_by_nusp
        activity = 'qp'
        turma = load_turma()
        for aula in aulas:
            parse_by_nusp(turma, activity, aula)

    elif '-l' in argv:
        from modules.parsers import parse_by_nusp
        activity = 'list'
        turma = load_turma()
        for entry in argv[2:]:
            parse_by_nusp(turma, activity, entry)

    elif '-a' in argv:
        from modules.parsers import parse_by_group
        activity = 'atc'
        turma = load_turma()
        for aula in aulas:
            parse_by_group(turma, activity, aula)

    elif '-e' in argv:
        from modules.parsers import parse_by_nusp
        activity = 'exam'
        turma = load_turma()
        for aula in aulas:
            parse_by_nusp(turma, activity, aula, identifiers = ['usp', 'nota'])

    elif '-m' in argv:
        from modules.parsers import parse_by_nusp
        activity = 'mid_exam'
        turma = load_turma()
        for aula in aulas:
            parse_by_nusp(turma, activity, aula, identifiers = ['usp', 'nota'])

    elif '-t' in argv:
        import modules.tests as ts
        if 'f' in argv[2:]:
            ts.test_attendance()
        elif 'q' in argv[2:]:
            ts.test_nusp_activity('qp')
        elif 'l' in argv[2:]:
            ts.test_nusp_activity('list')
        elif 'e' in argv[2:]:
            ts.test_nusp_activity('exam')
        elif 'a' in argv[2:]:
            ts.test_nusp_activity('atc')
        elif 'g' in argv[2:]:
            ts.test_groups_forge()
        else:
            pass

    elif '-g' in argv:
        from modules.forge_groups import forge_groups
        turma = load_turma()
        forge_groups(turma)

    elif '-h' in argv:
        helper()
    else:
        print("Incorrect input. Usage:")
        helper()


