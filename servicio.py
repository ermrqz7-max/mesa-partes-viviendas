import persistencia
from copy import deepcopy
from modelo import crear_solicitud, TRANSICIONES, NIVELES, ESTADOS
from tiempo import ahora
from validacion import validar_solicitud
from codigos import generar_codigo
from clasificacion import clasificar_dano
from faq import plazo_por_nivel
from algoritmos import (ordenar_por_prioridad, ordenar_por_codigo,
                        busqueda_binaria_codigo, busqueda_lineal_dni,
                        buscar_duplicado)


class MesaDePartes:
    def __init__(self, ruta=persistencia.RUTA):
        self.ruta = ruta
        self.solicitudes = persistencia.cargar(ruta)

    def registrar(self, datos):
        errores = validar_solicitud(datos)
        if len(errores) > 0:
            return {"ok": False, "errores": errores}
        limpios = {}
        for campo in datos:
            limpios[campo] = datos[campo].strip()
        limpios["tipo"] = limpios["tipo"].upper()
        dup = buscar_duplicado(self.solicitudes, limpios["direccion"],
                               limpios["tipo"], limpios["fecha_desastre"])
        if dup is not None:
            return {"ok": False,
                    "errores": ["Solicitud duplicada. Código existente: " + dup["codigo"]]}
        nivel = clasificar_dano(limpios["descripcion"])
        codigo = generar_codigo(self.solicitudes)
        fecha_registro = ahora().strftime("%Y-%m-%d %H:%M:%S")
        s = crear_solicitud(codigo, limpios, nivel, fecha_registro)
        # Guardar primero evita confirmar un registro que no pudo persistirse.
        nuevas = self.solicitudes + [s]
        persistencia.guardar(nuevas, self.ruta)
        self.solicitudes = nuevas
        return {"ok": True, "solicitud": s}

    def consultar_por_codigo(self, codigo):
        ordenada = ordenar_por_codigo(self.solicitudes)
        return busqueda_binaria_codigo(ordenada, codigo.strip().upper())

    def consultar_por_dni(self, dni):
        return busqueda_lineal_dni(self.solicitudes, dni.strip())

    def bandeja_priorizada(self):
        activas = []
        for s in self.solicitudes:
            if s["estado"] != "ATENDIDO":
                activas.append(s)
        return ordenar_por_prioridad(activas)

    def actualizar_estado(self, codigo, nuevo, observacion=""):
        s = self.consultar_por_codigo(codigo)
        if s is None:
            return "No existe una solicitud con ese código."
        nuevo = nuevo.strip().upper()
        if nuevo not in TRANSICIONES[s["estado"]]:
            return "No se puede pasar de " + s["estado"] + " a " + nuevo + "."
        nuevas = deepcopy(self.solicitudes)
        for copia in nuevas:
            if copia["codigo"] == s["codigo"]:
                copia["estado"] = nuevo
                copia["observacion"] = observacion.strip()
                copia.setdefault("historial", []).append({
                    "estado": nuevo,
                    "fecha": ahora().strftime("%Y-%m-%d %H:%M:%S"),
                    "observacion": observacion.strip(),
                })
                break
        persistencia.guardar(nuevas, self.ruta)
        self.solicitudes = nuevas
        return ""

    def plazo_estimado(self, s):
        return plazo_por_nivel(s["nivel"])

    def resumen(self):
        por_nivel = {}
        for nivel in NIVELES:
            por_nivel[nivel] = 0
        por_estado = {}
        for estado in ESTADOS:
            por_estado[estado] = 0
        for s in self.solicitudes:
            por_nivel[s["nivel"]] += 1
            por_estado[s["estado"]] += 1
        return por_nivel, por_estado
