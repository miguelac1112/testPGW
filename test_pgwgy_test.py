#!/usr/bin/env python

import datetime
import time
import sys
import codecs

decode_hex = codecs.getdecoder("hex_codec")
sys.path.append("..")

from libDiameter import *
from libGxGy import *

def MGyI2(session_id,o_host,state,msisdn,imsi,apn,ratinggroup):
    
    CCR_avps=[]
    CCR_avps.append(encodeAVP("Session-Id", session_id))
    CCR_avps.append(encodeAVP("Auth-Application-Id",DIAMETER_GY_APPLICATION_ID))
    CCR_avps.append(encodeAVP("Origin-Host",o_host))
    CCR_avps.append(encodeAVP("Origin-Realm",GY_ORIGIN_REALM))
    CCR_avps.append(encodeAVP("Destination-Realm",GY_DESTINATION_REALM))
    CCR_avps.append(encodeAVP("Service-Context-Id",GY_SERVICE_CONTEXT_ID))
    CCR_avps.append(encodeAVP("CC-Request-Type",1))                                   #-- 1: INITIAL_REQUEST
    CCR_avps.append(encodeAVP("CC-Request-Number",0))                                 #-- 0: First CCR, sequence starts in 1 for CCR-U/T
    CCR_avps.append(encodeAVP("User-Name",GY_USER_NAME))
    CCR_avps.append(encodeAVP("Origin-State-Id",state))
    CCR_avps.append(encodeAVP("Event-Timestamp", int(time.time()) ))    
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",0),encodeAVP("Subscription-Id-Data",msisdn)]))
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",1),encodeAVP("Subscription-Id-Data",imsi  )]))
    CCR_avps.append(encodeAVP("Multiple-Services-Indicator",1))                       #-- 1: Always MSCC enabled
    #-- User-Equipment-Info
    CCR_avps.append("000001ca4000002c000001cb4000000c00000000000001cc4000001833353136323631313535383933363130")
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",0))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))
    CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","08-44090000465000004650"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC","71610"))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC","71610"))
    CCR_avps.append("000000178000000e000028af0a000000")
    CCR_avps.append("0000001680000019000028af8217f601378d17f6010848b8fc000000")
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","06"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","100.126.21.176"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.165.224.41"))  
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","190.119.6.25"))  
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","190.113.204.20"))  
#    CCR_avps.append(encodeAVP("Service-Information",[encodeAVP("PS-Information",[encodeAVP("Called-Station-Id",apn),encodeAVP("3GPP-RAT-Type","01"),encodeAVP("3GPP-SGSN-MCC-MNC","716010"),encodeAVP("3GPP-GGSN-Address","10.10.10.10"),encodeAVP("3GPP-Charging-Id",0)])]))
#    CCR_avps.append(encodeAVP("Service-Information",[encodeAVP("PS-Information",[encodeAVP("Called-Station-Id",apn),encodeAVP("3GPP-RAT-Type","01"),encodeAVP("3GPP-GGSN-Address","10.10.10.10"),encodeAVP("3GPP-Charging-Id",0)])]))
#    CCR_avps.append(encodeAVP("Route-Record",o_host))
    
    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)    
    
    return msg

