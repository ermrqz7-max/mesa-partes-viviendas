from tiempo import leer_fecha, hoy
from modelo import TIPOS_DESASTRE

CAMPOS_OBLIGATORIOS = [
    "dni", "nombres", "telefono", "direccion",
    "sector", "tipo", "fecha_desastre", "descripcion",
]


def es_dni_valido(dni):
    dni = dni.strip()
    return len(dni) == 8 and dni.isdigit()


def es_telefono_valido(telefono):
    telefono = telefono.strip()
    return len(telefono) == 9 and telefono.isdigit() and telefono[0] == "9"


def validar_fecha_desastre(texto):
    fecha = leer_fecha(texto)
    if fecha is None:
        return "La fecha no es válida."
    if fecha > hoy():
        return "La fecha no puede ser posterior a hoy."
    return ""


def validar_solicitud(datos):
    errores = []
    for campo in CAMPOS_OBLIGATORIOS:
        if datos.get(campo, "").strip() == "":
            errores.append("El campo " + campo + " es obligatorio.")
    if len(errores) > 0:
        return errores
    if not es_dni_valido(datos["dni"]):
        errores.append("El DNI debe tener 8 dígitos numéricos.")
    if not es_telefono_valido(datos["telefono"]):
        errores.append("El teléfono debe tener 9 dígitos y empezar en 9.")
    if datos["tipo"].strip().upper() not in TIPOS_DESASTRE:
        errores.append("Tipo de desastre no válido.")
    mensaje = validar_fecha_desastre(datos["fecha_desastre"])
    if mensaje != "":
        errores.append(mensaje)
    if len(datos["descripcion"].strip()) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres.")
    return errores