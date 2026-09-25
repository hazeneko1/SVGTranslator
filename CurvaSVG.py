# -*- coding: utf-8 -*-
"""
Convierte coordenadas de la curva de la estrella entre 3 "tamaños":

  1) PIXELES REALES  -> los que salen del console.log en tu web (M 172.8,82.53 C ...)
  2) LIENZO PEQUEÑO   -> el que usas en el editor SVG online (100 x 47.8 aprox)
  3) CODIGO JS        -> los multiplicadores vw*0.XX / vh*0.XX que van en tu página

USO (desde cmd, dentro de la carpeta donde guardaste este archivo):

    python curva.py

El script te pregunta qué quieres hacer y luego te pide que pegues el
path. No hace falta que quites la M, la C ni las comas: busca los 8
números que haya en el texto, estén como estén escritos.

Si tu resolución de pantalla real es distinta a 1920 x 917.76,
cambia los dos números ANCHO_REAL y ALTO_REAL de aquí abajo.
"""

import re
import sys

ANCHO_REAL = 1920      # tu ancho de pantalla real (vw)
ALTO_REAL = 917.76     # tu alto de pantalla real (vh)

LIENZO_X = 100                                    # ancho del lienzo pequeño del editor
LIENZO_Y = ALTO_REAL / (ANCHO_REAL / LIENZO_X)    # alto del lienzo pequeño (guarda la proporción)

# Divisor único para achicar de píxeles reales al lienzo pequeño SIN deformar
# (usamos el mismo número para x e y, si no la curva saldría estirada)
DIVISOR = ANCHO_REAL / LIENZO_X


def extraer_numeros(texto):
    """Saca los 8 números del texto, venga como venga escrito (con M, C, comas, etc.)."""
    encontrados = re.findall(r'-?\d+\.?\d*', texto)
    numeros = [float(n) for n in encontrados]
    if len(numeros) != 8:
        print(f"\nHe encontrado {len(numeros)} números y necesito exactamente 8")
        print("(sx sy c1x c1y c2x c2y ex ey). Revisa el texto que has pegado.\n")
        sys.exit(1)
    return numeros


def modo_down(numeros):
    """Píxeles reales -> lienzo pequeño (para pegar en el editor SVG)."""
    sx, sy, c1x, c1y, c2x, c2y, ex, ey = [n / DIVISOR for n in numeros]

    print(f"\nLienzo pequeño resultante: {LIENZO_X} x {LIENZO_Y:.2f}\n")
    print("Pega esto en el editor SVG (campo Path Data):\n")
    print(f"M {sx:.2f},{sy:.2f} C {c1x:.2f},{c1y:.2f} {c2x:.2f},{c2y:.2f} {ex:.2f},{ey:.2f}")
    print()


def modo_up(numeros):
    """Lienzo pequeño -> código JS listo para pegar en la web."""
    sx, sy, c1x, c1y, c2x, c2y, ex, ey = numeros

    resultado = {
        "sx": sx / LIENZO_X, "sy": sy / LIENZO_Y,
        "c1x": c1x / LIENZO_X, "c1y": c1y / LIENZO_Y,
        "c2x": c2x / LIENZO_X, "c2y": c2y / LIENZO_Y,
        "ex": ex / LIENZO_X, "ey": ey / LIENZO_Y,
    }

    print(f"\nLienzo pequeño usado: {LIENZO_X} x {LIENZO_Y:.2f}\n")
    print("Código JS listo para pegar:\n")
    print(f"  var sx = vw * {resultado['sx']:.4f}, sy = vh * {resultado['sy']:.4f};   // START")
    print(f"  var c1x = vw * {resultado['c1x']:.4f}, c1y = vh * {resultado['c1y']:.4f};   // tirador de inicio")
    print(f"  var c2x = vw * {resultado['c2x']:.4f}, c2y = vh * {resultado['c2y']:.4f};   // tirador de fin")
    print(f"  var ex = vw * {resultado['ex']:.4f}, ey = vh * {resultado['ey']:.4f};    // END")
    print()


def preguntar_modo():
    print("=" * 60)
    print("¿Qué quieres hacer?")
    print()
    print("  1) Tengo el console.log de mi web (píxeles reales) y")
    print("     quiero achicarlo para editar la curva en SVG Path Editor")
    print()
    print("  2) Ya edité la curva en SVG Path Editor y quiero pasarla")
    print("     a código JS para pegarla en mi web")
    print("=" * 60)

    while True:
        eleccion = input("\nEscribe 1 o 2 y pulsa Enter: ").strip()
        if eleccion in ("1", "2"):
            return eleccion
        print("Solo puedes escribir 1 o 2, prueba otra vez.")


def main():
    eleccion = preguntar_modo()

    if eleccion == "1":
        print("\nPega aquí el path completo del console.log (con M, C y comas, tal cual) y pulsa Enter:")
    else:
        print("\nPega aquí el path del lienzo pequeño del editor y pulsa Enter:")

    texto = input("> ")
    numeros = extraer_numeros(texto)

    if eleccion == "1":
        modo_down(numeros)
    else:
        modo_up(numeros)


if __name__ == "__main__":
    main()