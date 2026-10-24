from datetime import datetime, timedelta, timezone

PERU = timezone(timedelta(hours=-5))


def ahora():
    return datetime.now(PERU)


def hoy():
    return ahora().date()


def leer_fecha(texto):
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None