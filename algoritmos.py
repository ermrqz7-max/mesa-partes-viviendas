from modelo import PRIORIDAD
from clasificacion import normalizar
from tiempo import leer_fecha

EQUIVALENCIAS = {"avenida": "av", "jiron": "jr", "manzana": "mz", "lote": "lt"}
IGNORAR = ["n", "nro", "numero", "nº"]


def va_antes(a, b):
    if PRIORIDAD[a["nivel"]] != PRIORIDAD[b["nivel"]]:
        return PRIORIDAD[a["nivel"]] > PRIORIDAD[b["nivel"]]
    return a["fecha_registro"] < b["fecha_registro"]


def ordenar_por_prioridad(solicitudes):
    """Inserción estable: mayor daño primero y luego fecha más antigua."""
    lista = list(solicitudes)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and va_antes(actual, lista[j]):
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = actual
    return lista


def ordenar_por_codigo(solicitudes):
    """Prepara una copia ordenada para la búsqueda binaria."""
    lista = list(solicitudes)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and lista[j]["codigo"] > actual["codigo"]:
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = actual
    return lista


def busqueda_binaria_codigo(lista_ordenada, codigo):
    """La precondición es recibir la lista ordenada por código ascendente."""
    izq = 0
    der = len(lista_ordenada) - 1
    while izq <= der:
        medio = (izq + der) // 2
        actual = lista_ordenada[medio]["codigo"]
        if actual == codigo:
            return lista_ordenada[medio]
        elif actual < codigo:
            izq = medio + 1
        else:
            der = medio - 1
    return None


def busqueda_lineal_dni(solicitudes, dni):
    """Reúne todos los expedientes de un solicitante, no solo el primero."""
    encontrados = []
    for s in solicitudes:
        if s["dni"] == dni:
            encontrados.append(s)
    return encontrados


def normalizar_direccion(direccion):
    texto = normalizar(direccion)
    limpio = ""
    for c in texto:
        if c.isalnum():
            limpio += c
        else:
            limpio += " "
    resultado = []
    for palabra in limpio.split():
        if palabra not in IGNORAR:
            if palabra.isdigit():
                palabra = str(int(palabra))
            resultado.append(EQUIVALENCIAS.get(palabra, palabra))
    return " ".join(resultado)


def buscar_duplicado(solicitudes, direccion, tipo, fecha_desastre):
    """Vivienda y tipo iguales, hasta 7 días, expediente activo; el DNI no decide."""
    clave = normalizar_direccion(direccion)
    fecha_nueva = leer_fecha(fecha_desastre)
    for s in solicitudes:
        if s["estado"] != "ATENDIDO":
            fecha_s = leer_fecha(s["fecha_desastre"])
            misma_direccion = normalizar_direccion(s["direccion"]) == clave
            mismo_tipo = s["tipo"] == tipo
            mismo_evento = abs((fecha_s - fecha_nueva).days) <= 7
            if misma_direccion and mismo_tipo and mismo_evento:
                return s
    return None
