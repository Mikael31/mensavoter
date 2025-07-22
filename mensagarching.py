import requests, pandas as pd, datetime as dt
from bs4 import BeautifulSoup

URL  = "https://www.studierendenwerk-muenchen-oberbayern.de/mensa/speiseplan/speiseplan_457_-de.html"
HEAD = {"User-Agent": "MensaScraper/1.0"}

resp = requests.get(URL, headers=HEAD, timeout=15)
resp.encoding = "utf-8"                       # ← Umlaut-Fix
soup = BeautifulSoup(resp.text, "lxml")

rows = []
for day in soup.select("div.c-schedule__item"):
    date_str = day.select_one("div.c-schedule__header span strong").text.strip()
    date_iso = dt.datetime.strptime(date_str, "%d.%m.%Y").date().isoformat()

    for li in day.select("ul.c-menu-dish-list li"):
        cat  = li.select_one(".stwm-artname").get_text(strip=True)
        name = li.select_one("p.c-menu-dish__title").get_text(" ", strip=True)
        rows.append({"date": date_iso, "category": cat, "dish": name})

df = pd.DataFrame(rows)

# nur heute
today_iso = dt.date.today().isoformat()
today_df  = df[df["date"] == today_iso]

pd.set_option("display.max_colwidth", None)   # volle Spaltenbreite anzeigen
print(today_df)                               # Öl & Co. stimmen jetzt
    today_df.to_json(
    "mensaplan_heute.json",   # Dateiname
    orient="records",         # 1 Gericht = 1 Objekt in einer Liste
    force_ascii=False,        # Umlaute bleiben echte Zeichen
    indent=2                  # schön formatiert
)