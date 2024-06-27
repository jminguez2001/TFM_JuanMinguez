import numpy as np


def calculaAnalyticParams(x, y, w, c1, c2, T, LEVEL0, K1, K2, K3, R, D, B, item_indices, customer_indices, I, I_0):
    
    # Calcular el neto de producción y el neto de compra K3
    net_productionK3 = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K3])
    net_purchaseK3 = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K3])
    totalCostK3 = net_productionK3+net_purchaseK3
    perCent_net_productionK3 = net_productionK3/totalCostK3*100
    perCent_net_purchaseK3 = net_purchaseK3/totalCostK3*100
    
    # Calcular el neto de producción y el neto de compra
    net_production = np.sum([c1[i] * x[i, t] for t in range(1, len(T)) for i in K1 + K3])
    net_purchase = np.sum([c2[i] * y[i, t] for t in range(1, len(T)) for i in K2 + K3])
    totalCost = net_production+net_purchase
    perCent_net_production = net_production/totalCost*100
    perCent_net_purchase = net_purchase/totalCost*100
    
    # Inventario comprometido inicial
    I0_comprometido = np.sum([c1[i] * I_0[i] for i in K1 + K3]) + np.sum([c2[i] * I_0[i] for i in K2 + K3])
    # Inventario comprometido final
    If_comprometido = np.sum([c1[i] * I[i, len(T)] for i in K1 + K3]) + np.sum([c2[i] * I[i, len(T)] for i in K2 + K3])
    
    
    # Margen beneficios
    revenue = np.sum([D[t][item_indices[i], customer_indices[r]] * B[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R for i in LEVEL0 for t in range(1, len(T))])
    margen = (1-revenue/totalCost)*100
    
    return margen, I0_comprometido, If_comprometido, net_production, perCent_net_production, net_purchase, perCent_net_purchase, net_productionK3, perCent_net_productionK3, net_purchaseK3, perCent_net_purchaseK3
