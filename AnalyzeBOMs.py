import pandas as pd
import os
from helpers.logger import initLogger
from BOM_graph.DrawBOM import DrawingBOM, Draw_NonDirectedGraph
from BOM_graph.StudyBOM import Study_BOM


if __name__ == '__main__':
    """
    Este script analiza la conectividad del grafo de la lista de materiales (BOM).
    Realiza las siguientes tareas:
    1. Inicializa el logger.
    2. Lee el archivo pickle de la BOM.
    3. Estudia la conectividad del grafo de la BOM.
    4. Dibuja el grafo no dirigido de la BOM y elimina el nodo desconectado (44).
    5. Vuelve a estudiar la conectividad y dibuja el grafo por capas.
    """
    
    # Inicializar el logger
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                    os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando ejecución para establecer conexion a la base de datos...')
    
    # Leer el archivo pickle de la BOM
    BOM = pd.read_pickle('./DataFiles/BOM.pkl')
    
    # Estudiar la conectividad del grafo de la BO
    Study_BOM(BOM) # No es conexo
    Draw_NonDirectedGraph(BOM, logger) # El nodo 44 está separado de los demás -> Eliminar línea
    
    # Eliminar el nodo desconectado y reiniciar el índice
    BOM = BOM[BOM['MyBOMITEMID'] != 44].reset_index(drop=True)
    
    # Volver a estudiar la conectividad y dibujar el grafo por capas
    Study_BOM(BOM) # Está conectado + dibujar por capas  
    DrawingBOM(BOM)
    
    