# Disclaimer: This was intentionally not implemented with pandas for portability reasons, but it could be implemented in a more suscint and elegant way using that module

def check_files(files = [], only_one = True):
    if len(files) == 0:
        raise NoFilesFoundError
    elif only_one:
        if len(files) > 1:
            print("\033[38;5;1mMultiple files found:\033[0m")
            for file in files:
                print(f"\033[38;5;1m{file}\033[0m")
            return 1

    copy_strings = [ f"({i})" for i in range(10) ] 
    for elem in copy_strings:
        for file in files:
            if elem in file:
                print(f"Found a possible duplicate file: {file}. Aborting")
                return 1

def parse_by_nusp(turma, activity = '', num = 0, target = './'):
    '''
    INPUT:
        Object <Turma> defined in the modules.common module (Essentially a list of tuples containing the name, nusp and group of the students)
        Activity type: 'qp', 'atc' or 'list'
        Number of the activity. For list with parts the input may contain a letter e.g. 1a, 1b, 5d, etc
    OUTPUT: Saves "nusp, grade" in file in the corresponding directory under ./grades and prints *only* the the grades in *alphabetical* order.
    DESCRIPITION: Seeks for the files containing the grades of the students (default location is ~/Dowloads) and parses then keeping only the largest grade for each student (if no grades are found then atributes 0). If the activity has several parts (ATCs) then the average grade is determined for each group (always selecting the highest grade for any given group member present in each file) and then distributes it accordingly. For ATCs the attedence of each class is taken into account, and students that wheren't in class will end up with 0.
    '''
    from modules.common import search_dir, change_last, Turma
    
    # Determines the unique set of substrings for the given activity type that indentify the file containing the grades
    if activity == 'qp':
        unique_strings =  ['QPrev', f'aula {num}']
        only_one = True
    elif activity == 'atc':
        unique_strings = ['ATC', f'{num:02d}']
        only_one = False
    elif activity == 'list':
        num_part = ''
        char_part = ''
        for char in num:
            if char.isdigit():
                num_part = num_part + char
            else:
                char_part = char_part + char
        unique_strings = [f'Lista {num_part}', 'notas']
        if char_part != '':
            unique_strings.append(f"parte {char_part.upper()}")
        only_one = True
    else:
        print(f"Invalid activity type {activity}")
        return 1

    files = search_dir(target, unique_strings)

    if len(files) == 0:
        print("\033[38;5;1mNo files found for this class\033[0m")
        return 1
    elif only_one:
        if len(files) > 1:
            print("\033[38;5;1mMultiple files found:\033[0m")
            for file in files:
                print(f"\033[38;5;1m{file}\033[0m")
            return 1

    copy_strings = [ f"({i})" for i in range(10) ] 
    for elem in copy_strings:
        for file in files:
            if elem in file:
                print(f"Found a possible duplicate file: {file}. Aborting")
                return 1

    print("Found files:")
    for file in files:
        print(f"\033[38;5;2m{file}\033[0m")

    if activity == 'atc':
        try:
            freq_file = open(f'./grades/freqs/aula_{num}.csv', 'r')
            freqs = {}
            for line in freq_file.read().splitlines():
                nusp, group = line.split(',')
                freqs[nusp] = str(group)
        except FileNotFoundError:
            print("No attedance was made for this class, aborting.")
            return 1
        for name, nusp in turma.nusps.items():
            if str(nusp) not in freqs.keys():
                print(f"Warning! Student {name} - {nusp} was not in the attedence!")
                freq[str(nusp)] = '0'
    else:
        pass

    # Locates the indexes of the columns containing the nusps and the grades
    with open(files[0]) as f:
        fields = f.readline().strip().rsplit(',')
        nusp_idx = -1
        grade_idx = -1
        index = 0
        for field in fields:
            if 'usp' in field.lower():
                nusp_idx = index
            elif 'avaliar' in field.lower():
                grade_idx = index
            else:
                pass
            index += 1
        if -1 in (nusp_idx, grade_idx):
            print("Could not find columns with nusp or grades!")
            return 1

    final_grades = {}
    for nusp in turma.nusps.values():
        final_grades[nusp] = 0

    final_groups = {}
    for group in set(turma.groups):
        final_groups[group] = 0

    for file in files:
        grades = {}
        group_grades = {}
        with open(file, 'r') as f:
            next(f)
            for line in f.read().splitlines():
                line = change_last(line, '-', '0,0')
                line = change_last(line, ',', '.')
                fields = line.rsplit(',')

                nusp = fields[nusp_idx]
                grade = str(fields[grade_idx])
                grade = grade.replace('\"', '')
                grade = float(grade.replace(',', '.'))

                if nusp in turma.nusps.values():
                    if activity == 'atc':
                        group = turma.groups[nusp]
                        if group in group_grades.keys():
                            if grade >= group_grades[group]:
                                group_grades[group] = grade
                            else:
                                pass
                        else:
                            group_grades[group] = grade
                    else:
                        if nusp in grades.keys():
                            if grade >= grades[nusp]:
                                grades[nusp] = grade
                            else:
                                pass
                        else:
                            grades[nusp] = grade
                else:
                    pass
        if activity == 'atc':
            for group, grade in group_grades.items():
                if group in final_groups.keys():
                    final_groups[group] += grade
                else:
                    final_groups[group] = grade
        else:
            for nusp, grade in grades.items():
                if nusp in final_grades.keys():
                    final_grades[nusp] += grade
                else:
                    final_grades[nusp] = grade
    
    if activity == 'atc':
        final_groups['0'] = 0
        for key in final_groups.keys():
            final_groups[key] /= len(files)
        for nusp in turma.nusps.values():
            final_grades[nusp] = final_groups[ freqs[nusp] ]
    else:
        for nusp in final_grades.keys():
            final_grades[nusp] /= len(files)

    turma.sort()
    for name, nusp, group in turma.students:
        print(f"{nusp} - {final_grades[nusp]}")

