# Disclaimer: This was intentionally not implemented with pandas for portability reasons, but it could be implemented in a more suscint and elegant way using that module

def parse_grades(turma, activity = '', num = 0):
    '''
    INPUT: List of tuples containing the name, nusp and group of the students, number of the class
    OUTPUT: Saves "grade, nusp" in file in ./grades/qprev and prints >only< the the grades in *alphabetical* order
    '''
    from modules.common import search_dir, change_last, Turma

    unique_strings = {
            'qp' : ['QPrev', f'aula {num}'],
            'atc' : ['ATC', f'{num:02d}'],
            'list' : ['Lista {num}', 'notas']
            }

    files = search_dir('./', unique_strings[activity])

    if len(files) == 0:
        print("\033[38;5;1mNo files found for this class\033[0m")
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
            freq_file = open('./grades/freqs/aula_{num}.csv', 'r')
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
            print('-' * 70)
            print(file)
            print('-' * 70)
            for line in f.read().splitlines():
                print(line)
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

def atc_parse(turma, aula):
    '''
    INPUT: List of tuples containing the name, nusp and group of the students, number of the class
    OUTPUT: Saves "grade, nusp" in file in ./grades/atc and prints >only< the the grades in *alphabetical* order
    '''
    from modules.common import search_dir, change_last, sort_class

    nusps = []
    groups = {}

    try:
        freq_file = open('./grades/freqs/aula_{aula}.csv', 'r')
        for line in freq_file.read().splitlines():
            nusp, group = line.split(',')
            nusps.append(nusp)
            groups[nusp] = str(group)
    except FileNotFoundError:
        print("No attedance was made for this class")
        return 1

    final_grades = {}
    for name, nusp, group in turma.students:
        final_grades[group] = 0

        if str(nusp) not in groups.keys():
            print(f"Warning! Student {name} - {nusp} was not in the attedence!")
            groups[str(nusp)] = '0'

    activityivity_strings = ['ATC', f'{aula:02d}']
    files = search_dir('./', activityivity_strings)

    partes = [ f"parte {i}" for i in range(4) ]
    for parte in partes:
        for file in files:
            matches = []
            if parte in file:
                matches.append(file)
            if len(matches) > 1:
                print("Warning! Multiple files found for part {parte}:")
                for f  in matches:
                    print(f)
                return 1
            else:
                pass

    if len(files) == 0:
        print("\033[38;5;1mNo files found for this class\033[0m")
        return 1
    else:
        print(f"\033[38;5;2mFound files {files}\033[0m")
        pass

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
            exit(0)

    for file in files:
        grades = {}
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

                if nusp in nusps:
                    group = groups[nusp]
                    if group in grades.keys():
                        if grade >= grades[group]:
                            grades[group] = grade
                        else:
                            pass
                    else:
                        grades[group] = grade
                else:
                    pass
        for group, grade in grades.items():
            if group in final_grades.keys():
                final_grades[group] += grade
            else:
                final_grades[group] = grade
    
    for key in final_grades.keys():
        final_grades[key] /= len(files)
    final_grades['0'] = 0

    for group, grade in final_grades.items():
        print(f"{group} - {grade}")

    print('-' * 40)

    turma.sort()
    for name, nusp, group in turma.students:
        print(f"{nusp} - {final_grades[group]}")
def list_parse(turma, num, parte = ''):
    '''
    INPUT: List of tuples containing the name, nusp and group of the students, number of the list
    OUTPUT: Saves "grade, nusp" in file in ./grades/list and prints >only< the the grades in *alphabetical* order
    '''
    from modules.common import search_dir, change_last, sort_class

    nusps = []

    final_grades = {}
    for name, nusp, group in turma:
        final_grades[group] = 0

    activityivity_strings = ['Lista {num}', 'notas']
    if parte != '':
        activityivity_strings.append(f'parte {parte}')
    files = search_dir('./', activityivity_strings)

    if len(files) > 1:
        print("Warning! Multiple files found:")
        for file in files:
            print(f"\033[38;5;3m{file}\033[0m")
        print("Exiting before it's too late :o")
        return 1
    elif len(files) == 0:
        print("\033[38;5;1mNo files found for this class\033[0m")
        return 1
    else:
        print(f"\033[38;5;2mFound files {files}\033[0m")
        pass

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
            exit(0)

    grades = {}
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

            if nusp in nusps:
                if nusp in grades.keys():
                    if grade >= grades[nusp]:
                        grades[nusp] = grade
                    else:
                        pass
                else:
                    grades[group] = grade
            else:
                pass

    for nusp, grade in grades.items():
        print(f"{nusp} - {grade}")

if __name__ == '__main__':
    from modules.dummy_class import dummy_class
    from modules.fake_grades import fake_grades, fake_attedence

    students = 10
    activity = 'atc'
    turma = dummy_class(students)

    for name, nusp, group in turma.students:
        print(f'{name} - {nusp} - {group}')
    print('-' * 70)

    num = 98
    fake_grades(turma, num, activity, './')
    fake_attedence(turma, num)

    parse_grades(turma, activity, num) 

    exit(0)

