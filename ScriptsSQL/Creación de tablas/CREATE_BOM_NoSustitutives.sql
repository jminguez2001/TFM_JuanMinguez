CREATE TABLE iPurchase.BOM_NoSustitutives AS 
WITH NoSustitutives AS ( -- Se seleccionan las listas de materiales facilitadas inicialmente sin sustitutivos de la maestro de la empresa
    WITH myBOMs AS( -- Se seleccionan las BOM que se facilitaron inicialmente
		SELECT DISTINCT BOMID, SUBSIDIARYID FROM iPurchase.BOM_fewDATA -- Esta tabla contiene los identificadores de las BOM con las que se trabajará
	) SELECT
		ba.BOMID,
	    ba.ITEMID,
	    ba.BOMQTY,
	    ba.UNITID,
	    ba.PMFPLANGROUPID,
	    ba.PRIORITY,
	    ba.SUBSIDIARYID,
	    ba.BOMITEMID,
	    ba.COMPANYID,
	    ba.LEVEL,
	    ba.PATH,
	    ba.PARENTBOMITEMID,
	    ba.MAXIBOQTY,
	    ba.ORDERTYPE,
	    ba.BOMREALQTY,
	    ba.DEFAULTORDERTYPETREE,
	    ba.PURCHCOSTWEIGHT,
	    ba.COSTWEIGHT,
	    ba.CATALOG,
	    ba.BOMCATALOG,
	    ba.ITEMPATH
	FROM 
	myBOMs mb LEFT JOIN fersadv.BOMTree_ALL ba -- Se cruzan con la maestro sin sustitutivos
	ON HASH(mb.BOMID,mb.SUBSIDIARYID)=HASH(ba.BOMID,ba.SUBSIDIARYID)
	WHERE ba.APPROVED = TRUE
	AND (ba.BOMITEMID NOT LIKE '67%'
        AND ba.BOMITEMID NOT LIKE '68%'
        AND ba.BOMITEMID NOT LIKE '69%'
        AND ba.BOMITEMID NOT LIKE '7%'
        AND ba.BOMITEMID NOT LIKE '8%') -- Se desprecian los embalajes
),
NEWBOMITEMID AS ( 
    SELECT
        BOMITEMID,
        ROW_NUMBER() OVER (ORDER BY BOMITEMID) AS MyBOMITEMID
    FROM
        (SELECT DISTINCT BOMITEMID FROM NoSustitutives) AS distinct_bomitems
),
NEWBOMID AS (
    SELECT
        BOMID,
        ROW_NUMBER() OVER (ORDER BY BOMID) AS MyBOMID
    FROM
        (SELECT DISTINCT BOMID FROM NoSustitutives) AS distinct_bomid
),
NEWITEMID AS (
    SELECT
        ns.ITEMID,
        ni.MyBOMITEMID AS MyITEMID
    FROM
        NoSustitutives ns
    LEFT JOIN NEWBOMITEMID ni ON ns.ITEMID = ni.BOMITEMID
),
NEWPARENTID AS (
    SELECT
        ns.PARENTBOMITEMID,
        np.MyBOMITEMID AS MyPARENTBOMITEMID
    FROM
        NoSustitutives ns
    LEFT JOIN NEWBOMITEMID np ON ns.PARENTBOMITEMID = np.BOMITEMID
)
SELECT
	ns.BOMID,
	nb.MyBOMID,
    ns.COMPANYID,
    ns.SUBSIDIARYID,
    ns.ITEMID,
    t1.MyITEMID,
    ns.PARENTBOMITEMID,
    t2.MyPARENTBOMITEMID,
    ns.BOMITEMID,
    ni.MyBOMITEMID,
    ns.LEVEL,
    --ns.PRIORITY,
    --ns.PMFPLANGROUPID,
    ns.MAXIBOQTY,
    ns.UNITID,
    ns.BOMREALQTY,
    --ns.ORDERTYPE,
    --ns.DEFAULTORDERTYPETREE,
    ns.ITEMPATH,
    ns.PATH,
    ns.CATALOG,
    ns.BOMCATALOG
FROM
NoSustitutives ns
LEFT JOIN NEWBOMITEMID ni ON ns.BOMITEMID = ni.BOMITEMID
LEFT JOIN NEWBOMID nb ON ns.BOMID = nb.BOMID
LEFT JOIN (SELECT DISTINCT ITEMID, MyITEMID FROM NEWITEMID) t1 ON ns.ITEMID = t1.ITEMID
LEFT JOIN (SELECT DISTINCT PARENTBOMITEMID, MyPARENTBOMITEMID FROM NEWPARENTID) t2 ON ns.PARENTBOMITEMID = t2.PARENTBOMITEMID;

