import pandas as pd

def chargeToy():
    """Define los valores del entorno de juguete

    Returns:
        pd.DataFrame: diferentes df con los datos del modelo de juguete
    """
    BOM_dict = {
                'MyBOMID': [1, 1, 1, 1, 1, 
                            2, 2, 2, 2, 2, 2, 2, 2, 
                            3, 3, 3, 3, 3],
                'MyITEMID': [1, 1, 1, 1, 1, 
                             2, 2, 2, 2, 2, 2, 2, 2, 
                             3, 3, 3, 3, 3],
                'MyPARENTBOMITEMID': [1, 1, 1, 4, 4, 
                                      2, 2, 2, 2, 6, 6, 7, 7, 
                                      3, 3, 3, 7, 7],
                'MyBOMITEMID': [1, 4, 5, 9, 11, 
                                2, 5, 6, 7, 9, 10, 10, 11, 
                                3, 7, 8, 10, 11],
                'LEVEL': [0, 1, 1, 2, 2, 
                          0, 1, 1, 1, 2, 2, 2, 2, 
                          0, 1, 1, 2, 2],
                'MAXIBOQTY': [1, 4, 2, 25, 10, 
                              1, 4, 6, 2, 20, 15, 15, 10, 
                              1, 4, 1, 15, 15]
            }
    data_types_BOM = {
        'MyBOMID': 'int64',
        'MyITEMID': 'int64',
        'MyPARENTBOMITEMID': 'int64',
        'MyBOMITEMID': 'int64',
        'LEVEL': 'int64',
        'MAXIBOQTY': 'int64'
    }
    
    BOM = pd.DataFrame(BOM_dict).astype(data_types_BOM)
    
    MixedItems_dict = {
        'MyBOMITEMID': [1, 4, 6],
        'RUNTIME_COST': [20, 5, 10],
        'SETUP_COST': [200, 120, 150],
        'LEADTIME_ROUTES': [1, 1, 1],
        'MOQ_Fabricacion': [40, 35, 35],
        'UNITPRICE_Compra': [30, 5, 12],
        'LEADTIME': [1, 2, 1],
        'MOQ_Compra': [15, 10, 10]
    }
    data_types_mixed = {
        'MyBOMITEMID': 'int64',
        'RUNTIME_COST': 'int64',
        'SETUP_COST': 'int64',
        'LEADTIME_ROUTES': 'int64',
        'MOQ_Fabricacion': 'int64',
        'UNITPRICE_Compra': 'int64',
        'LEADTIME': 'int64',
        'MOQ_Compra': 'int64'
    }
    MixedItems = pd.DataFrame(MixedItems_dict).astype(data_types_mixed)
    
    PurchaseItems_dict = {
        'MyBOMITEMID': [8, 5, 9, 10, 11],
        'UNITPRICE_Compra': [20, 25, 2, 3, 2],
        'LEADTIME': [1, 0, 1, 2, 1],
        'MOQ_Compra': [10, 15, 75, 45, 30]
    }
    data_types_purchase = {
        'MyBOMITEMID': 'int64',
        'UNITPRICE_Compra': 'int64',
        'LEADTIME': 'int64',
        'MOQ_Compra': 'int64'
    }
    PurchaseItems = pd.DataFrame(PurchaseItems_dict).astype(data_types_purchase)
    
    RouteItems_dict = {
        'MyBOMITEMID': [2, 3, 7],
        'RUNTIME_COST': [10, 15, 5],
        'SETUP_COST': [150, 150, 80],
        'LEADTIME': [1, 2, 0],
        'MOQ_Fabricacion': [200, 75, 75]
    }
    data_types_routes = {
        'MyBOMITEMID': 'int64',
        'RUNTIME_COST': 'int64',
        'SETUP_COST': 'int64',
        'LEADTIME': 'int64',
        'MOQ_Fabricacion': 'int64'
    }
    RouteItems = pd.DataFrame(RouteItems_dict).astype(data_types_routes)
    
    Orders_dict = {
        'MyBOMITEMID': [1, 1, 1, 2, 2, 3, 
                        1, 2, 2, 
                        1, 2, 3, 
                        1, 2, 3, 3],
        'CUSTOMERID': ['a', 'b', 'c', 'a', 'd', 'e', 
                       'a', 'f', 'b', 
                       'b', 'c', 'g', 
                       'd', 'e', 'f', 'g'],
        'QUANTITY': [30, 25, 10, 30, 15, 25, 
                     15, 25, 30, 
                     15, 25, 15, 
                     50, 40, 50, 35],
        'UNITPRICE_EUR': [500, 750, 1000, 450, 800, 500, 
                          700, 400, 600, 
                          900, 500, 750, 
                          650, 800, 1000, 700],
        'END_DATE': [
            '2024-07-02 00:00:00', '2024-07-02 00:00:00', '2024-07-02 00:00:00', '2024-07-02 00:00:00', '2024-07-02 00:00:00', '2024-07-02 00:00:00',
            '2024-08-02 00:00:00', '2024-08-02 00:00:00', '2024-08-02 00:00:00',
            '2024-09-02 00:00:00', '2024-09-02 00:00:00', '2024-09-02 00:00:00',
            '2024-10-02 00:00:00', '2024-10-02 00:00:00', '2024-10-02 00:00:00', '2024-10-02 00:00:00'
        ]
    }
    
    Orders_dict['END_DATE'] = pd.to_datetime(Orders_dict['END_DATE'], format='%Y-%m-%d %H:%M:%S')
    
    Orders = pd.DataFrame(Orders_dict).astype({
        'MyBOMITEMID': 'int64',
        'CUSTOMERID': 'str',
        'QUANTITY': 'int64',
        'UNITPRICE_EUR': 'float64',
        'END_DATE': 'datetime64[ns]'
    })
    
    Stock_dict = {
        'MyBOMITEMID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        'STOCK': [0, 15, 10, 20, 15, 10, 2, 10, 70, 50, 100]
    }

    # Create the DataFrame with specified data types
    Stock = pd.DataFrame(Stock_dict).astype({
        'MyBOMITEMID': 'int64',
        'STOCK': 'int64'
    })
    
    return BOM, MixedItems, PurchaseItems, RouteItems, Orders, Stock