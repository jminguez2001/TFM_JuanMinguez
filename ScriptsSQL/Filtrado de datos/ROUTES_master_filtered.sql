-- Crear la tabla con los campos necesarios de la FABRICACION
CREATE TABLE iPurchase.ROUTES_master_Filtered AS
WITH ROUTES AS (
SELECT ITEMID, ROUTEID, LINEROUTEID, COMPANYID, SUBSIDIARYID, RUNTIME_COST, SETUP_COST, CURRENCYCODE 
FROM iPurchase.ROUTES_master
WHERE APPROVED IS TRUE AND ACTIVE IS TRUE AND "LEVEL" = 0
ORDER BY ITEMID, ROUTEID, LINEROUTEID
), MOQROUTES AS (
	SELECT COMPANYID, SUBSIDIARYID, ITEMID,
	CASE LINEROUTEID
	    WHEN 'ZI' THEN 700
	    WHEN 'ZC' THEN 700
	    WHEN 'ZB' THEN 700
	    WHEN 'Z3' THEN 300
	    WHEN 'Z2' THEN 500
	    WHEN 'Z1' THEN 700
	    WHEN 'Z0-CP' THEN 700
	    WHEN 'Z0-CG' THEN 700
	    WHEN 'Z0-A' THEN 700
	    WHEN 'LASER-KITS' THEN 1
	    WHEN 'LASER-3' THEN 1
	    WHEN 'LASER-2' THEN 1
	    WHEN 'LASER-1' THEN 1
	    WHEN 'BIKONE' THEN 1
	    WHEN 'B2Z-RW' THEN 1
	    WHEN 'B2Z-FW' THEN 1
	    WHEN 'B1Z-RT' THEN 1
	    WHEN 'B1Z-RM' THEN 1
	    WHEN 'B1Z-KRBC' THEN 1
	    ELSE NULL -- It will be null for the values coming from LINEROUTEID = ''
	END AS MOQs, 1 AS ORDERTYPE
	FROM ROUTES
) SELECT r.*, moq.MOQs
FROM 
ROUTES r LEFT JOIN MOQROUTES moq
ON r.ITEMID = moq.ITEMID
;