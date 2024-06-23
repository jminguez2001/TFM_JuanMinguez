import itertools
import pickle
import pandas as pd
from Environments.multipleTesting import Test

if __name__ == '__main__':
    """Runs different configurations of the model and saves the results"""

    # Parametros para las diferentes configuraciones
    modo = "default"
    A_Stock = [True] # Si se dispone de stock a tiempo 0
    MOQs_AsParms = [True] # Si se toman como parametros la MOQ1 o no
    leadtime_purchase = [True] # Si se consideran leadtimes de compra
    leadtime_routes = [False] # Si se consideran leadtimes de fabrica
    c_act_Multiplier = [1] # Multiplicador de los costes de activacion
    lt_multipliers = [1] # Multiplicador de los leadtimes de compra
    ltf_multipliers = [1] # Multiplicador de los leadtimes de fabricacion
    MOQ1_multipliers = [1] # Multiplicador de las MOQ1
    c1_fc2 = [False] # Si se consideran los costes de fabricacion de los item mixtos como funcion de los de compra
    c1_fc2_multiplier = [1] # Multiplicador para poner los costes de fabricacion como funcion de los de compra
    Param_I_0 = [True] # Si se considera el inventario inicial como parametro
    Costes_invent = [False] # Si se consideran costes de inventario
    Invent_Capacity = [False] # Si se consideran capacidades de inventario
    Fabrica_Capacity = [False] # Si se consideran capacidades de fabrica
    minimum_delivery_rate = [0] # Ratio de pedidos satisfechos

    # Inicializamos el df y las listas de los resultados
    results = pd.DataFrame(columns=['Environment', 'Available_Stock', 'Param_MOQ', 'leadtime_purchase', 'leadtime_routes',
                                    'Param_I_0', 'Costes_invent', 'Invent_Capacity', 'Fabrica_Capacity', 
                                    'minimum_delivery_rate', 'c1_fc2',
                                    'c_act_Multiplier', 'lt_Multiplier', 'ltf_Multiplier',
                                    'MOQ1_Multiplier', 'c1_fc2_Multiplier',
                                    'PerCent_udsNoSatisfechas', 'PerCent_PedidosNoSatisfechos', 'ObjVal', 'T_CPU'])
    X_results = []
    Y_results = []
    I_results = []
    W_results = []

    # Generate Cartesian product of parameter lists
    parameter_combinations = itertools.product(
        A_Stock, MOQs_AsParms, leadtime_purchase, leadtime_routes, Param_I_0,
        Costes_invent, Invent_Capacity, Fabrica_Capacity, c1_fc2, minimum_delivery_rate
    )

    contador = 1
    for s, m, lp, lr, i0_p, ci, IQ, FQ, c1Asc2, mdr in parameter_combinations:
        c_act_Multiplier_aux = c_act_Multiplier if not m else [0]
        lt_multipliers_aux = lt_multipliers if lp else [0]
        ltf_multipliers_aux = ltf_multipliers if lr else [0]
        MOQ1_multipliers_aux = MOQ1_multipliers if m else [1]
        c1_fc2_multiplier_aux = c1_fc2_multiplier if c1Asc2 else [1]
        if not (not i0_p and not IQ): # No tiene sentido considerar casos en los que I_0 sea una variable y no haya limite en la capacidad de inventario
            for cMult, ltm, ltfm, MOQ1m, c1Asc2m in itertools.product(c_act_Multiplier_aux, lt_multipliers_aux, 
                                                            ltf_multipliers_aux, MOQ1_multipliers_aux,
                                                            c1_fc2_multiplier_aux):
                PerCent_udsNoSatisfechas, PerCent_PedidosNoSatisfechos, optSol, TCPU,solI, solX, solY, solW = Test(
                    mode=modo, Available_Stock=s, Param_MOQ=m,
                    leadtime_purchase=lp, leadtime_routes=lr, Param_I_0=i0_p,
                    Costes_invent=ci, Invent_Capacity=IQ, Fabrica_Capacity=FQ,
                    c_act_Multiplier=cMult, lt_Multiplier=ltm, ltf_Multiplier=ltfm, MOQ1_multipliter = MOQ1m,
                    c1_fc2 = c1Asc2, c1_fc2_multiplier = c1Asc2m,
                    minimum_delivery_rate = mdr,
                    index = contador)

                new_row = {
                    'Environment': modo, 'Available_Stock': s, 'Param_MOQ': m, 'leadtime_purchase': lp, 'leadtime_routes': lr, 
                    'Param_I_0': i0_p, 'Costes_invent': ci, 'Invent_Capacity': IQ, 'Fabrica_Capacity': FQ, 
                    'minimum_delivery_rate': mdr, 'c1_fc2' : c1Asc2,
                    'c_act_Multiplier': cMult, 'lt_Multiplier': ltm, 'ltf_Multiplier': ltfm,
                    'MOQ1_Multiplier':MOQ1m, 'c1_fc2_Multiplier':c1Asc2m, 
                    'PerCent_udsNoSatisfechas': PerCent_udsNoSatisfechas, 'PerCent_PedidosNoSatisfechos': PerCent_PedidosNoSatisfechos, 'ObjVal': optSol,
                    'T_CPU': TCPU
                }

                results = results._append(new_row, ignore_index=True)
                I_results.append(solI)
                X_results.append(solX)
                Y_results.append(solY)
                W_results.append(solW)
                contador += 1

                                
    
    print(results.iloc[:, 5:])
    results.to_excel("./Resultados/RESULTADOS.xlsx", sheet_name = "resultados", index=False)
    with open('./Resultados/I_results.pkl', 'wb') as f:
        pickle.dump(I_results, f)
    with open('./Resultados/X_results.pkl', 'wb') as f:
        pickle.dump(X_results, f)
    with open('./Resultados/Y_results.pkl', 'wb') as f:
        pickle.dump(Y_results, f)
    with open('./Resultados/W_results.pkl', 'wb') as f:
        pickle.dump(W_results, f)        