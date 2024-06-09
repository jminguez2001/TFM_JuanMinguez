-- Añadir MyBOMITEMID a SalesOrders
CREATE TABLE iPurchase.SalesOrders AS
SELECT t1.MyBOMITEMID, t2.* FROM
(SELECT DISTINCT MyBOMITEMID, BOMITEMID FROM iPurchase.BOM_NoSustitutives) as t1
INNER JOIN 
(SELECT * FROM iPurchase.SalesOrders_NoSustitutives) as t2
ON UPPER(t1.BOMITEMID ) = UPPER(t2.ITEMID);