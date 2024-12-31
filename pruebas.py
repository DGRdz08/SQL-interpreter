import pandas as pd

# Leer el archivo CSV en un DataFrame
df = pd.read_csv("employees.csv")

# Actualizar el salario de todos los empleados en el departamento de IT
df.loc[df['department'] == 'HR', 'salary'] = 67943

# Guardar los cambios en el archivo CSV
df.to_csv("employees.csv", index=False)

print("Sueldo de los empleados de HR actualizado y guardado en 'empleados_actualizados.csv'.")
