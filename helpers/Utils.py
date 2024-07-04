import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def random_partition(netQTY, DIM, ratio): 
    """
    random_partition genera una partición aleatoria de una cantidad asignando una cantidad mínima a cada partición.

    Args:
        netQTY (int): cantidad total a distribuir.
        DIM (int): número de particiones a realizar.
        ratio (float): proporción de la cantidad neta que debe asignarse como cantidad mínima.

    Returns:
        list: partición de la cantidad.
    """
    baseQTY = int(netQTY*ratio)
    QTY = netQTY - baseQTY*DIM
    # Generar valores aleatorios entre 0 y QTY para DIM-1 dimensiones
    random_values = [random.randint(0, QTY) for _ in range(DIM - 1)]
    # Incluir 0 y QTY como los límites inferiores y superiores
    random_values.extend([0, QTY])
    # Ordenar los valores
    random_values.sort()
    # Calcular las diferencias entre valores consecutivos
    partition = [random_values[i+1] - random_values[i] for i in range(DIM)]
    return list(map(lambda x: x + baseQTY, partition))

def generate_random_dates(dimension, futureMonth):
    """
    generate_random_dates genera fechas aleatorias dentro de un mes.

    Args:
        dimension (int): número de fechas a generar.
        futureMonth (int): meses que transcurrirán entre el mes actual y el mes en el que se generarán las fechas.

    Returns:
        list: fechas generadas aleatoriamente.
    """
    # Obtener la fecha actual
    current_date = datetime.now()

    # Añadir el número de meses futuros a la fecha actual
    future_date = current_date + relativedelta(months=+futureMonth)

    # Obtener el inicio y fin del mes futuro
    start_date = future_date.replace(day=1)
    end_date = (start_date + relativedelta(months=+1)) - timedelta(days=1)

    # Generar una lista de fechas aleatorias dentro del mes
    random_dates = [start_date + (end_date - start_date) * random.random() for _ in range(dimension)]

    return random_dates


