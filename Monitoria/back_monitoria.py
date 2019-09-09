from sys import argv

if __name__ == '__main__':
    aulas = list(filter(lambda x : x.isnumeric(), argv))
    if '-f' in argv:
        from modules.parsers import attendance
        from modules.common import Turma
        from modules.dummy_class import dummy_class

        turma = dummy_class(15)

        for aula in aulas:
            attendance(turma, aula)

    elif '-q' in argv:
        from modules.parsers import parse_by_nusp
        from modules.dummy_class import dummy_class
        from modules.fake_grades import fake_grades
        activity = 'qp'

        turma = dummy_class(15)
        for aula in aulas:
            fake_grades(turma, aula, activity, './')
            parse_by_nusp(turma, activity, aula)

    elif '-l' in argv:
        from modules.parsers import parse_by_nusp
        from modules.dummy_class import dummy_class
        from modules.fake_grades import fake_grades
        activity = 'list'
        turma = dummy_class(15)

        for entry in argv[2:]:
            fake_grades(turma, entry, activity, './')
            parse_by_nusp(turma, activity, entry)

    elif '-a' in argv:
        from modules.parsers import parse_by_group
        from modules.dummy_class import dummy_class
        from modules.fake_grades import fake_grades, fake_attedence
        activity = 'atc'

        turma = dummy_class(15)
        for aula in aulas:
            fake_grades(turma, aula, activity, './')
            fake_attedence(turma, aula)
            parse_by_group(turma, activity, aula)

    elif '-e' in argv:
        from modules.parsers import parse_by_nusp
        from modules.dummy_class import dummy_class
        from modules.fake_grades import fake_exam
        activity = 'exam'

        turma = dummy_class(15)
        for aula in aulas:
            fake_exam(turma, activity, aula, '.')
            parse_by_nusp(turma, activity, aula, identifiers = ['usp', 'nota'])

    elif '-m' in argv:
        from modules.parsers import parse_by_nusp
        from modules.dummy_class import dummy_class
        from modules.fake_grades import fake_exam
        activity = 'mid_exam'

        turma = dummy_class(15)
        for aula in aulas:
            fake_exam(turma, activity, aula, '.')
            parse_by_nusp(turma, activity, aula, identifiers = ['usp', 'nota'])

    elif '-t' in argv:
        print('Tests')

    elif '-g' in argv:
        from modules.forge_groups import forge_groups
        from modules.dummy_class import dummy_class
        from modules.common import targets
        from modules.fake_grades import fake_exam, fake_attedence, fake_grades
        from modules.parsers import parse_by_group, parse_by_nusp

        turma = dummy_class(20)
        files = []
        for num in range(10):
            fake_attedence(turma, num)
            for activity in ['exam', 'mid_exam']:
                fake_exam(turma, activity, num, '.')
                parse_by_nusp(turma, activity, num, identifiers = ['nusp', 'nota'])
            for activity in ['qp', 'list']:
                fake_grades(turma, activity, num)
                parse_by_nusp(turma, activity, num)
            for activity in ['atc']:
                fake_grades(turma, activity, num)
                parse_by_group(turma, activity, num)
        for name, nusp, group in turma.students:
            print(f"{name} - {nusp}")
        print('-' * 70)
        forge_groups(turma)

    else:
        pass

