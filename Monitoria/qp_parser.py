# Disclaimer: This was intentionally not implemented with pandas for portability reasons, but it could be implemented in a more suscint and elegant way using that module


def qp_parse(turma, aula):
    '''
    INPUT: List of tuples containing the name, nusp and group of the students, number of the class
    OUTPUT: Saves "grade, nusp" in file in ./grades/qprev and prints >only< the the grades in *alphabetical* order
    '''
    from modules.common import search_dir, change_last

    activity_strings = ['QPrev', f'aula {aula}']

    files = search_dir('./', activity_strings)

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
        print(f"\033[38;5;2mFound file {files[0]}\033[0m")
        pass

    names = []
    nusps = []
    groups = []

    for name, nusp, group in turma:
        names.append(name)
        nusps.append(str(nusp))
        groups.append(group)

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
    with open(files[0], 'r') as dfile:
        next(dfile)
        for line in dfile.read().splitlines():
            # We make the assumption that the grades are in the last column, if tihs is not true the next two lines have to be adjusted
            #if '-' in line:
            line = change_last(line, '-', '0,0') # Regularizes the last column
            line = change_last(line, ',', '.') # Converts comma separated numbers

            fields = line.rsplit(',')

            name = fields[1] + ' ' + fields[0] #Not used, but kept just in case
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
                    grades[nusp] = grade
            else:
                pass

    for nusp, grade in grades.items():
        print(f"{nusp} - {grade}")

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
    for name, nusp, group in turma:
        final_grades[group] = 0

        if str(nusp) not in groups.keys():
            print(f"Warning! Student {name} - {nusp} was not in the attedence!")
            groups[str(nusp)] = '0'

    activity_strings = ['ATC', f'{aula:02d}']
    files = search_dir('./', activity_strings)

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

    sort_class(turma)
    for name, nusp, group in turma:
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

    activity_strings = ['Lista {num}', 'notas']
    if parte != '':
        activity_strings.append(f'parte {parte}')
    files = search_dir('./', activity_strings)

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
    turma = dummy_class(students)
    for name, nusp, group in turma:
        print(f'{name} - {nusp} - {group}')
    print('-' * 70)
    aula = 98
    fake_grades(turma, aula, 'atc', './')
    fake_attedence(turma, aula)

    atc_parse(turma, aula) 

    exit(0)

