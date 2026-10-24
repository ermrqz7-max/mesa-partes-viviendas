import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from modelo import crear_solicitud
from persistencia import CAMPOS_BASE, cargar, guardar
from servicio import MesaDePartes
from test_base import datos_validos


class PersistenciaTest(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / "solicitudes.csv"

    def test_archivo_inexistente(self):
        self.assertEqual([], cargar(self.ruta))

    def test_ida_y_vuelta_preserva_tildes_comas_saltos_e_historial(self):
        s = crear_solicitud("MPV-2026-0001", datos_validos(
            descripcion='Hay grietas, humedad y "filtración".\nSegunda línea.'),
            "MODERADO", "2026-10-23 10:00:00")
        guardar([s], self.ruta)
        self.assertEqual([s], cargar(self.ruta))

    def test_csv_antiguo_sin_historial_no_inventa_movimientos(self):
        s = crear_solicitud("MPV-2026-0001", datos_validos(),
                            "MODERADO", "2026-10-23 10:00:00")
        s.pop("historial")
        with self.ruta.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS_BASE)
            escritor.writeheader()
            escritor.writerow(s)
        self.assertEqual([], cargar(self.ruta)[0]["historial"])

    def test_archivo_danado_se_rechaza(self):
        self.ruta.write_text("columna_equivocada\nvalor\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            cargar(self.ruta)

    def test_reemplazo_fallido_conserva_archivo_anterior(self):
        guardar([], self.ruta)
        original = self.ruta.read_bytes()
        with patch("persistencia.os.replace", side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                guardar([], self.ruta)
        self.assertEqual(original, self.ruta.read_bytes())
        self.assertEqual([], list(self.ruta.parent.glob("*.tmp")))

    def test_registro_fallido_no_altera_memoria(self):
        mesa = MesaDePartes(self.ruta)
        with patch("persistencia.guardar", side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                mesa.registrar(datos_validos())
        self.assertEqual([], mesa.solicitudes)

    def test_transicion_fallida_no_altera_estado(self):
        mesa = MesaDePartes(self.ruta)
        codigo = mesa.registrar(datos_validos())["solicitud"]["codigo"]
        with patch("persistencia.guardar", side_effect=PermissionError):
            with self.assertRaises(PermissionError):
                mesa.actualizar_estado(codigo, "OBSERVADO", "Dato por confirmar")
        self.assertEqual("PENDIENTE", mesa.consultar_por_codigo(codigo)["estado"])

    def test_historial_se_conserva_al_reiniciar(self):
        mesa = MesaDePartes(self.ruta)
        codigo = mesa.registrar(datos_validos())["solicitud"]["codigo"]
        self.assertEqual("", mesa.actualizar_estado(codigo, "OBSERVADO", "No contesta"))
        nueva_mesa = MesaDePartes(self.ruta)
        s = nueva_mesa.consultar_por_codigo(codigo)
        self.assertEqual(["PENDIENTE", "OBSERVADO"],
                         [h["estado"] for h in s["historial"]])
        self.assertEqual("No contesta", s["historial"][-1]["observacion"])


if __name__ == "__main__":
    unittest.main()
