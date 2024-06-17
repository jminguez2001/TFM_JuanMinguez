import itertools
import pickle
import pandas as pd
from Environments.multipleTesting import Test

if __name__ == '__main__':
    """Runs different configurations of the model and saves the results"""

    # Define parameter lists
    A_Stock = [True]
    MOQs_AsParms = [True]
    leadtime_purchase = [True]
    leadtime_routes = [False]
    c_act_Multiplier = [1]
    lt_multipliers = [1]
    ltf_multipliers = [1]
    Param_I_0 = [True, False]
    Costes_invent = [True, False]
    Invent_Capacity = [True, False]
    Fabrica_Capacity = [True, False]

    # Initialize results DataFrame and lists
    results = pd.DataFrame(columns=['Environment', 'Available_Stock', 'Param_MOQ', 'leadtime_purchase', 'leadtime_routes',
                                    'Param_I_0', 'Costes_invent', 'Invent_Capacity', 'Fabrica_Capacity',
                                    'c_act_Multiplier', 'lt_Multiplier', 'ltf_Multiplier',
                                    'PerCent_udsNoSatisfechas', 'PerCent_PedidosNoSatisfechos', 'ObjVal'])
    X_results = []
    Y_results = []
    I_results = []
    W_results = []

    # Generate Cartesian product of parameter lists
    parameter_combinations = itertools.product(
        A_Stock, MOQs_AsParms, leadtime_purchase, leadtime_routes, Param_I_0,
        Costes_invent, Invent_Capacity, Fabrica_Capacity
    )

    for s, m, lp, lr, i0_p, ci, IQ, FQ in parameter_combinations:
        c_act_Multiplier_aux = c_act_Multiplier if not m else [1]
        lt_multipliers_aux = lt_multipliers if lp else [1]
        ltf_multipliers_aux = ltf_multipliers if lr else [1]

        for cMult, ltm, ltfm in itertools.product(c_act_Multiplier_aux, lt_multipliers_aux, ltf_multipliers_aux):
            PerCent_udsNoSatisfechas, PerCent_PedidosNoSatisfechos, optSol, solI, solX, solY, solW, D, item_indices, customer_indices, K1, K2, K3, T = Test(
                mode="TOY", Available_Stock=s, Param_MOQ=m,
                leadtime_purchase=lp, leadtime_routes=lr, Param_I_0=i0_p,
                Costes_invent=ci, Invent_Capacity=IQ, Fabrica_Capacity=FQ,
                c_act_Multiplier=cMult, lt_Multiplier=ltm, ltf_Multiplier=ltfm)

            new_row = {
                'Environment': "TOY", 'Available_Stock': s, 'Param_MOQ': m, 'leadtime_purchase': lp, 'leadtime_routes': lr, 
                'Param_I_0': i0_p, 'Costes_invent': ci, 'Invent_Capacity': IQ, 'Fabrica_Capacity': FQ,
                'c_act_Multiplier': cMult, 'lt_Multiplier': ltm, 'ltf_Multiplier': ltfm, 
                'PerCent_udsNoSatisfechas': PerCent_udsNoSatisfechas, 'PerCent_PedidosNoSatisfechos': PerCent_PedidosNoSatisfechos, 'ObjVal': optSol
            }

            results = results._append(new_row, ignore_index=True)
            I_results.append(solI)
            X_results.append(solX)
            Y_results.append(solY)
            W_results.append(solW)

                                
    
    print(results)
    results.to_excel("./Resultados/RESULTADOS.xlsx", sheet_name = "resultados", index=False)
    with open('./Resultados/I_results.pkl', 'wb') as f:
        pickle.dump(I_results, f)
    with open('./Resultados/X_results.pkl', 'wb') as f:
        pickle.dump(X_results, f)
    with open('./Resultados/Y_results.pkl', 'wb') as f:
        pickle.dump(Y_results, f)
    with open('./Resultados/W_results.pkl', 'wb') as f:
        pickle.dump(W_results, f)        
    with open('./Resultados/D.pkl', 'wb') as f:
        pickle.dump(D, f)
    with open('./Resultados/item_indices.pkl', 'wb') as f:
        pickle.dump(item_indices, f)
    with open('./Resultados/customer_indices.pkl', 'wb') as f:
        pickle.dump(customer_indices, f)
    with open('./Resultados/K1.pkl', 'wb') as f:
        pickle.dump(K1, f)
    with open('./Resultados/K2.pkl', 'wb') as f:
        pickle.dump(K2, f)
    with open('./Resultados/K3.pkl', 'wb') as f:
        pickle.dump(K3, f)
    with open('./Resultados/T.pkl', 'wb') as f:
        pickle.dump(T, f)