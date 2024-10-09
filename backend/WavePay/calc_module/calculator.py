import logging

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - [ID: %(thread)d] - %(message)s'
)
logger = logging.getLogger(__name__)

class SurfFeeCalculator:
    def __init__(self, position_rates, expenses, irpf_rate):
        """
        Inicializa el calculador con tarifas, gastos adicionales e IRPF.
        :param position_rates: Diccionario con tarifas por día para cada posición.
        :param expenses: Diccionario con los gastos de desplazamiento, manutención, refresh, etc.
        :param irpf_rate: Tasa de IRPF a aplicar (por ejemplo, 0.15 para 15%).
        """
        self.position_rates = position_rates
        self.expenses = expenses
        self.irpf_rate = irpf_rate
        logger.info(f"Inicializando SurfFeeCalculator con IRPF: {irpf_rate}")

    def calculate_hourly_rate(self, daily_rate):
        """
        Calcula la tarifa por hora a partir de la tarifa diaria.
        :param daily_rate: Tarifa diaria.
        :return: Tarifa por hora.
        """
        hourly_rate = daily_rate / 8
        logger.info(f"Calculando tarifa por hora a partir de tarifa diaria {daily_rate}: {hourly_rate:.2f}")
        return hourly_rate

    def calculate_fee(self, hours, position):
        """
        Calcula la tarifa del campeonato para un participante basado en las horas y el puesto, descontando IRPF.
        :param hours: Número de horas del campeonato.
        :param position: Posición del participante (ej. 'director_competicion', 'delegado', etc.)
        :return: Tarifa calculada para el participante después del IRPF.
        """
        if position not in self.position_rates:
            logger.error(f"Puesto {position} no válido.")
            raise ValueError(f"Puesto {position} no válido.")
        if hours < 0:
            logger.error(f"Número de horas no puede ser negativo: {hours}")
            raise ValueError(f"Número de horas no puede ser negativo: {hours}")
        
        daily_rate = self.position_rates[position]
        hourly_rate = self.calculate_hourly_rate(daily_rate)
        fee_before_irpf = hourly_rate * hours
        fee_after_irpf = fee_before_irpf * (1 - self.irpf_rate)
        logger.info(f"Calculando tarifa para {position} por {hours} horas: {fee_after_irpf:.2f} € después de IRPF")
        return fee_after_irpf

    def calculate_expenses(self, travel_distance_km, full_meal_days, half_meal_days, lodging_days):
        """
        Calcula los gastos adicionales como desplazamiento, manutención y alojamiento.
        :param travel_distance_km: Distancia recorrida en kilómetros.
        :param full_meal_days: Días con manutención completa.
        :param half_meal_days: Días con media manutención.
        :param lodging_days: Días de alojamiento.
        :return: Gastos adicionales totales.
        """
        travel_cost = travel_distance_km * self.expenses['kilometraje']
        meal_cost = (full_meal_days * self.expenses['manutencion_completa']) + (half_meal_days * self.expenses['media_manutencion'])
        lodging_cost = lodging_days * self.expenses['alojamiento']
        
        total_expenses = travel_cost + meal_cost + lodging_cost
        logger.info(f"Calculando gastos adicionales: desplazamiento {travel_cost:.2f} €, manutención {meal_cost:.2f} €, alojamiento {lodging_cost:.2f} €, total: {total_expenses:.2f} €")
        return total_expenses

    def calculate_refresh_cost(self, refresh_days, operator_days):
        """
        Calcula los costos del sistema de Refresh.
        :param refresh_days: Días de trabajo del sistema Refresh.
        :param operator_days: Días de trabajo del operador.
        :return: Costos del sistema Refresh.
        """
        refresh_cost = refresh_days * self.expenses['refresh']
        operator_cost = operator_days * self.expenses['operator']
        total_refresh_cost = refresh_cost + operator_cost
        logger.info(f"Calculando costos del sistema Refresh: {total_refresh_cost:.2f} €")
        return total_refresh_cost
