import sqlite3
from typing import List, Optional, Tuple

DB_NAME = "cacajogos.db"


def conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def inicializar_banco():
    with conectar() as conn:
        cursor = conn.cursor()

        # Tabela com controle de último preço notificado
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jogos_monitorados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cheapshark_id TEXT NOT NULL UNIQUE,
                titulo TEXT NOT NULL,
                preco_alvo REAL NOT NULL,
                ultimo_preco_notificado REAL DEFAULT NULL,
                ativo INTEGER DEFAULT 1,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historico_precos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogo_id INTEGER NOT NULL,
                preco_atual REAL NOT NULL,
                link_oferta TEXT,
                consultado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (jogo_id) REFERENCES jogos_monitorados(id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()


def adicionar_jogo(cheapshark_id: str, titulo: str, preco_alvo: float) -> bool:
    sql = """
        INSERT INTO jogos_monitorados (cheapshark_id, titulo, preco_alvo, ativo)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(cheapshark_id) DO UPDATE SET
            preco_alvo = excluded.preco_alvo,
            ultimo_preco_notificado = NULL,
            ativo = 1;
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (cheapshark_id, titulo, preco_alvo))
            conn.commit()
            return True
    except sqlite3.Error as erro:
        print(f"Erro ao salvar jogo: {erro}")
        return False


def listar_jogos_ativos() -> List[Tuple]:
    sql = """
        SELECT id, cheapshark_id, titulo, preco_alvo, ultimo_preco_notificado 
        FROM jogos_monitorados 
        WHERE ativo = 1;
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def atualizar_ultimo_alerta(jogo_id: int, preco_notificado: float):
    """Registra que o usuário já foi notificado sobre este preço."""
    sql = """
        UPDATE jogos_monitorados
        SET ultimo_preco_notificado = ?
        WHERE id = ?;
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (preco_notificado, jogo_id))
        conn.commit()


def registrar_historico(
    jogo_id: int, preco_atual: float, link_oferta: str
) -> bool:
    sql = """
        INSERT INTO historico_precos (jogo_id, preco_atual, link_oferta)
        VALUES (?, ?, ?);
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (jogo_id, preco_atual, link_oferta))
            conn.commit()
            return True
    except sqlite3.Error as erro:
        print(f"Erro ao registrar histórico: {erro}")
        return False


if __name__ == "__main__":
    inicializar_banco()
    print("Banco atualizado com suporte anti-spam!")