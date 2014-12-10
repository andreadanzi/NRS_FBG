#!/usr/bin/python

import os, sys, MySQLdb,sqlite3, logging, re, csv, hashlib, time, shutil
import settings

from datetime import datetime

class GibeToNrs():
  def __init__(self,e_uid,n_uid, csv_folder,logger, node_id=0):
    self.logger = logger
    self.csv_folder = csv_folder
    self.env_uid = e_uid
    self.n_uid = n_uid
    self.nodeselected_id = node_id
    if( not os.path.isdir(self.csv_folder) ):
      raise IOError("CSV Folder %s does not exists" % self.csv_folder)
    os.chdir(self.csv_folder)
    self.nrs_environment_id = self.check_env_uid()
    self.iRun = 0
    self.import_file_path = ""
    self.shutdown = False
  
  def set_import_file(self,importFilePath):
    self.import_file_path =  importFilePath
  
  def run(self):
    self.logger.info("GibeToNrs started on %s is starting up" % (self.csv_folder))
    try:
      if os.path.exists(self.csv_folder):
        self.read_csv_folder()
    except SyntaxError, e:
      self.logger.error( "Error: %s" % e )
      self.shutdown = True;
    self.logger.info("GibeToNrs started on %s is shutting down with iRun=%d" % (self.csv_folder,self.iRun))
  
  
  def import_itemlist(self,itemlist):
    self.logger.info("GibeToNrs.import_itemlist started on %d items"% len(itemlist))   
    bulk_insert_row = []
    bulk_insert_row.append(("nrs_environment_id", "nrs_node_id","nrs_datastream_id","sample_no","value_at","datetime_at","updated"  ))
    sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
    dsItems = self.get_datastream_for_lambda(self.nodeselected_id)
    sample = 0
    foundQty = 1
    skipped_rows=[]
    for row in itemlist:
      sample = sample + 1
      cols = row.split('\t')
      if len(cols) < len(dsItems) + 2:
        self.logger.info("GibeToNrs.import_itemlist row number %d, there are %d measures against %d datastream....some measures were lost! " %(sample, len(cols)-2,len(dsItems)))
      elif len(cols) > len(dsItems) + 2:
        self.logger.error("GibeToNrs.import_itemlist, too many measures (%d), skipping row number %d" % (len(cols),sample))
        skipped_rows.append(row)
        continue
      sdate = "%s" % cols[0] ### first item is the date
      stime = "%s" % cols[1] ### second item is the time
      if len(stime)==8:
        stime = stime + ".000"
      dt=datetime.strptime(sdate + " " +stime,"%d/%m/%Y %H:%M:%S.%f")
      sAt = dt.strftime('%Y%m%d%H%M%S%f')
      iProg = 2   
      for dsItem in dsItems:
        dsLambda = dsItem['lambda']
        dsRange = dsItem['range']
        dsCh = dsItem['ch']
        nrs_datastream_id = dsItem['id']
        flast_value = 0.0
        bFound = False
        if iProg == len(cols):
            self.logger.info("GibeToNrs.import_itemlist, measures number (%d) out of range , skipping ds %d! " % (len(cols),nrs_datastream_id) )
            continue;
        current_value = "%s" % cols[iProg]
        current_value = current_value.strip().replace(',','.')
        fcurrent_value = round(float(current_value),3)
        if fcurrent_value < dsLambda + dsRange and fcurrent_value > dsLambda - dsRange:
          bFound = True
          iProg = iProg + 1
          foundQty = foundQty + 1
        else:
          current_value = "-998"
          self.logger.error("GibeToNrs.import_itemlist, Datastream %d not found for sample %d; current value is %f and lambda should be %f within a range of %f" % (nrs_datastream_id,sample,fcurrent_value,dsLambda,dsRange))
        bulk_insert_row.append((self.nrs_environment_id, self.nodeselected_id,nrs_datastream_id,sample,current_value,sAt,sUpdated  ))
    if not os.path.exists(self.csv_folder+"/tmp"):
      os.mkdir(self.csv_folder+"/tmp")
    csv_file = time.strftime('%Y%m%d%H%M%S')
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv", 'wb') as importcsvfile:
      writer = csv.writer(importcsvfile,delimiter='|')
      writer.writerows(bulk_insert_row)
    self.logger.info("File %s written" % (self.csv_folder+"/tmp/" + csv_file + ".csv"))	    
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
      dr = csv.DictReader(infile, delimiter='|')
      to_db = [(di['nrs_environment_id'], di['nrs_node_id'], di['nrs_datastream_id'], di['sample_no'], di['value_at'], di['datetime_at'], di['updated']) for di in dr]
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
      dr = csv.DictReader(infile, delimiter='|')        
      del_db = [(dd['nrs_datastream_id'], dd['datetime_at']) for dd in dr]
    #20140710
    csv_file = time.strftime('%Y%m%d%H%M%S')
    sFilePath = os.path.join( self.csv_folder,  "skipped_rows_%s.csv" % csv_file )
    f = file(sFilePath, 'w')
    f.writelines(skipped_rows)
    f.close()
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    dd_dict = {}
    for delitem in del_db:
      if delitem[0] not in dd_dict:
        dd_dict[delitem[0]] = { 'min':delitem[1] ,'max': delitem[1]}
      else:
        if dd_dict[delitem[0]]['min'] > delitem[1]:
          dd_dict[delitem[0]]['min'] = delitem[1]
        if dd_dict[delitem[0]]['max'] < delitem[1]:
          dd_dict[delitem[0]]['max'] = delitem[1]
    sTmpWhere = "1<>1"
    for key, value in dd_dict.items():
      sTmpWhere = sTmpWhere + " OR ( nrs_datastream_id=%s AND datetime_at >= '%s' AND datetime_at <= '%s' )" % (key,value['min'],value['max'])
    sDeleteQuery = """DELETE FROM nrs_datapoint WHERE %s """ % sTmpWhere
    self.logger.info("GibeToNrs.import_itemlist sDeleteQuery = %s"% sDeleteQuery)
    try:
      db_cur.execute(sDeleteQuery)
      sInsertQuery = """INSERT INTO nrs_datapoint ( 
                           nrs_environment_id, 
                           nrs_node_id, 
                           nrs_datastream_id, 
                           sample_no, 
                           value_at, 
                           datetime_at, 
                           updated
                        ) VALUES (?, ?, ?, ?, ?, ?, ?);"""
      self.logger.info("GibeToNrs.import_itemlist sInsertQuery = %s"% sInsertQuery)
      db_cur.executemany(sInsertQuery, to_db)
      db_conn.commit()
    except MySQLdb.Error, e:
      self.logger.error("GibeToNrs.import_itemlist An error has been passed. %s" %e  )
      db_conn.rollback()    
    db_conn.close()
    self.logger.info("GibeToNrs.import_itemlist Terminated, %d samples processed and %d imported!" % (sample,foundQty))
    return foundQty
  
  
  
  def run_itemlist(self,itemlist):  
    self.logger.info("run_itemlist started on %d items"% len(itemlist))    
    bulk_insert = {}
    node_uid = self.n_uid
    bulk_insert_row = []
    bulk_insert_row.append(("nrs_environment_id", "nrs_node_id","nrs_datastream_id","sample_no","value_at","datetime_at","updated"  ))
    sample=1      
    i=0
    sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
    dsItems = self.get_datastream_for_lambda(self.nodeselected_id)
    iRow = 0
    for row in itemlist:
      #self.logger.info("GibeToNrs on %s reads CSV sample number %d" % (self.csv_folder,sample) )
      iRow = iRow + 1
      cols = row.split('\t')
      #self.logger.info("GibeToNrs on %s reads CSV sample number %d" % (self.csv_folder,sample) )
      if len(cols) < len(dsItems) + 2:
        self.logger.info("GibeToNrs.run_itemlist row number %d, there are %d measures against %d datastream....some measures were lost! " %(iRow, len(cols)-2,len(dsItems)))
      elif len(cols) > len(dsItems) + 2:
        self.logger.info("GibeToNrs.run_itemlist, too many measures (%d), skipping row number %d" % (len(cols),iRow))
        continue
      icol=0
      isensor=1
      ds_prefix="_%02d."
      ds_prefix_no = 0
      sAt=""
      flast_value=0.0
      for col in cols:
        icol=icol+1
        if icol==1:
          # first col is date
          sdate = "%s" % col
        elif icol==2:
          # time
          stime = "%s" % col
          if len(stime)==8:
            stime = stime + ".000"
          dt=datetime.strptime(sdate + " " +stime,"%d/%m/%Y %H:%M:%S.%f")
          sAt = dt.strftime('%Y%m%d%H%M%S%f')           
        elif icol > 2:
          current_value = "%s" % col
          current_value = current_value.strip()
          current_value = current_value.replace(',','.')
          fcurrent_value = float(current_value)
          fcurrent_value = round(fcurrent_value,3)
          dsCh = dsItems[icol-3]['ch']
          isensor = isensor
          dsLambda = dsItems[icol-3]['lambda']
          dsRange = dsItems[icol-3]['range']
          # todo: verificare se il criterio +-2 va bene          
          if fcurrent_value < dsLambda + dsRange and fcurrent_value > dsLambda - dsRange:
            nrs_datastream_id = dsItems[icol-3]['id']
          else:
            self.logger.info("GibeToNrs.run_itemlist row number %d, colummn number %d; there is a value (%f) does not match with lambda (%f) of datastream %s " %(iRow, icol,fcurrent_value, dsLambda, dsItems[icol-3]['title']))
            continue
          bulk_insert_row.append((self.nrs_environment_id, self.nodeselected_id,nrs_datastream_id,sample,current_value,sAt,sUpdated  ))
          i=i+1
          isensor = isensor + 1
      sample=sample+1
    self.logger.info("GibeToNrs.run_itemlist, bulk_insert_row is ready with %d samples and %d rows" % (sample-1,i))
    if not os.path.exists(self.csv_folder+"/tmp"):
      os.mkdir(self.csv_folder+"/tmp")
    csv_file = time.strftime('%Y%m%d%H%M%S')
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv", 'wb') as importcsvfile:
      writer = csv.writer(importcsvfile,delimiter='|')
      writer.writerows(bulk_insert_row)
    self.logger.info("File %s written" % (self.csv_folder+"/tmp/" + csv_file + ".csv"))	    
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
      dr = csv.DictReader(infile, delimiter='|')
      to_db = [(di['nrs_environment_id'], di['nrs_node_id'], di['nrs_datastream_id'], di['sample_no'], di['value_at'], di['datetime_at'], di['updated']) for di in dr]
    with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
      dr = csv.DictReader(infile, delimiter='|')        
      del_db = [(dd['nrs_datastream_id'], dd['datetime_at']) for dd in dr]
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    dd_dict = {}
    for delitem in del_db:
      if delitem[0] not in dd_dict:
        dd_dict[delitem[0]] = { 'min':delitem[1] ,'max': delitem[1]}
      else:
        if dd_dict[delitem[0]]['min'] > delitem[1]:
          dd_dict[delitem[0]]['min'] = delitem[1]
        if dd_dict[delitem[0]]['max'] < delitem[1]:
          dd_dict[delitem[0]]['max'] = delitem[1]
    sTmpWhere = "1<>1"
    for key, value in dd_dict.items():
      sTmpWhere = sTmpWhere + " OR ( nrs_datastream_id=%s AND datetime_at >= '%s' AND datetime_at <= '%s' )" % (key,value['min'],value['max'])
    sDeleteQuery = """DELETE FROM nrs_datapoint WHERE %s """ % sTmpWhere
    self.logger.info("GibeToNrs.run_itemlist sDeleteQuery = %s"% sDeleteQuery)
    try:
      db_cur.execute(sDeleteQuery)
      sInsertQuery = """INSERT INTO nrs_datapoint ( 
                           nrs_environment_id, 
                           nrs_node_id, 
                           nrs_datastream_id, 
                           sample_no, 
                           value_at, 
                           datetime_at, 
                           updated
                        ) VALUES (?, ?, ?, ?, ?, ?, ?);"""
      self.logger.info("GibeToNrs.run_itemlist sInsertQuery = %s"% sInsertQuery)
      db_cur.executemany(sInsertQuery, to_db)
      db_conn.commit()
    except MySQLdb.Error, e:
      self.logger.error("GibeToNrs.run_itemlist An error has been passed. %s" %e  )
      db_conn.rollback()    
    db_conn.close()
    return sample-1
    #saved_folder = time.strftime('%Y%m%d%H%M')
    #if not os.path.exists(self.csv_folder+"/"+saved_folder):
    #  os.mkdir(self.csv_folder+"/"+saved_folder)
    #shutil.move(self.csv_folder+"/"+files,self.csv_folder+"/"+saved_folder)
    #self.logger.info("GibeToNrs on %s moved file %s into %s" % (self.csv_folder,files,saved_folder) )
    #db_conn = sqlite3.connect(settings.database)
    #db_cur = db_conn.cursor()
    #sQuery = """INSERT INTO nrs_csv_client (folder,file_name,sha256sum,noitems,saved_folder) VALUES ('%s','%s','%s',%d,'%s')""" % (self.csv_folder,files,sha256sum,i,saved_folder)
    #try:
    #  db_cur.execute(sQuery)
    #  db_conn.commit()
    #except MySQLdb.Error, e:
    #  self.logger.error("An error has been passed. %s" %e  )
    #  db_conn.rollback()    
    #db_conn.close()
  

  def get_datastream_for_lambda(self,node_id):
    sSql = """SELECT id
                ,title
                ,lambda_value
                ,ch
                ,lambda_range
                FROM 
                nrs_datastream
                WHERE 
                nrs_node_id = %d
                ORDER BY ch, lambda_value""" % node_id
    db_conn = sqlite3.connect(settings.database)        
    db_cur = db_conn.cursor()
    retVal= db_cur.execute(sSql)
    rows = retVal.fetchall()
    dsItems = []
    for row in rows:
        dsData={'id':row[0],'title':row[1],'lambda':float(row[2]),'ch':int(row[3]),'range':float(row[4])}
        dsItems.append(dsData)
    return dsItems
        
  
  def read_csv_folder(self):
    if os.path.exists(self.csv_folder) == True and os.path.isfile(self.import_file_path) == True:
      self.logger.info("GibeToNrs.read_csv_folder on %s founds regular file %s" % (self.csv_folder,self.import_file_path) )
      sha256sum = self.sha256Checksum(self.import_file_path)
      bulk_insert = {}
      node_uid = self.n_uid
      bulk_insert_row = []
      bulk_insert_row.append(("nrs_environment_id", "nrs_node_id","nrs_datastream_id","sample_no","value_at","datetime_at","updated"  ))
      sample=1      
      i=0
      sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
      dsItems = self.get_datastream_for_lambda(self.nodeselected_id)
      with open(self.import_file_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')  
        iRow = 0
        for row in csv_reader:
          iRow = iRow + 1
          #self.logger.info("GibeToNrs on %s reads CSV sample number %d" % (self.csv_folder,sample) )
          if len(row) != len(dsItems) + 2:
              self.logger.info("GibeToNrs.read_csv_folder row number %d, there are %d measures against %d datastream....something wrong " %(iRow, len(row)-2,len(dsItems)))
              if len(row) > len(dsItems) + 2:
                  self.logger.info("GibeToNrs.read_csv_folder, too many measures, skipping row number %d" % iRow)
                  continue
          icol=0
          isensor=1
          ds_prefix="_%02d."
          ds_prefix_no = 0
          sAt=""
          for col in row:
            icol=icol+1
            if icol==1:
              # first col is date
              sdate = "%s" % col
            elif icol==2:
              # time
              stime = "%s" % col
              if len(stime)==8:
                stime = stime + ".000"
              dt=datetime.strptime(sdate + " " +stime,"%d/%m/%Y %H:%M:%S.%f")
              sAt = dt.strftime('%Y%m%d%H%M%S%f')           
            elif icol > 2:
              current_value = "%s" % col
              current_value = current_value.strip()
              current_value = current_value.replace(',','.')
              fcurrent_value = float(current_value)
              fcurrent_value = round(fcurrent_value,3)
              dsCh = dsItems[icol-3]['ch']
              isensor = isensor
              dsLambda = dsItems[icol-3]['lambda']
              dsRange = dsItems[icol-3]['range']
              # todo: verificare se il criterio +-2 va bene
              if fcurrent_value < dsLambda + dsRange and fcurrent_value > dsLambda - dsRange:
                  nrs_datastream_id = dsItems[icol-3]['id']
              else:
                  self.logger.info("GibeToNrs.read_csv_folder row number %d, colummn number %d; there is a value (%f) does not match with lambda (%f) of datastream %s " %(iRow, icol,fcurrent_value, dsLambda, dsItems[icol-3]['title']))
                  continue
              bulk_insert_row.append((self.nrs_environment_id, self.nodeselected_id,nrs_datastream_id,sample,current_value,sAt,sUpdated  ))
              i=i+1
              isensor = isensor + 1
          sample=sample+1
      self.logger.info("bulk_insert_row is ready with %d samples and %d rows" % (sample-1,i))
      if not os.path.exists(self.csv_folder+"/tmp"):
        os.mkdir(self.csv_folder+"/tmp")
      csv_file = time.strftime('%Y%m%d%H%M%S')
      with open(self.csv_folder+"/tmp/" + csv_file + ".csv", 'wb') as importcsvfile:
        writer = csv.writer(importcsvfile,delimiter='|')
        writer.writerows(bulk_insert_row)
      self.logger.info("File %s written" % (self.csv_folder+"/tmp/" + csv_file + ".csv"))	    
      with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
        dr = csv.DictReader(infile, delimiter='|')
        to_db = [(di['nrs_environment_id'], di['nrs_node_id'], di['nrs_datastream_id'], di['sample_no'], di['value_at'], di['datetime_at'], di['updated']) for di in dr]
      with open(self.csv_folder+"/tmp/" + csv_file + ".csv",'rb') as infile:
        dr = csv.DictReader(infile, delimiter='|')        
        del_db = [(dd['nrs_datastream_id'], dd['datetime_at']) for dd in dr]
      db_conn = sqlite3.connect(settings.database)
      # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
      db_cur = db_conn.cursor()
      dd_dict = {}
      for delitem in del_db:
        if delitem[0] not in dd_dict:
          dd_dict[delitem[0]] = { 'min':delitem[1] ,'max': delitem[1]}
        else:
          if dd_dict[delitem[0]]['min'] > delitem[1]:
            dd_dict[delitem[0]]['min'] = delitem[1]
          if dd_dict[delitem[0]]['max'] < delitem[1]:
            dd_dict[delitem[0]]['max'] = delitem[1]
      sTmpWhere = "1<>1"
      for key, value in dd_dict.items():
        sTmpWhere = sTmpWhere + " OR ( nrs_datastream_id=%s AND datetime_at >= '%s' AND datetime_at <= '%s' )" % (key,value['min'],value['max'])
      sDeleteQuery = """DELETE FROM nrs_datapoint WHERE %s """ % sTmpWhere
      try:
        db_cur.execute(sDeleteQuery)
        sInsertQuery = """INSERT INTO nrs_datapoint ( 
                             nrs_environment_id, 
                             nrs_node_id, 
                             nrs_datastream_id, 
                             sample_no, 
                             value_at, 
                             datetime_at, 
                             updated
                          ) VALUES (?, ?, ?, ?, ?, ?, ?);"""
        db_cur.executemany(sInsertQuery, to_db)
        db_conn.commit()
      except MySQLdb.Error, e:
        self.logger.error("An error has been passed. %s" %e  )
        db_conn.rollback()    
      db_conn.close()
      saved_folder = time.strftime('%Y%m%d%H%M')
      if not os.path.exists(self.csv_folder+"/"+saved_folder):
        os.mkdir(self.csv_folder+"/"+saved_folder)
      shutil.move(self.import_file_path,self.csv_folder+"/"+saved_folder)
      self.logger.info("GibeToNrs moved file %s into %s" % (self.import_file_path,saved_folder) )
      db_conn = sqlite3.connect(settings.database)
      # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
      db_cur = db_conn.cursor()
      sQuery = """INSERT INTO nrs_csv_client (folder,file_name,sha256sum,noitems,saved_folder) VALUES ('%s','%s','%s',%d,'%s')""" % (self.csv_folder,os.path.basename(self.import_file_path),sha256sum,i,saved_folder)
      try:
        db_cur.execute(sQuery)
        db_conn.commit()
      except MySQLdb.Error, e:
        self.logger.error("An error has been passed. %s" %e  )
        db_conn.rollback()    
      db_conn.close()


  def check_env_uid(self):
    return_value = 0
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    sQuery = """SELECT id FROM nrs_environment WHERE environment_uid = '%s' """ % self.env_uid
    retVal= db_cur.execute(sQuery)
    row = retVal.fetchone()  
    if row:
      return_value = row[0]
      #self.logger.info("Fetched Environment with ID %d and UID %s" % (return_value,self.env_uid))
    else:
      sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
      sQuery = """INSERT INTO nrs_environment (title,environment_uid,status,updated) VALUES ('%s','%s',%d,'%s')""" % (self.env_uid,self.env_uid,4,sUpdated)
      retVal= db_cur.execute(sQuery)
      db_conn.commit()
      sQuery = """SELECT id FROM nrs_environment WHERE environment_uid = '%s' """ % self.env_uid
      retVal= db_cur.execute(sQuery)
      row = retVal.fetchone()  
      if row:
        return_value = row[0]
        #self.logger.info("Inserted Environment with ID %d and UID %s" % (return_value,self.env_uid))
    db_conn.close()
    return return_value


  def check_node_uid(self,nrs_environment_id, node_uid):
    return_value = 0
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    sQuery = """SELECT id FROM nrs_node WHERE nrs_environment_id = %d AND node_uid='%s' """ % (nrs_environment_id, node_uid)
    retVal= db_cur.execute(sQuery)
    row = retVal.fetchone()  
    if row:
      return_value = row[0]
    else:
      sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
      sQuery = """INSERT INTO nrs_node (title,nrs_environment_id,node_uid,status,updated) VALUES ('%s',%d,'%s',%d,'%s')""" % (node_uid,nrs_environment_id,node_uid,4,sUpdated)
      retVal= db_cur.execute(sQuery)
      db_conn.commit()
      sQuery = """SELECT id FROM nrs_node WHERE nrs_environment_id = %d AND node_uid='%s' """ % (nrs_environment_id, node_uid)
      retVal= db_cur.execute(sQuery)
      row = retVal.fetchone()  
      if row:
        return_value = row[0]
    db_conn.close()
    return return_value

  def check_datastream_uid(self, nrs_environment_id,nrs_node_id, f_lambda, isensor, prefix, node_uid):
    datastream_uid = "%s%09.03f" % (prefix, f_lambda)
    datastream_max_uid = "%s%09.03f" % (prefix, f_lambda+1.0)
    datastream_min_uid = "%s%09.03f" % (prefix, f_lambda-1.0)
    datastream_title = "%s%s%s%02d" % (self.env_uid ,node_uid,prefix,isensor)
    ds_uid = self.env_uid + node_uid + datastream_uid
    ds_max_uid = self.env_uid + node_uid + datastream_max_uid
    ds_min_uid = self.env_uid + node_uid + datastream_min_uid
    return_value = 0
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    sQuery = """SELECT id FROM nrs_datastream WHERE nrs_environment_id = %d AND nrs_node_id =%d AND datastream_uid>='%s' AND datastream_uid<='%s'""" % (nrs_environment_id,nrs_node_id, ds_min_uid,ds_max_uid)
    #self.logger.info("Here the Query %s" % sQuery)
    retVal= db_cur.execute(sQuery)
    row = retVal.fetchone()  
    if row:
      return_value = row[0]
      #self.logger.info("Fetched Datastream with ID %d and UID %s" % (return_value,ds_uid))
    else:
      sUpdated = time.strftime('%Y-%m-%d %H:%M:%S')
      sQuery = """INSERT INTO nrs_datastream (title,nrs_environment_id,nrs_node_id,datastream_uid,updated,factor_title) VALUES ('%s',%d,%d,'%s','%s','%f')""" % (datastream_title,nrs_environment_id,nrs_node_id,ds_uid,sUpdated,f_lambda)
      retVal= db_cur.execute(sQuery)
      db_conn.commit()
      sQuery = """SELECT id FROM nrs_datastream WHERE nrs_environment_id = %d AND nrs_node_id =%d AND datastream_uid='%s' """ % (nrs_environment_id,nrs_node_id, ds_uid)
      retVal= db_cur.execute(sQuery)
      row = retVal.fetchone()  
      if row:
        return_value = row[0]
        #self.logger.info("Inserted Datastream with ID %d and UID %s" % (return_value,ds_uid))
    db_conn.close()
    return return_value

  def sql_execute(self, sQuery):
    retVal = 0
    db_conn = sqlite3.connect(settings.database)
    # db_conn = MySQLdb.connect(host=settings.hostname, port=settings.portnumber, user=settings.username,passwd=settings.password,db=settings.database)
    db_cur = db_conn.cursor()
    try:
      retVal = db_cur.execute(sQuery)
      db_conn.commit()
    except MySQLdb.Error, e:
      self.logger.error("An error has been passed. %s %s" % (e, sQuery) )
      db_conn.rollback() 
    db_conn.close()
    return retVal

  def sha256Checksum(self,filePath):
    fh = open(filePath, 'rb')
    m = hashlib.sha256()
    while True:
      data = fh.read(8192)
      if not data:
          break
      m.update(data)
    return m.hexdigest()
