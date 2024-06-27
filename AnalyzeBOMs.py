import pandas as pd
import os
from helpers.logger import initLogger
from BOM_graph.DrawBOM import DrawingBOM, Draw_NonDirectedGraph
from BOM_graph.StudyBOM import Study_BOM


if __name__ == '__main__':
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                    os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando ejecución para establecer conexion a la base de datos...')
    
    BOM = pd.read_pickle('./DataFiles/BOM.pkl')
    
    # BOMs = [14, 15] # Looking for a small selection
    # BOM = BOM[BOM['MyBOMID'].isin(BOMs)]
    
    # Study the connectivity of the graph
    Study_BOM(BOM) # It is non connected
    Draw_NonDirectedGraph(BOM, logger) # The node 44 is appart from the others -> Delete line
    
    BOM = BOM[BOM['MyBOMITEMID'] != 44].reset_index(drop=True)
    
    Study_BOM(BOM) # It is connected + draw by layers 
    DrawingBOM(BOM)
    
    