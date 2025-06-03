import oracledb

username = 'SYS'
password = 'Not@1943ma'
dsn      = 'localhost:1521/XE'

# modo thin (sem Instant Client) ou thick (com init_oracle_client acima)
conn = oracledb.connect(
    user   = username,
    password = password,
    dsn    = dsn,
    mode   = oracledb.SYSDBA    # para autenticar como SYSDBA
)
conn.autocommit = True
cur = conn.cursor()

# 2) Crie o usuário/esquema FUNDACAO
try:
    cur.execute("CREATE USER fundacao IDENTIFIED BY fundacao_pw")
    print("Usuário FUNDACAO criado.")
except oracledb.DatabaseError as e:
    print("Erro ao criar usuário (talvez já exista):", e)

# 3) Conceda privilégios
privs = [
    "GRANT CONNECT TO fundacao",
    "GRANT RESOURCE TO fundacao",          # DDL básico
    "ALTER USER fundacao QUOTA UNLIMITED ON USERS"
]
for p in privs:
    try:
        cur.execute(p)
        print("Executado:", p)
    except oracledb.DatabaseError as e:
        print("Erro em", p, e)

cur.close()
conn.close()
