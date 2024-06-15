import numpy as np
import networkx as nx 
import pandas as pd
import datetime as dt
from BOM_graph.StudyBOM import GenerateGraph

def charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv, leadtime_purchase = True, leadtime_routes = False):
    # Grafo
    G = GenerateGraph(BOM, typeG_ND = False, connected = True)

    # Items
    NN = sorted(G.nodes)
    NN_len = sorted(NN)
    K1 = sorted(RouteItems["MyBOMITEMID"].unique().tolist())
    K2 = sorted(PurchaseItems["MyBOMITEMID"].unique().tolist())
    K3 = sorted(MixedItems["MyBOMITEMID"].unique().tolist())
    LEVEL0 = sorted(BOM.loc[ BOM["LEVEL"] == 0,"MyBOMITEMID"].unique().tolist())

    # Arcos 
    # arcos = sorted(G.edges)

    # Layers
    layers_dict = {}
    for node in G.nodes:
        layer = G.nodes[node]["layer"]
        if layer not in layers_dict:
            layers_dict[layer] = []
        layers_dict[layer].append(node)
    layers = [sorted(nodes) for layer, nodes in sorted(layers_dict.items())]

    # Conjuntos N(i) e inversos
    N = {}
    # Encontrar los ítems necesarios para cada ítem i en Kt ∪ K3
    for i in sorted(K1+K3):
        N[i] = [j for _, j in G.edges(i)]

    N_reverse = {j: [] for j in NN}
    for j, neighbors in N.items():
        for i in neighbors:
            N_reverse[i].append(j)

    # Clientes
    R = sorted(Orders["CUSTOMERID"].unique().tolist())
    R_len = len(R)

    # Periodos de tiempo en el horizonte temporal
    date_range = pd.date_range(start= dt.datetime.now().strftime("%Y-%m-01"), periods= Tenv, freq='MS')
    T = date_range.tolist() # De hoy a 12 meses

    # Demanda y precios de venta
    # LEVEL0 = layers[0]+[39]
    # Map MyBOMITEMID and CUSTOMERID to indices
    item_indices = {item: idx for idx, item in enumerate(LEVEL0)} # El 39 es un ítem a nivel 0 y Layer 1
    customer_indices = {customer: idx for idx, customer in enumerate(R)}
    D = []
    B = []
    for period_start in T:
        period_end = period_start + pd.DateOffset(months=1) - pd.DateOffset(days=1)  # End of the month
        period_df = Orders[(Orders['END_DATE'] >= period_start) & (Orders['END_DATE'] <= period_end)]
        
        # Create matrices for quantities and prices
        period_matrixD = np.zeros((len(LEVEL0), R_len))
        period_matrixB = np.zeros((len(LEVEL0), R_len))
        
        # Fill the matrices
        for _, row in period_df.iterrows():
            item_idx = item_indices[row['MyBOMITEMID']]
            customer_idx = customer_indices[row['CUSTOMERID']]
            period_matrixD[item_idx, customer_idx] = row['QUANTITY']
            period_matrixB[item_idx, customer_idx] = row['UNITPRICE_EUR']
        
        # Append the period matrices to the lists
        D.append(period_matrixD)
        B.append(period_matrixB)
    
    # Costes de activacion
    c_act = {**dict(zip(RouteItems["MyBOMITEMID"], RouteItems["SETUP_COST"])), 
    **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["SETUP_COST"]))}
        
    # Costes por unidad
    c1 = {**dict(zip(RouteItems["MyBOMITEMID"], RouteItems["RUNTIME_COST"])), 
    **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["RUNTIME_COST"]))}
    c2 = {**dict(zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["UNITPRICE_Compra"])), 
    **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["UNITPRICE_Compra"]))}

    # MOQs
    MOQ1 = {**dict(zip(RouteItems["MyBOMITEMID"], RouteItems["MOQ_Fabricacion"])), 
    **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["MOQ_Fabricacion"]))}
    MOQ2 = {**dict(zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["MOQ_Compra"])), 
    **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["MOQ_Compra"]))}

    # Lead times Compra
    if leadtime_purchase:
        lt = {**dict(zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["LEADTIME"])), 
        **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["LEADTIME"]))}
    else:
        lt = {**dict.fromkeys(PurchaseItems["MyBOMITEMID"], 0), 
        **dict.fromkeys(MixedItems["MyBOMITEMID"], 0)}

    # Lead Times Fabricacion
    if leadtime_routes:
        ltf = {**dict(zip(RouteItems["MyBOMITEMID"], RouteItems["LEADTIME"])), 
        **dict(zip(MixedItems["MyBOMITEMID"], MixedItems["LEADTIME_ROUTES"]))}
    else:
        ltf = {**dict.fromkeys(RouteItems["MyBOMITEMID"], 0), 
        **dict.fromkeys(MixedItems["MyBOMITEMID"], 0)}

    # Stock
    I_0 = dict(zip(Stock["MyBOMITEMID"], Stock["STOCK"]))


    # Matriz alpha
    # Construir la matriz alpha
    alpha = {}

    for i in sorted(K1 + K3):
        alpha[i] = {}
        for j in N[i]:
            maxibo_qty = BOM[(BOM['MyPARENTBOMITEMID'] == i) & (BOM['MyBOMITEMID'] == j)]['MAXIBOQTY']
            if not maxibo_qty.empty:
                alpha[i][j] = maxibo_qty.values[0]
            else:
                alpha[i][j] = 0

    return (NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, MOQ1, MOQ2, lt, ltf, I_0, alpha)