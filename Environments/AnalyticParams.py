import numpy as np


def calculaAnalyticParams(x, y, w, c1, c2, c_std, T, LEVEL0, K1, K2, K3, R, D, B, item_indices, customer_indices, I, I_0):

    
    # Calcular costes
    net_production = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K2 + K3])
    totalCost = net_production + net_purchase
    
    # Unidades fabricadas
    uds_fabricadas = np.sum([x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    
    # Inventario comprometido inicial
    I0_comprometido = np.sum([c_std[i] * I_0[i] for i in K1 + K2 + K3]) 
    # Inventario comprometido final
    If_comprometido = np.sum([c_std[i] * I[i, len(T)-1] for i in K1 + K2 + K3])
    
    
    # Margen beneficios
    revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R for i in LEVEL0 for t in range(1, len(T))])
    margen = (1-totalCost/revenue)*100
    
    return  margen, I0_comprometido, If_comprometido, net_purchase, uds_fabricadas
