select
nrs_datastream.id, 
nrs_datastream.title, 
AVG(nrs_datastream.constant_value+(nrs_datapoint.value_at - nrs_datastream.lambda_value)/nrs_datastream.factor_value) AS avg_value_at ,
nrs_datapoint.datetime_at
FROM

fbg_picture,
nrs_datastream_picture,
nrs_datastream,
nrs_datapoint

WHERE
fbg_picture.filename = 'H665_20121105.png' AND
fbg_picture.filename = nrs_datastream_picture.filename AND
nrs_datastream_picture.datastream_id = nrs_datastream.id AND
nrs_datastream.id = nrs_datapoint.nrs_datastream_id AND
nrs_datapoint.datetime_at <= '20121231' AND nrs_datapoint.datetime_at >= '20121001'
GROUP BY nrs_datastream.id, nrs_datapoint.datetime_at
ORDER BY nrs_datastream.id, nrs_datapoint.datetime_at

