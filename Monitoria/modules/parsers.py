# Disclaimer: This was intentionally not implemented with pandas for portability reasons, but it could be implemented in a more slick and elegant way using that module
from modules.common import targets

def already_done(file):
    from os.path import isfile
    if isfile(file):
        print("\033[93mActivity has already been accounted for. Overwrite? (yes/no)\033[0m")
        ans = input("> ")
        return ans.lower() not in ('y', 'yes')
    else:
        return False

def check_files(files = [], only_one = True):
    '''
        Input: Array containing file names and if there can be more than one file
        Raises: Invalid input if array is empty, AmbiguousFileError if files are ambiguous.
    '''
    from modules.errors import InvalidInputError, AmbiguousFileError

    # Seek for copies in files
    copy_strings = [ f"({i})" for i in range(10) ]
    for elem in copy_strings:
        for file in files:
            if elem in file:
                raise AmbiguousFileError("Found possible duplicate files:", files)

    if len(files) == 0:
        raise InvalidInputError("No files found!")
    elif only_one:
        if len(files) > 1:
            raise AmbiguousFileError("Multiple files found for this class", files)
    else:
        pass

    return 

def dicts_not_ordered():
    '''
        Tests if dicts keys and values remain in the order they were added. This should be default for python 3.6+, but its always better to be in the safe side
    '''
    d1 = {}
    d1['a'] = 'A'
    d1['b'] = 'B'
    d1['c'] = 'C'
    d1['d'] = 'D'
    d1['e'] = 'E'

    d2 = {}
    d2['e'] = 'E'
    d2['d'] = 'D'
    d2['c'] = 'C'
    d2['b'] = 'B'
    d2['a'] = 'A'
    return d1 != d2

def seek_column_index(file, strings = [], sep = ',', persist = True):
    '''
        Description: Seeks in file (default is CSV) the column index that contains each string.
        Input: <File name>, <strings to seek in columns>, <IFS of file>.
        Output: Tuple containing the corresponding index of each string given in input. If a string is not found return -1 as its index.
        Disclaimer: In python3.6+ dicts hold the order in which they where created, which guarantees that the returned tuple will be in the correct order. If you're running this in a older version of python the module ordereddic from collections will be needed.
    '''

    from sys import version_info
    from modules.errors import InvalidInputError
    if version_info < (3, 6) or dicts_not_ordered():
        from collections import OrderedDic
        indexes = OrderedDic()
    else:
        indexes = {}

    indexes = {}
    for string in strings:
        indexes[string] = -1

    with open(file, 'r') as f:
        fields = f.readline().strip().rsplit(sep)
        index = 0
        for field in fields:
            for string in strings:
                if string in field.lower():
                    indexes[string] = index
                    break
                else:
                    pass
            index += 1

    if -1 in indexes.values():
        if persist:
            # Try with ' ' as IFS
            print("try 1")
            indexes = {}
            for string in strings:
                indexes[string] = -1

            with open(file, 'r') as f:
                fields = f.readline().strip().rsplit(' ')
                index = 0
                for field in fields:
                    for string in strings:
                        if string in field.lower():
                            indexes[string] = index
                            break
                        else:
                            pass
                    index += 1

            # Try again seeking "nusp-like" and "grade-like" numbers
#            if -1 in indexes.values():
#                print("try 2")
#                indexes = {}
#                for string in strings:
#                    indexes[string] = -1
#                with open(file, 'r') as f:
#                    fields = f.readline().strip().rsplit(sep)
#                    index = 0
#                    for field in fields:
#                        if field.isnumeric():
#                            if int(field) > 10000:
#                                indexes['nusp'] = index
#                        else:
#                            try:
#                                num = float(field)
#                            except ValueError:
#                                pass
#                            else:
#                                indexes['avaliar'] = index # Standard names for the grades string
#                                indexes['nota'] = index #
#                        index += 1

    pos = 0
    for value in indexes.values():
        if value == -1:
            raise InvalidInputError(f"No matching column for string \'{strings[pos]}\' found in file \'{file}\' \n > Header: {fields}")
        else:
            pos += 1

    return tuple(indexes.values())

