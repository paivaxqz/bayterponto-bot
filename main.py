import os, json, random, time, base64, uuid
from http.client import HTTPSConnection
from datetime import datetime, timezone, timedelta

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL = os.environ["DISCORD_CHANNEL_ID"]
BR = timezone(timedelta(hours=-3))
DEFAULT_MSG = "**ENTRADA: 18h **\n**PAUSA:  **\n**SAIDA: 00:00**"

_raw = os.environ.get("SCHEDULES", "")
SCHEDS = json.loads(_raw) if _raw else [{"h": 18, "m": 0, "msg": DEFAULT_MSG, "on": True}]

def _headers():
    bn = random.choice([318537, 318600, 319001, 319450])
    sp = base64.b64encode(json.dumps({
        "os": "Windows", "browser": "Chrome", "device": "",
        "system_locale": "pt-BR",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "browser_version": "128.0.0.0", "os_version": "10",
        "referrer": "https://discord.com/channels/@me",
        "referring_domain": "discord.com",
        "release_channel": "stable",
        "client_build_number": bn,
        "client_event_source": None, "design_id": 0,
    }, separators=(",", ":")).encode()).decode()
    d1, d2 = uuid.uuid4().hex, uuid.uuid4().hex + uuid.uuid4().hex[:32]
    return {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "X-Super-Properties": sp,
        "X-Discord-Locale": "pt-BR",
        "X-Discord-Timezone": "America/Sao_Paulo",
        "X-Debug-Options": "bugReporterEnabled",
        "Origin": "https://discord.com",
        "Referer": f"https://discord.com/channels/@me/{CHANNEL}",
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": f"__dcfduid={d1}; __sdcfduid={d2}; locale=pt-BR",
    }

def _req(method, path, body=None):
    c = HTTPSConnection("discord.com")
    c.request(method, "/api/v9" + path, body=json.dumps(body) if body else None, headers=_headers())
    r = c.getresponse()
    s, d = r.status, r.read().decode()
    c.close()
    return s, d

def _nonce():
    return str(((int(time.time() * 1000) - 1420070400000) << 22) | random.randint(0, 4194303))

def send(msg):
    _req("GET", f"/channels/{CHANNEL}/messages?limit=1")
    time.sleep(random.uniform(1.0, 2.5))
    _req("POST", f"/channels/{CHANNEL}/typing")
    time.sleep(random.uniform(2.0, 4.5))
    _req("POST", f"/channels/{CHANNEL}/typing")
    time.sleep(random.uniform(1.5, 3.0))
    return _req("POST", f"/channels/{CHANNEL}/messages", {
        "content": msg, "nonce": _nonce(), "tts": False, "flags": 0
    })

sent = {}
print(f"[BOT] Iniciado | {len(SCHEDS)} alarme(s)")
for i, s in enumerate(SCHEDS):
    print(f"  {s['h']:02d}:{s['m']:02d} {'ON' if s.get('on', True) else 'OFF'}")

while True:
    now = datetime.now(BR)
    day = now.strftime("%Y%m%d")
    for i, s in enumerate(SCHEDS):
        if not s.get("on", True):
            continue
        k = f"{day}{i}"
        if k in sent:
            continue
        if now.hour == s["h"] and now.minute == s["m"]:
            time.sleep(random.uniform(3, 25))
            st, _ = send(s.get("msg", DEFAULT_MSG))
            if st == 200:
                print(f"[OK] {now.strftime('%H:%M:%S')} alarme {i}")
                sent[k] = 1
            else:
                print(f"[ERR] {now.strftime('%H:%M:%S')} alarme {i}: {st}")
    for old in [x for x in sent if not x.startswith(day)]:
        del sent[old]
    time.sleep(15)
