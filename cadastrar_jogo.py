from typing import List
import requests

from database import adicionar_jogo, inicializar_banco

BASE_URL = "https://www.cheapshark.com/api/1.0"
HEADERS = {"User-Agent": "CacaJogosApp/1.0 (ygort97@gmail.com)"}


def pesquisar_jogos(termo: str) -> List[dict]:
    url = f"{BASE_URL}/games"
    params = {"title": termo}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json()[:5]
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao buscar na API: {erro}")
    return []


def fluxo_cadastro():
    inicializar_banco()

    termo = input("\nDigite o nome do jogo que quer monitorar: ").strip()
    if not termo:
        print("Busca cancelada.")
        return

    jogos = pesquisar_jogos(termo)
    if not jogos:
        print(f"Nenhum jogo encontrado para '{termo}'.")
        return

    print("\nSelecione o jogo desejado:")
    for i, jogo in enumerate(jogos, start=1):
        nome = jogo.get("external")
        preco = jogo.get("cheapest")
        cs_id = jogo.get("gameID")
        print(f"[{i}] {nome} | ID: {cs_id} | Menor preço atual: ${preco}")

    escolha = input("\nDigite o número da opção (1 a 5) ou 0 para cancelar: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(jogos) + 1):
        print("Operação cancelada.")
        return

    jogo_selecionado = jogos[int(escolha) - 1]
    cs_id = jogo_selecionado.get("gameID")
    titulo_oficial = jogo_selecionado.get("external")

    preco_alvo_str = input(
        f"Qual o seu preço-alvo em dólares para '{titulo_oficial}'? (Ex: 8.50): "
    ).replace(",", ".").strip()

    try:
        preco_alvo = float(preco_alvo_str)
    except ValueError:
        print("Valor inválido. Use números no formato 0.00.")
        return

    sucesso = adicionar_jogo(
        cheapshark_id=cs_id,
        titulo=titulo_oficial,
        preco_alvo=preco_alvo,
    )

    if sucesso:
        print(f"\n[SUCESSO] '{titulo_oficial}' cadastrado com meta de ${preco_alvo:.2f}!")
    else:
        print("\n[ERRO] Não foi possível salvar no banco.")


if __name__ == "__main__":
    fluxo_cadastro()