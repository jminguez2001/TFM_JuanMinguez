import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from helpers.logger import *
import matplotlib.patches as mpatches  


def DrawingBOM(BOM):
    """DrawingBOM For a given data fram with several BOMs it draws its corresponding graphs

    Args:
        BOM (pd.DataFrame): BOMs to be drawn 
    """
    logger = initLogger(os.path.splitext(os.path.basename(__file__))[0],
                        os.path.splitext(os.path.basename(__file__))[0])
    logger.info('Comenzando el proceso de dibujar la BOM')
    GND = nx.Graph()
    GD = nx.DiGraph()

    logger.info('Se añaden los ejes...')
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']:
            GD.add_edge(row['MyPARENTBOMITEMID'], row['MyBOMITEMID'])
            GND.add_edge(row['MyPARENTBOMITEMID'], row['MyBOMITEMID'])
    
    # Assign layer attribute to nodes based on reversed topological generations
    for layer, nodes in enumerate(nx.topological_generations(GD)):
        for node in nodes:
            GD.nodes[node]["layer"] = layer
            GND.nodes[node]["layer"] = layer
    
    # Dynamically create a color map based on the unique values of layer
    unique_layers = sorted(set(nx.get_node_attributes(GD, 'layer').values()))
    colors = plt.cm.Accent 
    layer_color_map = {layer: colors(i / (len(unique_layers) - 1)) for i, layer in enumerate(unique_layers)}

    # Assign colors to nodes based on their layer
    node_colorsND = [layer_color_map[GD.nodes[node]['layer']] for node in GND.nodes]
    node_colorsD = [layer_color_map[GD.nodes[node]['layer']] for node in GD.nodes]

    # Set the positions of the nodes
    posND = nx.spring_layout(GND)
    # Compute the multipartite layout using the "layer" node attribute
    posD = nx.multipartite_layout(GD, subset_key="layer")

    labels = {row['MyBOMITEMID']: row['MyBOMITEMID'] for _, row in BOM.iterrows()}
    legend_handles = [mpatches.Patch(color=layer_color_map[layer], label=f'Layer {layer}') for layer in unique_layers]

    logger.info("Se muestra el grafo no dirigido asociado")
    # Plot non directed Graph
    figD, axD = plt.subplots()
    nx.draw_networkx(GND, pos=posND, labels=labels, with_labels=True, node_color=node_colorsND, node_size=500, font_size=10, ax=axD)
    plt.legend(handles=legend_handles, title="Layers", loc='best')
    axD.set_title("Non directed Graph", fontsize = 20)
    figD.tight_layout()
    plt.show()

    logger.info("Se muestra el grafo dirigido asociado")
    # Plot directed Graph
    figD, axD = plt.subplots()
    nx.draw_networkx(GD, pos=posD, labels=labels, with_labels=True, node_color=node_colorsD, node_size=500, font_size=10, ax=axD)
    plt.legend(handles=legend_handles, title="Layers", loc='best')
    axD.set_title("Reversed DAG layout in topological order with layers colored", fontsize = 20)
    figD.tight_layout()
    plt.show()

    
    
def Draw_NonDirectedGraph(BOM, logger):
    # Create graph
    G = nx.Graph()

    logger.info('Se añaden los ejes...')
    #Add nodes
    nodes = set(BOM['MyBOMITEMID'])
    G.add_nodes_from(nodes)
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']: # Avoid self-edges 
            G.add_edge(row['MyPARENTBOMITEMID'], row['MyBOMITEMID'])

    logger.info('Se dibuja el grafo...')
    # Assign default color to all nodes
    node_colors = 'skyblue'  # Example default color

    # Positioning the nodes
    pos = nx.spring_layout(G)  
    labels = {row['MyBOMITEMID']: row['MyBOMITEMID'] for _, row in BOM.iterrows()}

    # Draw the graph
    nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors, node_size=500, font_size=10)
    plt.show()

def DrawDirectGraph(BOM, logger):
    # Create directed graph
    GD = nx.DiGraph()

    logger.info('Se añaden los ejes...')
    # Add edges from MyBOMITEMID to MyPARENTBOMITEMID
    for _, row in BOM.iterrows():
        if row['MyPARENTBOMITEMID'] != row['MyBOMITEMID']:
            GD.add_edge(row['MyPARENTBOMITEMID'], row['MyBOMITEMID'])

    logger.info('Se dibuja el grafo...')
    

    # Assign layer attribute to nodes based on reversed topological generations
    for layer, nodes in enumerate(nx.topological_generations(GD)):
        for node in nodes:
            GD.nodes[node]["layer"] = layer

    # Dynamically create a color map based on the unique values of layer
    unique_layers = sorted(set(nx.get_node_attributes(GD, 'layer').values()))
    colors = plt.cm.Accent 
    layer_color_map = {layer: colors(i / (len(unique_layers) - 1)) for i, layer in enumerate(unique_layers)}

    # Assign colors to nodes based on their layer
    node_colors = [layer_color_map[GD.nodes[node]['layer']] for node in GD.nodes]

    # Compute the multipartite layout using the "layer" node attribute
    posD = nx.multipartite_layout(GD, subset_key="layer")

    labels = {row['MyBOMITEMID']: row['MyBOMITEMID'] for _, row in BOM.iterrows()}
    legend_handles = [mpatches.Patch(color=layer_color_map[layer], label=f'Layer {layer}') for layer in unique_layers]

    fig, ax = plt.subplots()
    nx.draw_networkx(GD, pos=posD, labels=labels, with_labels=True, node_color=node_colors, node_size=500, font_size=10, ax=ax)
    plt.legend(handles=legend_handles, title="Layers", loc='best')
    ax.set_title("Reversed DAG layout in topological order with layers colored")
    fig.tight_layout()
    plt.show()



    