import configparser
import base64
import warnings
import pandas as pd
import copy
import os
import globalParameters
from helpers.logger import initLogger
from  DB_conexion.verticaConnector import verticaConn, executeQuery
from SQL_python.SQLstatements import *


if __name__ == '__main__':
    """
    Este script principal configura el logger y establece una conexión con la base de datos de Vertica
    para extraer datos esenciales como la lista de materiales (BOM), artículos mixtos, artículos de compra,
    rutas, órdenes de venta, stock y coste estándar. Los datos extraídos se guardan en archivos pickle
    para su uso posterior.
    """
    # Inicializar el logger
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                    os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando ejecución para establecer conexion a la base de datos...')
    default_environment = globalParameters.ENVIRONMENT
    config = configparser.ConfigParser()
    config.read('contexts\\' + 'DB_Context.ini') # Usamos la configuración de la base de datos
    
    # Configuración del entorno y lectura del archivo de configuración de la base de datos
    verticaConnDEV = verticaConn(config[default_environment]['environment'],
                                    config[default_environment]['host'],
                                    config[default_environment]['port'], 
                                    config[default_environment]['DB'],
                                    config[default_environment]['fersaUsr'], 
                                    base64.b64decode(config[default_environment]['fersaPwd']).decode("utf-8"),
                                    os.path.splitext(os.path.basename(__file__))[0])
    
    warnings.simplefilter(action='ignore', category=UserWarning)
    
    # Ejecutar consultas para obtener datos esenciales
    BOM = executeQuery(verticaConnDEV, "SELECT DISTINCT MyBOMID, MyITEMID, MyPARENTBOMITEMID, MyBOMITEMID, \"LEVEL\", MAXIBOQTY FROM iPurchase.BOM_NoSustitutives;")
    MixedItems = executeQuery(verticaConnDEV, query_identify_MixedItems)
    PurchaseItems = executeQuery(verticaConnDEV, query_identify_PurchaseItems)
    RouteItems = executeQuery(verticaConnDEV, query_identify_RouteItems)
    Orders = executeQuery(verticaConnDEV, "SELECT * FROM iPurchase.SalesOrders")
    Stock = executeQuery(verticaConnDEV, query_getSTOCK)
    StandardCost = executeQuery(verticaConnDEV, query_getStdCost)
   
    # Guardar los datos obtenidos en archivos pickle
    BOM.to_pickle('./DataFiles/BOM.pkl')
    MixedItems.to_pickle('./DataFiles/MixedItems.pkl')
    PurchaseItems.to_pickle('./DataFiles/PurchaseItems.pkl')
    RouteItems.to_pickle('./DataFiles/RouteItems.pkl')
    Orders.to_pickle('./DataFiles/Orders.pkl')
    Stock.to_pickle('./DataFiles/Stock.pkl')
    StandardCost.to_pickle('./DataFiles/StandardCost.pkl')
    
    logger.info('Se finaliza la ejecución.')
 