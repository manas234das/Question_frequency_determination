"""
This Script converts the csv file to tsv file
"""

import csv
# Specify the paths of the files
csv.writer(open('500_questions.tsv', 'w+'), delimiter='\t').writerows(csv.reader(open("500_questions.csv")))
