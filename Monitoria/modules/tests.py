from modules.common import Turma, targets
import modules.fakes as fk

test_num = 99

def clean_files(target = './', string = ''):
    from modules.common import search_dir
    from os import remove

    files = search_dir(target, [string])
    for file in files:
        remove(file)
    return 

def test_attendance(studs = 10):
    from modules.parsers import attendance
    from modules.common import Turma
    activity = 'freq'

    turma = fk.dummy_class(studs)

    attendance(turma, test_num)

    clean_files(targets[activity], str(test_num))
    clean_files(targets[activity], fk.fake_id)
    clean_files('./', test_num)

def test_nusp_activity(activity = '', studs = 10):
    from modules.parsers import parse_by_nusp

    turma = fk.dummy_class(studs)

    if activity in ('exam', 'mid_exam'):
        fk.fake_exam(turma, activity, test_num, '.')
        parse_by_nusp(turma, activity, test_num, identifiers = ['usp', 'nota'], target = './')
    else:
        fk.fake_grades(turma, activity, test_num, './')
        parse_by_nusp(turma, activity, test_num, './')

def test_group_activity(activity = '', studs = 10):
    from modules.parsers import parse_by_group

    turma = fk.dummy_class(studs)
    fk.fake_attedence(turma, test_num)
    fk.fake_grades(turma, activity, test_num, './')
    parse_by_group(turma, activity, test_num, './')

    clean_files(targets[activity], str(test_id))
    clean_files(targets[activity], fk.fake_id)
    clean_files('./')

def test_groups_forge(studs = 50, create_grades = True):
    from modules.forge_groups import forge_groups
    from modules.common import load_turma, targets
    from modules.parsers import parse_by_group, parse_by_nusp

    if create_grades:
        turma = fk.dummy_class(20)

        for num in range(test_num - 9, test_num):
            fk.fake_attedence(turma, num)
            for activity in ['exam', 'mid_exam']:
                fk.fake_exam(turma, activity, num, '.')
                parse_by_nusp(turma, activity, num, identifiers = ['usp', 'nota'], target = './')
            for activity in ['qp', 'list']:
                fk.fake_grades(turma, activity, num, './')
                parse_by_nusp(turma, activity, num, './')
            for activity in ['atc']:
                fk.fake_grades(turma, activity, num, './')
                parse_by_group(turma, activity, num, './')
    else:
        turma = load_turma()

    forge_groups(turma, test = True)

    if create_grades:
        for num in range(test_num - 9, test_num):
            for t in targets.values():
                clean_files(t, str(num))
                clean_files(t, fk.fake_id)
            clean_files('./', str(num))

