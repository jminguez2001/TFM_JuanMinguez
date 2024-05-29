import os
import pandas as pd
import polars as pl
import configparser
import base64
import warnings
import globalParameters
import random

from helpers.logger import *
from SQL.SQLstatements import *
from DB_conexion.verticaConnector import *
from helpers.Utils import random_partition, generate_random_dates
 
def generateOrders_df(pl_master, pl_Orders, MonthlyQTY, StableMQTY, NotStableMQTY, ratioForNonStable):
    """generateOrders_df iterates through the months of the time horizon to generate orders according to the guidelines explained in CreateOrdersFewDATA.

    Args:
        pl_master (polars.DataFrame): Selection of ITEMS for which orders will be generated, identified as stable or not
        pl_Orders (polars.DataFrame): Data frame with the structure of the output data frame
        MonthlyQTY (int): Total monthly quantity to generate
        StableMQTY (int): Monthly quantity assigned to stable orders
        NotStableMQTY (int): Monthly quantity assigned to non-stable orders
        ratioForNonStable (float): Ratio representing the quantity of non-stable items receiving orders each month

    Returns:
        polars.DataFrame: Data frame with the order details
    """

    dimension1 =  pl_master.filter(pl.col("ORDERTYPE") == 1).shape[0]
    dimension0 =  pl_master.filter(pl.col("ORDERTYPE") == 0).shape[0]
    baseQTY_ratio1 = 0.05/dimension1 # the base quantity ratio will be ratio corresponding to the 5 percent of StableQTY/dimension1
    for i in range(7, 13): # Iterate over the next 7-12 months to generate orders each month
        for flag, data in pl_master.group_by("ORDERTYPE"):
            if flag == 1:
                partition = random_partition(StableMQTY, dimension1, baseQTY_ratio1)
                dates = generate_random_dates(dimension1, i)
                data = data.with_columns(pl.Series("QUANTITY", partition))
                data = data.with_columns(pl.Series("END_DATE", dates))
                pl_Orders = pl.concat([pl_Orders, data])

            else:
                confirmedOrders = [1 if random.random() <= ratioForNonStable else 0 for _ in range(dimension0)] # generate flags that identify if an item will receive orders or not during this month
                data = data.with_columns(pl.Series("ConfirmedOrders", confirmedOrders)) # add flag column
                pl_orders0 = data.filter(pl.col("ConfirmedOrders") == 1).select(["ITEMID", "ORDERTYPE"]) # filter to mantain only the items with orders during this month
                baseQTY_ratio0 = 0.05/pl_orders0.shape[0] # minimum quantity ratio for each order
                partition = random_partition(NotStableMQTY, pl_orders0.shape[0], baseQTY_ratio0)
                dates = generate_random_dates(pl_orders0.shape[0], i)
                pl_orders0 = pl_orders0.with_columns(pl.Series("QUANTITY", partition))
                pl_orders0 = pl_orders0.with_columns(pl.Series("END_DATE", dates))
                pl_Orders = pl.concat([pl_Orders, pl_orders0])
    return pl_Orders






def CreateOrdersFewDATA():
    """CreateOrdersFewDATA Se generan las ordenes de pedido y se suben a la tabla correspondiente en BBDD
    
    Criterios para generar los pedidos:
        - El 20% de los diferentes items encontrados en las BOM reciben pedidos todos los meses (pedidos estables), el resto algunos meses solo.
        - Se tiene un total QTY_Month a distribuir entre los pedidos de ese mes, de las cuales el 70%
          es para los pedidos estables y el resto para los que no.
        - Se generan pedidos mensuales en un horizonte temporal de 7 a 12 meses.
    """

    # Parameters for creating orders 
    schema = "iPurchase"
    table = "SalesOrders_NoSustitutives"
    flagRatio = 0.20 # ratio of stable itmes
    QTY_Month = 7000 # total amount of units ordered each month
    StableMonthlyQTY = int(0.7*QTY_Month)
    NotStableMonthlyQTY = int(QTY_Month -StableMonthlyQTY)
    random.seed(123) # For reproducibility

    default_environment = globalParameters.ENVIRONMENT
    config = configparser.ConfigParser()
    config.read('contexts\\' + 'DB_Context.ini') # We use the data base config
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                        os.path.splitext(os.path.basename(__file__))[0])
    
    logger.info('Comenzando el proceso de crear órdenes de pedidos...')
    # Connect to vertica -to get enabled tables
    verticaConnDEV = verticaConn(config[default_environment]['environment'],
                                    config[default_environment]['host'],
                                    config[default_environment]['port'], 
                                    config[default_environment]['DB'],
                                    config[default_environment]['fersaUsr'], 
                                    base64.b64decode(config[default_environment]['fersaPwd']).decode("utf-8"),
                                    os.path.splitext(os.path.basename(__file__))[0])
    # Ignoring warnings while fixing vertica connection
    warnings.simplefilter(action='ignore', category=UserWarning)

    logger.info('Seleccionamos los diferentes ITEMID que se encuentran en nuestras BOMs')
    pl_BOMs = pl_executeQuery(verticaConnDEV, query_Select_BOMs_NoSustitutives)

    flags = [1 if random.random() <= flagRatio else 0 for _ in range(pl_BOMs.shape[0])] # generate stable orders identifiers
    pl_BOMs = pl_BOMs.with_columns(pl.Series("ORDERTYPE", flags)) # add identifier's column

    pl_Orders = pl_BOMs.clear() # empty copy of the data frame
    pl_Orders = pl_Orders.with_columns([pl.col("ITEMID").alias("QUANTITY").cast(pl.Int64), pl.col("ITEMID").alias("END_DATE").cast(pl.Datetime),]) # add empty columns QUANTITY and END_DATE
    
    logger.info('Se procede a generar las ordenes de pedido')
    pl_Orders = generateOrders_df(pl_BOMs, pl_Orders, QTY_Month, StableMonthlyQTY, NotStableMonthlyQTY, 0.4)

    logger.info(f'Se procede a añadir los datos a {schema}.{table}')
    pdfToVertica(verticaConnDEV, schema, table, pl_Orders.to_pandas())
    
    logger.info('Se finaliza el proceso de generar ordenes de pedido.')
    


