from typing import Optional, Tuple
import requests

from database import (
    atualizar_ultimo_alerta,
    listar_jogos_ativos,
    registrar_historico,
)
from notifier import enviar_alerta_discord

BASE_URL = "https://www.cheapshark.com/api/1.0"
HEADERS = {"User-Agent": "CacaJogosApp/1.0 (ygort97@gmail.com)"}


def obter_menor_oferta(cheapshark_id: str) -> Optional[Tuple[float, str]]:
    url = f"{BASE_URL}/games"
    params = {"id": cheapshark_id}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        dados = response.json()
        ofertas = dados.get("deals", [])

        if not ofertas:
            return None

        menor_oferta = min(ofertas, key=lambda o: float(o.get("price", 999999)))
        menor_preco = float(menor_oferta.get("price"))
        deal_id = menor_oferta.get("dealID")

        return menor_preco, deal_id

    except requests.exceptions.RequestException as erro:
        print(f"[ERRO] Falha de conexão: {erro}")
        return None


def verificar_precos():
    jogos = listar_jogos_ativos()

    if not jogos:
        print("Nenhum jogo ativo para monitorar.")
        return

    print(f"\nIniciando verificação de {len(jogos)} jogo(s)...")
    print("=" * 60)

    for jogo in jogos:
        id_banco, cs_id, titulo, preco_alvo, ultimo_preco_notificado = jogo

        resultado = obter_menor_oferta(cs_id)
        if not resultado:
            print(f"[PULADO] Informações indisponíveis para '{titulo}'.")
            continue

        preco_atual, deal_id = resultado
        # Link real que redireciona para a loja da oferta
        link_oferta = f"https://www.cheapshark.com/redirect?dealID={deal_id}"

        # Registra histórico de checagem
        registrar_historico(
            jogo_id=id_banco, preco_atual=preco_atual, link_oferta=link_oferta
        )

        print(f"Jogo: {titulo}")
        print(f"Preço atual: ${preco_atual:.2f} | Meta: ${preco_alvo:.2f}")

        # Regra de negócio: Atingiu meta e não foi notificado com o mesmo valor ou superior
        atingiu_meta = preco_atual <= preco_alvo
        novo_desconto = (
            ultimo_preco_notificado is None
            or preco_atual < ultimo_preco_notificado
        )

        if atingiu_meta and novo_desconto:
            print(">>> Disparando alerta no Discord...")
            sucesso = enviar_alerta_discord(
                titulo=titulo,
                preco_atual=preco_atual,
                preco_alvo=preco_alvo,
                link_oferta=link_oferta,
            )
            if sucesso:
                atualizar_ultimo_alerta(id_banco, preco_atual)
        elif atingiu_meta and not novo_desconto:
            print(
                ">>> Meta atingida, mas você já foi avisado sobre esse valor (Anti-spam ativado)."
            )
        else:
            print(f"Ainda acima da meta por ${preco_atual - preco_alvo:.2f}.")

        print("-" * 60)


if __name__ == "__main__":
    verificar_precos()