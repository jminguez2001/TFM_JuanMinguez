WITH PARENTS_No_Priority AS ( -- PARENTBOMITEMIDs que se identifican posteriormente con BOMITEMIDs de prioridad >1
    SELECT 
        t2.MyBOMID AS t2_MyBOMID, 
        t2.MyBOMITEMID AS t2_MyBOMITEMID, 
        t2."LEVEL" AS t2_LEVEL,
        t2.PRIORITY AS t2_PRIORITY, 
        t2.PMFPLANGROUPID AS t2_PMFPLANGROUPID, 
        t1.MyBOMID AS t1_MyBOMID, 
        t1.MyITEMID AS t1_MyITEMID, 
        t1.MyPARENTBOMITEMID AS t1_MyPARENTBOMITEMID, 
        t1.MyBOMITEMID AS t1_MyBOMITEMID, 
        t1."LEVEL" AS t1_LEVEL,
        t1.PRIORITY AS t1_PRIORITY
    FROM 
        (SELECT DISTINCT MyBOMID, MyBOMITEMID, "LEVEL", PRIORITY, PMFPLANGROUPID  
         FROM iPurchase.BOM_fewDATA_MyIDs 
         WHERE PRIORITY > 1) t2
    INNER JOIN 
        iPurchase.BOM_fewDATA_MyIDs t1
    ON t1.MyPARENTBOMITEMID = t2.MyBOMITEMID AND t1.MyBOMID = t2.MyBOMID
) 
SELECT -- Seleccionamos aquellos BOMITEMIDs asociados al PMFPLANGROUPID de los anteriores elementos considerados PARENTS sin prioridad
    t3.MyBOMID AS t3_MyBOMID, 
    t3.MyBOMITEMID AS t3_MyBOMITEMID, 
    t3."LEVEL" AS t3_LEVEL, 
    t3.PRIORITY AS t3_PRIORITY, 
    t3.PMFPLANGROUPID AS t3_PMFPLANGROUPID, 
    pnp.t2_MyBOMID, 
    pnp.t2_MyBOMITEMID, 
    pnp.t2_LEVEL, 
    pnp.t2_PRIORITY, 
    pnp.t2_PMFPLANGROUPID, 
    pnp.t1_MyBOMID, 
    pnp.t1_MyITEMID, 
    pnp.t1_MyPARENTBOMITEMID, 
    pnp.t1_MyBOMITEMID, 
    pnp.t1_LEVEL, 
    pnp.t1_PRIORITY
FROM
    PARENTS_No_Priority pnp
LEFT JOIN
    (SELECT * FROM iPurchase.BOM_fewDATA_MyIDs WHERE PRIORITY in (0,1)) t3
ON 
    pnp.t2_MyBOMID = t3.MyBOMID 
    AND pnp.t2_LEVEL = t3."LEVEL" 
    AND t3.PMFPLANGROUPID = pnp.t2_PMFPLANGROUPID;