def parse_by_group(turma, activity = '', num = 0, target = './'):
    '''
    INPUT:
        Object <Turma> defined in the modules.common module (Essentially a list of tuples containing the name, nusp and group of the students)
        Activity type: 'atc'. No other activity is parsed by group, but a custom one could be implemented
        Number of the activity. For list with parts the input may contain a letter e.g. 1a, 1b, 5d, etc
    OUTPUT: Saves "nusp, grade" in file in the corresponding directory under ./grades and prints *only* the the grades in *alphabetical* order.
    DESCRIPITION: Seeks for the files containing the grades of the students (default location is ~/Dowloads) and parses then keeping only the largest grade for each student (if no grades are found then atributes 0). If the activity has several parts (ATCs) then the average grade is determined for each group (always selecting the highest grade for any given group member present in each file) and then distributes it accordingly. For ATCs the attedence of each class is taken into account, and students that wheren't in class will end up with 0.
    '''
    from modules.common import search_dir, change_last, Turma
    
    # Determines the unique set of substrings for the given activity type that indentify the file containing the grades
    if activity == 'atc':
        unique_strings = ['ATC', f'{num:02d}']
        only_one = False
    else:
        print(f"Invalid activity type {activity}")
        return 1

    files = search_dir(target, unique_strings)

    if len(files) == 0:
        print("\033[38;5;1mNo files found for this class\033[0m")
        return 1
    elif only_one:
        if len(files) > 1:
            print("\033[38;5;1mMultiple files found:\033[0m")
            for file in files:
                print(f"\033[38;5;1m{file}\033[0m")
            return 1

    copy_strings = [ f"({i})" for i in range(10) ] 
    for elem in copy_strings:
        for file in files:
            if elem in file:
                print(f"Found a possible duplicate file: {file}. Aborting")
                return 1

    print("Found files:")
    for file in files:
        print(f"\033[38;5;2m{file}\033[0m")

    if activity == 'atc':
        try:
            freq_file = open(f'./grades/freqs/aula_{num}.csv', 'r')
            freqs = {}
            for line in freq_file.read().splitlines():
                nusp, group = line.split(',')
                freqs[nusp] = str(group)
        except FileNotFoundError:
            print("No attedance was made for this class, aborting.")
            return 1
        for name, nusp in turma.nusps.items():
            if str(nusp) not in freqs.keys():
                print(f"Warning! Student {name} - {nusp} was not in the attedence!")
                freq[str(nusp)] = '0'
    else:
        pass

    # Locates the indexes of the columns containing the nusps and the grades
    with open(files[0]) as f:
        fields = f.readline().strip().rsplit(',')
        nusp_idx = -1
        grade_idx = -1
        index = 0
        for field in fields:
            if 'usp' in field.lower():
                nusp_idx = index
            elif 'avaliar' in field.lower():
                grade_idx = index
            else:
                pass
            index += 1
        if -1 in (nusp_idx, grade_idx):
            print("Could not find columns with nusp or grades!")
            return 1

    final_grades = {}
    for nusp in turma.nusps.values():
        final_grades[nusp] = 0

    final_groups = {}
    for group in set(turma.groups):
        final_groups[group] = 0

    for file in files:
        grades = {}
        group_grades = {}
        with open(file, 'r') as f:
            next(f)
            for line in f.read().splitlines():
                line = change_last(line, '-', '0,0')
                line = change_last(line, ',', '.')
                fields = line.rsplit(',')

                nusp = fields[nusp_idx]
                grade = str(fields[grade_idx])
                grade = grade.replace('\"', '')
                grade = float(grade.replace(',', '.'))

                if nusp in turma.nusps.values():
                    if activity == 'atc':
                        group = turma.groups[nusp]
                        if group in group_grades.keys():
                            if grade >= group_grades[group]:
                                group_grades[group] = grade
                            else:
                                pass
                        else:
                            group_grades[group] = grade
                    else:
                        if nusp in grades.keys():
                            if grade >= grades[nusp]:
                                grades[nusp] = grade
                            else:
                                pass
                        else:
                            grades[nusp] = grade
                else:
                    pass
        if activity == 'atc':
            for group, grade in group_grades.items():
                if group in final_groups.keys():
                    final_groups[group] += grade
                else:
                    final_groups[group] = grade
        else:
            for nusp, grade in grades.items():
                if nusp in final_grades.keys():
                    final_grades[nusp] += grade
                else:
                    final_grades[nusp] = grade
    
    if activity == 'atc':
        final_groups['0'] = 0
        for key in final_groups.keys():
            final_groups[key] /= len(files)
        for nusp in turma.nusps.values():
            final_grades[nusp] = final_groups[ freqs[nusp] ]
    else:
        for nusp in final_grades.keys():
            final_grades[nusp] /= len(files)

    turma.sort()
    for name, nusp, group in turma.students:
        print(f"{nusp} - {final_grades[nusp]}")

if __name__ == '__main__':
    from modules.dummy_class import dummy_class
    from modules.fake_grades import fake_grades, fake_attedence

    students = 10
    activity = 'list'
    turma = dummy_class(students)

    for name, nusp, group in turma.students:
        print(f'{name} - {nusp} - {group}')
    print('-' * 70)

    num = '1b'
    fake_grades(turma, num, activity, './')
    fake_attedence(turma, num)

    parse_grades(turma, activity, num) 

    exit(0)

