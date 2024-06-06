import configparser
import base64
import warnings
import pandas as pd
import globalParameters
import copy

from DB_Operations.createPurchases import CreateOrdersFewDATA
from  DB_conexion.verticaConnector import *
from BOM_graph.DrawBOM import DrawingBOM
from BOM_graph.StudyBOM import Study_BOM


if __name__ == '__main__':
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                    os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando ejecución del Main...')
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
    # BOM = executeQuery(verticaConnDEV, "SELECT DISTINCT MyBOMID, MyITEMID, MyPARENTBOMITEMID, MyBOMITEMID, \"LEVEL\" FROM iPurchase.BOM_NoSustitutives WHERE MyBOMID != 12;")
    CreateOrdersFewDATA()
    # Study_BOM(BOM)
    # DrawingBOM(BOM)

    
    logger.info('Se finaliza la ejecución del Main.')
 