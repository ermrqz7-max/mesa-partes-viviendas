# Mesa de Partes Digital – Vivienda

Proyecto nuestro (Grupo 3)
Prototipo en Python para registrar y dar seguimiento a solicitudes de evaluación de viviendas afectadas por desastres naturales.

## Qué hace

- Registra solicitudes con código único (MPV-AAAA-NNNN).
- Valida los datos y detecta solicitudes duplicadas.
- Clasifica el daño de forma **preliminar** (no reemplaza la evaluación técnica EDAN).
- Ordena la bandeja por prioridad y busca por código o DNI.
- Actualiza el estado con transiciones válidas y guarda todo en CSV.

## Módulos

- main.py: menú de consola
- servicio.py: clase MesaDePartes
- validacion.py, codigos.py, clasificacion.py
- algoritmos.py: ordenamiento, búsquedas y duplicados
- persistencia.py: lectura y escritura de CSV
- faq.py, modelo.py, tiempo.py

## Cómo ejecutarlo

    python main.py

Requiere Python 3.10 o superior. Los datos de prueba son ficticios.