def parse_by_nusp(turma, activity = '', num = 0, target = '/home/ariel/Downloads', identifiers = ['usp', 'avaliar'] , sep = ',', persist = True):
    '''
    INPUT:
        Object <Turma> defined in the modules.common module (Essentially a list of tuples containing the name, nusp and group of the students)
        Activity type: 'qp' or 'list'. Custom types may be implemented
        Number of the activity. For list with parts the input may contain a letter e.g. 1a, 1b, 5d, etc
    OUTPUT: Saves "nusp, grade" in file in the corresponding directory under ./grades and prints *only* the grades in *alphabetical* order.
    DESCRIPTION: Seeks for the files containing the grades of the students (default location is ~/Downloads) and parses then keeping only the largest grade for each student (if no grades are found then attributes 0).
    '''
    from modules.common import search_dir, nth_repl, Turma
    
    # Determines the unique set of substrings for the given activity type that identify the grades file
    only_one = True
    if activity == 'qp':
        unique_strings =  ['QPrev', f'aula {num}-'] #the - here is to differentiate '1' from '11', for example
    elif activity == 'list':
        num_part = ''
        char_part = ''
        for char in str(num):
            if char.isdigit():
                num_part = num_part + char
            else:
                char_part = char_part + char
        unique_strings = [f'Lista {num_part}', 'notas']
        if char_part != '':
            unique_strings.append(f"parte {char_part.upper()}")
    elif activity == 'exam':
        unique_strings = [f'Prova {num}']
    elif activity == 'mid_exam':
        unique_strings = [f'Provinha {num}']
    else:
        print(f"Invalid activity type {activity}")
        return 1

    if already_done(f'{targets[activity]}/{activity}_{num}.csv'):
        return 

    files = search_dir(target, unique_strings)
    check_files(files, only_one)

    print("Found files:")
    for file in files:
        print(f"\033[38;5;2m{file}\033[0m")

    # Locates the indexes of the columns containing the nusps and the grades
    nusp_idx, grade_idx = seek_column_index(target + '/'  + files[0], identifiers, sep, persist)

    final_grades = {}
    for nusp in turma.nusps.values():
        final_grades[nusp] = 0

    for file in files:
        grades = {}
        file = target + '/' + file
        with open(file, 'r') as f:
            next(f)
            for line in f.read().splitlines():
                fields = line.rsplit(',')

                nusp = fields[nusp_idx]
                grade = str(fields[grade_idx])
                if '-' in grade or grade == '':
                    grade = 0.
                elif len(fields) <= 2:
                    grade = float(fields[grade_idx])
                else:
                    # The grades are comma separated numbers <SIGH>,
                    # so we need to join then.
                    grade = grade + '.' + str(fields[grade_idx + 1])
                    # They are also surrounded by " that need to be removed.
                    grade = grade.replace('\"', '')
                    grade = float(grade)

                if nusp in turma.nusps.values():
                    if nusp in grades.keys():
                        if grade >= grades[nusp]:
                            grades[nusp] = grade
                        else:
                            pass
                    else:
                        grades[nusp] = grade
                else:
                    pass
        for nusp, grade in grades.items():
            if nusp in final_grades.keys():
                final_grades[nusp] += grade
            else:
                final_grades[nusp] = grade
    
    for nusp in final_grades.keys():
        final_grades[nusp] /= len(files)

    turma.sort()
    outf = open(f'{targets[activity]}/{activity}_{num}.csv', "w+")
    for name, nusp, group in turma.students:
        outf.write(f"{nusp},{final_grades[nusp]}\n")
        print(f"{final_grades[nusp]}")
    outf.close()

