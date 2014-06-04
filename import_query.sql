INSE
RT INTO 
nrs_node
(node_uid , nrs_environment_id, title, active, status, updated)
select distinct nrs_environment.environment_uid ||  sws_mappa_sensori.mod as node_uid, nrs_environment.id as nrs_environment_id, 'MOD_' || sws_mappa_sensori.mod as title, 1 as active, 4 as status, CURRENT_TIMESTAMP
from 
sws_mappa_sensori, nrs_environment


INSERT INTO 
nrs_datastream
(nrs_node_id, title, datastream_uid,nrs_environment_id, samples_num, factor_title, factor_value, factor_value_2, lambda_value, constant_value, updated)
select distinct nrs_node.id as nrs_node_id,
sws_mappa_sensori.nome as title,
nrs_node.node_uid || '_' || substr('00' || sws_mappa_sensori.ch, -2,2) || '.' ||  sws_mappa_sensori.nome as datastream_uid,
nrs_node.nrs_environment_id as nrs_environment_id,
10 as samples_num,
 sws_mappa_sensori.lambda as factor_title,
 sws_mappa_sensori.sensitivity as factor_value,
 sws_mappa_sensori.sensitivity2 as factor_value_2,
  sws_mappa_sensori.lambda as lambda_value,
  sws_mappa_sensori.t0 as constant_value, CURRENT_TIMESTAMP
from nrs_node, sws_mappa_sensori
WHERE
nrs_node.node_uid = 'GIBE3' ||  sws_mappa_sensori.mod

update 
sws_mappa_sensori
SET sensitivity2 = 0 WHERE sensitivity2 IS NULL

UPDATE nrs_datastream
SET 
factor_value_2 = (  SELECT sws_mappa_sensori.sensitivity2   from  sws_mappa_sensori, nrs_datastream JOIN nrs_node ON nrs_node.node_uid = 'GIBE3' ||  sws_mappa_sensori.mod WHERE  nrs_datastream.datastream_uid = nrs_node.node_uid || '_' || substr('00' || sws_mappa_sensori.ch, -2,2) || '.' ||  sws_mappa_sensori.nome )


