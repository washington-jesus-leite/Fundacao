import oracledb

def cria_esquema_fundacao(
    sys_user: str = "SYS",
    sys_password: str = "Not@1943ma",
    cdb_dsn: str = "localhost:1521/XE",     # DSN do CDB (container raiz)
    pdb_name: str = "XEPDB1",               # nome do PDB alvo
    new_user: str = "FUNDACAO",
    new_password: str = "fundacao_pw"
):
    """
    1) Conecta ao CDB$ROOT como SYSDBA
    2) ALTER SESSION SET CONTAINER=<pdb_name>
    3) CREATE USER + GRANTs + QUOTA
    """
    try:
        conn = oracledb.connect(
            user=sys_user,
            password=sys_password,
            dsn=cdb_dsn,
            mode=oracledb.SYSDBA
        )
        conn.autocommit = True
        cur = conn.cursor()
        print(f"Conectado ao CDB raiz via {cdb_dsn}")
    except oracledb.DatabaseError as e:
        print("Falha ao conectar como SYSDBA:", e)
        return

    try:
        # 2) mudar para o PDB
        cur.execute(f'ALTER SESSION SET CONTAINER={pdb_name}')
        print(f"Session alterada para PDB {pdb_name}")
    except oracledb.DatabaseError as e:
        print("Erro ao alterar container:", e)
        cur.close()
        conn.close()
        return

    # 3) criar usuário
    try:
        cur.execute(f"CREATE USER {new_user} IDENTIFIED BY {new_password}")
        print(f"Usuário {new_user} criado com sucesso.")
    except oracledb.DatabaseError as e:
        print("Aviso/erro ao criar usuário (talvez já exista):", e)

    # 4) conceder privilégios
    privs = [
        f"GRANT CONNECT TO {new_user}",
        f"GRANT RESOURCE TO {new_user}",
        f"ALTER USER {new_user} QUOTA UNLIMITED ON USERS"
    ]
    for stmt in privs:
        try:
            cur.execute(stmt)
            print("Executado:", stmt)
        except oracledb.DatabaseError as e:
            print("Erro em", stmt, "->", e)

    cur.close()
    conn.close()
    print("Conexão encerrada.")

if __name__ == "__main__":
    cria_esquema_fundacao()