def parse_by_group(turma, activity = '', num = 0, target = '/home/ariel/Downloads', identifiers = ['usp', 'avaliar'], sep =',', persist = True):
    '''
    INPUT:
        1) Object <Turma> defined in the modules.common module (Essentially a list of tuples containing the name, nusp and group of the students)
        2) Activity type: 'atc'. No other activity is parsed by group, but a custom one could be implemented
        3) Number of the activity.
    OUTPUT: Saves "nusp, grade" in file in the corresponding directory under ./grades and prints *only* the grades in *alphabetical* order.
    DESCRIPTION: Seeks for the files containing the grades of the students (default location is ~/Downloads) and parses then keeping only the largest grade for each group (if no grades are found then attributes 0). The average grade is determined for each group (always selecting the highest grade for any given group member present in each file) and then distributes it accordingly. For ATCs the attendance of each class is taken into account, and students that weren't in class will end up with 0.
    '''
    from modules.common import search_dir, Turma
    
    # Determines the unique set of substrings for the given activity type that identify the file containing the grades
    if activity == 'atc':
        unique_strings = [f'ATC-{int(num):02d}']
        only_one = False
    else:
        print(f"Invalid activity type {activity}")
        return 1

    if already_done(f'{targets[activity]}/{activity}_{num}.csv'):
        return

    files = search_dir(target, unique_strings)
    check_files(files, only_one)

    print("Found files:")
    for file in files:
        print(f"\033[38;5;2m{file}\033[0m")

    # Accounts the attendance of the given class
    freqs = {}
    try:
        freq_file = open(f'{targets["freq"]}/freq_{num}.csv', 'r')
    except FileNotFoundError:
        print("No attendance was made for this class, aborting.")
        return 1
    else:
        for line in freq_file.read().splitlines():
            nusp, group = line.split(',')
            freqs[nusp] = str(group)
        for name, nusp in turma.nusps.items():
            if str(nusp) not in freqs.keys():
                print(f"Warning! Student {name} - {nusp} was not in the attendance!")
                freq[str(nusp)] = '0'

    # Locates the indexes of the columns containing the nusps and the grades
    nusp_idx, grade_idx = seek_column_index(target + '/' + files[0], identifiers, sep, persist)

    final_grades = {}
    for nusp in turma.nusps.values():
        final_grades[nusp] = 0

    final_groups = {}
    for group in set(turma.groups.values()):
        final_groups[group] = 0

    for file in files:
        file = target + '/' + file
        grades = {}
        group_grades = {}
        with open(file, 'r') as f:
            next(f)
            for line in f.read().splitlines():
                fields = line.rsplit(',')

                nusp = fields[nusp_idx]
                grade = str(fields[grade_idx])
                if '-' in grade or grade == '':
                    grade = 0.
                else:
                    # The grades are comma separated numbers <SIGH>,
                    # so we need to join then.
                    grade = grade + '.' + str(fields[grade_idx + 1])
                    # They are also surrounded by " that need to be removed.
                    grade = grade.replace('\"', '')
                    grade = float(grade)

                if nusp in turma.nusps.values():
                    group = turma.groups[nusp]
                    if group in group_grades.keys():
                        if grade >= group_grades[group]:
                            group_grades[group] = grade
                        else:
                            pass
                    else:
                        group_grades[group] = grade
                else:
                    pass
        for group, grade in group_grades.items():
            if group in final_groups.keys():
                final_groups[group] += grade
            else:
                final_groups[group] = grade
    
    final_groups['0'] = 0
    for key in final_groups.keys():
        final_groups[key] /= len(files)
    for nusp in turma.nusps.values():
        final_grades[nusp] = final_groups[ freqs[nusp] ]

    turma.sort()
    outf = open(f'{targets[activity]}/{activity}_{num}.csv', "w+")
    for name, nusp, group in turma.students:
        outf.write(f"{nusp},{final_grades[nusp]}\n")
        print(f"{final_grades[nusp]}")
    outf.close()

def attendance(turma, aula):
    '''
    Using a iterative menu, takes account of the attendance of a given class

    Usage: Hit enter do attribute the students default group (for the current attendance list) or type in a valid group (invalid groups are discarded). Pressing 0 imedetly accounts an absence. Upon a valid input skips to the next student. Use directional arrows to move up and down the menu, <esc> escapes. You can overwrite the attendance of a student by just going back to him. Please be aware that if no mistakes are made (and there is no students in different groups) you can make the attendance ONLY pressing 0 and enter, which is pretty cool.
    '''
    from modules.menu import create_menu, abbreviate_name

    if already_done(f'{targets["freq"]}/freq_{aula}.csv'):
        return

    # Abbreviates middle names for a better display (and to complicate the code). Maps nusps to abbreviated names.
    names = [ abbreviate_name(n) for n in turma.names ]
    nusps = { abbreviate_name(n) : nusp for n, nusp in turma.nusps.items()}
    dv = [turma.groups[nusp] for nusp in turma.nusps.values() ]

    result = create_menu(names, dv)

    outf = open(f'{targets["freq"]}/freq_{aula}.csv', "w+")
    for name, freq in result.items():
        if name != '':
            outf.write(f"{nusps[name]},{freq.replace(' ','')}\n")
        else:
            pass
    outf.close()
    
    end_result = {}
    for name, freq in result.items():
        if name != '':
            end_result[nusps[name]] = freq.replace(' ','')

    turma.sort()
    for name, nusp, group in turma.students:
        print(end_result[nusp])

    return

if __name__ == '__main__':
    '''
        Tests the functions with a dummy class when called as main
    '''
    from modules.dummy_class import dummy_class
    from modules.fake_grades import fake_grades, fake_attedence

    students = 10
    activity = 'list'
    turma = dummy_class(students)

    for name, nusp, group in turma.students:
        print(f'{name} - {nusp} - {group}')
    print('-' * 70)

    num = '1a'
    fake_grades(turma, num, activity, './')
    fake_attedence(turma, num)

    if activity == 'act':
        parse_by_group(turma, activity, num) 
    else:
        parse_by_nusp(turma, activity, num) 

    exit(0)

