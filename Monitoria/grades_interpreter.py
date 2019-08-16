import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

class_df = pd.read_csv('class.csv', dtype=object, header=0, index_col=False)

print(class_df.info())

print('-' * 70)
print(class_df)
print('-' * 70)
print(class_df['Nome'])

freq = []

for student in list(class_df['Nome']):
    print(student + " is in the class")

print('-' * 70)
grades = pd.read_csv('4302111-2019-QPrev - aula 24-notas.csv', header=0, usecols = ['Número USP', 'Avaliar/10,00'], dtype = object)
grades['Avaliar/10,00'] = grades['Avaliar/10,00'].apply(lambda grade: grade.replace(',','.'))
grades['Avaliar/10,00'] = grades['Avaliar/10,00'].apply(lambda grade: grade.replace('-',''))
grades['Avaliar/10,00'] = pd.to_numeric(grades['Avaliar/10,00'])
grades = grades.dropna()

print(grades.info())
print('-' * 70)
print(grades)

print("The average grade")
print(grades['Avaliar/10,00'])
