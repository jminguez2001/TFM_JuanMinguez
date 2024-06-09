import configparser
import base64
import warnings
import pandas as pd
import copy
from  DB_conexion.verticaConnector import *
from SQL_python.SQLstatements import *


if __name__ == '__main__':
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                    os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando ejecución para establecer conexion a la base de datos...')
    default_environment = globalParameters.ENVIRONMENT
    config = configparser.ConfigParser()
    config.read('contexts\\' + 'DB_Context.ini') # We use the data base config
    
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
    
    # We are using select distinct because there are repeated rows due to the itempath -> talk with diego   
    BOM = executeQuery(verticaConnDEV, "SELECT DISTINCT MyBOMID, MyITEMID, MyPARENTBOMITEMID, MyBOMITEMID, \"LEVEL\" FROM iPurchase.BOM_NoSustitutives;")
    MixedItems = executeQuery(verticaConnDEV, query_identify_MixedItems)
    PurchaseItems = executeQuery(verticaConnDEV, query_identify_PurchaseItems)
    RouteItems = executeQuery(verticaConnDEV, query_identify_RouteItems)

    BOM.to_pickle('./DataFiles/BOM.pkl')
    MixedItems.to_pickle('./DataFiles/MixedItems.pkl')
    PurchaseItems.to_pickle('./DataFiles/PurchaseItems.pkl')
    RouteItems.to_pickle('./DataFiles/RouteItems.pkl')
    
    logger.info('Se finaliza la ejecución.')
 