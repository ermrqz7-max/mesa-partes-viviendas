from modelo import PRIORIDAD


def va_antes(a, b):
    if PRIORIDAD[a["nivel"]] != PRIORIDAD[b["nivel"]]:
        return PRIORIDAD[a["nivel"]] > PRIORIDAD[b["nivel"]]
    return a["fecha_registro"] < b["fecha_registro"]


def ordenar_por_prioridad(solicitudes):
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
    lista = list(solicitudes)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and lista[j]["codigo"] > actual["codigo"]:
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = actual
    return lista