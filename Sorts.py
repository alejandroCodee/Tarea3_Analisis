#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import time
import csv
import os
from datetime import datetime

# =============== SORTS ===============

def insertion_sort(arr):
    a = arr
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key

def selection_sort(arr):
    a = arr
    n = len(a)
    for i in range(n):
        min_i = i
        for j in range(i+1, n):
            if a[j] < a[min_i]:
                min_i = j
        if min_i != i:
            a[i], a[min_i] = a[min_i], a[i]

def bubble_sort(arr):
    a = arr
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n-1-i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped:
            break

def merge_sort(arr):
    a = arr
    if len(a) <= 1:
        return
    tmp = [0] * len(a)

    def _merge(a, l, m, r, tmp):
        i, j, k = l, m+1, l
        while i <= m and j <= r:
            if a[i] <= a[j]:
                tmp[k] = a[i]; i += 1
            else:
                tmp[k] = a[j]; j += 1
            k += 1
        while i <= m:
            tmp[k] = a[i]; i += 1; k += 1
        while j <= r:
            tmp[k] = a[j]; j += 1; k += 1
        for t in range(l, r+1):
            a[t] = tmp[t]

    def _ms(a, l, r, tmp):
        if l >= r: return
        m = (l + r) // 2
        _ms(a, l, m, tmp)
        _ms(a, m+1, r, tmp)
        _merge(a, l, m, r, tmp)

    _ms(a, 0, len(a)-1, tmp)

def heap_sort(arr):
    a = arr
    n = len(a)

    def heapify(a, n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and a[l] > a[largest]: largest = l
        if r < n and a[r] > a[largest]: largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(a, n, largest)

    for i in range(n//2 - 1, -1, -1):
        heapify(a, n, i)
    for i in range(n-1, 0, -1):
        a[0], a[i] = a[i], a[0]
        heapify(a, i, 0)

def quick_sort(arr):
    a = arr
    if len(a) <= 1:
        return

    def _qs(a, l, r):
        while l < r:
            i, j = l, r
            pivot_index = (l + r) // 2  
            pivot = a[pivot_index]
            while i <= j:
                while a[i] < pivot: i += 1
                while a[j] > pivot: j -= 1
                if i <= j:
                    a[i], a[j] = a[j], a[i]
                    i += 1; j -= 1
            if (j - l) < (r - i):
                if l < j: _qs(a, l, j)
                l = i
            else:
                if i < r: _qs(a, i, r)
                r = j
    _qs(a, 0, len(a)-1)

ALGORITHMS = {
    "insertion": ("Insertion Sort", insertion_sort),
    "selection": ("Selection Sort", selection_sort),
    "bubble":    ("Bubble Sort",    bubble_sort),
    "merge":     ("Merge Sort",     merge_sort),
    "heap":      ("Heap Sort",      heap_sort),
    "quick":     ("Quick Sort",     quick_sort),
}


def generar_array_aleatorio(tamano, repeticion, semilla_base=2025):
    """
    Mismos datos para mismo tamaño+repetición en TODAS las ejecuciones.
    Así comparas entre algoritmos aunque corran por separado.
    """
    semilla = semilla_base + tamano * 10 + repeticion
    rng = random.Random(semilla)
    return [rng.randint(-1_000_000, 1_000_000) for _ in range(tamano)]

def esta_ordenado(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

CSV_FILE = "resultados_sort.csv"
HEADERS = ["algoritmo", "tamano", "distribucion", "repeticion", "tiempo_ms", "promedio_ms", "fecha_hora"]

def guardar_resultados_csv(filas):
    escribir_header = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if escribir_header: w.writerow(HEADERS)
        w.writerows(filas)

def parse_args():
    """
    Uso:
      python sorts.py <algoritmo> [--sizes 100,50000,200000] [--reps 3]
    """
    if len(sys.argv) < 2:
        return None, None, None
    clave = sys.argv[1].lower()
    tamanos = [100, 50000, 200000]
    repeticiones = 3
    for i, tok in enumerate(sys.argv[2:], start=2):
        if tok == "--sizes" and i+1 < len(sys.argv):
            tamanos = [int(x.strip()) for x in sys.argv[i+1].split(",")]
        if tok == "--reps" and i+1 < len(sys.argv):
            repeticiones = int(sys.argv[i+1])
    return clave, tamanos, repeticiones

def mostrar_ayuda():
    print("Uso:")
    print("  python sorts.py <algoritmo> [--sizes 100,50000,200000] [--reps 3]")
    print("Algoritmo: insertion | selection | bubble | merge | heap | quick")
    print("Ejemplos:")
    print("  python sorts.py insertion")
    print("  python sorts.py quick --sizes 100,1000,10000,200000 --reps 3")


def benchmark_un_algoritmo(clave_algoritmo, tamanos, repeticiones):
    if clave_algoritmo not in ALGORITHMS:
        print("Algoritmo no válido."); return
    nombre_bonito, funcion_sort = ALGORITHMS[clave_algoritmo]

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filas_csv = []

    print(f"=== BENCHMARK: {nombre_bonito} ===")
    print(f"Tamaños: {tamanos}")
    print(f"Repeticiones por tamaño: {repeticiones}")
    print(f"Distribución: Aleatorio\n")

    try:
        for tam in tamanos:
            tiempos = []
            print(f"-> Tamaño: {tam:,}")
            for rep in range(1, repeticiones + 1):
                arr = generar_array_aleatorio(tam, rep)

                t0 = time.perf_counter()
                funcion_sort(arr)
                t1 = time.perf_counter()

                dt_ms = (t1 - t0) * 1000.0

                if not esta_ordenado(arr):
                    print("  ✗ Error: el arreglo no quedó ordenado correctamente.")
                    raise RuntimeError("Orden incorrecto")

                tiempos.append(dt_ms)
                print(f"   Repetición {rep}: {dt_ms:.3f} ms")

                filas_csv.append([
                    nombre_bonito,
                    tam,
                    "Aleatorio",
                    rep,
                    f"{dt_ms:.3f}",
                    "",   
                    fecha_hora
                ])

            prom = sum(tiempos) / len(tiempos)
            print(f"   Promedio: {prom:.3f} ms\n")
            for i in range(1, repeticiones + 1):
                filas_csv[-i][5] = f"{prom:.3f}"

    except KeyboardInterrupt:
        print("\n[Interrumpido por usuario] Guardando resultados parciales...")

    # Guardar lo que haya
    if filas_csv:
        guardar_resultados_csv(filas_csv)
        print(f"Resultados añadidos a '{CSV_FILE}'.")
        print("Columnas: algoritmo, tamaño, distribución, repetición, tiempo_ms, promedio_ms, fecha_hora\n")
    else:
        print("No hubo resultados para guardar.")

# ====================== MAIN ======================

if __name__ == "__main__":
    clave, tamanos, repeticiones = parse_args()
    if clave is None:
        mostrar_ayuda(); sys.exit(1)
    if clave not in ALGORITHMS:
        print(f"Algoritmo desconocido: {clave}\n"); mostrar_ayuda(); sys.exit(1)
    benchmark_un_algoritmo(clave, tamanos, repeticiones)
