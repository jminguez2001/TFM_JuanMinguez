import pandas as pd
from Environments.multipleTesting import Test

if __name__ == '__main__':
    """Corre diferentes configuraciones del modelo y guarda los resultados
    """
    
    # data = ["TOY"]
    A_Stock = [True]
    MOQs = [True]
    leadtime_purchase = [True]
    leadtime_routes = [True]
    c_act_Multiplier = [1]
    lt_multipliers = [1, 0.5, 2]
    ltf_multipliers = [1, 0.5, 2]
    
    
    results = pd.DataFrame(columns=['Environment', 'Available_Stock', 'Param_MOQ', 'leadtime_purchase', 'leadtime_routes',
                                    'c_act_Multiplier', 'lt_Multiplier',  'ltf_Multiplier',
                                    'PerCent_udsNoSatisfechas', 'PerCent_PedidosNoSatisfechos', 'ObjVal'])
    
    for s in A_Stock:
        for m in MOQs:
            for lp in leadtime_purchase:
                for lr in leadtime_routes:
                    for cMult in c_act_Multiplier:
                        for ltm in lt_multipliers:
                            for ltfm in ltf_multipliers:  
                                PerCent_udsNoSatisfechas, PerCent_PedidosNoSatisfechos, optSol  = Test(mode = "TOY", Available_Stock = s, Param_MOQ = m, 
                                                                                                    leadtime_purchase = lp, leadtime_routes = lr, 
                                                                                                    c_act_Multiplier = cMult, lt_Multiplier = ltm, ltf_Multiplier = ltfm)
                                new_row = {'Environment': "TOY", 'Available_Stock': s, 'Param_MOQ': m, 'leadtime_purchase': lp, 'leadtime_routes': lr,
                                     'c_act_Multiplier': cMult, 'lt_Multiplier': ltm,  'ltf_Multiplier': ltfm,       
                                    'PerCent_udsNoSatisfechas': PerCent_udsNoSatisfechas, 'PerCent_PedidosNoSatisfechos': PerCent_PedidosNoSatisfechos, 'ObjVal': optSol}
                                results = results._append(new_row, ignore_index=True)
    
    print(results)
