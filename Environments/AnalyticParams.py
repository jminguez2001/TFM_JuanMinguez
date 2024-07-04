import numpy as np


def calculaAnalyticParams(x, y, w, c1, c2, c_std, T, LEVEL0, K1, K2, K3, R, D, B, item_indices, customer_indices, I):
    """
    calculaAnalyticParams calcula parámetros analíticos para evaluar costos, producción y márgenes de beneficio.

    Args:
        x (dict): diccionario de unidades producidas.
        y (dict): diccionario de unidades compradas.
        w (dict): diccionario que indica si se ha satisfecho el pedido correspondiente.
        c1 (dict): diccionario de costos de producción.
        c2 (dict): diccionario de costos de compra.
        c_std (dict): diccionario de costos estándar.
        T (list): lista de periodos de tiempo.
        LEVEL0 (list): lista de niveles iniciales de los artículos.
        K1 (list): lista de índices de artículos fabricados.
        K2 (list): lista de índices de artículos comprados externamente.
        K3 (list): lista de índices de artículos que se pueden fabricar y comprar.
        R (list): lista de clientes.
        D (list): lista de demanda por periodo, cliente e ítem.
        B (list): lista de precios por periodo, cliente e ítem.
        item_indices (dict): diccionario de índices de artículos.
        customer_indices (dict): diccionario de índices de clientes.
        I (dict): diccionario de niveles de inventario.

    Returns:
        tuple: conteniendo margen de beneficio, inventario comprometido inicial y final, 
               compras netas y unidades fabricadas.
    """
    
    # Calcular costes
    net_production = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K2 + K3])
    totalCost = net_production + net_purchase
    
    # Unidades fabricadas
    uds_fabricadas = np.sum([x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    
    # Inventario comprometido inicial
    I0_comprometido = np.sum([c_std[i] * I[i, 0] for i in K1 + K2 + K3]) 
    # Inventario comprometido final
    If_comprometido = np.sum([c_std[i] * I[i, len(T)-1] for i in K1 + K2 + K3])
    
    
    # Margen beneficios
    revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R for i in LEVEL0 for t in range(1, len(T))])
    margen = (1-totalCost/revenue)*100
    
    return  margen, I0_comprometido, If_comprometido, net_purchase, uds_fabricadas
