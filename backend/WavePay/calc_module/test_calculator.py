import unittest
import logging
from calc_module.calculator import SurfFeeCalculator

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestSurfFeeCalculator(unittest.TestCase):

    def setUp(self):
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
        self.calculator = SurfFeeCalculator(position_rates, expenses, irpf_rate)

    def test_calculate_fee(self):
        hours = 5
        position = 'director_competicion'
        expected_fee = (189.87 / 8) * hours * (1 - 0.15)
        calculated_fee = self.calculator.calculate_fee(hours, position)
        logger.info(f"Calculando tarifa para {position} por {hours} horas: {calculated_fee:.2f} €")
        self.assertAlmostEqual(calculated_fee, expected_fee, places=2)

    def test_invalid_position(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_fee(5, 'invalid_position')
        logger.info("Prueba de puesto no válido realizada correctamente.")

    def test_calculate_expenses(self):
        travel_distance_km = 100
        full_meal_days = 2
        half_meal_days = 1
        lodging_days = 2
        expected_expenses = (100 * 0.19) + (2 * 37.40) + (1 * 18.70) + (2 * 65.97)
        calculated_expenses = self.calculator.calculate_expenses(travel_distance_km, full_meal_days, half_meal_days, lodging_days)
        logger.info(f"Calculando gastos adicionales: {calculated_expenses:.2f} €")
        self.assertAlmostEqual(calculated_expenses, expected_expenses, places=2)

    def test_calculate_refresh_cost(self):
        refresh_days = 2
        operator_days = 2
        expected_refresh_cost = (2 * 200) + (2 * 50)
        calculated_refresh_cost = self.calculator.calculate_refresh_cost(refresh_days, operator_days)
        logger.info(f"Calculando costos del sistema Refresh: {calculated_refresh_cost:.2f} €")
        self.assertAlmostEqual(calculated_refresh_cost, expected_refresh_cost, places=2)

    def test_calculate_fee_with_zero_hours(self):
        hours = 0
        position = 'delegado'
        expected_fee = 0.0
        calculated_fee = self.calculator.calculate_fee(hours, position)
        logger.info(f"Calculando tarifa para {position} por {hours} horas: {calculated_fee:.2f} €")
        self.assertAlmostEqual(calculated_fee, expected_fee, places=2)

    def test_calculate_fee_negative_hours(self):
        hours = -5
        position = 'delegado'
        with self.assertRaises(ValueError):
            self.calculator.calculate_fee(hours, position)
        logger.info("Prueba de horas negativas realizada correctamente.")

    def test_calculate_expenses_with_zero_distance(self):
        travel_distance_km = 0
        full_meal_days = 2
        half_meal_days = 1
        lodging_days = 2
        expected_expenses = (0 * 0.19) + (2 * 37.40) + (1 * 18.70) + (2 * 65.97)
        calculated_expenses = self.calculator.calculate_expenses(travel_distance_km, full_meal_days, half_meal_days, lodging_days)
        logger.info(f"Calculando gastos adicionales con distancia cero: {calculated_expenses:.2f} €")
        self.assertAlmostEqual(calculated_expenses, expected_expenses, places=2)

if __name__ == "__main__":
    unittest.main()
