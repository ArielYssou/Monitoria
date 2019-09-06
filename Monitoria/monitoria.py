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
        print('Test')

    elif '-m' in argv:
        print('Mid-Exam')

    else:
        pass

