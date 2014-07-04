import socket
import sys
import time

def alert(msg):
    print >>sys.stderr, msg
    #sys.exit(1)

class SCPICli():
    PORT=3500
    PORT2READ=3365
    HOST="10.0.0.10"
    def __init__(self,host=HOST,port=PORT, port2read=PORT2READ):
        self.host = host
        self.port = port
        self.port2read = port2read
        self.status = -1
        self.iden = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket2read = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S_000=chr(0)+chr(0)+chr(0)
        self.S_000F=self.S_000+chr(70)
        self.S_0006=self.S_000+chr(6)
        self.S_0004=self.S_000+chr(4)
        self.S_000E=self.S_000+chr(69)
        self.S_000NEWLINE=self.S_000+chr(10)
        self.S_000SEMICOLON=self.S_000+chr(59)
        self.ACK_OK = ":ACK"
        self.ACK = ":ACK:"
        self.NACK = ":NACK:"
        
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            time.sleep(0.5)
            return True
        except Exception, e:
            alert('something\'s wrong with %s:%d. Exception type is %s' % (self.host, self.port, `e`))
            return False
        
    def connect2read(self):
        self.socket2read = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)
        try:
            self.socket2read.connect((self.host, self.port2read)) 
            time.sleep(1)
            return True
        except Exception, e:
            alert('something\'s wrong with %s:%d. Exception type is %s' % (self.host, self.port2read, `e`))
            return False
    
    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def close2read(self):
        self.socket2read.shutdown(socket.SHUT_RDWR)
        self.socket2read.close()
        
    def sendCmd(self,cmd):
        pre_cmd = self.S_000+chr(len(cmd))
        self.socket.send(pre_cmd)
        retBytes = self.socket.send(cmd)
        return retBytes
        
    def recvData(self):
        retMsg = ''
        bytes_recd = 0
        chunks = []
        try:
            data = self.socket.recv(1024)
            if data == '':
                raise RuntimeError("recvData socket connection broken")
            bytes_recd = bytes_recd + len(data)
            chunks.append(data)
            while len(data) > 0:
              data = self.socket.recv(1024)
              bytes_recd = bytes_recd + len(data)
              chunks.append(data)
            return retMsg.join(chunks)
        except socket.timeout:
            return retMsg.join(chunks)
    
    def recv2readData(self):
        retMsg = ''
        bytes_recd = 0
        chunks = []
        try:
            data = self.socket2read.recv(1024)
            if data == '':
                data = data
            bytes_recd = bytes_recd + len(data)
            chunks.append(data)
            while len(data) > 0:
              data = self.socket2read.recv(1024)
              bytes_recd = bytes_recd + len(data)
              chunks.append(data)
            return retMsg.join(chunks)
        except socket.timeout:
            return retMsg.join(chunks)
        
    def recv2readDataMax(self,maxLen=1000):
        retMsg = ''
        bytes_recd = 0
        chunks = []
        try:
            data = self.socket2read.recv(1024)
            if data == '':
                raise RuntimeError("recv2readDataMax socket2read connection broken")
            bytes_recd = bytes_recd + len(data)
            chunks.append(data)
            while bytes_recd < maxLen:
              data = self.socket2read.recv(1024)
              bytes_recd = bytes_recd + len(data)
              chunks.append(data)
            return retMsg.join(chunks)
        except socket.timeout:
            return retMsg.join(chunks)
    
    def getIDEN(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":IDEN?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                self.iden = self.parseACK(retData)
                returnVal = self.iden
            self.close()
        return returnVal   
         
    def parseACK(self,retData):
        ret=''
        if len(retData) > 4 and self.ACK in retData[4:]:
            ret = retData[9:]
        elif len(retData) > 4 and self.NACK in retData[4:]:
            error = retData[10:]                
        elif len(retData) > 4 and self.ACK_OK in retData[4:]:
            ret = 'OK'
        return ret
    
    def parseWAVE(self,retData):
        ret=[]
        if len(retData) > 4 and self.ACK in retData[4:]:
            ret = retData[9:].split(',')
        elif len(retData) > 4 and self.NACK in retData[4:]:
            error = retData[10:]                
        elif len(retData) > 4 and self.ACK_OK in retData[4:]:
            ret = []
        return ret
    
    def parseDATA(self,retData,maxLen=0):
        ret = []
        retVal = self.parseACK(retData)
        if retVal == 'OK':
            if maxLen==0:
                retData = self.recv2readData()
            else:
                retData = self.recv2readDataMax(maxLen)
            if retData == None:
                ret = []
            else:
                if len(retData) > 4 and self.S_000 in retData[4:]:
                    read = 0
                    while read < len(retData):
                        length = int(retData[read:read+4].encode('hex'), 16)
                        item = retData[read+4:length+read+4]
                        read = read + length + 4
                        if item:
                            cols = item.split(":",2)
                            datearray = cols[0].split('.')
                            sDate = "%s/%s/%s" % (datearray[2],datearray[1],datearray[0])
                            timearray = cols[1].split('.')
                            sTime = "%s:%s:%s" % (timearray[0],timearray[1],timearray[2])
                            ss = cols[2].split(':')
                            sValues = ''
                            for si in ss:
                                if len(si) > 0:
                                    if sValues == '':
                                        sValues = si
                                    else:
                                        sValues = sValues + ',' + si
                                #else:
                                #    if sValues == '':
                                #        sValues = "0.0"
                                #    else:
                                #        sValues = sValues + ',' +"0.0"
                            if len(sValues) > 0:
                                sValues = sValues.replace(',','\t')
                                sValues = sValues.replace('.',',')
                                ret.append("%s\t%s\t%s\n" % (sDate,sTime,sValues) )
                else:
                    ret = []
        return ret
        
    
    
    def getSTAT(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":STAT?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                returnVal = self.parseSTAT(retData) 
            self.close()
        return returnVal   
         
    def parseSTAT(self,retData):
        ret=''
        if len(retData) > 4 and self.ACK in retData[4:]:
            ret = retData[9:]
        elif len(retData) > 4 and self.NACK in retData[4:]:
            error = retData[10:]
        self.status = -1
        if ret == '0':
            self.status = 0
            return "0 Error"
        if ret == '1':
            self.status = 1
            return "1 Ready"
        if ret == '2':
            self.status = 2
            return "2 Free Acquisition"
        if ret == '3':
            self.status = 3
            return "3 Continuous Acquisition"
        if ret == '4':
            self.status = 4
            return "4 Scheduled Acquisition"
        if ret == '5':
            self.status = 5
            return "5 Warming Up"
        return "ND"
    
    
    #:SYSTem:DATE?
    def getDATE(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":SYST:DATE?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                returnVal = self.parseACK(retData) 
            self.close()
        return returnVal  


    #:SYST:IPAD:192.168.2.100:255.255.255.0:0.0.0.0 
    def setIPAD(self,sIPAD,sSM,sGW):
        iRet = None
        if self.connect():
            iRet = self.sendCmd(":SYST:IPAD:%s:%s:%s" % (sIPAD,sSM,sGW))
            self.close()
        return iRet   


    #:SYST:TIME?
    def getTIME(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":SYST:TIME?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                returnVal = self.parseACK(retData) 
            self.close()
        return returnVal   
    
    
    #:ACQU:SCHE:PERI?
    def getPERI(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":ACQU:SCHE:PERI?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                returnVal = self.parseACK(retData) 
            self.close()
        return returnVal   
    
    #:ACQU:SCHE:SAMP?
    def getSAMP(self):
        returnVal = None
        if self.connect():
            iRet = self.sendCmd(":ACQU:SCHE:SAMP?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = retdata
            else:
                returnVal = self.parseACK(retData)
            self.close()
        return returnVal
    
    #:MEMO:LIST:DIRE?
    def getDIRE(self):
        returnVal = []
        if self.connect():
            iRet = self.sendCmd(":MEMO:LIST:DIRE?")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = []
            else:
                ret = self.parseACK(retData)
                returnVal = ret.split(";")
            self.close()
        return returnVal
        
    #:ACQU:WAVE:CHAN:1?
    def getWAVE(self,channel):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:WAVE:CHAN:%d?" % channel)
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                ret = self.parseACK(retData)
                sValues = ret.replace(',','\t')
                returnVal = sValues.replace('.',',')
            self.close()
        return returnVal
    

    #:ACQU:SCHE:SAMP:NNNN
    def setSAMP(self,sNN):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:SCHE:SAMP:%s" % sNN)
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal
    
    #:ACQU:SCHE:PERI:HH:MM:SS
    def setPERI(self,sHHMMSS):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:SCHE:PERI:%s" % sHHMMSS)
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal    
  
    #:MEMO:DELE
    def deleteMEMO(self):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":MEMO:DELE")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal  
  
    #:ACQU:WAVE:CONT:STAR 
    def startCONT(self):
        returnVal = []
        if self.connect():
            iRet = self.sendCmd(":ACQU:WAVE:CONT:STAR")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = []
            else:
                 if self.connect2read():
                    returnVal = self.parseDATA(retData,1000)
                    self.close2read()
            self.close()
        return returnVal
  
    #:ACQU:SCHE:STAR
    def startSCHEDULE(self):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:SCHE:STAR")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal  


    #:ACQU:STAR
    def startACQU(self):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:STAR")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal
    
    
    #:RECA
    def reca(self):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":RECA")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal
    
    #:ACQU:WAVE:CHAN:1? 
    def getWAVE(self, sChan):
        returnVal = []
        if self.connect():
            iRet = self.sendCmd(":ACQU:WAVE:CHAN:%s?" % sChan)
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = []
            else:
                returnVal = self.parseWAVE(retData)
            self.close()
        return returnVal


    #:ACQU:STOP
    def stopACQU(self):
        returnVal = ""
        if self.connect():
            iRet = self.sendCmd(":ACQU:STOP")
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = ""
            else:
                returnVal = self.parseACK(retData)  
            self.close()
        return returnVal
    
    #:MEMO:RECA:DATA:20120602?
    def getDATA(self, sYYYYMMDD):
        returnVal = []
        if self.connect():
            iRet = self.sendCmd(":MEMO:RECA:DATA:%s?" % sYYYYMMDD)
            retData = None
            if iRet > 0:
                retData = self.recvData()
            if retData == None:
                returnVal = []
            else:
                if self.connect2read():
                    returnVal = self.parseDATA(retData)
                    self.close2read()
            self.close()
        return returnVal
    
if __name__ == '__main__':
    dev = SCPICli("192.107.91.76",3500)
    res=dev.getIDEN()
    res=dev.getIDEN()
    res=dev.getSTAT()
    if not res.startswith("1"):
        res=dev.stopACQU()
    res=dev.getPERI()
    res=dev.getSAMP()
    res=dev.getDIRE()
    res=dev.getSTAT()
    res=dev.getTIME()
    res=dev.getDATE()
    #if not res.startswith("4"):
    #    res=dev.startSCHEDULE()
    res=dev.getDATA("20121128")
    print res