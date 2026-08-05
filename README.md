<p align="center">
  <img src=".github/assets/banner.svg" alt="BayterPonto" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/host-Square%20Cloud-5865F2?style=flat-square&logo=icloud&logoColor=white" alt="Square Cloud"/>
  <img src="https://img.shields.io/badge/ram-~20MB-00C853?style=flat-square&logo=memory&logoColor=white" alt="RAM"/>
  <img src="https://img.shields.io/badge/deps-zero-FF6D00?style=flat-square&logo=pypi&logoColor=white" alt="Zero deps"/>
</p>

---

Bot leve que envia mensagem de ponto em um canal do Discord no horário programado. Roda 24/7 no Square Cloud usando **zero dependências externas** — apenas stdlib do Python.

<br/>

<p align="center">
  <img src=".github/assets/how-it-works.svg" alt="Como funciona" width="520"/>
</p>

## Funcionalidades

- Envio automático no horário configurado (padrão 18:00 BRT)
- Anti-detecção: headers reais do Chrome, cookies simulados, typing indicators, nonce snowflake
- Jitter aleatório entre 3-25s pra parecer humano
- Múltiplos alarmes via variável de ambiente
- ~20MB de RAM — cabe no plano gratuito

## Setup

**1.** Clone o repo

```
git clone https://github.com/paivaxqz/bayterponto-bot.git
```

**2.** Configure as variáveis de ambiente no Square Cloud:

| Variável | Descrição |
|---|---|
| `DISCORD_TOKEN` | Token da conta Discord |
| `DISCORD_CHANNEL_ID` | ID do canal de destino |
| `SCHEDULES` | *(opcional)* JSON com alarmes customizados |

**3.** Suba o zip no [Square Cloud Dashboard](https://squarecloud.app/dashboard)

## Alarmes customizados

Por padrão o bot envia às 18:00. Pra configurar outros horários, defina a env `SCHEDULES`:

```json
[
  {"h": 18, "m": 0, "msg": "**ENTRADA: 18h **\n**PAUSA:  **\n**SAIDA: 00:00**", "on": true},
  {"h": 12, "m": 30, "msg": "**ALMOCO**", "on": true}
]
```

## Estrutura

```
├── main.py             # bot principal (~90 linhas)
├── squarecloud.app     # config do Square Cloud
├── requirements.txt    # vazio (zero deps)
└── .github/assets/     # SVGs do README
```

## Painel Web

O painel de controle roda separado no Vercel — permite testar a conexão e fazer envios manuais.

---

<p align="center">
  <img src=".github/assets/footer.svg" alt="footer" width="400"/>
</p>
