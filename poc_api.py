import requests

BASE_URL = "https://www.cheapshark.com/api/1.0"


def buscar_jogo(titulo: str):
    url = f"{BASE_URL}/games"
    params = {"title": titulo}
    headers = {
        "User-Agent": "CacaJogosApp/1.0 (ygort97@gmail.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Erro da API (Status {response.status_code}): {response.text}")
            return

        jogos = response.json()

        if not jogos:
            print(f"Nenhum jogo encontrado com o termo '{titulo}'.")
            return
            

        jogos_filtrados = jogos[:5]

        print(f"\nResultados encontrados para '{titulo}':\n" + "-" * 50)
        for jogo in jogos_filtrados:
            nome = jogo.get("external")
            game_id = jogo.get("gameID")
            menor_preco = jogo.get("cheapest")
            deal_id = jogo.get("cheapestDealID")

            print(f"Jogo: {nome}")
            print(f"ID CheapShark: {game_id}")
            print(f"Menor preço atual: ${menor_preco}")
            print(
                f"Link da oferta: https://www.cheapshark.com/redirect?dealID={deal_id}"
            )
            print("-" * 50)

    except requests.exceptions.RequestException as erro:
        print(f"Erro ao conectar com a API: {erro}")


if __name__ == "__main__":
    termo = input("Digite o nome do jogo que deseja buscar: ").strip()
    if termo:
        buscar_jogo(termo)
    else:
        print("Nome do jogo não pode ser vazio.")