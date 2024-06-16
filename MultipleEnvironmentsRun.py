import pandas as pd
from Environments.multipleTesting import Test

if __name__ == '__main__':
    """Corre diferentes configuraciones del modelo y guarda los resultados
    """
    
    # data = ["TOY"]
    A_Stock = [True]
    MOQs_AsParms = [True, False]
    leadtime_purchase = [True, False]
    leadtime_routes = [True, False]
    c_act_Multiplier = [1, 2]
    lt_multipliers = [1, 0.5, 2]
    ltf_multipliers = [1, 0.5, 2]
    
    
    results = pd.DataFrame(columns=['Environment', 'Available_Stock', 'Param_MOQ', 'leadtime_purchase', 'leadtime_routes',
                                    'c_act_Multiplier', 'lt_Multiplier',  'ltf_Multiplier',
                                    'PerCent_udsNoSatisfechas', 'PerCent_PedidosNoSatisfechos', 'ObjVal'])
    
    for s in A_Stock:
        for m in MOQs_AsParms:
            for lp in leadtime_purchase:
                for lr in leadtime_routes:
                    c_act_Multiplier_aux = c_act_Multiplier if not m else [1]
                    for cMult in c_act_Multiplier_aux:
                        lt_multipliers_aux = lt_multipliers if lp else [1]
                        ltf_multipliers_aux = ltf_multipliers if lr else [1]
                        for ltm in lt_multipliers_aux:
                            for ltfm in ltf_multipliers_aux:  
                                PerCent_udsNoSatisfechas, PerCent_PedidosNoSatisfechos, optSol  = Test(mode = "TOY", Available_Stock = s, Param_MOQ = m, 
                                                                                                    leadtime_purchase = lp, leadtime_routes = lr, 
                                                                                                    c_act_Multiplier = cMult, lt_Multiplier = ltm, ltf_Multiplier = ltfm)
                                new_row = {'Environment': "TOY", 'Available_Stock': s, 'Param_MOQ': m, 'leadtime_purchase': lp, 'leadtime_routes': lr,
                                     'c_act_Multiplier': cMult, 'lt_Multiplier': ltm,  'ltf_Multiplier': ltfm,       
                                    'PerCent_udsNoSatisfechas': PerCent_udsNoSatisfechas, 'PerCent_PedidosNoSatisfechos': PerCent_PedidosNoSatisfechos, 'ObjVal': optSol}
                                results = results._append(new_row, ignore_index=True)
    
    print(results)
    results.to_excel("./Resultados/RESULTADOS.xlsx", sheet_name = "resultados", index=False)
