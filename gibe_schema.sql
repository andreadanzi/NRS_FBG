CREATE TABLE `location` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT ,  `location_name` varchar(255) DEFAULT NULL,  `country_id` int(11) NOT NULL DEFAULT '0',  `latitude` double NOT NULL DEFAULT '0',  `longitude` double NOT NULL DEFAULT '0',  `location_visible` tinyint(4) NOT NULL DEFAULT '1',  `location_date` datetime DEFAULT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE `nrs_csv_client` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `active` tinyint(4) NOT NULL DEFAULT '1',  `folder` text,  `file_name` text,  `sha256sum` text,  `noitems` int(11) NOT NULL DEFAULT '0',  `saved_folder` text,  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE `nrs_datapoint` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `nrs_environment_id` int(11) NOT NULL DEFAULT '0',  `nrs_node_id` int(11) NOT NULL DEFAULT '0',  `nrs_datastream_id` int(11) NOT NULL DEFAULT '0',  `incident_id` int(11) NOT NULL DEFAULT '0',  `sample_no` int(11) NOT NULL DEFAULT '0',  `value_at` decimal(10,6) NOT NULL,  `datetime_at` varchar(29) NOT NULL DEFAULT '0000-00-00 00:00:00.000000',  `updated` datetime DEFAULT NULL);
CREATE TABLE `nrs_environment` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `title` varchar(100) NOT NULL,  `environment_uid` varchar(32) NOT NULL,  `description` text,  `status` tinyint(4) NOT NULL DEFAULT '3',  `updated` datetime DEFAULT NULL,  `location_id` bigint(20) DEFAULT NULL,  `location_name` varchar(100) DEFAULT NULL,  `location_disposition` varchar(255) DEFAULT NULL,  `location_exposure` varchar(255) DEFAULT NULL,  `location_latitude` varchar(255) DEFAULT NULL,  `location_longitude` varchar(255) DEFAULT NULL,  `location_elevation` int(11) DEFAULT '0',  `feed` text,  `active` tinyint(4) NOT NULL DEFAULT '1',  `person_first` varchar(200) DEFAULT NULL,  `person_last` varchar(200) DEFAULT NULL,  `person_email` varchar(120) DEFAULT NULL,  `person_phone` varchar(60) DEFAULT NULL,  `automatic_reports` tinyint(4) NOT NULL DEFAULT '0');
CREATE TABLE `nrs_meta` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `nrs_entity_id` int(11) NOT NULL DEFAULT '0',  `nrs_entity_type` tinyint(4) NOT NULL DEFAULT '0',  `meta_key` varchar(255) DEFAULT NULL,  `meta_value` longtext);
CREATE TABLE `nrs_node` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `nrs_environment_id` int(11) NOT NULL DEFAULT '0',  `title` varchar(100) DEFAULT NULL,  `node_uid` varchar(32) NOT NULL,  `description` text,  `status` tinyint(4) NOT NULL DEFAULT '3',  `node_disposition` varchar(255) DEFAULT NULL,  `node_exposure` varchar(255) DEFAULT NULL,  `last_update` datetime DEFAULT NULL,  `risk_level` tinyint(4) NOT NULL DEFAULT '1',  `updated` datetime DEFAULT NULL,  `active` tinyint(4) NOT NULL DEFAULT '1');
CREATE TABLE `nrs_datastream` (  `id` INTEGER PRIMARY KEY AUTOINCREMENT,  `nrs_node_id` int(11) NOT NULL DEFAULT '0',  `title` varchar(100) DEFAULT NULL,  `datastream_uid` varchar(32) NOT NULL,  `unit_label` varchar(100) DEFAULT NULL,  `unit_type` varchar(100) DEFAULT NULL,  `unit_symbol` varchar(100) DEFAULT NULL,  `unit_format` varchar(100) DEFAULT NULL,  `tags` text,  `current_value` float NOT NULL DEFAULT '0',  `min_value` float DEFAULT NULL,  `max_value` float DEFAULT NULL,  `updated` datetime DEFAULT NULL,  `nrs_environment_id` int(11) NOT NULL DEFAULT '0',  `active` tinyint(4) NOT NULL DEFAULT '1',  `samples_num` int(11) NOT NULL DEFAULT '10',  `factor_title` varchar(100) DEFAULT NULL,  `factor_value` decimal(10,6) NOT NULL DEFAULT '1.000000',  `lambda_value` decimal(10,6) NOT NULL DEFAULT '0.000000',  `constant_value` decimal(10,6) NOT NULL DEFAULT '0.000000');
CREATE TABLE nrs_datastream_picture (id INTEGER PRIMARY KEY AUTOINCREMENT, datastream_id int(11) NOT NULL DEFAULT '0', filename TEXT, filepath TEXT, px int(11)  NULL DEFAULT '0', py int(11) NULL DEFAULT '0', description TEXT);