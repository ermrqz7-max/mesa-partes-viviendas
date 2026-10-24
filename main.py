from servicio import MesaDePartes
from modelo import TIPOS_DESASTRE, TRANSICIONES
from faq import PREGUNTAS, buscar_preguntas, obtener_respuesta


def pedir(texto):
    return input(texto).strip()


def elegir_de_lista(titulo, opciones):
    print(titulo)
    for i in range(len(opciones)):
        print(f"  {i + 1}. {opciones[i]}")
    eleccion = pedir("Elija una opción: ")
    if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
        return opciones[int(eleccion) - 1]
    return ""


def mostrar_solicitud(s, mesa):
    print("-" * 50)
    print("Código:", s["codigo"])
    print("Nivel preliminar:", s["nivel"], "| Plazo referencial:", mesa.plazo_estimado(s))
    print("Estado:", s["estado"])
    print("Tipo:", s["tipo"], "| Fecha del desastre:", s["fecha_desastre"])
    print("Dirección:", s["direccion"], "-", s["sector"])
    if s["observacion"] != "":
        print("Observación:", s["observacion"])


def opcion_registrar(mesa):
    print("\n--- Registrar solicitud ---")
    datos = {
        "dni": pedir("DNI (8 dígitos): "),
        "nombres": pedir("Nombres y apellidos: "),
        "telefono": pedir("Celular (9 dígitos, empieza en 9): "),
        "direccion": pedir("Dirección de la vivienda: "),
        "sector": pedir("Sector / AA.HH.: "),
        "tipo": elegir_de_lista("Tipo de desastre:", TIPOS_DESASTRE),
        "fecha_desastre": pedir("Fecha del desastre (DD/MM/AAAA): "),
        "descripcion": pedir("Descripción del daño: "),
    }
    resultado = mesa.registrar(datos)
    if resultado["ok"]:
        s = resultado["solicitud"]
        print("\nSolicitud registrada con código", s["codigo"], "- nivel preliminar:", s["nivel"])
        print("Aviso: la clasificación es preliminar y no reemplaza la evaluación técnica (EDAN).")
    else:
        for error in resultado["errores"]:
            print(" -", error)


def opcion_consultar(mesa):
    print("\n--- Consultar solicitud ---")
    modo = pedir("1. Por código   2. Por DNI: ")
    if modo == "1":
        s = mesa.consultar_por_codigo(pedir("Código (MPV-AAAA-NNNN): "))
        if s is None:
            print("No se encontró ninguna solicitud con ese código.")
        else:
            mostrar_solicitud(s, mesa)
    elif modo == "2":
        encontradas = mesa.consultar_por_dni(pedir("DNI: "))
        if len(encontradas) == 0:
            print("No se encontraron solicitudes para ese DNI.")
        for s in encontradas:
            mostrar_solicitud(s, mesa)
    else:
        print("Opción no válida.")


def opcion_bandeja(mesa):
    print("\n--- Bandeja priorizada ---")
    bandeja = mesa.bandeja_priorizada()
    if len(bandeja) == 0:
        print("No hay solicitudes activas.")
    for s in bandeja:
        print(s["codigo"], "|", s["nivel"], "|", s["estado"], "|", s["fecha_registro"], "|", s["sector"])


def opcion_estado(mesa):
    print("\n--- Actualizar estado ---")
    codigo = pedir("Código de la solicitud: ")
    s = mesa.consultar_por_codigo(codigo)
    if s is None:
        print("No existe una solicitud con ese código.")
        return
    permitidos = TRANSICIONES[s["estado"]]
    if len(permitidos) == 0:
        print("Esta solicitud ya está en un estado final (ATENDIDO).")
        return
    print("Estado actual:", s["estado"])
    nuevo = elegir_de_lista("Nuevo estado:", permitidos)
    if nuevo == "":
        print("Opción no válida.")
        return
    observacion = pedir("Observación (opcional): ")
    mensaje = mesa.actualizar_estado(codigo, nuevo, observacion)
    if mensaje == "":
        print("Estado actualizado a", nuevo)
    else:
        print(mensaje)


def opcion_resumen(mesa):
    print("\n--- Resumen ---")
    por_nivel, por_estado = mesa.resumen()
    print("Por nivel:")
    for nivel in por_nivel:
        print("  ", nivel, ":", por_nivel[nivel])
    print("Por estado:")
    for estado in por_estado:
        print("  ", estado, ":", por_estado[estado])


def opcion_faq():
    print("\n--- Preguntas frecuentes ---")
    for i in range(len(PREGUNTAS)):
        print(f"{i + 1}. {PREGUNTAS[i]['pregunta']}")
    entrada = pedir("Número de pregunta o palabra a buscar (Enter = volver): ")
    if entrada == "":
        return
    if entrada.isdigit():
        respuesta = obtener_respuesta(int(entrada) - 1)
        if respuesta is None:
            print("Número fuera de rango.")
        else:
            print(respuesta)
    else:
        coincidencias = buscar_preguntas(entrada)
        if len(coincidencias) == 0:
            print("No hay coincidencias.")
        for item in coincidencias:
            print("\n" + PREGUNTAS[item[0]]["pregunta"])
            print(PREGUNTAS[item[0]]["respuesta"])
            
def mostrar_menu():
    print("\n===== MESA DE PARTES DIGITAL - VIVIENDA =====")
    print("\n1. Registrar solicitud")
    print("2. Consultar solicitud")
    print("3. Bandeja priorizada")
    print("4. Actualizar estado")
    print("5. Resumen")
    print("6. Preguntas frecuentes")
    print("0. Salir")


def main():
    mesa = MesaDePartes()
    while True:
        mostrar_menu()
        opcion = pedir("Opción: ")
        if opcion == "1":
            opcion_registrar(mesa)
        elif opcion == "2":
            opcion_consultar(mesa)
        elif opcion == "3":
            opcion_bandeja(mesa)
        elif opcion == "4":
            opcion_estado(mesa)
        elif opcion == "5":
            opcion_resumen(mesa)
        elif opcion == "6":
            opcion_faq()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()