# pylint: disable=invalid-name
"""
Módulo para contar la frecuencia de palabras en un archivo.

El nombre del archivo "wordCount" no cumple con el PEP8,
sin embargo se deja debido a que es un requisito de la tarea.
"""

import sys
import time
from pathlib import Path


def read_words_from_file(file_path):
    """
    Lee todas las palabras del archivo.
    Retorna lista de palabras.
    """
    words = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                # Extraer palabras de la línea usando algoritmo básico
                line_words = extract_words(line)
                for word in line_words:
                    words.append(word)
    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except (IOError, OSError) as error:
        print(f"Error al leer archivo: {error}")
        sys.exit(1)

    return words


def is_numeric_value(word):
    """
    Verifica si una palabra es un número (decimal, binario o hexadecimal).
    Retorna True si es un número, False en caso contrario.
    """
    if not word:
        return False

    # Verificar si es un número decimal (solo dígitos)
    is_decimal = True
    for char in word:
        if '0' <= char <= '9':
            continue
        is_decimal = False
        break
    if is_decimal:
        return True

    # Verificar si es un número binario (solo 0 y 1)
    if len(word) > 1:
        is_binary = True
        for char in word:
            if char not in ('0', '1'):
                is_binary = False
                break
        if is_binary:
            return True

    # Verificar si es un número hexadecimal (0-9, a-f)
    is_hex = True
    has_hex_char = False
    for char in word:
        if '0' <= char <= '9':
            continue
        if 'a' <= char <= 'f':
            has_hex_char = True
            continue
        is_hex = False
        break
    if is_hex and has_hex_char:
        return True

    return False


def extract_words(text):
    """
    Extrae palabras de un texto usando algoritmo básico.
    Retorna lista de palabras en minúsculas.
    """
    words = []
    current_word = ""

    for char in text:
        # Verificar si el carácter es alfanumérico
        is_alphanumeric = False
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            is_alphanumeric = True
        elif '0' <= char <= '9':
            is_alphanumeric = True

        if is_alphanumeric:
            # Convertir a minúscula manualmente
            if 'A' <= char <= 'Z':
                # Convertir mayúscula a minúscula
                lowercase_char = chr(ord(char) + 32)
                current_word = current_word + lowercase_char
            else:
                current_word = current_word + char
        else:
            # Si encontramos un separador y hay una palabra acumulada
            if current_word != "":
                # Verificar si es un número y excluirlo
                if is_numeric_value(current_word):
                    print(f"Error: Dato inválido detectado (no es string): '{current_word}'")
                else:
                    words.append(current_word)
                current_word = ""

    # Agregar la última palabra si existe
    if current_word != "":
        # Verificar si es un número y excluirlo
        if is_numeric_value(current_word):
            print(f"Error: Dato inválido detectado (no es string): '{current_word}'")
        else:
            words.append(current_word)

    return words


def count_word_frequency(words):
    """
    Cuenta la frecuencia de cada palabra usando algoritmo básico.
    Retorna diccionario con palabra y su frecuencia.
    """
    frequency = {}

    for word in words:
        if word in frequency:
            frequency[word] = frequency[word] + 1
        else:
            frequency[word] = 1

    return frequency


def format_output(file_name, word_data):
    """
    Formatea la cadena de salida para mostrar y escribir en archivo.

    Args:
        file_name: Nombre del archivo de entrada
        word_data: Diccionario conteniendo frecuencias y metadatos
    """
    output = []
    output.append("=" * 60)
    output.append("RESULTADOS DE CONTEO DE PALABRAS")
    output.append("=" * 60)
    output.append(f"Archivo: {file_name}")
    output.append(f"Total de palabras: {word_data['total_words']}")
    output.append(f"Palabras distintas: {word_data['distinct_words']}")
    output.append("=" * 60)
    output.append(f"{'Palabra':<30} {'Frecuencia':<15}")
    output.append("-" * 60)

    for word, freq in word_data['frequencies']:
        output.append(f"{word:<30} {freq:<15}")

    output.append("=" * 60)
    output.append(f"Tiempo de ejecución: {word_data['elapsed_time']:.4f} segundos")
    output.append("=" * 60)

    return "\n".join(output)


def write_results_to_file(output_text, output_dir=None):
    """
    Escribe resultados a WordCountResults.txt en el directorio especificado.
    """
    if output_dir is None:
        script_dir = Path(__file__).parent
        output_dir = script_dir.parent / "results"

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_file = output_path / "WordCountResults.txt"

        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(output_text)
            file.write("\n\n")

        print(f"\nResultados guardados en: {output_file}")
    except (IOError, OSError) as error:
        print(f"Error al escribir resultados en archivo: {error}")


def main():
    """
    Función principal para ejecutar el conteo de palabras.
    """

    if len(sys.argv) < 2:
        print("Uso: python wordCount.py archivoConDatos.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    script_dir = Path(__file__).parent
    base_path = script_dir.parent / "tests"
    file_path = base_path / file_name

    start_time = time.time()

    print(f"Leyendo datos de: {file_path}")
    words = read_words_from_file(file_path)

    if len(words) == 0:
        print("Error: No se encontraron palabras en el archivo.")
        sys.exit(1)

    print(f"Se leyeron {len(words)} palabras.")
    print("\nContando frecuencias...")

    frequency = count_word_frequency(words)

    # Convertir diccionario a lista de tuplas para ordenar
    frequency_list = []
    for word, freq in frequency.items():
        frequency_list.append((word, freq))

    # Ordenar por frecuencia descendente usando algoritmo básico (bubble sort)
    list_length = len(frequency_list)
    for i in range(list_length):
        for j in range(list_length - 1 - i):
            if frequency_list[j][1] < frequency_list[j + 1][1]:
                # Intercambiar
                frequency_list[j], frequency_list[j + 1] = (
                    frequency_list[j + 1], frequency_list[j]
                )

    word_data = {
        'total_words': len(words),
        'distinct_words': len(frequency),
        'frequencies': frequency_list,
        'elapsed_time': time.time() - start_time
    }

    output_text = format_output(file_name, word_data)

    print("\n" + output_text)

    write_results_to_file(output_text)


if __name__ == "__main__":
    main()
