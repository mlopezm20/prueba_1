import os
import sys
import openpyxl

# --- CONFIGURACIÓN DE REGLAS DE NEGOCIO ---
REQUIRED_EXCEL_COLUMNS = ["ID", "Caso de Prueba", "Precondición", "Pasos", "Resultado Esperado"]
MAX_GHERKIN_STEP_LINES = 1  # Cada paso (Dado/Cuando/Entonces/Y) no debe tener saltos de línea extra
MAX_STEP_TEXT_LENGTH = 120   # Un paso no debería exceder X caracteres sin fragmentarse

def validate_excel(excel_path):
    print(f"--- 📊 Validando Excel: {excel_path} ---")
    if not os.path.exists(excel_path):
        print(f"❌ Error: El archivo Excel '{excel_path}' no existe.")
        return False

    try:
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active

        # Obtener los nombres de las columnas (Fila 1)
        headers = [cell.value for cell in sheet[1] if cell.value is not None]
        print(f"Columnas encontradas: {headers}")

        # Validar columnas requeridas
        missing_columns = [col for col in REQUIRED_EXCEL_COLUMNS if col not in headers]
        if missing_columns:
            print(f"❌ ERROR: Faltan las siguientes columnas obligatorias en el Excel: {missing_columns}")
            return False

        print("✅ Validación de columnas en Excel: EXITOSA")
        return True
    except Exception as e:
        print(f"❌ Error al leer el archivo : {e}")
        return False


def validate_gherkin(gherkin_dir):
    print(f"\n--- 🥒 Validando Archivos Gherkin (.feature) en: {gherkin_dir} ---")
    if not os.path.isdir(gherkin_dir):
        print(f"❌ Error: El directorio '{gherkin_dir}' no existe.")
        return False

    all_valid = True
    keywords = ["Dado ", "Cuando ", "Entonces ", "Y ", "Pero ", "Given ", "When ", "Then ", "And ", "But "]

    for root, _, files in os.walk(gherkin_dir):
        for file in files:
            if file.endswith(".feature"):
                file_path = os.path.join(root, file)
                print(f"Revisando: {file}")

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    stripped_line = line.strip()

                    # Revisa si la línea empieza con una palabra clave de Gherkin
                    if any(stripped_line.startswith(kw) for kw in keywords):
                        # Regla 1: Límite de caracteres por paso para evitar pasos demasiado largos/complejos
                        if len(stripped_line) > MAX_STEP_TEXT_LENGTH:
                            print(f"  ❌ Error en línea {line_num}: El paso es demasiado largo ({len(stripped_line)} caracteres). "
                                  f"Límite permitido: {MAX_STEP_TEXT_LENGTH}. Fragmenta el paso usando 'Y' / 'And'.")
                            all_valid = False

                        # Regla 2: Un paso no debe tener saltos de línea internos o ser multilínea no permitido
                        if "\n" in stripped_line or "\r" in stripped_line:
                            print(f"  ❌ Error en línea {line_num}: Un paso individual no puede contener múltiples líneas.")
                            all_valid = False

    if all_valid:
        print("✅ Validación de archivos Gherkin: EXITOSA")
    return all_valid


if __name__ == "__main__":
    excel_status = validate_excel("data/casos_prueba.xlsx")
    gherkin_status = validate_gherkin("requirements")

    if excel_status and gherkin_status:
        print("\n🎉 TODAS LAS VALIDACIONES PASARON CORRECTAMENTE.")
        sys.exit(0)  # Retorna código 0 (Éxito a Jenkins)
    else:
        print("\n💥 SE ENCONTRARON ERRORES DE DOCUMENTACIÓN.")
        sys.exit(1)  # Retorna código 1 (Fallo a Jenkins)