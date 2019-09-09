def mean(arr = []):
    return sum(arr) / len(arr)

def GroupGenerator():
    num = 0
    char = 'B'
    for index in range(24):
        if char == 'A':
            char = 'B'
        else:
            char = 'A'
            num += 1
        yield str(num) + char

def forge_groups(turma):
    from modules.common import targets, search_dir, Turma, class_file
    from modules.errors import StudentNotInClassError, InvalidInputError 
    from random import shuffle
    from datetime import datetime
    from os.path import isfile
    from shutil import copyfile

    grades = {}
    for activity, target in targets.items():
        for name, nusp, group in turma.students:
            grades[(activity, nusp)] = []

    weights = {
            'freq' : 1,
            'qp' : 0.05,
            'atc' : 0.05,
            'list' : 0.05,
            'exam' : 0.25,
            'mid_exam' : 0.60
            }
    norm = sum(weights.values())

    for activity in targets.keys():
        if activity not in weights.keys():
            raise InvalidInputError(f"You forgot to issue the weight for activity {activity}")
        else:
            weights[activity] /= norm 

    for activity, target in targets.items():
        for file in search_dir(targets[activity], activity):
            with open(f"{targets[activity]}/{file}", 'r') as f:
                for line in f.read().splitlines():
                    print(line)
                    nusp, grade = line.split(',')
                    if nusp in turma.nusps.values():
                        if grade not in ('-', ''):
                            try:
                                grade = float(grade)
                            except:
                                grade = 10 # If the activity is 'freqs' then the grade is acctually a group and cannot be converted to a float directly
                            finally:
                                grades[(activity, nusp)].append(grade)
                        else:
                            grades[(activity, nusp)].append(0)
                    else:
                        raise StudentNotInClassError(f"Intruder! {nusp}")
    
    final_grades = {}
    names = {}
    for activity, target in targets.items():
        print('-' * 70)
        print(activity)
        print('-' * 70)
        for name, nusp, group in turma.students:
            names[nusp] = name
            if nusp not in final_grades.keys():
                final_grades[nusp] = mean(grades[(activity, nusp)]) * weights[activity]
            else:
                final_grades[nusp] += mean(grades[(activity, nusp)]) * weights[activity]

    grades_repos = final_grades.copy()

    while True:
        final_grades = grades_repos.copy()
        new_group = {}
        siberia_tresh = 3.5
        for nusp, grade in final_grades.items():
            if grade < siberia_tresh:
                new_group[nusp] = '13S'

        for nusp, grade in new_group.items():
            final_grades.pop(nusp)

        sorted_grades = sorted( final_grades.items(), key = lambda x: x[1] ) 
        
        tier_sizes = int( len(sorted_grades) / 3 )

        tiers = [[] , [], []]
        leftovers = []
        for tier in range(3):
            for index in range(tier_sizes):
                tiers[tier].append( sorted_grades.pop() )
            if tier == 1:
                for index in range(len(sorted_grades) % 3):
                    leftovers.append( sorted_grades.pop() )

        for tier in tiers:
            shuffle(tier)

        group_gen = GroupGenerator()
        for index in range(tier_sizes):
            group = group_gen.__next__()
            for tier in tiers:
                nusp, grade = tier.pop()
                new_group[nusp] = group

        if len(leftovers) == 1:
            group = group_gen.__next__()

            nusp = list(new_group.keys())[-1]
            new_group[nusp] = group

            nusp, grade = leftovers[-1]
            new_group[nusp] = group
        elif len(leftovers) == 2:
            group = group_gen.__next__()
            for nusp, grade in leftovers:
                new_group[nusp] = group
        else:
            pass
        
        colors = {
                'A' : 214,
                'B' : 230,
                'S' : 222
                }
        turma = Turma()
        for nusp, group in new_group.items():
            turma.add(names[nusp], nusp, group)
        turma.group_sort()

        for name, nusp, group in turma.students:
            if 'A' in group:
                print(f"\033[38;5;{colors['A']}m{name:<30} - {str(nusp):9} - {group} - {grades_repos[nusp]:.2f}\033[0m")
            elif 'B' in group:
                print(f"\033[38;5;{colors['B']}m{name:<30} - {str(nusp):9} - {group} - {grades_repos[nusp]:.2f}\033[0m")
            else:
                print(f"\033[38;5;{colors['S']}m{name:<30} - {str(nusp):9} - {group} - {grades_repos[nusp]:.2f}\033[0m")


        print("Are you satisfied with these groups? (yes/no)")
        ans = input("> ")
        if ans.lower() in ('y', 'yes'):
            fname = f'./files/old/Chamada_{datetime.now().strftime("%B")}.csv'
            print(f"Backing up last group composition under \'{fname}\'")
            if isfile(fname):
                print("Warning! There is already a group composition for this month, overwrite? (yes/no)")
                ans = input("> ")
                if ans.lower() in ('y', 'yes'):
                    copyfile(class_file, fname)
                else:
                    break

            for name, nusp, group in turma.students:
                print(f"{name},{nusp},{group}")

            turma.sort()
            with open(class_file, 'w+') as f:
                for name, nusp, group in turma.students:
                    f.write(f"{name},{nusp},{group}\n")
            break
        elif ans.lower() in ('n', 'no'):
            print("Try again? (yes/no)")
            ans = input("> ")
            if ans.lower() in ('y', 'yes'):
                continue
            elif ans.lower() in ('n', 'no'):
                break
        else:
            break

def ad_hoc_groups(turma):
    '''
    Using a iterative menu, prompts the user with the class whose groups are to be informed by hand for each student. Luckly you will never need to use this, but nevertheless here we are
    '''

    from modules.common import Turma
    from modules.menu import create_menu
    from os.path import isfile
    from shutils import copyfile
    
    dv = []
    for name in turma.students:
        dv.append('')

    new_turma = Turma()
    result = create_menu(turma.names, dv)
    for name, group in result:
        new_turma.add(name, turma.nusp[name], group.replace(' ','') )

    fname = f'./files/old/Chamada_{datetime.now().strftime("%B")}.csv'
    print(f"Backing up last group composition under \'{fname}\'")
    if isfile(fname):
        print("Warning! There is already a group composition for this month, overwrite? (yes/no)")
        ans = input("> ")
        if ans.lower() in ('y', 'yes'):
            copyfile(class_file, fname)
        else:
            return
    new_turma.sort()
    with open(class_file, 'w+') as f:
        for name, nusp, group in new_turma.students:
            print(f"{name},{nusp},{group}")
            f.write(f"{name},{nusp},{group}\n")

    return
