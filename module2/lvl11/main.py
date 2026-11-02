import json
from datetime import datetime
from pathlib import Path

import requests

URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
OUTPUT = Path("data/rates.json")


def main() -> None:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    rates = {r["cc"]: r["rate"] for r in response.json() if r["cc"] in ("USD", "EUR", "PLN")}

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(rates, indent=2), encoding="utf-8")
    print(f"{datetime.now():%H:%M:%S} Курси НБУ: {rates}")
    print(f"Збережено у {OUTPUT}")


if __name__ == "__main__":
    main()
