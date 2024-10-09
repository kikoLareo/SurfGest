import unittest
from .calculator import SurfFeeCalculator
import logging

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestSurfFeeCalculator(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo para las pruebas
        logger.info('Configurando datos de prueba para SurfFeeCalculator')
        self.position_rates = {
            'director_competicion': 189.87,
            'delegado': 143.04,
            'xefe_xuices_nacional': 176.47,
            'xefe_xuices_rexional': 143.04,
            'xuices_nacional': 117.65,
            'xuices_rexional': 94.94,
            'infraestructura': 113.92,
            'speaker': 117.65
        }
        self.expenses = {
            'kilometraje': 0.19,
            'manutencion_completa': 37.40,
            'media_manutencion': 18.70,
            'alojamiento': 65.97,
            'refresh': 200,
            'operator': 50
        }
        self.irpf_rate = 0.15
        self.calculator = SurfFeeCalculator(self.position_rates, self.expenses, self.irpf_rate)
        logger.info('SurfFeeCalculator configurado con éxito')

    def test_calculate_hourly_rate(self):
        daily_rate = 189.87
        expected_hourly_rate = daily_rate / 8
        logger.info(f'Calculando tarifa por hora a partir de tarifa diaria {daily_rate}')
        self.assertAlmostEqual(self.calculator.calculate_hourly_rate(daily_rate), expected_hourly_rate, places=2)
        logger.info(f'Tarifa por hora calculada correctamente: {expected_hourly_rate:.2f}')

    def test_calculate_fee_valid_position(self):
        hours = 5
        position = 'director_competicion'
        expected_fee = (self.position_rates[position] / 8 * hours) * (1 - self.irpf_rate)
        logger.info(f'Calculando tarifa para {position} por {hours} horas')
        self.assertAlmostEqual(self.calculator.calculate_fee(hours, position), expected_fee, places=2)
        logger.info(f'Tarifa calculada correctamente para {position}: {expected_fee:.2f}')

    def test_calculate_fee_invalid_position(self):
        logger.info('Probando cálculo de tarifa con posición inválida')
        with self.assertRaises(ValueError):
            self.calculator.calculate_fee(5, 'invalid_position')
        logger.info('Error capturado correctamente para posición inválida')

    def test_calculate_fee_negative_hours(self):
        logger.info('Probando cálculo de tarifa con horas negativas')
        with self.assertRaises(ValueError):
            self.calculator.calculate_fee(-5, 'director_competicion')
        logger.info('Error capturado correctamente para horas negativas')

    def test_calculate_expenses(self):
        travel_distance_km = 100
        full_meal_days = 2
        half_meal_days = 1
        lodging_days = 2

        logger.info('Calculando gastos adicionales para desplazamiento, manutención y alojamiento')
        expected_travel_cost = travel_distance_km * self.expenses['kilometraje']
        expected_meal_cost = (full_meal_days * self.expenses['manutencion_completa']) + (half_meal_days * self.expenses['media_manutencion'])
        expected_lodging_cost = lodging_days * self.expenses['alojamiento']
        expected_total_expenses = expected_travel_cost + expected_meal_cost + expected_lodging_cost

        self.assertAlmostEqual(self.calculator.calculate_expenses(travel_distance_km, full_meal_days, half_meal_days, lodging_days), expected_total_expenses, places=2)
        logger.info(f'Gastos adicionales calculados correctamente: {expected_total_expenses:.2f}')

    def test_calculate_refresh_cost(self):
        refresh_days = 2
        operator_days = 2

        logger.info('Calculando costos del sistema Refresh')
        expected_refresh_cost = refresh_days * self.expenses['refresh']
        expected_operator_cost = operator_days * self.expenses['operator']
        expected_total_refresh_cost = expected_refresh_cost + expected_operator_cost

        self.assertAlmostEqual(self.calculator.calculate_refresh_cost(refresh_days, operator_days), expected_total_refresh_cost, places=2)
        logger.info(f'Costos del sistema Refresh calculados correctamente: {expected_total_refresh_cost:.2f}')

if __name__ == '__main__':
    unittest.main()