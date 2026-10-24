from datetime import datetime, timedelta, timezone
import re

PERU = timezone(timedelta(hours=-5))


def ahora():
    return datetime.now(PERU)


def hoy():
    return ahora().date()


def leer_fecha(texto):
    """Exige DD/MM/AAAA y devuelve None cuando la fecha no existe."""
    texto = texto.strip()
    if not re.fullmatch(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", texto):
        return None
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return None
