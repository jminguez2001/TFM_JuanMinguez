
-- Items de fabricacion y compra
SELECT * FROM iPurchase.ROUTES_master_Filtered rmf
INNER JOIN
(SELECT * FROM 
(SELECT DISTINCT BOMITEMID FROM iPurchase.BOM_NoSustitutives) t1
INNER JOIN 
(SELECT * FROM iPurchase.PURCHPRICE_master_Filtered) t2
ON UPPER(t1.BOMITEMID) = UPPER(t2.ITEMID)
WHERE t2.UNITPRICE IS NOT NULL
) t3
ON UPPER(rmf.ITEMID)= UPPER(t3.ITEMID)
;


-- Items de compra
SELECT * FROM iPurchase.ROUTES_master_Filtered rmf
RIGHT JOIN
(SELECT * FROM 
(SELECT DISTINCT BOMITEMID FROM iPurchase.BOM_NoSustitutives) t1
INNER JOIN 
(SELECT * FROM iPurchase.PURCHPRICE_master_Filtered) t2
ON UPPER(t1.BOMITEMID) = UPPER(t2.ITEMID)
-- WHERE t2.UNITPRICE IS NOT NULL
) t3
ON UPPER(rmf.ITEMID)= UPPER(t3.ITEMID)
WHERE rmf.ITEMID IS NULL
;

-- Items de fabricacion
SELECT * FROM 
(SELECT * FROM 
(SELECT DISTINCT BOMITEMID FROM iPurchase.BOM_NoSustitutives) t1
INNER JOIN 
(SELECT * FROM iPurchase.ROUTES_master_Filtered) t2
ON UPPER(t1.BOMITEMID) = UPPER(t2.ITEMID)) t3
LEFT JOIN 
(SELECT * FROM iPurchase.PURCHPRICE_master_Filtered) t4
ON UPPER(t3.ITEMID)= UPPER(t4.ITEMID)
WHERE t4.UNITPRICE IS NULL
;