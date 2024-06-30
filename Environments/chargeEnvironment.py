import pandas as pd
from Environments.Df_TOY import chargeToy


def chargeEnv(mode = "default"):
    match mode:
        case "default":
            BOM = pd.read_pickle('./DataFiles/BOM.pkl')
            BOM = BOM[BOM['MyBOMITEMID'] != 44].reset_index(drop=True) # Delete non connected element
            MixedItems = pd.read_pickle('./DataFiles/MixedItems.pkl')
            MixedItems = MixedItems[MixedItems['MyBOMITEMID'] != 44].reset_index(drop=True) # Delete non connected element
            PurchaseItems = pd.read_pickle('./DataFiles/PurchaseItems.pkl')
            RouteItems = pd.read_pickle('./DataFiles/RouteItems.pkl')
            Orders = pd.read_pickle('./DataFiles/Orders.pkl')
            Orders = Orders[Orders['MyBOMITEMID'] != 44].reset_index(drop=True)
            Orders['END_DATE'] = pd.to_datetime(Orders['END_DATE'])
            Stock = pd.read_pickle('./DataFiles/Stock.pkl')
            Stock = Stock[Stock['MyBOMITEMID'] != 44].reset_index(drop=True)
            StdCost = pd.read_pickle('./DataFiles/StandardCost.pkl')
            StdCost = StdCost[StdCost['MyBOMITEMID'] != 44].reset_index(drop=True)
            Tenv = 13
            
            # Inventamos los valores que no se nos dan, ya luego se verá que se hace
            RouteItems["LEADTIME"] = 0 
            MixedItems["LEADTIME_ROUTES"] = 0
            Stock["Invent_Cost"] = 2.61
            
            Stock["CAPACITY"] = 2000 
            Stock.loc[Stock["ITEMID"].str.startswith('42'), "CAPACITY"] = 40000
            
            RouteItems["CAPACITY"] = 2000000
            MixedItems["CAPACITY"] = 2000000
            
            return (BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, StdCost, Tenv)
        case "TOY":
            BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock = chargeToy()
            return (BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock, [], 5) # la lista vacia es porque el uso de StdCost se desarrollo posteriormente a TOY, una vez TOY ya no se usaba