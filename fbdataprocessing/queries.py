#!/usr/bin/python
# -*- coding: utf-8 -*-
query = {}

query["WA"] = """
SELECT so.num, soitem.productNum, so.billToName, pickitem.qty, qtyinventory.qtyonhand - qtycommitted.qty as qtyonhand, qtyinventory.qtyonorderpo, qtyinventory.qtyonorderto, (qtyinventory.qtyonorderpo + qtyinventory.qtyonorderto) as qtyonordertotal,soitem.statusId as soitemstatusId, so.statusId as sostatusId, pickitem.statusId as pickitemstatusId, soitem.typeId as soitemtypeId, soitem.dateLastModified, soitem.note, so.salesman, pick.locationgroupid, so.dateIssued
FROM soitem
LEFT JOIN so
    ON so.id = soitem.soid
LEFT JOIN pickitem
    ON pickitem.soItemId = soitem.id
LEFT JOIN part
            ON part.defaultProductId = soitem.productid
LEFT JOIN (SELECT * FROM qtyinventory WHERE locationgroupid = "7") as qtyinventory
        ON qtyinventory.partid = part.id
LEFT JOIN (SELECT * FROM qtycommitted WHERE locationgroupid = "7") as qtycommitted
                ON qtycommitted.partid = part.id
LEFT JOIN (SELECT * FROM pick WHERE locationgroupid = "7") as pick
                ON pickitem.pickId = pick.id
WHERE pick.locationgroupId = "7"
AND (soitem.statusId LIKE "10" OR soitem.statusId LIKE "30" OR soitem.statusId LIKE "20")
AND (so.statusId LIKE "20" OR so.statusId LIKE "25")
AND productNum NOT LIKE ("NX-%") AND productNum NOT LIKE ("FREIGHT%") AND productNum NOT LIKE ("HIK-CENTRAL-P%")
AND soitem.typeId NOT LIKE ("90")
ORDER BY so.dateIssued
"""

query["QLD"] = """
SELECT so.num, soitem.productNum, so.billToName, pickitem.qty, qtyinventory.qtyonhand - qtycommitted.qty as qtyonhand, qtyinventory.qtyonorderpo, qtyinventory.qtyonorderto, (qtyinventory.qtyonorderpo + qtyinventory.qtyonorderto) as qtyonordertotal,soitem.statusId as soitemstatusId, so.statusId as sostatusId, pickitem.statusId as pickitemstatusId, soitem.typeId as soitemtypeId, soitem.dateLastModified, soitem.note, so.salesman, pick.locationgroupid
FROM soitem
LEFT JOIN so
    ON so.id = soitem.soid
LEFT JOIN pickitem
    ON pickitem.soItemId = soitem.id
LEFT JOIN part
            ON part.defaultProductId = soitem.productid
LEFT JOIN (SELECT * FROM qtyinventory WHERE locationgroupid = "1") as qtyinventory
        ON qtyinventory.partid = part.id
LEFT JOIN (SELECT * FROM qtycommitted WHERE locationgroupid = "1") as qtycommitted
                ON qtycommitted.partid = part.id
LEFT JOIN (SELECT * FROM pick WHERE locationgroupid = "1") as pick
                ON pickitem.pickId = pick.id
WHERE pick.locationgroupId = "1"
AND (soitem.statusId LIKE "10" OR soitem.statusId LIKE "30" OR soitem.statusId LIKE "20")
AND (so.statusId LIKE "20" OR so.statusId LIKE "25")
AND productNum NOT LIKE ("NX-%") AND productNum NOT LIKE ("FREIGHT%") AND productNum NOT LIKE ("HIK-CENTRAL-P%")
AND soitem.typeId NOT LIKE ("90")
"""

query["NSW"] = """
SELECT so.num, soitem.productNum, so.billToName, pickitem.qty, qtyinventory.qtyonhand - qtycommitted.qty as qtyonhand, qtyinventory.qtyonorderpo, qtyinventory.qtyonorderto, (qtyinventory.qtyonorderpo + qtyinventory.qtyonorderto) as qtyonordertotal,soitem.statusId as soitemstatusId, so.statusId as sostatusId, pickitem.statusId as pickitemstatusId, soitem.typeId as soitemtypeId, soitem.dateLastModified, soitem.note, so.salesman, pick.locationgroupid
FROM soitem
LEFT JOIN so
    ON so.id = soitem.soid
LEFT JOIN pickitem
    ON pickitem.soItemId = soitem.id
LEFT JOIN part
            ON part.defaultProductId = soitem.productid
LEFT JOIN (SELECT * FROM qtyinventory WHERE locationgroupid = "34") as qtyinventory
        ON qtyinventory.partid = part.id
LEFT JOIN (SELECT * FROM qtycommitted WHERE locationgroupid = "34") as qtycommitted
                ON qtycommitted.partid = part.id
LEFT JOIN (SELECT * FROM pick WHERE locationgroupid = "34") as pick
                ON pickitem.pickId = pick.id
WHERE pick.locationgroupId = "34"
AND (soitem.statusId LIKE "10" OR soitem.statusId LIKE "30" OR soitem.statusId LIKE "20")
AND (so.statusId LIKE "20" OR so.statusId LIKE "25")
AND productNum NOT LIKE ("NX-%") AND productNum NOT LIKE ("FREIGHT%") AND productNum NOT LIKE ("HIK-CENTRAL-P%")
AND soitem.typeId NOT LIKE ("90")
"""

query["VIC"] = """
SELECT so.num, soitem.productNum, so.billToName, pickitem.qty, qtyinventory.qtyonhand - qtycommitted.qty as qtyonhand, qtyinventory.qtyonorderpo, qtyinventory.qtyonorderto, (qtyinventory.qtyonorderpo + qtyinventory.qtyonorderto) as qtyonordertotal,soitem.statusId as soitemstatusId, so.statusId as sostatusId, pickitem.statusId as pickitemstatusId, soitem.typeId as soitemtypeId, soitem.dateLastModified, soitem.note, so.salesman, pick.locationgroupid
FROM soitem
LEFT JOIN so
    ON so.id = soitem.soid
LEFT JOIN pickitem
    ON pickitem.soItemId = soitem.id
LEFT JOIN part
            ON part.defaultProductId = soitem.productid
LEFT JOIN (SELECT * FROM qtyinventory WHERE locationgroupid = "10") as qtyinventory
        ON qtyinventory.partid = part.id
LEFT JOIN (SELECT * FROM qtycommitted WHERE locationgroupid = "10") as qtycommitted
                ON qtycommitted.partid = part.id
LEFT JOIN (SELECT * FROM pick WHERE locationgroupid = "10") as pick
                ON pickitem.pickId = pick.id
WHERE pick.locationgroupId = "10"
AND (soitem.statusId LIKE "10" OR soitem.statusId LIKE "30" OR soitem.statusId LIKE "20")
AND (so.statusId LIKE "20" OR so.statusId LIKE "25")
AND productNum NOT LIKE ("NX-%") AND productNum NOT LIKE ("FREIGHT%") AND productNum NOT LIKE ("HIK-CENTRAL-P%")
AND soitem.typeId NOT LIKE ("90")
"""