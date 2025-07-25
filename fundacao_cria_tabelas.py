import oracledb

# 1) Conexão com usuário fundacao
conn = oracledb.connect(
    user = "SYS",
    password = "Not@1943ma",
    dsn = "localhost:1521/XE",     # DSN do CDB (container raiz)
    mode=oracledb.SYSDBA
)
cur = conn.cursor()

# 2) Criação das tabelas no schema FUNDACAO
ddls = [
"""
CREATE TABLE CARGO (
  CODIGO       NUMBER         PRIMARY KEY,
  NOME_CARGO   VARCHAR2(100)  NOT NULL
)
""",
"""
CREATE TABLE PROVENTO (
  CODIGO       NUMBER         PRIMARY KEY,
  DESCR_PROV   VARCHAR2(100)  NOT NULL
)
""",
"""
CREATE TABLE DESCONTO (
  CODIGO       NUMBER         PRIMARY KEY,
  NOME_DESC    VARCHAR2(100)  NOT NULL
)
""",
"""
CREATE TABLE TAXAS (
  CODTAXAS     NUMBER         PRIMARY KEY,
  NOME_TAXA    VARCHAR2(100)  NOT NULL
)
""",
"""
CREATE TABLE CADASTRO_FUNC (
  MATRICULA        NUMBER           PRIMARY KEY,
  NOME             VARCHAR2(100)    NOT NULL,
  CPF              VARCHAR2(14)     UNIQUE NOT NULL,
  VINCULO          VARCHAR2(50),
  CARGO_COD        NUMBER,
  SALARIO          NUMBER(15,2),
  DEPARTAMENTO     VARCHAR2(50),
  DESCONTO_COD     NUMBER,
  PROVENTO_COD     NUMBER,
  ATIVO            NUMBER(1)        DEFAULT 1 CHECK (ATIVO IN (1,2)),
  DATA_ADMISSAO    DATE,
  DATA_EXONERACAO  DATE,
  CONSTRAINT FK_CAD_CARGO   FOREIGN KEY (CARGO_COD)   REFERENCES CARGO(CODIGO),
  CONSTRAINT FK_CAD_DESC    FOREIGN KEY (DESCONTO_COD) REFERENCES DESCONTO(CODIGO),
  CONSTRAINT FK_CAD_PROV    FOREIGN KEY (PROVENTO_COD) REFERENCES PROVENTO(CODIGO)
)
""",
"""
CREATE TABLE FOLHA (
  MATRICULA     NUMBER,
  CPF           VARCHAR2(14),
  SALARIO       NUMBER(15,2),
  PROV_COD      NUMBER,
  DESC_COD      NUMBER,
  CALFOLHA      NUMBER(15,2),
  DATA_FOLHA    DATE,
  CONSTRAINT PK_FOLHA        PRIMARY KEY (MATRICULA, DATA_FOLHA),
  CONSTRAINT FK_FLH_CAD      FOREIGN KEY (MATRICULA)   REFERENCES CADASTRO_FUNC(MATRICULA),
  CONSTRAINT FK_FLH_PROV     FOREIGN KEY (PROV_COD)     REFERENCES PROVENTO(CODIGO),
  CONSTRAINT FK_FLH_DESC     FOREIGN KEY (DESC_COD)     REFERENCES DESCONTO(CODIGO)
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
