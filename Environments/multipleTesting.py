import numpy as np
import pandas as pd
import datetime as dt
import globalParameters
from gurobipy import *
from Environments.chargeEnvironment import chargeEnv
from Environments.chargeSetParams import charge_SetParams



def Test(mode = "TOY", Available_Stock = True, Param_MOQ = True, 
         leadtime_purchase = True, leadtime_routes = False,
         Param_I_0 = True, Costes_invent = False, Invent_Capacity = False
         , Fabrica_Capacity = False 
         , c_act_Multiplier = 1, lt_Multiplier = 1, ltf_Multiplier = 1, MOQ1_multipliter = 1
         , c1_fc2 = False, c1_fc2_multiplier = 1
         , minimum_delivery_rate = 0):
    """Simula el modelo para la configuracion introducida

    Args:
        mode (str, optional): Entorno de simulacion, es decir, los datos de entrada. Defaults to "TOY".
        Available_Stock (bool, optional): Si se considera stock inicial o no. Defaults to True.
        Param_MOQ (bool, optional): Si se considera las MOQ1 como parametros o se deja libre como variable. Defaults to True.
        leadtime_purchase (bool, optional): Si se consideran lead times de compra o no. Defaults to True.
        leadtime_routes (bool, optional): Si se consideran lead times de fabricacion o no. Defaults to False.
        c_act_Multiplier (int, optional): multiplicador de los costes de activacion. Defaults to 1.
        lt_Multiplier (int, optional): multiplicador de los lead time de compra. Defaults to 1.
        ltf_Multiplier (int, optional): multiplicador de los lead time de fabricacion. Defaults to 1.

    Returns:
        float: parametros que describen la solucion (% de unidades demandadas no satisfechas, % de pedidos no satisfechos, valor optimo de la f.objetivo)
    """
    
    
    # Definicion de los parametros del entorno gurobi
    params = globalParameters.params
    env = Env(params = params)
    
    # Definición de los parámetros del problema
    BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv = chargeEnv(mode = mode)


    NN, K1, K2, K3, LEVEL0, N, N_reverse, layers, R, T, D, B, item_indices, customer_indices, c_act, c1, c2, c_invent, Q_invent, Q_fabrica, MOQ1, MOQ2, lt, ltf, I_0, alpha = charge_SetParams(BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, Tenv)
    

    # Se modifican los valores segun la configuracion introducida
    if not Available_Stock:
        I_0.update({key: 0 for key in Stock["MyBOMITEMID"]})
    
    if Param_MOQ:
        c_act.update({key: 0 for key in RouteItems["MyBOMITEMID"]})
        c_act.update({key: 0 for key in MixedItems["MyBOMITEMID"]})
    
    # Lead times Compra
    if not leadtime_purchase:
        lt.update({key: 0 for key in PurchaseItems["MyBOMITEMID"]})
        lt.update({key: 0 for key in MixedItems["MyBOMITEMID"]})

    # Lead Times Fabricacion
    if not leadtime_routes:
        ltf.update({key: 0 for key in RouteItems["MyBOMITEMID"]})
        ltf.update({key: 0 for key in MixedItems["MyBOMITEMID"]})
    
    if not Costes_invent:
        for i in NN:
            c_invent[i] = 0
    
    if not Invent_Capacity:
        for i in NN:
            Q_invent[i] = 2000000
    
    if not Fabrica_Capacity:
        for i in K1+K3:
            Q_fabrica[i] = 2000000
    
    # Multiplicador de los costes de activacion:
    c_act = {key: value*c_act_Multiplier for key, value in c_act.items()}
    
    # Multiplicador LeadTimes
    lt = {key: int(value*lt_Multiplier) for key, value in lt.items()} # Me aseguro de que la solucion es entera, ejemplo int(3*0.5) = 1
    ltf = {key: int(value*ltf_Multiplier) for key, value in ltf.items()}
    
    # Multiplicador de las MOQ1
    MOQ1  = {key: int(value * MOQ1_multipliter) if value != 1 else value for key, value in MOQ1.items()}
    
    # c1(c2)
    if c1_fc2:
        c1.update({key: float(c2[key]) * c1_fc2_multiplier for key in MixedItems["MyBOMITEMID"]})
        c1.update({key: float(c1[key]) for key in RouteItems["MyBOMITEMID"]})
    
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
        MOQ1 = modelo.addVars(MOQ1_indices, lb = 1, vtype= GRB.INTEGER, name = "MOQ1")
    if not Param_I_0:
        I_0_indices = [i for i in NN]
        I_0 = modelo.addVars(I_0_indices, lb = 0, vtype= GRB.INTEGER, name = "I_0") 

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

    if Param_MOQ:
        r6 = modelo.addConstrs(
            (x[i,t]>=MOQ1[i]*z1[i,t] for i in K1+K3 for t in range(1, len(T))
                ),name="R6" )
    else:
        r6 = modelo.addConstrs(
            (x[i,t] + 1000000*(1-z1[i,t])>=MOQ1[i] for i in K1+K3 for t in range(1, len(T))
                ),name="R6" )

    r7 = modelo.addConstrs(
        (y[i,t] >= MOQ2[i]*z2[i,t] for i in K2+K3 for t in range(1, len(T))
            ),name="R7" )

    # Restricciones de activacion de variables binarias
    if Fabrica_Capacity:
        r8 = modelo.addConstrs(
            (x[i,t] <= z1[i,t]*Q_fabrica[i] for i in K1+K3 for t in range(1, len(T)) # se incluye la restriccion de capacidad de fabricacion
            ),name="R8" )
    else:
        r8 = modelo.addConstrs(
            (x[i,t] <= z1[i,t]*420000 for i in K1+K3 for t in range(1, len(T)) # se incluye la restriccion de capacidad de fabricacion
            ),name="R8" )
    r9 = modelo.addConstrs(
        (y[i,t] <= z2[i,t]*420000 for i in K2+K3 for t in range(1, len(T))
        ),name="R9" )
    
    # Restricciones de capacidad de Inventario
    if Invent_Capacity:
        if not Param_I_0:
            r10 = modelo.addConstrs (
                (I_0[i] <= Q_invent[i] for i in NN), name="R10" )

        r11 = modelo.addConstrs (
            (It[i, t] <= Q_invent[i] for i in NN for t in range(1, len(T))), name="R11" ) 

    # r12 = modelo.addConstr(quicksum(D[t][item_indices[i],customer_indices[r]]*w[i, r, t] for t in range(1, len(T)) for i in LEVEL0 for r in R if D[t][item_indices[i],customer_indices[r]]!= 0)
    #                        >= minimum_delivery_rate * 
    #                        quicksum(D[t][item_indices[i],customer_indices[r]] for t in range(1, len(T)) for i in LEVEL0 for r in R if D[t][item_indices[i],customer_indices[r]] != 0)
    #                        , name="r12")
    
    # entregados = quicksum(w[i, r, t] for t in range(1, len(T)) for i in LEVEL0 for r in R if D[t][item_indices[i],customer_indices[r]] != 0)
    # pedidos = quicksum(1 for t in range(1, len(T)) for i in LEVEL0 for r in R if D[t][item_indices[i],customer_indices[r]] != 0)                       
    # r12 = modelo.addConstr( entregados >= minimum_delivery_rate * pedidos
    #                        , name="r12")

    modelo.update()
    
    # Definición de la función objetivo
    modelo.setObjective(quicksum(quicksum(D[t][item_indices[i],customer_indices[r]]*B[t][item_indices[i],customer_indices[r]]*w[i,r,t] for r in R for i in LEVEL0) 
                                - quicksum(float(c1[i])*x[i,t] for i in K1+K3)
                                - quicksum(float(c2[i])*y[i,t] for i in K2+K3)
                                - quicksum(float(c_act[i])*z1[i,t] for i in K1+K3)
                                - quicksum(float(c_invent[i])*It[i,t] for i in NN)
                                for t in range(1, len(T))), sense = GRB.MAXIMIZE)
    
    # Optimizacion
    modelo.optimize()
    
    NoSatisfecha = totalPedidos = udsNoSatisfecha = totalUds = 0

    for t in range(1, len(T)):
        for i in LEVEL0:
            for r in R:
                demand = D[t][item_indices[i], customer_indices[r]]
                if demand != 0:
                    totalPedidos += 1
                    totalUds += demand
                    if w[i, r, t].X == 0:
                        NoSatisfecha += 1
                        udsNoSatisfecha += demand
    
    # Se guardan las soluciones
    solI = {(i, t): None for i in NN for t in range(0, len(T))}
    solX = {(i, t): None for i in set(K1 + K3) for t in range(1, len(T))}
    solY = {(i, t): None for i in set(K2 + K3) for t in range(1, len(T))}
    solW = {(i,r,t): None for i in set(LEVEL0) for r in R for t in range(1, len(T))}
    solI.update({(i, 0): (I_0[i] if Param_I_0 else I_0[i].X) for i in NN})
    solX.update({(i, t): x[i, t].X for t in range(1, len(T)) for i in set(K1 + K3)})
    solY.update({(i, t): y[i, t].X for t in range(1, len(T)) for i in set(K2 + K3)})
    solI.update({(i, t): It[i, t].X for t in range(1, len(T)) for i in NN})
    solW.update({(i,r,t): w[i,r,t].X for i in set(LEVEL0) for r in R for t in range(1, len(T))})
    
    
    # Si quiero ver resultados
    # with open('output.txt', 'w') as file:
    #     for t in range(1, len(T)):
    #         for i in LEVEL0:
    #             for r in R:
    #                 if w[i, r, t].X != 0 and D[t][item_indices[i]][customer_indices[r]] != 0:
    #                     file.write(f"Item, cliente, horizonte temporal: {i, r, t}\n")
    #                     file.write(f"Demanda {D[t][item_indices[i]][customer_indices[r]]}\n")
    #                     if t == 1:
    #                         file.write(f"Stock antes: {I_0[i]}\n")
    #                     else:
    #                         file.write(f"Stock antes: {It[i, t-1].X}\n")
    #                     file.write(f"Stock despues: {It[i, t].X}\n")
    #                     if i in K1 + K3:
    #                         file.write(f"Cantidad Producida {x[i, t].X}\n")
    #                     if i in K2 + K3:
    #                         file.write(f"Cantidad Comprada {y[i, t].X}\n")
    #                         if lt[i] < t:
    #                             file.write(f"Cantidad comprada previamente que llega ahora {y[i, t-lt[i]].X}\n")
    #                         if i in K2:
    #                             lead_time = PurchaseItems.loc[PurchaseItems["MyBOMITEMID"] == i, "LEADTIME"].values[0]
    #                         if i in K3:
    #                             lead_time = MixedItems.loc[MixedItems["MyBOMITEMID"] == i, "LEADTIME"].values[0]
    #                         file.write(f"Lead time {lead_time}\n")
    #                 else:
    #                     if D[t-1][item_indices[i]][customer_indices[r]] != 0:
    #                         file.write(f"Item, cliente, horizonte temporal: {i, r, t}\n")
    #                         file.write(f"NO SE SATISFACE\n")
    #         file.write("------------------------------------------\n")
    
    
    
    sol = modelo.getAttr("ObjVal")
    modelo.close()
    env.close()

    return udsNoSatisfecha/totalUds*100, NoSatisfecha/totalPedidos*100, sol, solI, solX, solY, solW, D, B, item_indices, customer_indices, K1, K2, K3, T