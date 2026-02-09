# pylint: disable=invalid-name
"""
Módulo para convertir números de un archivo a binario y hexadecimal.

El nombre del archivo "convertNumbers" no cumple con el PEP8,
sin embargo se deja debido a que es un requisito de la tarea.
"""

import sys
import time
from pathlib import Path


def read_data_from_file(file_path):
    """
    Lee números del archivo, manejando datos inválidos.
    Retorna lista de números enteros válidos.
    """
    numbers = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    number = int(float(line))
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


def convert_to_binary(number):
    """
    Convierte un número entero a binario usando algoritmo básico.
    Para números negativos usa complemento a dos (32 bits).
    Retorna la representación binaria como string.
    """
    if number == 0:
        return "0"

    if number > 0:
        binary = ""
        temp = number
        while temp > 0:
            remainder = temp % 2
            binary = str(remainder) + binary
            temp = temp // 2
        return binary

    # Complemento a dos para números negativos (32 bits)
    # Convertir a representación sin signo de 32 bits
    unsigned = (1 << 32) + number
    binary = ""
    temp = unsigned
    while temp > 0:
        remainder = temp % 2
        binary = str(remainder) + binary
        temp = temp // 2
    # Asegurar que tenga exactamente 32 bits
    while len(binary) < 32:
        binary = "0" + binary
    return binary


def convert_to_hexadecimal(number):
    """
    Convierte un número entero a hexadecimal usando algoritmo básico.
    Para números negativos usa complemento a dos (32 bits).
    Retorna la representación hexadecimal como string.
    """
    if number == 0:
        return "0"

    hex_digits = "0123456789ABCDEF"

    if number > 0:
        hexadecimal = ""
        temp = number
        while temp > 0:
            remainder = temp % 16
            hexadecimal = hex_digits[remainder] + hexadecimal
            temp = temp // 16
        return hexadecimal

    # Complemento a dos para números negativos (32 bits)
    # Convertir a representación sin signo de 32 bits
    unsigned = (1 << 32) + number
    hexadecimal = ""
    temp = unsigned
    while temp > 0:
        remainder = temp % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        temp = temp // 16
    # Asegurar que tenga exactamente 8 dígitos hex (32 bits)
    while len(hexadecimal) < 8:
        hexadecimal = "0" + hexadecimal
    return hexadecimal


def format_output(file_name, conversion_data):
    """
    Formatea la cadena de salida para mostrar y escribir en archivo.

    Args:
        file_name: Nombre del archivo de entrada
        conversion_data: Diccionario conteniendo conversiones y metadatos
    """
    output = []
    output.append("=" * 70)
    output.append("RESULTADOS DE CONVERSIÓN")
    output.append("=" * 70)
    output.append(f"Archivo: {file_name}")
    output.append(f"Números procesados: {conversion_data['count']}")
    output.append("=" * 70)
    output.append(f"{'Número':<15} {'Binario':<30} {'Hexadecimal':<15}")
    output.append("-" * 70)

    for item in conversion_data['conversions']:
        output.append(f"{item['decimal']:<15} {item['binary']:<30} {item['hex']:<15}")

    output.append("=" * 70)
    output.append(f"Tiempo de ejecución: {conversion_data['elapsed_time']:.4f} segundos")
    output.append("=" * 70)

    return "\n".join(output)


def write_results_to_file(output_text, output_dir=None):
    """
    Escribe resultados a ConvertionResults.txt en el directorio especificado.
    """
    if output_dir is None:
        output_dir = Path(
            r"D:\Documentos\Maestria Inteligencia artificial"
            r"\Pruebas de software y aseguramiento de la calidad"
            r"\A4.2\5.2\results"
        )

    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_file = output_path / "ConvertionResults.txt"

        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(output_text)
            file.write("\n\n")

        print(f"\nResultados guardados en: {output_file}")
    except (IOError, OSError) as error:
        print(f"Error al escribir resultados en archivo: {error}")


def main():
    """
    Función principal para ejecutar la conversión de números.
    """

    if len(sys.argv) < 2:
        print("Uso: python convertNumbers.py archivoConDatos.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    base_path = Path(
        r"D:\Documentos\Maestria Inteligencia artificial"
        r"\Pruebas de software y aseguramiento de la calidad\A4.2\5.2\P2"
    )
    file_path = base_path / file_name

    start_time = time.time()

    print(f"Leyendo datos de: {file_path}")
    numbers = read_data_from_file(file_path)

    if len(numbers) == 0:
        print("Error: No se encontraron números válidos en el archivo.")
        sys.exit(1)

    print(f"Se leyeron exitosamente {len(numbers)} números.")
    print("\nConvirtiendo números...")

    conversions = []
    for num in numbers:
        binary = convert_to_binary(num)
        hexadecimal = convert_to_hexadecimal(num)
        conversions.append({
            'decimal': num,
            'binary': binary,
            'hex': hexadecimal
        })

    end_time = time.time()
    elapsed_time = end_time - start_time

    conversion_data = {
        'count': len(numbers),
        'conversions': conversions,
        'elapsed_time': elapsed_time
    }

    output_text = format_output(file_name, conversion_data)

    print("\n" + output_text)

    write_results_to_file(output_text)


if __name__ == "__main__":
    main()
