import oracledb

# Conexão como esquema fundacao
conn = oracledb.connect("fundacao/fundacao_pw@localhost/XEPDB1")
cur = conn.cursor()

# Inserir um cargo
cur.execute("INSERT INTO CARGO (CODIGO, NOME_CARGO) VALUES (:1, :2)",
            (10, "Desenvolvedor"))
# Inserir desconto
cur.execute("INSERT INTO DESCONTO (CODIGO, NOME_DESC) VALUES (20, 'INSS')")
# Inserir provento
cur.execute("INSERT INTO PROVENTO (CODIGO, DESCR_PROV) VALUES (30, 'PLR')")
conn.commit()

# Inserir funcionário
cur.execute("""
  INSERT INTO CADASTRO_FUNC
    (MATRICULA,NOME,CPF,VINCULO,CARGO_COD,SALARIO,DEPARTAMENTO,
     DESCONTO_COD,PROVENTO_COD,ATIVO,DATA_ADMISSAO)
  VALUES (:m,:n,:c,:v,:cc,:s,:d,:dc,:pc,1,SYSDATE)
""", {
    "m": 1234, "n": "Maria Silva", "c": "987.654.321-00",
    "v": "CLT", "cc": 10, "s": 4500, "d": "Financeiro",
    "dc": 20, "pc": 30
})
conn.commit()

# Leitura de dados
for row in cur.execute("SELECT MATRICULA, NOME, SALARIO FROM CADASTRO_FUNC"):
    print(row)

# Adicionar coluna via DDL
cur.execute("ALTER TABLE CADASTRO_FUNC ADD EMAIL VARCHAR2(100)")
conn.commit()
print("Coluna EMAIL adicionada.")

cur.close()
conn.close()
