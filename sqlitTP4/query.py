import sqlite3
import json


conn = sqlite3.connect('trabalho.db')
cursor = conn.cursor()

# Queries
query_1 = """
SELECT d.nome AS departamento, AVG(hs.salario) AS media_salario
FROM Historico_Salarios hs
JOIN Funcionarios f ON hs.idFuncionario = f.idFuncionario
JOIN Departamentos d ON f.idDepartamento = d.id
JOIN Projetos p ON f.idFuncionario = p.idFuncionarioResponsavel
WHERE p.status = 'Concluído'
GROUP BY d.nome;
"""

# Query modificada para garantir resultados
query_2 = """
SELECT r.descricao, SUM(r.quantidade) AS quantidade_total
FROM Recursos r
WHERE r.tipo = 'Material'
GROUP BY r.descricao
ORDER BY quantidade_total DESC
LIMIT 3;
"""

query_3 = """
SELECT d.nome AS departamento, SUM(p.custo) AS custo_total
FROM Projetos p
JOIN Funcionarios f ON p.idFuncionarioResponsavel = f.idFuncionario
JOIN Departamentos d ON f.idDepartamento = d.id
WHERE p.status = 'Concluído'
GROUP BY d.nome;
"""

query_4 = """
SELECT p.nomeProjeto AS projeto_nome, p.custo, p.dataInicio, p.dataConclusao, f.nome AS funcionario_responsavel
FROM Projetos p
JOIN Funcionarios f ON p.idFuncionarioResponsavel = f.idFuncionario
WHERE p.status = 'Em Execução';
"""

query_5 = """
SELECT p.nomeProjeto AS projeto_nome, COUNT(d.idDependente) AS num_dependentes
FROM Projetos p
JOIN Funcionarios f ON p.idFuncionarioResponsavel = f.idFuncionario
JOIN Dependentes d ON f.idFuncionario = d.idFuncionario
GROUP BY p.idProjeto
ORDER BY num_dependentes DESC
LIMIT 1;
"""


queries = [query_1, query_2, query_3, query_4, query_5]

for query in queries:
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)


queriesJSON = [query_1, query_2, query_3]
nomesArquivos = ['media_salario_departamentos.json', 'top_recursos_materiais.json', 'custo_total_departamentos.json']

for consulta, nomeArquivo in zip(queriesJSON, nomesArquivos):
    cursor.execute(consulta)
    resultado = cursor.fetchall()

   
    colunas = [descricao[0] for descricao in cursor.description]
    dados = [dict(zip(colunas, linha)) for linha in resultado]


    with open(nomeArquivo, 'w', encoding='utf-8') as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)

    


conn.close()
