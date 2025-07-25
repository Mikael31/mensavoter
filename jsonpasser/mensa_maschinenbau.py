#!/usr/bin/env python3
# mensa_scraper.py – Scrape Mensa Garching Menü von Webseite und formatiere wie API

import datetime as dt
import json
import pathlib
import re
import requests

from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
URL = "https://www.studierendenwerk-muenchen-oberbayern.de/mensa/speiseplan/speiseplan_457_-de.html"
HEAD = {"User-Agent": "TUM-MensaScraper/1.0"}
OUT = pathlib.Path("data/mensa_maschinenbau.json")
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    """Lädt HTML und erzwingt UTF-8-Decodierung."""
    resp = requests.get(url, headers=HEAD, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text

def _extract_labels(li):
    """Extrahiert die Allergen-Kürzel (z. B. R, S, Kn) als Liste."""
    labels = []

    # Suche Text innerhalb von Klammern z. B. (R,S,Kn)
    text = li.get_text(" ", strip=True)
    match = re.findall(r"\(([^)]+)\)", text)
    for m in match:
        # Split by comma and clean
        for code in m.split(","):
            code = code.strip()
            if code and len(code) <= 5:  # Filter, damit wir nur Kürzel nehmen
                labels.append(code)

    # Alternative: Prüfe [Allergene]-Tag (falls vorhanden)
    allergen_tag = li.select_one("span, .c-menu-allergens")
    if allergen_tag:
        allergen_text = allergen_tag.get_text(strip=True)
        codes = [x.strip() for x in allergen_text.split(",")]
        labels.extend(codes)

    return list(set(labels))  # Doppelte entfernen


def parse_week(html: str) -> list:
    """Parst die ganze Woche in ein strukturiertes Python-Objekt."""
    soup = BeautifulSoup(html, "lxml")

    weekday_re = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    days = []

    for daybox in soup.select("div.c-schedule__item"):
        # Datum
        head = daybox.select_one("div.c-schedule__header span strong")
        if not head:
            continue
        head_txt = head.get_text(strip=True)
        m = weekday_re.search(head_txt)
        if not m:
            continue
        date_iso = dt.datetime.strptime(m.group(1), "%d.%m.%Y").date().isoformat()

        dishes = []
        for li in daybox.select("ul.c-menu-dish-list li"):
            name_tag = li.select_one("p.c-menu-dish__title")
            if not name_tag:
                continue
            name = name_tag.get_text(" ", strip=True)

            # Preis extrahieren (falls vorhanden)
            price_tag = li.select_one(".js-meal-price")
            price_text = price_tag.get_text(strip=True) if price_tag else ""
            price_val = _extract_price(price_text)

            # Labels (Allergene/Attribute)
            labels = _extract_labels(li)

            # Kategorie (z.B. Pasta, Fleisch)
            category = li.select_one(".stwm-artname")
            dish_type = category.get_text(strip=True) if category else "Sonstiges"

            dishes.append({
                "name": name,
                "prices": {
                    "students": {"base_price": price_val, "price_per_unit": 0.0, "unit": "100g"},
                    "staff":    {"base_price": price_val, "price_per_unit": 0.0, "unit": "100g"},
                    "guests":   {"base_price": price_val, "price_per_unit": 0.0, "unit": "100g"},
                },
                "labels": labels,
                "dish_type": dish_type
            })

        days.append({"date": date_iso, "dishes": dishes})

    return days


def _extract_price(price_text: str) -> float:
    """Hilfsfunktion: Preisstring zu float (z.B. '3,50 €' → 3.5)."""
    m = re.search(r"(\d+,\d+)", price_text)
    return float(m.group(1).replace(",", ".")) if m else 0.0


def main() -> None:
    html = fetch_html(URL)
    all_days = parse_week(html)

    today_iso = dt.date.today().isoformat()
    today_menu = next((d for d in all_days if d["date"] == today_iso), {"date": today_iso, "dishes": []})

    # JSON speichern
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(today_menu, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ JSON gespeichert:", OUT)


if __name__ == "__main__":
    main()