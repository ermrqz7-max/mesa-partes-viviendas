from copy import deepcopy
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from algoritmos import (normalizar_direccion, ordenar_por_prioridad,
                        ordenar_por_codigo, busqueda_binaria_codigo,
                        busqueda_lineal_dni, buscar_duplicado)
from clasificacion import clasificar_dano
from faq import PREGUNTAS, buscar_preguntas, obtener_respuesta
from modelo import crear_solicitud
from servicio import MesaDePartes
from tiempo import hoy
from test_base import datos_validos


def solicitud(numero=1, **cambios):
    s = crear_solicitud(f"MPV-2026-{numero:04d}", datos_validos(),
                        "MODERADO", "2026-10-23 10:00:00")
    s.update(cambios)
    return s


class AlgoritmosTest(unittest.TestCase):
    def test_normaliza_abreviaturas_tildes_signos_y_ceros(self):
        self.assertEqual(normalizar_direccion("Avenida Los Pinos N° 012"),
                         normalizar_direccion("Av. Los Pinos #12"))
        self.assertNotEqual(normalizar_direccion("Av Los Pinos 12"),
                            normalizar_direccion("Av Los Pinos 13"))

    def test_clasificacion_revisa_mayor_gravedad_primero(self):
        self.assertEqual("CRITICO", clasificar_dano("Hay grietas y la casa colapsó"))
        self.assertEqual("ALTO", clasificar_dano("El techo está dañado"))
        self.assertEqual("MODERADO", clasificar_dano("Presenta filtración"))
        self.assertEqual("LEVE", clasificar_dano("Daños en la pintura exterior"))

    def test_insercion_prioridad_fecha_y_no_modifica_entrada(self):
        lista = [solicitud(1, nivel="LEVE"),
                 solicitud(2, nivel="CRITICO", fecha_registro="2026-10-23 11:00:00"),
                 solicitud(3, nivel="CRITICO", fecha_registro="2026-10-23 09:00:00")]
        copia = deepcopy(lista)
        self.assertEqual(["MPV-2026-0003", "MPV-2026-0002", "MPV-2026-0001"],
                         [s["codigo"] for s in ordenar_por_prioridad(lista)])
        self.assertEqual(copia, lista)

    def test_busqueda_binaria_encuentra_y_descarta(self):
        lista = ordenar_por_codigo([solicitud(3), solicitud(1), solicitud(2)])
        for n in [1, 2, 3]:
            self.assertIsNotNone(busqueda_binaria_codigo(lista, f"MPV-2026-{n:04d}"))
        self.assertIsNone(busqueda_binaria_codigo(lista, "MPV-2026-0004"))
        self.assertIsNone(busqueda_binaria_codigo([], "MPV-2026-0001"))

    def test_busqueda_dni_devuelve_varios_expedientes(self):
        lista = [solicitud(1), solicitud(2), solicitud(3, dni="00000002")]
        self.assertEqual(2, len(busqueda_lineal_dni(lista, "00000001")))

    def test_duplicado_no_depende_del_dni_y_limite_es_siete_dias(self):
        fecha = hoy() - timedelta(days=10)
        s = solicitud(fecha_desastre=fecha.strftime("%d/%m/%Y"))
        for dias, esperado in [(7, True), (8, False), (-7, True)]:
            nueva = (fecha + timedelta(days=dias)).strftime("%d/%m/%Y")
            encontrado = buscar_duplicado([s], s["direccion"], "HUAICO", nueva)
            self.assertEqual(esperado, encontrado is not None)

    def test_atendido_o_tipo_distinto_permite_otro_reporte(self):
        s = solicitud(estado="ATENDIDO")
        self.assertIsNone(buscar_duplicado([s], s["direccion"], "HUAICO", s["fecha_desastre"]))
        s["estado"] = "PENDIENTE"
        self.assertIsNone(buscar_duplicado([s], s["direccion"], "TERREMOTO", s["fecha_desastre"]))

    def test_faq_tiene_catorce_y_busca_sin_tildes(self):
        self.assertEqual(14, len(PREGUNTAS))
        self.assertTrue(buscar_preguntas("CÓDIGO de seguimiento"))
        self.assertLessEqual(len(buscar_preguntas("evaluacion visita codigo")), 3)
        self.assertIsNone(obtener_respuesta(99))


class ServicioTest(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.mesa = MesaDePartes(Path(self.temporal.name) / "solicitudes.csv")

    def test_rechaza_duplicado_de_otro_familiar_sin_revelar_datos(self):
        original = self.mesa.registrar(datos_validos())["solicitud"]
        resultado = self.mesa.registrar(datos_validos(dni="00000002"))
        self.assertFalse(resultado["ok"])
        self.assertIn(original["codigo"], resultado["errores"][0])
        self.assertNotIn(original["nombres"], resultado["errores"][0])

    def test_ciclo_valido_salto_invalido_y_bandeja(self):
        codigo = self.mesa.registrar(datos_validos())["solicitud"]["codigo"]
        self.assertTrue(self.mesa.actualizar_estado(codigo, "ATENDIDO"))
        self.assertEqual("", self.mesa.actualizar_estado(codigo, "OBSERVADO"))
        self.assertEqual("", self.mesa.actualizar_estado(codigo, "PENDIENTE"))
        self.assertEqual("", self.mesa.actualizar_estado(codigo, "EVALUACION PROGRAMADA"))
        self.assertEqual("", self.mesa.actualizar_estado(codigo, "ATENDIDO"))
        self.assertEqual([], self.mesa.bandeja_priorizada())
        self.assertTrue(self.mesa.actualizar_estado(codigo, "PENDIENTE"))
        self.assertTrue(self.mesa.registrar(datos_validos())["ok"])

    def test_resumen_cuenta_niveles_y_estados(self):
        self.mesa.registrar(datos_validos())
        self.mesa.registrar(datos_validos(direccion="Calle de ejemplo 2",
                                         descripcion="La vivienda colapsó por completo"))
        niveles, estados = self.mesa.resumen()
        self.assertEqual(1, niveles["CRITICO"])
        self.assertEqual(1, niveles["MODERADO"])
        self.assertEqual(2, estados["PENDIENTE"])


if __name__ == "__main__":
    unittest.main()
