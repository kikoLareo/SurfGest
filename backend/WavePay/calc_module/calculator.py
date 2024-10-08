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

# Ejemplo de uso
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
        logger.error(e)

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