# 🎮 CaçaJogos — Monitor Inteligente de Promoções de Games

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/SQLite-3-lightgrey.svg)](https://www.sqlite.org/)
[![Discord](https://img.shields.io/badge/Discord-Webhooks-5865F2.svg)](https://discord.com/)
[![ODS ONU](https://img.shields.io/badge/ONU-ODS%2012%20%7C%20ODS%209-brightgreen.svg)](https://brasil.un.org/)

Aplicação autônoma em Python voltada ao rastreamento contínuo de preços de jogos para PC, persistência de séries temporais de valores e disparo de alertas em tempo real via Discord quando metas orçamentárias customizadas são atingidas.

---

## 📌 Arquitetura e Fluxo do Sistema

O sistema é modularizado em camadas de responsabilidade única:

```text
[CheapShark API] ◄─── (GET) ─── [tracker.py] ───► (POST) ───► [Discord Webhook]
                                     │
                             (Leitura / Escrita)
                                     ▼
                           [cacajogos.db (SQLite)]
                                ├── jogos_monitorados
                                └── historico_precos