def MGyU2(session_id,o_host,state,msisdn,imsi,apn,ratinggroup,usedquota,requestnumber):
    # Modifiqué esta función para aceptar 'requestnumber' como parámetro
    CCR_avps=[]
    CCR_avps.append(encodeAVP("Session-Id", session_id))
    CCR_avps.append(encodeAVP("Auth-Application-Id", DIAMETER_GY_APPLICATION_ID))
    CCR_avps.append(encodeAVP("Origin-Host", o_host))
    CCR_avps.append(encodeAVP("Destination-Host", GY_DESTINATION_HOST))
    CCR_avps.append(encodeAVP("Origin-Realm", GY_ORIGIN_REALM))
    CCR_avps.append(encodeAVP("Destination-Realm", GY_DESTINATION_REALM))
    CCR_avps.append(encodeAVP("Service-Context-Id", GY_SERVICE_CONTEXT_ID))
    CCR_avps.append(encodeAVP("CC-Request-Type", 2))  # 2: UPDATE_REQUEST
    CCR_avps.append(encodeAVP("CC-Request-Number", requestnumber))  # Usamos 'requestnumber' aquí
    CCR_avps.append(encodeAVP("User-Name", GY_USER_NAME))
    CCR_avps.append(encodeAVP("Origin-State-Id", state))
    CCR_avps.append(encodeAVP("Event-Timestamp", int(time.time())))
    CCR_avps.append(encodeAVP("Subscription-Id", [
        encodeAVP("Subscription-Id-Type", 0),
        encodeAVP("Subscription-Id-Data", msisdn)
    ]))
    CCR_avps.append(encodeAVP("Subscription-Id", [
        encodeAVP("Subscription-Id-Type", 1),
        encodeAVP("Subscription-Id-Data", imsi)
    ]))
    CCR_avps.append(encodeAVP("Multiple-Services-Indicator", 1))
    if requestnumber==1:
        CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Requested-Service-Unit",""),encodeAVP("Rating-Group",ratinggroup)]))
    else:
        CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Requested-Service-Unit",""),encodeAVP("Used-Service-Unit",[encodeAVP("CC-Total-Octets",usedquota)]),encodeAVP("Rating-Group",ratinggroup),encodeAVP("Reporting-Reason",3)]))
    CCR_avps.append("000001ca4000002c000001cb4000000c00000000000001cc4000001833353136323631313535383933363130")
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",0))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))
    CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","08-44090000465000004650"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC","71600"))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC","71600"))
    CCR_avps.append("000000178000000e000028af0a000000")
    CCR_avps.append("0000001680000019000028af8217f601378d17f6010848b8fc000000")
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","06"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","100.126.21.176"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.165.224.41"))  
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","190.119.6.25"))  
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","190.113.204.20"))  

    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)

    return msg

def MGyT2(session_id,o_host,state,msisdn,imsi,apn,usedquota):
    # From the trace taken on 2021/05/10, the AVPs structure of the CCR-I to send in
    # Telcel PERU network is:
    # 
    CCR_avps=[]
    CCR_avps.append(encodeAVP("Session-Id", session_id))
    CCR_avps.append(encodeAVP("Auth-Application-Id",DIAMETER_GY_APPLICATION_ID))
    CCR_avps.append(encodeAVP("Origin-Host",o_host))
    CCR_avps.append(encodeAVP("Destination-Host", GY_DESTINATION_HOST))
    CCR_avps.append(encodeAVP("Origin-Realm",GY_ORIGIN_REALM))
    CCR_avps.append(encodeAVP("Destination-Realm",GY_DESTINATION_REALM))
    CCR_avps.append(encodeAVP("Service-Context-Id",GY_SERVICE_CONTEXT_ID))
    CCR_avps.append(encodeAVP("CC-Request-Type",3))                                   #-- 1: INITIAL_REQUEST
    CCR_avps.append(encodeAVP("CC-Request-Number",2))                                 #-- 0: First CCR, sequence starts in 1 for CCR-U/T
    CCR_avps.append(encodeAVP("User-Name",GY_USER_NAME))
    CCR_avps.append(encodeAVP("Origin-State-Id",state))
    CCR_avps.append(encodeAVP("Event-Timestamp", int(time.time()) ))    
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",0),encodeAVP("Subscription-Id-Data",msisdn)]))
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",1),encodeAVP("Subscription-Id-Data",imsi  )]))
    CCR_avps.append(encodeAVP("Termination-Cause",1))
    CCR_avps.append(encodeAVP("Multiple-Services-Indicator",1))                       #-- 1: Always MSCC enabled
    #for i in range(len(ratinggroup)):
    #   CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Used-Service-Unit",[encodeAVP("CC-Total-Octets",usedquota[i])]),encodeAVP("Rating-Group",ratinggroup[i]),encodeAVP("Reporting-Reason",2)]))
    for rg, quota in usedquota.items():
        CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Used-Service-Unit", [encodeAVP("CC-Total-Octets", quota)]),encodeAVP("Rating-Group", rg),encodeAVP("Reporting-Reason", 2),]))
    #-- User-Equipment-Info
    CCR_avps.append("000001ca4000002c000001cb4000000c00000000000001cc4000001833353136323631313535383933363130")
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",0))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))
    CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","08-44090000465000004650"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC","71610"))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC","71610"))
    CCR_avps.append("000000178000000e000028af0a000000")
    CCR_avps.append("0000001680000019000028af8217f601378d17f6010848b8fc000000")
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","06"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","100.126.21.176"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.165.224.41"))  
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","190.119.6.25"))  
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","190.113.204.20"))  
    CCR_avps.append(encodeAVP("Route-Record",o_host))
    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)    
    
    return msg

