from tiempo import ahora


def existe_codigo(solicitudes, codigo):
    for s in solicitudes:
        if s["codigo"] == codigo:
            return True
    return False


def generar_codigo(solicitudes, anio=None):
    if anio is None:
        anio = ahora().year
    numero = 1
    for s in solicitudes:
        partes = s["codigo"].split("-")
        if partes[1] == str(anio):
            if int(partes[2]) >= numero:
                numero = int(partes[2]) + 1
    codigo = f"MPV-{anio}-{numero:04d}"
    while existe_codigo(solicitudes, codigo):
        numero += 1
        codigo = f"MPV-{anio}-{numero:04d}"
    if numero > 9999:
        raise ValueError("Se agotaron los 9999 códigos disponibles para este año.")
    return codigo
