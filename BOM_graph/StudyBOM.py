import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from helpers.logger import *
import matplotlib.patches as mpatches  


def Study_BOM(BOM):
    """Study_BOM given a list of BOMs checks if its associated graph is it is connected

    Args:
        BOM (pd.DataFrame): data frame containing the BOMs
    """
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0], os.path.splitext(os.path.basename(__file__))[0])
    logger.info("Se generan los grafos dirigidos y no dirigidos...")
    G = GenerateGraph(BOM, typeG_ND = True)
    G_Direct = GenerateGraph(BOM, typeG_ND = False)
    logger.info(f"El grafo asociado a las BOMs es conexo: {nx.is_connected(G)}")


    


def GenerateGraph(BOM, typeG_ND):
    """GenerateGraph Given a data frame of BOMs it generates the Graph associated

    Args:
        BOM (pd.DataFrame): data frame containing the BOMs
        typeG_ND (boolean): true to generate a non directed graph and false to generate a directed graph

    Returns:
        nx.Graph: graph associated with the list of BOMs
    """
    # Create graph
    if typeG_ND:
        G = nx.Graph()
    else:
        G = nx.DiGraph()
    
    #Add nodes
    nodes = set(BOM['MyBOMITEMID'])
    G.add_nodes_from(nodes)
    
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']:
            G.add_edge(row['MyBOMITEMID'], row['MyPARENTBOMITEMID'])
    
    return G