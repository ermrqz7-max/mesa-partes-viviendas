"""Comprobaciones de reglas del prototipo con datos enteramente ficticios."""
import unittest
from datetime import timedelta

from codigos import generar_codigo
from tiempo import hoy, leer_fecha
from validacion import es_dni_valido, es_telefono_valido, validar_solicitud


def datos_validos(**cambios):
    datos = {
        "dni": "00000001", "nombres": "Persona de ejemplo",
        "telefono": "900000001", "direccion": "Calle de ejemplo 1",
        "sector": "Sector ficticio", "tipo": "HUAICO",
        "fecha_desastre": (hoy() - timedelta(days=1)).strftime("%d/%m/%Y"),
        "descripcion": "La vivienda presenta grietas en una pared.",
    }
    datos.update(cambios)
    return datos


class ValidacionesTest(unittest.TestCase):
    def test_dni_con_cero_inicial(self):
        self.assertTrue(es_dni_valido("00000001"))

    def test_dni_rechaza_letras_longitud_y_digitos_no_ascii(self):
        for dni in ["123", "1234567A", "１２３４５６７８"]:
            with self.subTest(dni=dni):
                self.assertFalse(es_dni_valido(dni))

    def test_telefono_exige_nueve_digitos_y_prefijo_nueve(self):
        self.assertTrue(es_telefono_valido("900000001"))
        for tel in ["800000001", "900", "90000000x"]:
            self.assertFalse(es_telefono_valido(tel))

    def test_fecha_real_y_formato_estricto(self):
        self.assertIsNotNone(leer_fecha("29/02/2024"))
        for fecha in ["31/02/2026", "29/02/2025", "1/02/2026", "2026-02-01"]:
            self.assertIsNone(leer_fecha(fecha))

    def test_fecha_futura_rechazada(self):
        futura = (hoy() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.assertTrue(validar_solicitud(datos_validos(fecha_desastre=futura)))

    def test_campos_obligatorios_y_descripcion(self):
        self.assertTrue(validar_solicitud(datos_validos(sector="   ")))
        self.assertTrue(validar_solicitud(datos_validos(descripcion="Corta")))
        self.assertEqual([], validar_solicitud(datos_validos()))


class CodigosTest(unittest.TestCase):
    def test_correlativo_considera_archivo_y_anio(self):
        existentes = [{"codigo": "MPV-2025-0020"}, {"codigo": "MPV-2026-0007"}]
        self.assertEqual("MPV-2026-0008", generar_codigo(existentes, 2026))
        self.assertEqual("MPV-2027-0001", generar_codigo(existentes, 2027))

    def test_limite_preserva_formato_de_cuatro_digitos(self):
        with self.assertRaises(ValueError):
            generar_codigo([{"codigo": "MPV-2026-9999"}], 2026)


if __name__ == "__main__":
    unittest.main()
