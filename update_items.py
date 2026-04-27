"""
update_items.py
================
Convierte el Excel de la base de datos a items.json para el dashboard.

Este script lo ejecuta automáticamente la GitHub Action cuando subes un Excel.
También puedes correrlo manualmente:

    python update_items.py
    python update_items.py --excel ruta/al/archivo.xlsx --output items.json

Requisitos: pandas, openpyxl
    pip install pandas openpyxl
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: faltan dependencias. Instala con: pip install pandas openpyxl")
    sys.exit(1)


# Columnas que SÍ son fechas y deben convertirse a datetime.
# Las columnas "CUMPLIMIENTO FECHA..." NO van aquí porque son texto, no fecha.
DATE_COLUMNS = [
    'FECHA PASO DE PAQUETE', 'FECHA DECISIÓN MODELACIÓN', 'FECHA ENTREGA DEL DLLO',
    'FECHA PROG A CORTE', 'FECHA LIQUIDACIÓN', 'FECHA APROBACIÓN INSUMOS',
    'FECHA ENTREGA PARA ASIGNAR', 'FECHA ASIGNACIÓN A CONFECCIÓN',
    'FECHA SALIDA PRODUCCIÓN', 'FECHA CARGAR PT',
    'FECHA MÁXIMA DE PROGRAMACION A CORTE', 'FECHA LIMITE PRODUCCION',
    'FECHA MÁXIMA DE APROBACION', 'FECHA LÍMITE PT CLIENTE',
    'FECHA LIMITE ENTREGA A QA',
]


def safe(v, force_int=False, force_float=False):
    """Convierte un valor de pandas a un tipo JSON-friendly."""
    if pd.isna(v):
        return None
    if isinstance(v, pd.Timestamp):
        return v.strftime('%Y-%m-%d')
    if force_int:
        try: return int(v)
        except (ValueError, TypeError): return None
    if force_float:
        try:
            f = float(v)
            return None if np.isnan(f) else f
        except (ValueError, TypeError): return None
    if isinstance(v, (int, np.integer)): return int(v)
    if isinstance(v, (float, np.floating)):
        if np.isnan(v): return None
        return float(v)
    s = str(v).strip()
    if s in ('nan', 'NaT', ''): return None
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--excel', default='Base_de_datos_-_Items_URA.xlsx',
                        help="Ruta al Excel (default: Base_de_datos_-_Items_URA.xlsx)")
    parser.add_argument('--output', default='items.json', help="Ruta de salida")
    args = parser.parse_args()

    excel_path = Path(args.excel)
    if not excel_path.exists():
        # Buscar el primer .xlsx que empiece con "Base_de_datos" en el dir actual
        candidates = list(Path('.').glob('Base_de_datos*.xlsx'))
        if candidates:
            excel_path = candidates[0]
            print(f"  → Usando Excel detectado: {excel_path}")
        else:
            print(f"ERROR: no se encontró {args.excel} ni ningún 'Base_de_datos*.xlsx' en el directorio actual")
            sys.exit(1)

    print(f"Leyendo {excel_path}...")
    df = pd.read_excel(excel_path)

    # Normalización de texto
    for col in ['PROYECTO', 'CLIENTE', 'COLECCIÓN COMPLETA']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # REGLA: "Compra insumos" → "Desarrollo"
    if 'PROCESO ACTUAL' in df.columns:
        df['PROCESO ACTUAL'] = df['PROCESO ACTUAL'].replace({'Compra insumos': 'Desarrollo'})

    # Conversión de fechas — SOLO las que realmente son fechas
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    items = []
    for _, row in df.iterrows():
        items.append({
            'item': safe(row.get('ITEM'), force_int=True),
            'cliente': safe(row.get('CLIENTE')),
            'proyecto': safe(row.get('PROYECTO')),
            'coleccion': safe(row.get('COLECCIÓN COMPLETA')),
            'genero': safe(row.get('GENERO')),
            'categoria': safe(row.get('CATEGORIA')),
            'celula': safe(row.get('CELULA')),
            'tipo': safe(row.get('TIPO')),
            'equipo': safe(row.get('EQUIPO URA')),
            'unidades': safe(row.get('UNIDADES'), force_int=True),
            'estado': safe(row.get('ESTADO ÍTEM GENERAL')),
            'proceso': safe(row.get('PROCESO ACTUAL')),
            'url': safe(row.get('URL')),
            'fecha_paso_paquete': safe(row.get('FECHA PASO DE PAQUETE')),
            'fecha_decision_modelacion': safe(row.get('FECHA DECISIÓN MODELACIÓN')),
            'fecha_entrega_dllo': safe(row.get('FECHA ENTREGA DEL DLLO')),
            'fecha_prog_corte': safe(row.get('FECHA PROG A CORTE')),
            'fecha_liquidacion': safe(row.get('FECHA LIQUIDACIÓN')),
            'fecha_aprob_insumos': safe(row.get('FECHA APROBACIÓN INSUMOS')),
            'fecha_asign_confeccion': safe(row.get('FECHA ASIGNACIÓN A CONFECCIÓN')),
            'fecha_salida_prod': safe(row.get('FECHA SALIDA PRODUCCIÓN')),
            'fecha_cargar_pt': safe(row.get('FECHA CARGAR PT')),
            'fecha_max_prog_corte': safe(row.get('FECHA MÁXIMA DE PROGRAMACION A CORTE')),
            'fecha_max_aprobacion': safe(row.get('FECHA MÁXIMA DE APROBACION')),
            'fecha_limite_prod': safe(row.get('FECHA LIMITE PRODUCCION')),
            'fecha_limite_pt_cliente': safe(row.get('FECHA LÍMITE PT CLIENTE')),
            'fecha_limite_qa': safe(row.get('FECHA LIMITE ENTREGA A QA')),
            'cumpl_aprob': safe(row.get('CUMPLIMIENTO APROBACION')),
            'cumpl_prog_corte': safe(row.get('CUMPLIMIENTO PROGRAMACION A CORTE')),
            'cumpl_pt': safe(row.get('CUMPLIMIENTO FECHA ENTREGA PT')),
            'cumpl_qa': safe(row.get('CUMPLIMIENTO FECHA ENTREGA A QA')),
            'estado_aprobacion': safe(row.get('ESTADO APROBACIÓN')),
            'estado_paquete': safe(row.get('ESTADO PAQUETE')),
            'estado_entrega_dllo': safe(row.get('ESTADO ENTREGA DEL DESARROLLO')),
            'estado_prog_corte': safe(row.get('ESTADO PROGRAMACIÓN A CORTE')),
            'estado_liq_corte': safe(row.get('ESTADO LIQUIDACIÓN CORTE')),
            'estado_lib_insumos': safe(row.get('ESTADO LIBERACIÓN INSUMOS')),
            'estado_asig_confeccion': safe(row.get('ESTADO ASIGNACIÓN A CONFECCIÓN')),
            'estado_qa': safe(row.get('ESTADO ENTREGA A QA')),
            'estado_cliente': safe(row.get('ESTADO ENTREGA A CLIENTE')),
        })

    payload = {
        'items': items,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_file': excel_path.name,
    }

    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, separators=(',', ':'))

    size_mb = output_path.stat().st_size / 1024 / 1024
    total_unidades = sum(it['unidades'] or 0 for it in items)

    print()
    print("✓ items.json generado correctamente")
    print(f"  Ítems:          {len(items):,}")
    print(f"  Unidades total: {total_unidades:,}")
    print(f"  Tamaño:         {size_mb:.2f} MB")
    print(f"  Actualizado:    {payload['last_updated']}")


if __name__ == '__main__':
    main()
