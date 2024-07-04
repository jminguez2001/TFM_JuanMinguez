import numpy as np
import networkx as nx 
import pandas as pd
import datetime as dt
from BOM_graph.StudyBOM import GenerateGraph

def charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, StdCost, Tenv):
    """
    charge_SetParams configura los parámetros necesarios para la optimización de la producción y la logística.

    Args:
        BOM (DataFrame): Lista de materiales.
        MixedItems (DataFrame): Ítems mixtos.
        PurchaseItems (DataFrame): Ítems de compra.
        RouteItems (DataFrame): Ítems de fabricación.
        Orders (DataFrame): Pedidos.
        Stock (DataFrame): Inventario.
        StdCost (DataFrame): Costes estándar.
        Tenv (int): Número de periodos de tiempo.

    Returns:
        tuple: conteniendo múltiples parámetros configurados para la optimización.
    """    
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
    date_range = pd.date_range(start= dt.datetime(2024, 6, 1).strftime("%Y-%m-01"), periods= Tenv, freq='MS') # The month of start must be June 2024 because it is when the 
                                                                                                              # orders where created
    T = date_range.tolist() # De hoy a 12 meses

    # Demanda y precios de venta
    item_indices = {item: idx for idx, item in enumerate(LEVEL0)} # Se mapean los items con los indices de la matriz
    customer_indices = {customer: idx for idx, customer in enumerate(R)} # Se mapean los customers con los indices de la matriz
    D = []
    B = []
    for period_start in T:
        period_end = period_start + pd.DateOffset(months=1) - pd.DateOffset(days=1)  # fin del mes
        period_df = Orders[(Orders['END_DATE'] >= period_start) & (Orders['END_DATE'] <= period_end)]
        
        # Matrices de demanda y precios de venta en el periodo t
        period_matrixD = np.zeros((len(LEVEL0), R_len))
        period_matrixB = np.zeros((len(LEVEL0), R_len))
        
        # se rellenan las matrices
        for _, row in period_df.iterrows():
            item_idx = item_indices[row['MyBOMITEMID']]
            customer_idx = customer_indices[row['CUSTOMERID']]
            period_matrixD[item_idx, customer_idx] = int(row['QUANTITY'])
            period_matrixB[item_idx, customer_idx] = float(row['UNITPRICE_EUR'])
        
        # Append the period matrices to the lists
        D.append(period_matrixD)
        B.append(period_matrixB)
    

    # Costes de activacion
    c_act = {
        **{key: float(value) for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["SETUP_COST"])},
        **{key: float(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["SETUP_COST"])}
    }

    # Costes por unidad
    c1 = {
        **{key: float(value) for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["RUNTIME_COST"])},
        **{key: float(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["RUNTIME_COST"])}
    }

    c2 = {
        **{key: float(value) for key, value in zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["UNITPRICE_Compra"])},
        **{key: float(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["UNITPRICE_Compra"])}
    }
    
    c_std = {**{key: float(value) for key, value in zip(StdCost["MyBOMITEMID"], StdCost["UNITPRICE"])} 
             }

    # Costes de inventario
    c_invent = {
        **{key: float(value) for key, value in zip(Stock["MyBOMITEMID"], Stock["Invent_Cost"])}
    }
    
    # Capacidad de inventario
    Q_invent = {
        **{key: int(value) for key, value in zip(Stock["MyBOMITEMID"], Stock["CAPACITY"])}
    }

    # Capacidad de fabricacion
    Q_fabrica = {
        **{key: int(value) for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["CAPACITY"])},
        **{key: int(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["CAPACITY"])}
    }

    # MOQs
    MOQ1 = {
        **{key: int(value) for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["MOQ_Fabricacion"])},
        **{key: int(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["MOQ_Fabricacion"])}
    }

    MOQ2 = {
        **{key: int(value) for key, value in zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["MOQ_Compra"])},
        **{key: int(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["MOQ_Compra"])}
    }

    # Lead times Compra
    lt = {
        **{key: int(value) for key, value in zip(PurchaseItems["MyBOMITEMID"], PurchaseItems["LEADTIME"])},
        **{key: int(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["LEADTIME"])}
    }

    # Lead Times Fabricacion
    ltf = {
        **{key: int(value) for key, value in zip(RouteItems["MyBOMITEMID"], RouteItems["LEADTIME"])},
        **{key: int(value) for key, value in zip(MixedItems["MyBOMITEMID"], MixedItems["LEADTIME_ROUTES"])}
    }

    # Stock
    I_0 = {key: int(value) for key, value in zip(Stock["MyBOMITEMID"], Stock["STOCK"])}




    # Matriz alpha
    # Construir la matriz alpha
    alpha = {}

    for i in sorted(K1 + K3):
        alpha[i] = {}
        for j in N[i]:
            maxibo_qty = BOM[(BOM['MyPARENTBOMITEMID'] == i) & (BOM['MyBOMITEMID'] == j)]['MAXIBOQTY']
            if not maxibo_qty.empty:
                alpha[i][j] = int(maxibo_qty.values[0])
            else:
                alpha[i][j] = 0

    return (NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, c_std, c_invent, Q_invent, Q_fabrica, MOQ1, MOQ2, lt, ltf, I_0, alpha)