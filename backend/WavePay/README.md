# Documentación del API para `SurfFeeCalculator`

## Introducción
Este documento describe cómo utilizar el API que se ha desarrollado para interactuar con el módulo `SurfFeeCalculator`. El API permite realizar cálculos relacionados con tarifas de campeonatos de surf, incluyendo costos de desplazamiento, manutención y costos del sistema Refresh, a través de una serie de endpoints RESTful. Este API está desarrollado utilizando Flask (Python) o puede implementarse en Node.js con Express (JavaScript).

### Endpoints Disponibles
- `/calculate_fee` (POST): Calcula la tarifa de un participante para un puesto específico.
- `/calculate_expenses` (POST): Calcula los gastos adicionales, incluyendo desplazamiento, manutención y alojamiento.
- `/calculate_refresh_cost` (POST): Calcula los costos del sistema Refresh y del operador.

## Instalación y Configuración

### Requisitos Previos
- Python 3 o Node.js, dependiendo de la versión que estés utilizando del API.
- Flask (Python) o Express (Node.js).

### Instalación del API con Flask
1. Clonar el proyecto en tu máquina local.
2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el servidor Flask desde el directorio raíz del proyecto:
   ```bash
   python app/api/surf_fee_api.py
   ```
   El servidor estará corriendo por defecto en `http://localhost:5000`.

### Instalación del API con Express (Node.js)
1. Clonar el proyecto en tu máquina local.
2. Instalar las dependencias de Node.js:
   ```bash
   npm install
   ```
3. Ejecutar el servidor Express desde el directorio `api_node`:
   ```bash
   node server.js
   ```
   El servidor estará corriendo por defecto en `http://localhost:5000`.

## Endpoints del API

### 1. `POST /calculate_fee`
Calcula la tarifa a pagar para un puesto específico.

#### URL
`/calculate_fee`

#### Método HTTP
`POST`

#### Datos del Request (JSON)
- **`hours`** (int, requerido): Número de horas trabajadas.
- **`position`** (str, requerido): El puesto del participante (ej. "director_competicion", "delegado").

#### Ejemplo de Request
```json
{
  "hours": 5,
  "position": "director_competicion"
}
```

#### Respuesta Exitosa (200)
- **`position`** (str): Puesto del participante.
- **`hours`** (int): Número de horas trabajadas.
- **`fee_after_irpf`** (float): Tarifa total después de la deducción del IRPF.

#### Ejemplo de Respuesta
```json
{
  "position": "director_competicion",
  "hours": 5,
  "fee_after_irpf": 803.19
}
```

#### Errores Comunes
- **400 Bad Request**: Parámetros faltantes o posición no válida.

### 2. `POST /calculate_expenses`
Calcula los gastos adicionales como desplazamiento, manutención y alojamiento.

#### URL
`/calculate_expenses`

#### Método HTTP
`POST`

#### Datos del Request (JSON)
- **`travel_distance_km`** (float, requerido): Distancia recorrida en kilómetros.
- **`full_meal_days`** (int, requerido): Días con manutención completa.
- **`half_meal_days`** (int, requerido): Días con media manutención.
- **`lodging_days`** (int, requerido): Días de alojamiento.

#### Ejemplo de Request
```json
{
  "travel_distance_km": 100,
  "full_meal_days": 2,
  "half_meal_days": 1,
  "lodging_days": 2
}
```

#### Respuesta Exitosa (200)
- **`travel_distance_km`** (float): Distancia recorrida.
- **`full_meal_days`** (int): Días con manutención completa.
- **`half_meal_days`** (int): Días con media manutención.
- **`lodging_days`** (int): Días de alojamiento.
- **`total_expenses`** (float): Total de gastos adicionales calculados.

#### Ejemplo de Respuesta
```json
{
  "travel_distance_km": 100,
  "full_meal_days": 2,
  "half_meal_days": 1,
  "lodging_days": 2,
  "total_expenses": 242.94
}
```

#### Errores Comunes
- **400 Bad Request**: Parámetros faltantes.

### 3. `POST /calculate_refresh_cost`
Calcula los costos del sistema Refresh.

#### URL
`/calculate_refresh_cost`

