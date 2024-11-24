import sqlite3
import csv
import os

db_path = 'trabalho.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def import_csv_to_table(csv_file, table_name):
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignora o cabeçalho
            for row in reader:
                placeholders = ', '.join(['?' for _ in row])
                cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)
            conn.commit()

csv_files_and_tables = [
    ('cargos.csv', 'Cargos'),
    ('departamentos.csv', 'Departamentos'),
    ('funcionarios.csv', 'Funcionarios'),
    ('historico_salarios.csv', 'Historico_Salarios'),
    ('dependentes.csv', 'Dependentes'),
    ('projetos.csv', 'Projetos'),
    ('recursos.csv', 'Recursos')
]

for csv_file, table_name in csv_files_and_tables:
    import_csv_to_table(csv_file, table_name)

conn.close()
