import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from helpers.logger import *
import matplotlib.patches as mpatches  


def DrawingBOM(BOM, typeDraw = 'directed'):
    """DrawingBOM For a given data fram with several BOMs it draws its corresponding graph

    Args:
        BOM (pd.DataFrame): BOMs to be drawn 
        typeDraw (str, optional): 'directed' or 'nondirected', for choosing between drawing a directed or non directed graph. Defaults to 'directed'.
    """
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                        os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando el proceso de dibujar la BOM')
    if  typeDraw == 'nondirected':
        logger.info("Se procede a construir el grafo no dirigido")
        Draw_NonDirectedGraph(BOM, logger)
    elif typeDraw == 'directed':
        logger.info("Se procede a construir el grafo dirigido")
        DrawDirectGraph(BOM, logger)
    else:
        logger.info(f"Argumento typeDraw{typeDraw} no válido")

    
    
def Draw_NonDirectedGraph(BOM, logger):
    # Create graph
    G = nx.Graph()

    logger.info('Se añaden los ejes...')
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']: # Avoid self-edges 
            G.add_edge(row['MyPARENTBOMITEMID'], row['MyBOMITEMID'])

    logger.info('Se dibuja el grafo...')
    # Dynamically create a color map based on the unique values of LEVEL
    unique_levels = sorted(BOM['LEVEL'].unique())
    colors = plt.cm.viridis  # Using viridis colormap for example
    level_color_map = {level: colors(i / (len(unique_levels) - 1)) for i, level in enumerate(unique_levels)}

    # Assign colors to nodes based on their LEVEL, ensuring we only color nodes present in the graph
    node_colors = []
    for node in G.nodes:
        try:
            color = level_color_map[BOM.loc[BOM['MyBOMITEMID'] == node, 'LEVEL'].values[0]]
        except IndexError:
            color = 'gray'  # Default color for nodes not found in BOM
        node_colors.append(color)

    # Positioning the nodes
    pos = nx.spring_layout(G)  
    labels = {row['MyBOMITEMID']: row['MyBOMITEMID'] for _, row in BOM.iterrows()}
    legend_handles = [mpatches.Patch(color=level_color_map[level], label=f'Level {level}') for level in unique_levels]

    # Draw the graph
    nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors, node_size=500, font_size=10)
    plt.legend(handles=legend_handles, title="Levels")
    plt.show()

def DrawDirectGraph(BOM, logger):
    # Create directed graph
    G = nx.DiGraph()

    logger.info('Se añaden los ejes...')
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']:
            G.add_edge(row['MyBOMITEMID'], row['MyPARENTBOMITEMID'])

    logger.info('Se dibuja el grafo...')
    
    # Reverse the graph
    G_reversed = G.reverse()

    # Assign layer attribute to nodes based on reversed topological generations
    for layer, nodes in enumerate(nx.topological_generations(G_reversed)):
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # Dynamically create a color map based on the unique values of layer
    unique_layers = sorted(set(nx.get_node_attributes(G, 'layer').values()))
    colors = plt.cm.Accent 
    layer_color_map = {layer: colors(i / (len(unique_layers) - 1)) for i, layer in enumerate(unique_layers)}

    # Assign colors to nodes based on their layer
    node_colors = [layer_color_map[G.nodes[node]['layer']] for node in G.nodes]

    # Compute the multipartite layout using the "layer" node attribute
    pos = nx.multipartite_layout(G, subset_key="layer")

    labels = {row['MyBOMITEMID']: row['MyBOMITEMID'] for _, row in BOM.iterrows()}
    legend_handles = [mpatches.Patch(color=layer_color_map[layer], label=f'Layer {layer}') for layer in unique_layers]

    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, labels=labels, with_labels=True, node_color=node_colors, node_size=500, font_size=10, ax=ax)
    plt.legend(handles=legend_handles, title="Layers", loc='best')
    ax.set_title("Reversed DAG layout in topological order with layers colored")
    fig.tight_layout()
    plt.show()



    