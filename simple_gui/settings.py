#!\\usr\\bin\\python
import os
hostname="127.0.0.1"
portnumber=3306
username="root"
password=""
gibedatafolder_path = "C:\\SWS"
gibelogfile_name = "GibeNRSApp.log"
environment_name = "GIBE3"
first_node = "TT"
gibelogfile_path = os.path.join(gibedatafolder_path,environment_name ,gibelogfile_name)
gibeimportfolder_path = os.path.join(gibedatafolder_path, environment_name)
database = os.path.join( gibedatafolder_path ,environment_name, "db","fbg_web.db")
environment_uid="459"