#### Método HTTP
`POST`

#### Datos del Request (JSON)
- **`refresh_days`** (int, requerido): Días de trabajo del sistema Refresh.
- **`operator_days`** (int, requerido): Días de trabajo del operador.

#### Ejemplo de Request
```json
{
  "refresh_days": 2,
  "operator_days": 2
}
```

#### Respuesta Exitosa (200)
- **`refresh_days`** (int): Días de trabajo del sistema Refresh.
- **`operator_days`** (int): Días de trabajo del operador.
- **`refresh_cost`** (float): Costo total del sistema Refresh.

#### Ejemplo de Respuesta
```json
{
  "refresh_days": 2,
  "operator_days": 2,
  "refresh_cost": 500
}
```

#### Errores Comunes
- **400 Bad Request**: Parámetros faltantes.

## Ejemplos de Uso con cURL
Puedes probar los endpoints usando `cURL` desde la línea de comandos:

### `POST /calculate_fee`
```bash
curl -X POST http://localhost:5000/calculate_fee \
-H "Content-Type: application/json" \
-d '{"hours": 5, "position": "director_competicion"}'
```

### `POST /calculate_expenses`
```bash
curl -X POST http://localhost:5000/calculate_expenses \
-H "Content-Type: application/json" \
-d '{"travel_distance_km": 100, "full_meal_days": 2, "half_meal_days": 1, "lodging_days": 2}'
```

### `POST /calculate_refresh_cost`
```bash
curl -X POST http://localhost:5000/calculate_refresh_cost \
-H "Content-Type: application/json" \
-d '{"refresh_days": 2, "operator_days": 2}'
```

## Cómo Probar el Código

### 1. Ejecutar el Backend
Primero, asegúrate de que el servidor backend esté corriendo. Dependiendo de la tecnología que uses, los pasos son:

- **Flask (Python)**: Ejecuta el siguiente comando desde el directorio raíz del proyecto:
  ```bash
  python app/api/surf_fee_api.py
  ```
  Esto iniciará el servidor Flask en `http://localhost:5000`.

- **Express (Node.js)**: Navega al directorio `api_node` y ejecuta:
  ```bash
  node server.js
  ```
  Esto iniciará el servidor Express en `http://localhost:5000`.

### 2. Usar cURL o Postman para Probar los Endpoints
Puedes usar `cURL` desde la terminal o **Postman** para probar los endpoints disponibles:

- **cURL**: Los ejemplos de solicitudes `cURL` se proporcionan en la sección anterior.
- **Postman**:
  - Abre Postman y crea una nueva solicitud.
  - Selecciona el método `POST` e ingresa la URL del endpoint (por ejemplo, `http://localhost:5000/calculate_fee`).
  - En la pestaña "Body", selecciona `raw` y el tipo `JSON`, luego ingresa el JSON necesario para la solicitud.
  - Haz clic en "Send" para enviar la solicitud y ver la respuesta.

### 3. Probar con el Frontend
Si has implementado el frontend en React para consumir este API:

- Primero, asegúrate de que el backend esté corriendo en `http://localhost:5000`.
- Luego, navega al directorio `frontend` y ejecuta:
  ```bash
  npm start
  ```
  Esto iniciará el servidor de desarrollo para el frontend en `http://localhost:3000`.

- En el navegador, abre `http://localhost:3000` y prueba la interfaz de usuario ingresando los valores para los cálculos. Haz clic en los botones correspondientes para ver los resultados obtenidos desde el backend.

### 4. Revisar los Logs
Si configuraste el backend para guardar logs en un archivo (`api_logs.log`), asegúrate de revisar este archivo para verificar que las solicitudes se están registrando correctamente. Además, también verás los logs en la consola donde el servidor está corriendo.

## Conclusión
Este API proporciona una manera sencilla de interactuar con el módulo `SurfFeeCalculator`. Puedes probarlo usando herramientas como `cURL`, **Postman** o un frontend en React. Asegúrate de que el backend esté corriendo y configurado para aceptar solicitudes desde el frontend.

Si tienes alguna pregunta adicional o necesitas más ejemplos, no dudes en consultarme.