import oracledb

# 1) Conexão com usuário fundacao
conn = oracledb.connect(
    user="fundacao",
    password="Not@1943ma",
    dsn="localhost/XEPDB1"
)
cur = conn.cursor()

# 2) Criação das tabelas no schema FUNDACAO
ddls = [
"""
CREATE TABLE CARGO (
  CODIGO      NUMBER       PRIMARY KEY,
  NOME_CARGO  VARCHAR2(100) NOT NULL
)
""",
"""
CREATE TABLE PROVENTO (
  CODIGO       NUMBER       PRIMARY KEY,
  DESCR_PROV   VARCHAR2(100) NOT NULL
)
""",
"""
CREATE TABLE DESCONTO (
  CODIGO       NUMBER       PRIMARY KEY,
  NOME_DESC    VARCHAR2(100) NOT NULL
)
""",
"""
CREATE TABLE TAXAS (
  CODTAXAS     NUMBER       PRIMARY KEY,
  NOME_TAXA    VARCHAR2(100) NOT NULL
)
""",
"""
CREATE TABLE CADASTRO_FUNC (
  MATRICULA       NUMBER        PRIMARY KEY,
  NOME            VARCHAR2(100) NOT NULL,
  CPF             VARCHAR2(14)  UNIQUE NOT NULL,
  VINCULO         VARCHAR2(50),
  CARGO_COD       NUMBER        REFERENCES CARGO(CODIGO),
  SALARIO         NUMBER(15,2),
  DEPARTAMENTO    VARCHAR2(50),
  DESCONTO_COD    NUMBER        REFERENCES DESCONTO(CODIGO),
  PROVENTO_COD    NUMBER        REFERENCES PROVENTO(CODIGO),
  ATIVO           NUMBER(1)     DEFAULT 1 CHECK (ATIVO IN (1,2)),
  DATA_ADMISSAO   DATE,
  DATA_EXONERACAO DATE
)
""",
"""
CREATE TABLE FOLHA (
  MATRICULA    NUMBER      REFERENCES CADASTRO_FUNC(MATRICULA),
  CPF          VARCHAR2(14),
  SALARIO      NUMBER(15,2),
  PROV_COD     NUMBER      REFERENCES PROVENTO(CODIGO),
  DESC_COD     NUMBER      REFERENCES DESCONTO(CODIGO),
  CALFOLHA     NUMBER(15,2),
  DATA_FOLHA   DATE,
  CONSTRAINT PK_FOLHA PRIMARY KEY (MATRICULA, DATA_FOLHA)
)
"""
]

for ddl in ddls:
    try:
        cur.execute(ddl)
        print("Executou DDL:", ddl.split()[2])
    except oracledb.DatabaseError as e:
        print("Erro criando tabela:", e)

conn.commit()
cur.close()
conn.close()
