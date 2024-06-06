CREATE TABLE iPurchase.CustomerPrices AS
WITH NoNull AS (
SELECT t1.ITEMID, t1."CATALOG",t2.COMPANYID, t2.SUBSIDIARYID, t2.CUSTOMERID, t2.UNITPRICE_EUR FROM
(SELECT DISTINCT ITEMID, "CATALOG" FROM iPurchase.BOM_NoSustitutives) t1
LEFT JOIN 
(SELECT * FROM fersadv.GlobalSalesPrices_ALL WHERE SUBSIDIARYID= 'FBEA') t2
ON t1.ITEMID = t2.ITEMID
WHERE t2.ITEMID IS NOT NULL
), WithNull AS (
SELECT t1.ITEMID, t1."CATALOG",t2.COMPANYID, t2.SUBSIDIARYID, t2.CUSTOMERID, t2.UNITPRICE_EUR FROM
(SELECT DISTINCT ITEMID, "CATALOG" FROM iPurchase.BOM_NoSustitutives) t1
LEFT JOIN 
(SELECT * FROM fersadv.GlobalSalesPrices_ALL WHERE SUBSIDIARYID= 'FBEA') t2
ON t1.ITEMID = t2.ITEMID
WHERE t2.ITEMID IS NULL -- Para aquellos nulos se tomaran posteriormente valores relacionados con ítems con el mismo nombre de catalogo
) (SELECT * FROM NoNull) UNION (SELECT * FROM WithNull);