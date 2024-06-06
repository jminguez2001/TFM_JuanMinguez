query_Select_BOMs_fewDATA = '''
SELECT DISTINCT ITEMID FROM iPurchase.BOM_fewDATA_Filtered;
'''

query_Select_BOMs_NoSustitutives = '''
SELECT DISTINCT ITEMID FROM iPurchase.BOM_NoSustitutives;
'''

query_Select_CustomerPrices = '''
SELECT * FROM iPurchase.CustomerPrices;
'''