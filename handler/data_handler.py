import pandas as pd

class DataHandler:
    """Handles all data operations on CSV files"""

    def execute_select(self, filename, columns, conditions=None):
        try:
            # Leer el archivo CSV
            df = pd.read_csv(filename)

            # Crear una copia temporal del DataFrame para modificaciones
            temp_df = df.copy()

            # Detectar y convertir solo las columnas que son completamente válidas como fechas
            date_columns = []
            for col in temp_df.columns:
                if pd.api.types.is_string_dtype(temp_df[col]):  # Verificar columnas de tipo string
                    try:
                        # Intentar conversión completa sin NaT
                        temp_conversion = pd.to_datetime(temp_df[col], errors='coerce')
                        if temp_conversion.notna().sum() > 0:  # Confirmar que tiene fechas válidas
                            temp_df[col] = temp_conversion
                            date_columns.append(col)
                    except Exception:
                        continue  # Ignorar columnas que no son completamente válidas como fechas

            print(f"Columnas detectadas como fechas: {date_columns}")

            # Evaluar condiciones
            if conditions:
                print(f"Condiciones recibidas: {conditions}")
                try:
                    # Procesar condiciones (soportar comparaciones simples)
                    if ">" in conditions or "<" in conditions or "=" in conditions:
                        # Separar columna, operador y valor
                        for operator in [">", "<", "="]:
                            if operator in conditions:
                                condition_column, condition_value = conditions.split(operator)
                                condition_column = condition_column.strip()
                                condition_value = condition_value.strip()

                                # Asegurar que la columna de texto no tenga espacios adicionales
                                if pd.api.types.is_string_dtype(temp_df[condition_column]):
                                    temp_df[condition_column] = temp_df[condition_column].str.strip()

                                # Determinar el tipo de datos de la columna
                                if condition_column in date_columns:
                                    # Convertir valor a datetime si la columna es de fecha
                                    condition_value = pd.to_datetime(condition_value, errors='coerce')
                                    if pd.isna(condition_value):
                                        raise ValueError(f"El valor '{condition_value}' no es una fecha válida.")
                                elif pd.api.types.is_numeric_dtype(temp_df[condition_column]):
                                    # Convertir valor a número si la columna es numérica
                                    condition_value = float(condition_value)
                                elif pd.api.types.is_string_dtype(temp_df[condition_column]):
                                    # Tratar valor como cadena si la columna es texto
                                    condition_value = condition_value.strip("'\"")  # Quitar comillas

                                # Generar máscara booleana
                                if operator == ">":
                                    mask = temp_df[condition_column] > condition_value
                                elif operator == "<":
                                    mask = temp_df[condition_column] < condition_value
                                elif operator == "=":
                                    mask = temp_df[condition_column] == condition_value
                                else:
                                    raise ValueError("Operador no soportado")
                                
                                # Filtrar las filas en la copia temporal
                                temp_df = temp_df[mask]
                                break  # Salir del bucle al encontrar el operador
                    else:
                        raise ValueError("Condición no soportada.")
                except Exception as e:
                    print(f"Error al procesar condiciones en SELECT: {e}")
                    return

            # Seleccionar columnas
            if columns != '*':
                temp_df = temp_df[columns]

            print(f"Resultado de la consulta:\n{temp_df}")
        except Exception as e:
            print(f"Error en SELECT: {e}")


    def execute_insert(self, filename, values):
        try:
            df = pd.read_csv(filename)
            new_row = pd.DataFrame([values], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(filename, index=False)
            print("Fila insertada correctamente.")
        except Exception as e:
            print(f"Error al procesar el INSERT: {e}")

    def execute_update(self, filename, set_clauses, conditions=None):
        # Leer el archivo CSV
        df = pd.read_csv(filename)

        # Analizar los set_clauses para obtener columnas y valores
        updates = {}
        for clause in set_clauses.split(", "):
            column, value = clause.split(" = ")
            value = value.strip()
            if value.startswith("'") and value.endswith("'"):  # Verificar si es una cadena
                value = value[1:-1]  # Quitar las comillas
            elif value.isdigit():  # Verificar si es un número
                value = int(value)
            updates[column.strip()] = value

        print(f"Actualizaciones a aplicar: {updates}")

        # Aplicar condiciones si las hay
        if conditions:
            print(f"Condiciones recibidas: {conditions}")
            try:
                # Dividir la condición en columna y valor
                condition_column, condition_value = conditions.split(" = ")
                condition_column = condition_column.strip()
                condition_value = condition_value.strip()

                # Procesar el valor de la condición
                if condition_value.startswith("'") and condition_value.endswith("'"):
                    condition_value = condition_value[1:-1]  # Quitar las comillas
                elif condition_value.isdigit():
                    condition_value = int(condition_value)

                print(f"Condición procesada: columna={condition_column}, valor={condition_value}")

                # Filtrar las filas que cumplen la condición
                condition = df[condition_column] == condition_value
                print(f"Máscara booleana generada:\n{condition}")

                # Actualizar solo las filas que cumplen la condición
                for column, value in updates.items():
                    df.loc[condition, column] = value
            except Exception as e:
                print(f"Error al procesar las condiciones: {e}")
                return
        else:
            print("No se proporcionaron condiciones, actualizando todas las filas.")
            for column, value in updates.items():
                df[column] = value

        # Guardar los cambios
        df.to_csv(filename, index=False)
        print(f"Archivo {filename} actualizado con éxito.")

    def execute_delete(self, filename, conditions=None):
        try:
            df = pd.read_csv(filename)

            # Filtrar filas según condiciones
            if conditions:
                print(f"Condiciones recibidas: {conditions}")
                try:
                    # Procesar la condición como una expresión booleana
                    condition_column, condition_value = conditions.split(" = ")
                    condition_column = condition_column.strip()
                    condition_value = condition_value.strip()

                    # Procesar el valor de la condición
                    if condition_value.startswith("'") and condition_value.endswith("'"):
                        condition_value = condition_value[1:-1]  # Quitar las comillas
                    elif condition_value.isdigit():
                        condition_value = int(condition_value)

                    print(f"Condición procesada: columna={condition_column}, valor={condition_value}")

                    # Generar una máscara booleana
                    mask = df[condition_column] == condition_value
                    print(f"Máscara booleana generada:\n{mask}")

                    # Eliminar las filas que cumplen la condición
                    df = df[~mask]
                except Exception as e:
                    print(f"Error al procesar la condición: {e}")
                    return
            else:
                # Sin condiciones, eliminar todas las filas
                print("No se proporcionaron condiciones, eliminando todas las filas.")
                df = df.iloc[0:0]

            # Guardar los cambios
            df.to_csv(filename, index=False)
            print("Registros eliminados correctamente.")
        except Exception as e:
            print(f"Error al procesar el DELETE: {e}")
