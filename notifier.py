import requests

# Cole aqui a URL copiada do Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1553095131664621648/nQRA7PZhGdo5FzHE-Z_9ayKBnXpcG47_oIktEeyZ9rHQeQ2MnwAq-NjL13QuRlKJJMl3"


def enviar_alerta_discord(
    titulo: str, preco_atual: float, preco_alvo: float, link_oferta: str
) -> bool:
    """Dispara um card estilizado (Embed) para o canal do Discord via Webhook."""
    if (
        not DISCORD_WEBHOOK_URL
        or "SUA_URL_DO_WEBHOOK_AQUI" in DISCORD_WEBHOOK_URL
    ):
        print(
            "[ERRO] Configure a variável DISCORD_WEBHOOK_URL com a URL gerada no Discord."
        )
        return False

    # Estrutura visual em formato de Embed do Discord (verde promocional: #2ecc71 / 3066993)
    payload = {
        "username": "CaçaJogos Alertas",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/686/686589.png",
        "embeds": [
            {
                "title": f"🎯 Meta Atingida: {titulo}",
                "description": f"O jogo atingiu ou superou a sua meta de preço!",
                "url": link_oferta,
                "color": 3066993,
                "fields": [
                    {
                        "name": "💵 Preço Atual",
                        "value": f"${preco_atual:.2f}",
                        "inline": True,
                    },
                    {
                        "name": "🎯 Preço-Alvo",
                        "value": f"${preco_alvo:.2f}",
                        "inline": True,
                    },
                    {
                        "name": "🛒 Onde Comprar",
                        "value": f"[Acessar Promoção]({link_oferta})",
                        "inline": False,
                    },
                ],
                "footer": {
                    "text": "CaçaJogos • Monitoramento Inteligente",
                },
            }
        ],
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)

        # Discord retorna HTTP 204 No Content quando a mensagem é entregue com sucesso
        if response.status_code in [200, 204]:
            print(f"[DISCORD] Alerta enviado com sucesso para '{titulo}'.")
            return True
        else:
            print(
                f"[DISCORD] Falha ao enviar alerta (Status {response.status_code}): {response.text}"
            )
            return False

    except requests.exceptions.RequestException as erro:
        print(f"[DISCORD] Erro de conexão com o Webhook: {erro}")
        return False


if __name__ == "__main__":
    # Teste de disparo individual
    print("Disparando mensagem de teste para o Discord...")
    enviar_alerta_discord(
        titulo="Dead by Daylight (Teste)",
        preco_atual=7.99,
        preco_alvo=10.00,
        link_oferta="https://www.cheapshark.com/redirect?dealID={deal_id}",
    )