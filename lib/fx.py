"""Historical FX rates from Frankfurter (ECB data)."""
import requests
from datetime import date, timedelta


def get_rate(from_ccy: str, to_ccy: str, on: date) -> float:
    if from_ccy == to_ccy:
        return 1.0
    # ECB only publishes on weekdays; walk back to last available date.
    d = on
    for _ in range(7):
        r = requests.get(
            f"https://api.frankfurter.app/{d.isoformat()}",
            params={"from": from_ccy, "to": to_ccy},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("rates", {}).get(to_ccy):
            return data["rates"][to_ccy]
        d -= timedelta(days=1)
    raise RuntimeError(f"No FX rate found for {from_ccy}->{to_ccy} near {on}")


def convert(amount: float, from_ccy: str, to_ccy: str, on: date) -> float:
    return amount * get_rate(from_ccy, to_ccy, on)
