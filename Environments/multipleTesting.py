import numpy as np
import pandas as pd
import datetime as dt
import globalParameters
from gurobipy import *
from Environments.chargeEnvironment import chargeEnv
import matplotlib.pyplot as plt
from Environments.chargeSetParams import charge_SetParams

def Test(mode = "TOY", Available_Stock = True, Param_MOQ = True, leadtime_purchase = True, leadtime_routes = False):
    # Definicion de los parametros del entorno gurobi

    #Dado el número de variables de este modelo, es necesario utilizar gurobi con una licencia académica (se obtiene gratuitamente en la web de gurobi)
    params = globalParameters.params
    env = Env(params = params)
    
    # Definición de los parámetros del problema
    BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv = chargeEnv(mode = mode)

    
    if not Available_Stock:
        Stock["STOCK"] = 0

    
    if Param_MOQ:
        NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, MOQ1, MOQ2, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv, leadtime_purchase, leadtime_routes)
    else:
        NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, _, _, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv, leadtime_purchase, leadtime_routes)
    
    # Inicialización del modelo
    modelo = Model("Ejercicio", env = env)    
    
    # Definición de las variables
    indices_x = [(i,t) for t in range(1,len(T)) for i in K1+K3]
    indices_z1 = [(i,t) for t in range(1,len(T))  for i in K1+K3]
    indices_y = [(i,t) for t in range(1,len(T))  for i in K2+K3]
    indices_z2 = [(i,t) for t in range(1,len(T))  for i in K2+K3]
    indices_w = [(i, r, t) for t in range(1,len(T))  for i in LEVEL0 for r in R]
    indices_I = [(i,t) for t in range(1,len(T))  for i in NN]

    x = modelo.addVars(indices_x, lb = 0, vtype = GRB.INTEGER, name = "x") 
    z1 = modelo.addVars(indices_z1, lb = 0, vtype = GRB.BINARY, name = "z1")
    y = modelo.addVars(indices_y, lb = 0, vtype = GRB.INTEGER, name = "y")
    z2 = modelo.addVars(indices_z2, lb = 0, vtype = GRB.BINARY, name = "z2")
    w = modelo.addVars(indices_w, lb = 0, vtype= GRB.BINARY, name = "w") 
    It =  modelo.addVars(indices_I, lb = 0, vtype= GRB.INTEGER, name = "It")

    if not Param_MOQ:
        MOQ1_indices = [i for i in K1+K3]
        MOQ2_indices = [i for i in K2+K3]
        MOQ1 = modelo.addVars(MOQ1_indices, lb = 0, vtype= GRB.INTEGER, name = "MOQ1") 
        MOQ2 =  modelo.addVars(MOQ2_indices, lb = 0, vtype= GRB.INTEGER, name = "MOQ2")

    modelo.update()
    
    # Restricciones
    # Inventario para el primer periodo, para items a nivel 0
    for i in set(K1).intersection(set(LEVEL0)):
        if ltf[i] < 1:
            modelo.addConstr(
                It[i,1] == I_0[i] + x[i, 1-ltf[i]] - quicksum(D[1][item_indices[i],customer_indices[r]]*w[i,r,1] for r in R),
                name=f"R10a_{i}"
            )
        if ltf[i] >= 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                name=f"R10b_{i}"
            )
    for i in set(K2).intersection(set(LEVEL0)):
        if lt[i] < 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] + y[i, 1-lt[i]] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                name=f"R20_{i}"
            )
        if lt[i] >= 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                name=f"R30_{i}"
            )   
    for i in set(K3).intersection(set(LEVEL0)):
        if lt[i] < 1:
            if ltf[i]<1:
                modelo.addConstr(
                    It[i, 1] == I_0[i] + x[i, 1-ltf[i]] + y[i, 1-lt[i]] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                    name=f"R401_{i}"
                )
            else:
                modelo.addConstr(
                    It[i, 1] == I_0[i] + y[i, 1-lt[i]] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                    name=f"R402_{i}"
                )
        else:
            if ltf[i]<1:            
                modelo.addConstr(
                    It[i, 1] == I_0[i] + x[i, 1-ltf[i]] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                    name=f"R501_{i}"
                )
            else:
                modelo.addConstr(
                    It[i, 1] == I_0[i] - quicksum(D[1][item_indices[i], customer_indices[r]] * w[i, r, 1] for r in R),
                    name=f"R502_{i}"
                )
            
        

    # Inventario para el primer periodo, para items a otro nivel
    for i in set(K1).intersection(set().union(*layers[1:])):
        if ltf[i] < 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] + x[i, 1-ltf[i]] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                name=f"R1a_{i}"
            )
        else:
            modelo.addConstr(
                It[i, 1] == I_0[i] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                name=f"R1b_{i}"
            )
    for i in set(K2).intersection(set().union(*layers[1:])):
        if lt[i] < 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] + y[i, 1-lt[i]] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                name=f"R2a_{i}"
            )
        if lt[i] >= 1:
            modelo.addConstr(
                It[i, 1] == I_0[i] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                name=f"R3a_{i}"
            )
    for i in set(K3).intersection(set().union(*layers[1:])):
        if lt[i] < 1:
            if ltf[i] < 1:
                modelo.addConstr(
                    It[i, 1] == I_0[i] + x[i, 1-ltf[i]] + y[i, 1-lt[i]] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                    name=f"R4a1_{i}"
                )
            else:
                modelo.addConstr(
                    It[i, 1] == I_0[i] + y[i, 1-lt[i]] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                    name=f"R4a2_{i}"
                )
        else:
            if ltf[i] < 1:
                modelo.addConstr(
                    It[i, 1] == I_0[i] + x[i, 1-ltf[i]] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                    name=f"R5a1_{i}"
                )
            else:
                modelo.addConstr(
                    It[i, 1] == I_0[i] - quicksum(alpha[j][i] * x[j, 1] for j in N_reverse[i]),
                    name=f"R5a2_{i}"
                )
        

    # Inventario para el resto de periodos, para items a nivel 0
    for i in set(K1).intersection(set(LEVEL0)):
        for t in range(2, len(T)):
            if ltf[i] < t:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] + x[i, t-ltf[i]] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                    name=f"R10ta_{i}_{t}"
                )
            else:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                    name=f"R10tb_{i}_{t}"
                )
    for i in set(K2).intersection(set(LEVEL0)):
        for t in range(2, len(T)):
            if lt[i] < t:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] + y[i, t-lt[i]] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                    name=f"R20t_{i}_{t}"
                )
            else:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                    name=f"R30t_{i}_{t}"
                )
    for i in set(K3).intersection(set(LEVEL0)):
        for t in range(2, len(T)):
            if lt[i] < t:
                if ltf[i] < t:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + x[i, t-ltf[i]] + y[i, t-lt[i]] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                        name=f"R40t1_{i}"
                    )
                else:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + y[i, t-lt[i]] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                        name=f"R40t2_{i}"
                    )
            else:
                if ltf[i] < t:            
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + x[i, t-ltf[i]] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                        name=f"R50t1_{i}"
                    )
                else:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] - quicksum(D[t][item_indices[i], customer_indices[r]] * w[i, r, t] for r in R),
                        name=f"R50t2_{i}"
                    )

    # Inventario para el resto de periodos, para items a otro nivel
    for i in set(K1).intersection(set().union(*layers[1:])):
        for t in range(2, len(T)):
            if ltf[i] < t:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] + x[i, t-ltf[i]] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                    name=f"R1atb_{i}_{t}"
                )
            else:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                    name=f"R1atb_{i}_{t}"
                )
    for i in set(K2).intersection(set().union(*layers[1:])):
        for t in range(2, len(T)):
            if lt[i] < t:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] + y[i, t-lt[i]] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                    name=f"R2at_{i}_{t}"
                )
            else:
                modelo.addConstr(
                    It[i, t] == It[i, t-1] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                    name=f"R3at_{i}_{t}"
                )
    for i in set(K3).intersection(set().union(*layers[1:])):
        for t in range(2, len(T)):
            if lt[i] < t:
                if ltf[i] < t:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + x[i, t-ltf[i]] + y[i, t-lt[i]] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                        name=f"R4at1_{i}_{t}"
                    )
                else:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + y[i, t-lt[i]] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                        name=f"R4at2_{i}_{t}"
                    )
            else:
                if ltf[i] < t:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] + x[i, t-ltf[i]] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                        name=f"R5at1_{i}_{t}"
                    )
                else:
                    modelo.addConstr(
                        It[i, t] == It[i, t-1] - quicksum(alpha[j][i] * x[j, t] for j in N_reverse[i]),
                        name=f"R5at2_{i}_{t}"
                    )


    # Restricciones de MOQs

    r6 = modelo.addConstrs(
        (x[i,t] + 42000*(1-z1[i,t])>=MOQ1[i] for i in K1+K3 for t in range(1, len(T))
        ),name="R6" )
    r7 = modelo.addConstrs(
        (y[i,t] + 42000*(1-z2[i,t])>= MOQ2[i] for i in K2+K3 for t in range(1, len(T))
        ),name="R7" )

    # Restricciones de activacion de variables binarias
    r8 = modelo.addConstrs(
        (x[i,t] <= z1[i,t]*42000 for i in K1+K3 for t in range(1, len(T))
        ),name="R8" )
    r9 = modelo.addConstrs(
        (y[i,t] <= z2[i,t]*42000 for i in K2+K3 for t in range(1, len(T))
        ),name="R9" )

    modelo.update()
    
    # Definición de la función objetivo
    modelo.setObjective(quicksum(quicksum(D[t][item_indices[i],customer_indices[r]]*B[t][item_indices[i],customer_indices[r]]*w[i,r,t] for r in R for i in LEVEL0) 
                                - quicksum(c1[i]*x[i,t] for i in K1+K3)
                                - quicksum(c2[i]*y[i,t] for i in K2+K3)
                                - quicksum(c_act[i]*z1[i,t] for i in K1+K3)
                                for t in range(1, len(T))), sense = GRB.MAXIMIZE)
    
    # Optimizacion
    modelo.optimize()
    
    NoSatisfecha = 0
    totalPedidos = 0
    udsNoSatisfecha = 0
    totalUds = 0
    for t in range(1, len(T)):
        for i in LEVEL0:
            for r in R:
                if D[t][item_indices[i],customer_indices[r]] != 0:
                    if w[i, r, t].X == 0:
                        NoSatisfecha += 1
                        udsNoSatisfecha += D[t][item_indices[i],customer_indices[r]]
                    totalPedidos += 1
                    totalUds += D[t][item_indices[i],customer_indices[r]]


    print(udsNoSatisfecha/totalUds*100)
    print(NoSatisfecha/totalPedidos*100)
    print(modelo.getAttr("ObjVal"))        