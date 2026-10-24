import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from tiempo import hoy

PROYECTO = Path(__file__).resolve().parents[1]


class ConsolaTest(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "solicitudes.csv"

    def ejecutar(self, entrada):
        entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, str(PROYECTO / "main.py"),
                               "--datos", str(self.ruta)], input=entrada,
                              text=True, encoding="utf-8", capture_output=True,
                              env=entorno, timeout=10)

    def test_menu_opcion_invalida_y_salida(self):
        r = self.ejecutar("9\n0\n")
        self.assertEqual(0, r.returncode)
        self.assertIn("Opción no válida", r.stdout)
        self.assertIn("Hasta luego", r.stdout)

    def test_registrar_cerrar_y_consultar_al_reiniciar(self):
        fecha = hoy().strftime("%d/%m/%Y")
        entrada = ("1\n00000001\nPersona ficticia\n900000001\nCalle de ejemplo 1\n"
                   f"Sector ficticio\n1\n{fecha}\nLa vivienda presenta grietas\n0\n")
        r = self.ejecutar(entrada)
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("Solicitud registrada", r.stdout)
        r = self.ejecutar("2\n2\n00000001\n0\n")
        self.assertEqual(0, r.returncode, r.stderr)
        self.assertIn("MODERADO", r.stdout)
        self.assertIn("Historial del expediente", r.stdout)

    def test_csv_invalido_se_informa_y_no_se_sobrescribe(self):
        self.ruta.write_text("columna_incorrecta\n", encoding="utf-8")
        original = self.ruta.read_bytes()
        r = self.ejecutar("0\n")
        self.assertEqual(1, r.returncode)
        self.assertIn("No se pudo cargar", r.stdout)
        self.assertEqual(original, self.ruta.read_bytes())

    def test_preguntas_frecuentes_se_pueden_consultar(self):
        r = self.ejecutar("6\n6\n0\n")
        self.assertEqual(0, r.returncode)
        self.assertIn("personal técnico competente", r.stdout)


if __name__ == "__main__":
    unittest.main()
