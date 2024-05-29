import os
import vertica_python

import pandas as pd
import polars as pl
from helpers.logger import *


class verticaConn:
    def __init__(self, environment, server, port, db, usr, pwd, taskParent):
        self.logger = initLogger(os.path.splitext(os.path.basename(__file__))[0], os.path.splitext(os.path.basename(__file__))[0])
        self.environment = environment
        self.db = db
        self.conn_info = {'host': server, 'port': port, 'user': usr, 'password': pwd, 'database': db}       
        try:
            with vertica_python.connect(**self.conn_info) as conn:  
                self.logger.info('Connection Vertica ok: db=' + db)
                self.connexion_established = True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.connexion_established = False

def executeQuery(verticaConnexion, query):
    """executeQuery Given a query it returns as a dataframe the vertica output of its execution


    Args:
        verticaConnexion (class verticaConn): object containing the necessary parameters for establishing a connexion to vertica.
        query (str): query to be executed

    Returns:
        pd.DataFrame: data frame containing the output of the SQL query.
    """
    try:
        with vertica_python.connect(**verticaConnexion.conn_info) as conn:
            with conn.cursor('dict') as cur:
                data = cur.execute(query).fetchall()
                tables = pd.DataFrame(data)
                return (tables)     

    except Exception as e:
        verticaConnexion.logger.error(e, exc_info=True)

def pl_executeQuery(verticaConnexion, query):
    '''
    Given a query it returns as a polars dataframe the vertica output of its execution
    '''
    try:
        with vertica_python.connect(**verticaConnexion.conn_info) as conn:
            with conn.cursor('dict') as cur:
                data = cur.execute(query).fetchall()
                tables = pd.DataFrame(data)
                data_pl = pl.from_pandas(tables)
                verticaConnexion.logger.info('Query ejecutada correctamente')
                return(data_pl)     

    except Exception as e:
        verticaConnexion.logger.error(e, exc_info=True)


def pdfToVertica(verticaConnexion, schemaTo, tablenameTo, pdf):
    """pdfToVertica updates the table in vertica with the pandas data frame

    Args:
        verticaConnexion (class verticaConn): object containing the necessary parameters for establishing a connexion to vertica.
        schemaTo (str): schema of the table that will be updated.
        tablenameTo (str): name of the table that will be updated.
        pdf (pd.DataFrame): data frame with which the table will be updated
    """
    try:
            with vertica_python.connect(**verticaConnexion.conn_info) as conn:
                with conn.cursor('dict') as cursor:          
                    cursor.copy(
                        "COPY {}.{} {} from stdin DELIMITER ';' NULL AS '' REJECTED DATA AS TABLE {}.{}".format(
                            schemaTo,
                            tablenameTo,
                            str(tuple(pdf.columns)).replace("'", ""),
                            schemaTo,
                            "tmp_rejectedData",
                        ),
                        pdf.to_csv(header=None, sep=";", index=False),
                    )
                    verticaConnexion.logger.info('Tabla actualizada correctamente.')

    except Exception as e:
        verticaConnexion.logger.error(e, exc_info=True)