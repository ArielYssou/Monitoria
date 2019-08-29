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

def fake_grades(turma, aula = 99, act = 'qp' , target = './', parts = 2):
    from datetime import date, datetime
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
    if act == 'qp':
        act_identifier = 'QPrev'
        files.append(f"{course_code}-2019-{act_identifier} - aula {aula}{part}-notas.csv")
    elif act == 'atc':
        act_identifier = 'ATC'
        for part in range(parts):
            files.append(f"{course_code}-2019-{act_identifier}-{aula:02d} (parte {part + 1})-notas.csv")

    for file in files:
        dfile = open(str(target+file), 'w+')

        for field in fields:
            dfile.write(field)
        dfile.write("\n")

        for name, nusp, group in turma:
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

def fake_attedence(turma, aula):
    from random import random
    freq = 0.6

    freq_file = open('./grades/freqs/aula_{aula}.csv', 'w')
    for name, nusp, group in turma:
        if random() <= freq:
            freq_file.write(f"{nusp},{group}\n")
        else:
            freq_file.write(f"{nusp},0\n")
    freq_file.close()

if __name__ == '__main__':
    from dummy_class import dummy_class

    turma = dummy_class(10)
    aula = 98
    act = 'atc'
    fake_grades(turma, aula, act)
    exit(0)


        

