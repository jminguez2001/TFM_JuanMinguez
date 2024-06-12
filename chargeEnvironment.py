import pandas as pd


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
            return (BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock)
        case "NoStock":
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
            Stock[""]
            return (BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock)