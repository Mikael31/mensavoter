#!/usr/bin/env python3
# mensa_scraper.py – Scrape Mensa Garching Menü von Webseite und formatiere wie API

import datetime as dt
import json
import pathlib
import re
import requests



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



def parse_week(html: str) -> dict:
    """Parst nur das Tagesmenü in ein strukturiertes Python-Objekt (ohne bs4)."""
    weekday_re = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    today_iso = dt.date.today().isoformat()

    # Find all day blocks
    day_blocks = re.findall(r'<div class="c-schedule__item">(.*?)</div>\s*</div>', html, re.S)

    for block in day_blocks:
        date_match = weekday_re.search(block)
        if not date_match:
            continue
        date_iso = dt.datetime.strptime(date_match.group(1), "%d.%m.%Y").date().isoformat()
        if date_iso != today_iso:
            continue

        dishes = []
        # Find each dish block
        for dish_match in re.findall(r'<li.*?>(.*?)</li>', block, re.S):
            # Extract dish name
            name_match = re.search(r'<p class="c-menu-dish__title">(.*?)</p>', dish_match, re.S)
            name = re.sub('<[^<]+?>', '', name_match.group(1)) if name_match else "Unbekannt"

            # Extract price
            price_match = re.search(r'class="js-meal-price">(.*?)</span>', dish_match, re.S)
            price_text = price_match.group(1).strip() if price_match else ""
            price_val = _extract_price(price_text)

            # Extract category
            cat_match = re.search(r'class="stwm-artname">(.*?)</span>', dish_match, re.S)
            dish_type = re.sub('<[^<]+?>', '', cat_match.group(1)) if cat_match else "Sonstiges"

            # Extract labels
            labels_matches = re.findall(r'<span class="js-meal-filter-tag.*?data-tag="(.*?)">', dish_match)
            labels = [label.strip().upper() for label in labels_matches]

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

        if date_iso == today_iso:
            return {"date": today_iso, "dishes": dishes}

    return {"date": today_iso, "dishes": []}


def _extract_price(price_text: str) -> float:
    """Hilfsfunktion: Preisstring zu float (z.B. '3,50 €' → 3.5)."""
    m = re.search(r"(\d+,\d+)", price_text)
    return float(m.group(1).replace(",", ".")) if m else 0.0


def main() -> None:
    html = fetch_html(URL)
    today_menu = parse_week(html)

    # JSON speichern
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(today_menu, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ JSON gespeichert:", OUT)


if __name__ == "__main__":
    main()