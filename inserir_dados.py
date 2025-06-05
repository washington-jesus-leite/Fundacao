import oracledb

def popula_dados(
    user: str = "fundacao",
    password: str = "fundacao_pw",
    dsn: str = "localhost:1521/XEPDB1"
):
    """
    Popula as tabelas CARGO, DESCONTO, PROVENTO, TAXAS, CADASTRO_FUNC e FOLHA
    no schema FUNDACAO2 do PDB XEPDB1.
    """
    # 1) Conecta ao PDB como o schema FUNDACAO2
    conn = oracledb.connect(
          user = "SYS",
          password = "Not@1943ma",
          dsn = "localhost:1521/XE",     # DSN do CDB (container raiz)
          mode=oracledb.SYSDBA
          )
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # 2) Insere registros em CARGO
        cargos = [
            (10, "Desenvolvedor"),
            (20, "Analista de Dados"),
            (30, "Gerente de Projeto")
        ]
        cur.executemany(
            "INSERT INTO CARGO (CODIGO, NOME_CARGO) VALUES (:1, :2)",
            cargos
        )
        print(f"{cur.rowcount} linhas inseridas em CARGO")

        # 3) Insere registros em DESCONTO
        descontos = [
            (100, "INSS"),
            (110, "IRRF")
        ]
        cur.executemany(
            "INSERT INTO DESCONTO (CODIGO, NOME_DESC) VALUES (:1, :2)",
            descontos
        )
        print(f"{cur.rowcount} linhas inseridas em DESCONTO")

        # 4) Insere registros em PROVENTO
        proventos = [
            (200, "PLR"),
            (210, "BONUS")
        ]
        cur.executemany(
            "INSERT INTO PROVENTO (CODIGO, DESCR_PROV) VALUES (:1, :2)",
            proventos
        )
        print(f"{cur.rowcount} linhas inseridas em PROVENTO")

        # 5) Insere registros em TAXAS
        taxas = [
            (300, "FGTS"),
            (310, "SEGURO DESEMPREGO")
        ]
        cur.executemany(
            "INSERT INTO TAXAS (CODTAXAS, NOME_TAXA) VALUES (:1, :2)",
            taxas
        )
        print(f"{cur.rowcount} linhas inseridas em TAXAS")

        # 6) Insere funcionários em CADASTRO_FUNC
        funcs = [
            {
                "m": 1234, "n": "Maria Silva",  "c": "987.654.321-00",
                "v": "CLT",   "cc": 10, "s": 4500.00,
                "dpt": "Financeiro", "dc": 100, "pc": 200
            },
            {
                "m": 5678, "n": "João Pereira", "c": "123.456.789-11",
                "v": "PJ",    "cc": 20, "s": 5500.00,
                "dpt": "TI",          "dc": 110, "pc": 210
            }
        ]
        cur.executemany("""
            INSERT INTO CADASTRO_FUNC (
                MATRICULA, NOME, CPF, VINCULO,
                CARGO_COD, SALARIO, DEPARTAMENTO,
                DESCONTO_COD, PROVENTO_COD,
                ATIVO, DATA_ADMISSAO
            ) VALUES (
                :m, :n, :c, :v,
                :cc, :s, :dpt,
                :dc, :pc,
                1, SYSDATE
            )
        """, funcs)
        print(f"{cur.rowcount} linhas inseridas em CADASTRO_FUNC")

        # 7) Insere registros em FOLHA
        folhas = [
            (1234, "987.654.321-00", 4500.00, 200, 100, 4500.00),
            (5678, "123.456.789-11", 5500.00, 210, 110, 5500.00)
        ]
        cur.executemany("""
            INSERT INTO FOLHA (
                MATRICULA, CPF, SALARIO,
                PROV_COD, DESC_COD, CALFOLHA,
                DATA_FOLHA
            ) VALUES (
                :1, :2, :3,
                :4, :5, :6,
                SYSDATE
            )
        """, folhas)
        print(f"{cur.rowcount} linhas inseridas em FOLHA")

        # 8) Commit geral
        conn.commit()
        print("Todas as inserções realizadas e commit efetuado.")

    except oracledb.DatabaseError as e:
        print("Erro durante inserção, efetuando rollback:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    popula_dados()
