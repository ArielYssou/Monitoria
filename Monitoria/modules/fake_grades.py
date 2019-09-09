def strTimeProp(start, end, format, prop):
    from time import mktime, strftime, strptime, localtime
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = mktime(strptime(start, format))
    etime = mktime(strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return strftime(format, localtime(ptime))

def RandomDate(start, end, prop):
    return strTimeProp(start, end, '%d/%m/%Y %H:%M', prop)

def fake_grades(turma, activity = '', num = 0, target = '.', parts = 2):
    from datetime import date, datetime
    from modules.common import Turma
    from random import random
    '''
    INPUT: Tuple with name, nusp and group.
        Activity type (QPrev, ATC, Lista)
        Number of subparts ( Some activitys have several parts, like ATCs)
    OUTPUT: File in ~/Dowloads with  a fake grades file
    '''

    fields = [
            'Sobenome,',
            'Nome,',
            'Endereço de email,',
            'Número USP,',
            'Estado,',
            'Iniciado em,',
            'Completo,',
            'Tempo utilizado,',
            'Avaliar/10,10'
            ]
    course_code = '4302111'
    fake_year = ['1/1/2027 0:01', '1/1/2027 23:59']

    files = []
    if activity == 'qp':
        act_identifier = 'QPrev'
        part = ''
        files.append(f"{target}/{course_code}-2019-{act_identifier} - aula {num}{part}-notas.csv")
    elif activity == 'atc':
        act_identifier = 'ATC'
        for part in range(parts):
            files.append(f"{target}/{course_code}-2019-{act_identifier}-{num:02d} (parte {part + 1})-notas.csv")
    elif activity == 'list':
        num_part = ''
        char_part = ''
        for char in str(num):
            if char.isdigit():
                num_part = num_part + char
            else:
                char_part = char_part + char
        if char_part != '':
            part = f" (parte {char_part.upper()})"
        else:
            part = ''
        files.append(f"{target}/{course_code}-2019-Lista {num_part}{part}-notas.csv")

    for file in files:
        dfile = open(file, 'w+')

        for field in fields:
            dfile.write(field)
        dfile.write("\n")

        for name, nusp, group in turma.students:
            # Family name and name
            names = name.rsplit()

            sobrenome = ''
            for subname in names[1:]:
                sobrenome += f"{subname}" + " "
            sobrenome = sobrenome[:-1]
            dfile.write(sobrenome + ',')

            nome = str(names[0])
            dfile.write(nome + ',')
            
            # Email
            fake_mail = nome.lower()
            fake_mail += '.' + str(names[1]).lower()
            fake_mail += '@usp.br'
            dfile.write(fake_mail + ',')

            # Nusp and status
            dfile.write(str(nusp) + ',')
            dfile.write('Finalizada,')

            # Start and end
            start = RandomDate(fake_year[0], fake_year[1], random())
            dfile.write(start + ',')
            end = RandomDate(start , fake_year[1], random())
            dfile.write(end + ',')
            
            # Time till finish
            d1 = datetime.strptime(start, '%d/%m/%Y %H:%M')
            d2 = datetime.strptime(end, '%d/%m/%Y %H:%M')  
            dfile.write(str((d2 - d1)).replace(',','') + ',')

            # Grade
            dfile.write("\"{:.4s}\"".format(str(10 * random()).replace('.',',')))

            dfile.write('\n')

        dfile.close()

def fake_attedence(turma, num):
    from random import random
    from modules.common import Turma, targets
    freq = 0.6

    freq_file = open(f'{targets["freq"]}/freq_{num}.csv', 'w+')
    for name, nusp, group in turma.students:
        if random() <= freq:
            freq_file.write(f"{nusp},{group}\n")
        else:
            freq_file.write(f"{nusp},0\n")
    freq_file.close()

def fake_exam(turma, exam_type = 'exam', num = 0, target = '.'):
    from random import random
    from modules.common import Turma
    freq = 0.6

    if exam_type == 'exam':
        grade_file = open(f"{target}/Prova {num}.csv", 'w+')
    elif exam_type == 'mid_exam':
        grade_file = open(f"{target}/Provinha {num}.csv", 'w+')
    else:
        grade_file = open(f"{target}/{exam_type} {num}.csv", 'w+')
    

    grade_file.write(f"nusp,nota\n")
    for name, nusp, group in turma.students:
        if random() <= freq:
            grade_file.write(f"{nusp},{10 * random():.3f}\n")
        else:
            grade_file.write(f"{nusp},\n")
    grade_file.close()

if __name__ == '__main__':
    from dummy_class import dummy_class

    turma = dummy_class(10)
    num = 98
    activity = 'atc'
    fake_grades(turma, activity, num)
    exit(0)
