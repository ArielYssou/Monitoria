from sys import argv
from modules.common import Turma, load_turma

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
        print('Tests')

    elif '-g' in argv:
        from modules.forge_groups import forge_groups
        turma = load_turma()
        forge_groups(turma)

    else:
        pass

