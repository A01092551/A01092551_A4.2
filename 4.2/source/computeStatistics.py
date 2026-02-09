# pylint: disable=invalid-name
"""
Módulo para calcular estadísticas descriptivas: promedio, mediana, moda,
varianza y desviación estándar.

El nombre del archivo no cumple con PEP8 'computeStatistics', sin embargo
se deja debido a que esta en las especificaciones de la tarea


"""

import sys
import time
from pathlib import Path


def read_data_from_file(file_path):
    """
    Lee números del archivo, manejando datos inválidos.
    Retorna lista de números válidos.
    """
    numbers = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    number = float(line)
                    numbers.append(number)
                except ValueError:
                    print(f"Error: Dato inválido en la línea {line_num}: '{line}'")
                    print("Continuando ejecución...")
    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except (IOError, OSError) as error:
        print(f"Error al leer archivo: {error}")
        sys.exit(1)

    return numbers


def calculate_mean(numbers):
    """
    Calcula el promedio usando algoritmo básico.
    """
    if len(numbers) == 0:
        return 0

    total = 0
    for num in numbers:
        total = total + num

    mean = total / len(numbers)
    return mean


def calculate_median(numbers):
    """
    Calcula la mediana usando algoritmo básico.
    """
    if len(numbers) == 0:
        return 0

    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    middle = length // 2

    if length % 2 == 0:
        median = (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2
    else:
        median = sorted_numbers[middle]

    return median


def calculate_mode(numbers):
    """
    Calcula la moda usando algoritmo básico.
    Retorna el valor más frecuente o "#N/A" si no hay valores repetidos.
    """
    if len(numbers) == 0:
        return "#N/A"

    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] = frequency[num] + 1
        else:
            frequency[num] = 1

    max_count = 0
    mode_value = numbers[0]

    for num, count in frequency.items():
        if count > max_count:
            max_count = count
            mode_value = num

    if max_count == 1:
        return "#N/A"

    return mode_value


def calculate_variance(numbers, mean):
    """
    Calcula la varianza usando algoritmo básico.
    """
    if len(numbers) == 0:
        return 0

    sum_squared_diff = 0
    for num in numbers:
        diff = num - mean
        squared_diff = diff * diff
        sum_squared_diff = sum_squared_diff + squared_diff

    variance = sum_squared_diff / len(numbers)
    return variance


def calculate_standard_deviation(variance):
    """
    Calcula la desviación estándar usando algoritmo básico.
    """
    std_dev = variance ** 0.5
    return std_dev


def format_output(file_name, stats_data):
    """
    Formatea la cadena de salida para mostrar y escribir en archivo.

    Args:
        file_name: Nombre del archivo de entrada
        stats_data: Diccionario conteniendo estadísticas y metadatos
    """
    output = []
    output.append("=" * 50)
    output.append("DESCRIPTIVE STATISTICS RESULTS")
    output.append("=" * 50)
    output.append(f"Archivo: {file_name}")
    output.append(f"Conteo: {stats_data['count']}")
    output.append(f"Promedio: {stats_data['mean']:.2f}")
    output.append(f"Mediana: {stats_data['median']:.2f}")
    if isinstance(stats_data['mode'], str):
        output.append(f"Moda: {stats_data['mode']}")
    else:
        output.append(f"Moda: {stats_data['mode']:.2f}")
    output.append(f"Desviación estándar: {stats_data['std_dev']:.2f}")
    output.append(f"Varianza: {stats_data['variance']:.2f}")
    output.append("=" * 50)
    output.append(f"Tiempo de ejecución: {stats_data['elapsed_time']:.4f} segundos")
    output.append("=" * 50)

    return "\n".join(output)


def write_results_to_file(output_text, output_dir=None):
    """
    Escribe resultados a StatisticsResults.txt en el directorio especificado.
    """
    if output_dir is None:
        output_dir = Path(
            r"D:\Documentos\Maestria Inteligencia artificial"
            r"\Pruebas de software y aseguramiento de la calidad"
            r"\A4.2\4.2\results"
        )

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_file = output_path / "StatisticsResults.txt"

        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(output_text)
            file.write("\n\n")

        print(f"\nResultados guardados en: {output_file}")
    except (IOError, OSError) as error:
        print(f"Error al escribir resultados en archivo: {error}")


def main():
    """
    Función principal para ejecutar el cálculo de estadísticas.
    """

    if len(sys.argv) < 2:
        print("Uso: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    base_path = Path(
        r"D:\Documentos\Maestria Inteligencia artificial"
        r"\Pruebas de software y aseguramiento de la calidad\A4.2\4.2\P1"
    )
    file_path = base_path / file_name

    start_time = time.time()

    print(f"Leyendo datos de: {file_path}")
    numbers = read_data_from_file(file_path)

    if len(numbers) == 0:
        print("Error: No se encontraron números válidos en el archivo.")
        sys.exit(1)

    print(f"Se leyeron exitosamente {len(numbers)} números.")
    print("\nCalculando estadísticas...")

    count = len(numbers)
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_standard_deviation(variance)

    end_time = time.time()
    elapsed_time = end_time - start_time

    stats_data = {
        'count': count,
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance,
        'std_dev': std_dev,
        'elapsed_time': elapsed_time
    }

    output_text = format_output(file_name, stats_data)

    print("\n" + output_text)

    write_results_to_file(output_text)


if __name__ == "__main__":
    main()
