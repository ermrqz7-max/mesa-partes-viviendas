# Mesa de Partes Digital – Viviendas

Prototipo académico del Grupo 3 para registrar y seguir solicitudes de evaluación
de viviendas afectadas por desastres naturales. La clasificación del daño es
preliminar y no sustituye la evaluación técnica EDAN. Los plazos son referenciales
del prototipo; no representan un compromiso de atención de una municipalidad.

## Requisitos y ejecución

Python 3.10 o superior. Solo utiliza la biblioteca estándar, sin instalaciones
adicionales. La revisión de esta entrega se ejecutó con Python 3.12.14.

Desde la carpeta del proyecto, en Windows:

```powershell
py main.py
```

También puede utilizarse `python main.py` si ese es el comando disponible.
El CSV se crea en `datos/solicitudes.csv`, relativo al proyecto. Los datos locales
de uso no se incluyen en Git por la regla `datos/` del archivo `.gitignore`.

Para abrir el conjunto de demostración con datos enteramente ficticios:

```powershell
py main.py --datos ejemplos/solicitudes_demo.csv
```

La aplicación guarda cualquier cambio en el CSV seleccionado. Conserva una copia
del ejemplo si deseas repetir exactamente la demostración.

## Funciones y reglas

- Menú de registro, consulta, bandeja priorizada, estados, resumen y 14 preguntas
  frecuentes, con búsqueda por palabras clave.
- DNI de ocho dígitos, celular de nueve que inicia en 9, campos obligatorios,
  descripción de al menos diez caracteres y fecha real DD/MM/AAAA no futura.
- Código único MPV-AAAA-NNNN; utiliza el mayor correlativo guardado del año,
  no vuelve a uno al reiniciar y rechaza superar 9999 expedientes anuales.
- Duplicado: dirección normalizada y tipo iguales, diferencia de hasta siete
  días entre fechas del desastre y expediente anterior no ATENDIDO. El DNI
  no forma parte de esa comparación. La dirección se interpreta dentro de la
  localidad del prototipo; no se implementa geolocalización.
- Clasificación por raíces de palabras: CRITICO, ALTO, MODERADO y LEVE.
- Ordenamiento manual por inserción: prioridad descendente y fecha ascendente.
  Búsqueda binaria sobre una copia ordenada por código y búsqueda lineal por DNI.
- Transiciones: PENDIENTE a EVALUACION PROGRAMADA u OBSERVADO; OBSERVADO a
  PENDIENTE; EVALUACION PROGRAMADA a ATENDIDO u OBSERVADO. ATENDIDO es final.
- Cada cambio conserva estado, fecha de Perú y observación. El historial es
  una lista en memoria y se serializa como JSON dentro de una columna del CSV.
- Escritura en archivo temporal y reemplazo atómico: la memoria se actualiza
  después de guardar. Un CSV con estructura inválida se informa y no se abre
  como una lista vacía. Se aceptan CSV previos sin columna de historial, sin
  inventar movimientos anteriores.

## Organización

| Archivo | Responsabilidad |
|---|---|
| main.py | Entradas, menú, resultados y errores de la consola |
| servicio.py | MesaDePartes y coordinación de las reglas |
| modelo.py | Estructura de solicitud, constantes y transiciones |
| tiempo.py | Hora de Perú UTC-5 y conversión de fechas |
| validacion.py | Reglas para los datos ingresados |
| codigos.py | Correlativo anual único |
| clasificacion.py | Normalización y nivel preliminar |
| algoritmos.py | Inserción, búsquedas y duplicados |
| persistencia.py | Lectura y guardado del CSV e historial |
| faq.py | Preguntas frecuentes y plazos referenciales |
| tests/ | Comprobaciones unitarias y de consola con datos ficticios |

## Comprobaciones de implementación

```powershell
py -m unittest discover -s tests -v
```

Se incluyen 31 comprobaciones. Verifican formatos, duplicados, algoritmos,
transiciones, persistencia, reinicio y errores de escritura. No constituyen
una validación de campo ni utilizan información de ciudadanos.

## Historial de versiones

La rama `entrega-punto-5` conserva los commits previos y los ajustes de esta
entrega. Para consultar el historial local:

```powershell
git log --oneline --decorate
```

Repositorio: https://github.com/ermrqz7-max/mesa-partes-viviendas

## Límites del prototipo

Aplicación de consola para un operador. No incluye autenticación, edición
simultánea, conexión municipal ni diagnóstico estructural. La búsqueda de
palabras no interpreta negaciones ni todo el contexto de una descripción;
por ejemplo, puede reconocer "grietas" en "no presenta grietas". La revisión
técnica es necesaria. La subsanación registra la constancia administrativa,
sin un editor general de los datos de la solicitud.
