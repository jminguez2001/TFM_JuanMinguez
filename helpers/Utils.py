import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def random_partition(netQTY, DIM, ratio): 
    """random_partition it generates a random partition of a quantity assinging a minimun quantity to each partition

    Args:
        netQTY (int): total quantity to be distributed
        DIM (int): number of partitions to be made
        ratio (float): ratio of the net quantity that must be assigned as minimum quantity

    Returns:
        list: partition of the quantity
    """
    baseQTY = int(netQTY*ratio)
    QTY = netQTY - baseQTY*DIM
    # Generate dimension1-1 random values between 0 and StableMQTY
    random_values = [random.randint(0, QTY) for _ in range(DIM - 1)]
    # Include 0 and StableMQTY as the lower and upper bounds
    random_values.extend([0, QTY])
    # Sort the values
    random_values.sort()
    # Calculate the differences between consecutive values
    partition = [random_values[i+1] - random_values[i] for i in range(DIM)]
    return list(map(lambda x: x + baseQTY, partition))

def generate_random_dates(dimension, futureMonth):
    """generate_random_dates generates random dates within a month 

    Args:
        dimension (int): number of dates to be generated
        futureMonth (int): months that will be between today's month and the moth within which the dates will be generated

    Returns:
        list: randomly generated dates
    """
    # Get the current date
    current_date = datetime.now()

    # Add 7 months to the current date
    future_date = current_date + relativedelta(months=+futureMonth)

    # Get the start and end of the month
    start_date = future_date.replace(day=1)
    end_date = (start_date + relativedelta(months=+1)) - timedelta(days=1)

    # Generate a list of random dates within the month
    random_dates = [start_date + (end_date - start_date) * random.random() for _ in range(dimension)]

    return random_dates