if __name__ == '__main__':
    LoadDictionary("dictDiameter.xml")
    HOST="10.20.12.28"
    PORT=3868
    O_HOST = "testpgw01.gy.epc.mnc000.mcc716.3gppnetwork.org"
    SESSION_ID=create_Session_Id(O_HOST)
    #IMSI="716001000000124"
    IMSI="716001000000141"
    #MSISDN="51914389110"
    MSISDN="51987654330"
    STATE_ID=192837465
    APN="mvno.pe"
    ##deben ser iguales RG y RG_ITERATIONS!!
    RG = [1, 25]  # Lista de Rating Groups
    RG_ITERATIONS = {1: 2, 25: 1}  # Cantidad de iteraciones para cada RG
    USED_UNITS = {rg: 0 for rg in RG}  # Diccionario para manejar unidades utilizadas por RG
    CCTO_AVP = 0 #Unidades entregadas por el OCS
    MSG_SIZE=4096

    # Establecemos REQUEST_NUMBER inicial
    REQUEST_NUMBER = 1

    Conn=Connect(HOST, PORT)
    
    # Envío de CER y recepción de CEA
    msg=CER(O_HOST, "client.test", HOST, 2011)
    msg2=decode_hex(msg)[0]
    #print('CER enviado ----------------------------------------------------')
    #print(msg2)
    Conn.send(msg2)
    received=Conn.recv(MSG_SIZE)
    #print('CER recibido ----------------------------------------------------')
    #print(received)

    SLA=HDRItem()
    stripHdr(SLA, received.hex())
    avps=splitMsgAVPs(SLA.msg)
    print('----------------------------------------------------')
    cmd=dictCOMMANDcode2name(SLA.flags, SLA.cmd)
    print(cmd)
    print('----------------------------------------------------')

    for avp in avps:
        #print("coded AVP: ", avp)
        print("Decoded AVP: ", decodeAVP(avp))
    
    time.sleep(2)

    #---------------------
    #--- CCR-Initial    ---
    #---------------------     
    msg=MGyI2(SESSION_ID, O_HOST, STATE_ID, MSISDN, IMSI, APN, RG)
    msg2 = decode_hex(msg)[0]
    #print('----------------------------------------------------')
    #print(f'El pgw envia como initial: {msg2}')
    #print('----------------------------------------------------')
    Conn.send(msg2)
    received = Conn.recv(MSG_SIZE)
    #print(f'Recibimos: {received}')
    
    GyCCA=HDRItem()
    stripHdr(GyCCA, received.hex())
    avps=splitMsgAVPs(GyCCA.msg)
    cmd=dictCOMMANDcode2name(GyCCA.flags, GyCCA.cmd)
    print('----------------------------------------------------')
    print(f'{cmd}')
   
    print("-------------------------------------------------------------------------------------------------------------------")
    for avp in avps:
        #print("coded AVP: ", avp)
        print("Decoded AVP: ", decodeAVP(avp))
    
    CLRC_avp = findAVP("Result-Code", avps)
    if CLRC_avp == 2001:
        print("CCR-I correct, let's continue")
    else:
        print("Command Level Result-Code: ", CLRC_avp)
        print("Ending")
        Conn.close()
        sys.exit(1)
   
    time.sleep(3)

    #---------------------
    #--- CCR-Update    ---
    #---------------------
    for rg, iterations in RG_ITERATIONS.items():  # Iterar sobre cada RG y sus iteraciones
        REQUEST_NUMBER=1
        CCTO_AVP = 0
        for i in range(iterations):
            print(f"--- Iteración {i + 1} de {iterations} para Rating Group: {rg} ---")
            msg = MGyU2(SESSION_ID, O_HOST, STATE_ID, MSISDN, IMSI, APN, rg, CCTO_AVP, REQUEST_NUMBER)
            msg2 = decode_hex(msg)[0]
            Conn.send(msg2)
            received = Conn.recv(MSG_SIZE)
            
            GyCCA = HDRItem()
            stripHdr(GyCCA, received.hex())
            avps = splitMsgAVPs(GyCCA.msg)
            cmd = dictCOMMANDcode2name(GyCCA.flags, GyCCA.cmd)
            print(f'{cmd}')

            for avp in avps:
                print("Decoded AVP: ", decodeAVP(avp))
            
            CLRC_avp = findAVP("Result-Code", avps)
            if CLRC_avp == 2001:
                print(f"CCR-U correct for RG: {rg}, let's continue")
                mscc_avp = findAVP("Multiple-Services-Credit-Control", avps)
                mscc_rc = findAVP("Result-Code", mscc_avp)
                if mscc_rc == 2001:
                    gsu_avp = findAVP("Granted-Service-Unit", mscc_avp)
                    CCTO_AVP = findAVP("CC-Total-Octets", gsu_avp)
                    print(f"Granted Units for RG {rg}: {CCTO_AVP}")
                    USED_UNITS[rg] += CCTO_AVP  # Actualizar las unidades utilizadas para este RG
                    print(f"Current Units for RG {rg}: {USED_UNITS[rg]}")
                elif mscc_rc == 4011:
                    print(f"RG: {rg} configured as free of charge with no supervision")
                elif mscc_rc == 5031:
                    print(f"RG: {rg} configured as blocked")
                elif mscc_rc == 4012:
                    print(f"RG: {rg} no balance for this")
                else:
                    print(f"Unexpected result code for RG {rg}: {mscc_rc}")
                    Conn.close()
                    sys.exit(1)
            else:
                print(f"Command Level Result-Code for RG {rg}: {CLRC_avp}")
                Conn.close()
                sys.exit(1)
            
            time.sleep(5)
            REQUEST_NUMBER += 1  # Incrementar el número de solicitud


    #---------------------
    #--- CCR-Terminate ---
    #---------------------
    msg = MGyT2(SESSION_ID, O_HOST, STATE_ID, MSISDN, IMSI, APN, USED_UNITS)
    msg2 = decode_hex(msg)[0]
    #print('----------------------------------------------------')
    #print(f'El pgw envia como terminated: {msg2}')
    #print('----------------------------------------------------')
    Conn.send(msg2)
    received = Conn.recv(MSG_SIZE)
    #print(f'Recibimos: {received}')
    
    GyCCA=HDRItem()
    stripHdr(GyCCA, received.hex())
    avps=splitMsgAVPs(GyCCA.msg)
    cmd=dictCOMMANDcode2name(GyCCA.flags, GyCCA.cmd)
    print('----------------------------------------------------')
    print(f'{cmd}')
    print("-------------------------------------------------------------------------------------------------------------------")
    for avp in avps:
        #print("coded AVP: ", avp)
        print("Decoded AVP: ", decodeAVP(avp))
        
    Conn.close()