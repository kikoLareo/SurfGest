# Documentación del Módulo `SurfFeeCalculator`

## Introducción
El módulo `SurfFeeCalculator` fue desarrollado para calcular las tarifas asociadas con campeonatos de surf, teniendo en cuenta varios factores como las horas trabajadas, los puestos desempeñados, los gastos de desplazamiento, manutención, alojamiento, y costos del sistema Refresh. Además, se considera la deducción del IRPF para algunas tarifas.

### Características
- Cálculo de tarifas por horas y puestos específicos en los campeonatos de surf.
- Cálculo de gastos adicionales como kilometraje, manutención y alojamiento.
- Inclusión de costos del sistema Refresh para mejorar la transparencia en el presupuesto.
- Aplicación de IRPF (Impuesto sobre la Renta de las Personas Físicas) a las tarifas calculadas.

## Estructura del Código
El archivo `calculator.py` está compuesto por la clase `SurfFeeCalculator` y varios métodos que permiten realizar los cálculos necesarios.

### Clase `SurfFeeCalculator`
La clase `SurfFeeCalculator` es la encargada de gestionar todos los cálculos relacionados con los campeonatos. Se inicializa con los siguientes parámetros:
- **`position_rates`**: Un diccionario que contiene las tarifas diarias para cada puesto (por ejemplo, "director_competicion", "delegado", etc.).
- **`expenses`**: Un diccionario que contiene los gastos adicionales, tales como kilometraje, manutención, alojamiento, costos del sistema Refresh y del operador.
- **`irpf_rate`**: Un valor decimal que representa el porcentaje de IRPF (ejemplo: 0.15 para un 15%).

### Métodos de la Clase
1. **`calculate_hourly_rate(daily_rate)`**: Calcula la tarifa por hora a partir de la tarifa diaria. La tarifa diaria se divide entre 8 (horas laborales estándar).
   - Parámetros: `daily_rate` (float) - Tarifa diaria.
   - Retorno: Tarifa por hora (float).

2. **`calculate_fee(hours, position)`**: Calcula la tarifa total a pagar para un puesto específico, descontando el IRPF.
   - Parámetros: `hours` (int) - Número de horas trabajadas; `position` (str) - El puesto del participante.
   - Retorno: Tarifa calculada después del IRPF (float).

3. **`calculate_expenses(travel_distance_km, full_meal_days, half_meal_days, lodging_days)`**: Calcula los gastos adicionales (kilometraje, manutención y alojamiento).
   - Parámetros: `travel_distance_km` (float) - Distancia recorrida en kilómetros; `full_meal_days` (int) - Días con manutención completa; `half_meal_days` (int) - Días con media manutención; `lodging_days` (int) - Días de alojamiento.
   - Retorno: Gastos adicionales totales (float).

4. **`calculate_refresh_cost(refresh_days, operator_days)`**: Calcula los costos del sistema Refresh y del operador.
   - Parámetros: `refresh_days` (int) - Días de uso del sistema Refresh; `operator_days` (int) - Días de trabajo del operador.
   - Retorno: Costos totales del sistema Refresh (float).

## Uso del Código
### Instalación de Dependencias
Para usar este módulo, primero asegúrate de tener Python instalado. Puedes instalar las dependencias necesarias mediante un archivo `requirements.txt` (si existiera) o utilizando los siguientes pasos:

1. Clona el repositorio donde se encuentra el archivo `calculator.py`.
2. Navega al directorio del proyecto:
   ```bash
   cd surfcharge
   ```
3. Crea un entorno virtual e instala cualquier dependencia adicional si fuera necesario:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   pip install -r requirements.txt  # Si hubiera un archivo de dependencias
   ```

### Ejemplo de Uso
Puedes utilizar el módulo ejecutando el archivo `calculator.py`. En el siguiente ejemplo, se demuestra cómo instanciar la clase `SurfFeeCalculator` y calcular las tarifas:

```python
if __name__ == "__main__":
    position_rates = {
        'director_competicion': 189.87,
        'delegado': 143.04,
        'xefe_xuices_nacional': 176.47,
        'xefe_xuices_rexional': 143.04,
        'xuices_nacional': 117.65,
        'xuices_rexional': 94.94,
        'infraestructura': 113.92,
        'speaker': 117.65
    }

    expenses = {
        'kilometraje': 0.19,                # €/km
        'manutencion_completa': 37.40,      # € por día
        'media_manutencion': 18.70,         # € por día
        'alojamiento': 65.97,               # € por día
        'refresh': 200,                     # € por día de trabajo del sistema Refresh
        'operator': 50                      # € por día de trabajo del operador
    }

    irpf_rate = 0.15  # 15% de IRPF

    calculator = SurfFeeCalculator(position_rates, expenses, irpf_rate)

    # Calcular tarifa de un participante
    hours = 5
    position = 'director_competicion'
    try:
        fee = calculator.calculate_fee(hours, position)
        print(f"La tarifa para el puesto {position} por {hours} horas después de IRPF es: {fee:.2f} €")
    except ValueError as e:
        print(e)

    # Calcular gastos de desplazamiento, manutención y alojamiento
    travel_distance_km = 100
    full_meal_days = 2
    half_meal_days = 1
    lodging_days = 2
    expenses_total = calculator.calculate_expenses(travel_distance_km, full_meal_days, half_meal_days, lodging_days)
    print(f"Gastos totales de desplazamiento, manutención y alojamiento: {expenses_total:.2f} €")

    # Calcular costos del sistema Refresh
    refresh_days = 2
    operator_days = 2
    refresh_cost = calculator.calculate_refresh_cost(refresh_days, operator_days)
    print(f"Costos del sistema Refresh: {refresh_cost:.2f} €")
```

### Ejecutar el Código
Para ejecutar el código, simplemente usa el comando:
```bash
python calculator.py
```
Esto mostrará los resultados de ejemplo, incluyendo las tarifas calculadas y los gastos adicionales.

## Pruebas
### Pruebas Unitarias
En el archivo `test_calculator.py` se incluyen pruebas unitarias para verificar el correcto funcionamiento de las funciones. Puedes ejecutar las pruebas usando el módulo `unittest` de la siguiente manera:

```bash
python -m unittest app.calc_module.test_calculator
```
Esto ejecutará todas las pruebas unitarias definidas en el archivo y te informará si alguna prueba falla.

### Prueba de Ejemplo
El script de prueba (`test_calculator.py`) contiene ejemplos como:
- Verificar que el cálculo de la tarifa por un puesto específico y ciertas horas sea el correcto.
- Asegurarse de que la deducción de IRPF se aplique correctamente.
- Verificar que las excepciones sean lanzadas adecuadamente si se ingresa un puesto no válido.

### Ajustes Adicionales
- Si necesitas ajustar la tasa de IRPF o las tarifas para diferentes puestos, puedes hacerlo editando el diccionario `position_rates` o el parámetro `irpf_rate` en el archivo principal.

## Conclusión
El módulo `SurfFeeCalculator` está diseñado para ser flexible y fácil de usar, permitiendo cálculos complejos de tarifas con mínimos pasos. Cualquier usuario que desee utilizar este módulo puede modificar las tarifas y los gastos según las necesidades específicas de su campeonato.

Si tienes preguntas adicionales o deseas hacer mejoras, estaré encantado de ayudarte.
