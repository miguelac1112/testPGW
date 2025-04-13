#!/usr/bin/env python

# definitions for Gx and Gy CCRs for Claro Peru and Claro Chile
import datetime
import time
import sys

# needed for the classes defined there.
sys.path.append(".")
from libDiameter import *

#-- DPR constants for Disconnect-Cause
DPR_REBOOTING                  = 0
DPR_BUSY                       = 1
DPR_DO_NOT_WANT_TO_TALK_TO_YOU = 2

DIAMETER_GY_APPLICATION_ID = 4

GY_ORIGIN_REALM       = "epc.mnc00.mcc716.3gppnetwork.org"
GY_DESTINATION_HOST   = "ocs.mnc00.mcc716.3gppnetwork.org"
GY_DESTINATION_REALM  = "epc.mnc00.mcc716.3gppnetwork.org"
GY_SERVICE_CONTEXT_ID = "vendor@3gpp.org"
GY_USER_NAME          = "test.com.pe"
MCC_MNC = "71600"

#------------------------------------------------------
#-- CER: Capabilities-Exchange-Request definition    --
#------------------------------------------------------
def CER(o_host,o_realm,o_ip,o_vendor):
    # o_host   => Origin-Host
    # o_realm  => Origin-Realm
    # o_ip     => Host-IP-Address
    # o_vendor => Vendor-Id
    
    #--- AVPs for CER ---
    CER_avps=[]
    CER_avps.append(encodeAVP("Origin-Host",o_host))
    CER_avps.append(encodeAVP("Origin-Realm",o_realm))
    CER_avps.append(encodeAVP("Host-IP-Address",o_ip))
    CER_avps.append(encodeAVP("Vendor-Id",o_vendor))
    #-- AVP() Product-Name
    CER_avps.append("0000010d0000000b53505300")
    #-- AVP() Inband-Security-Id
    CER_avps.append("0000012b4000000c00000000")
    #-- AVP() Vendor-Specific-Application-Id
    CER_avps.append("00000104400000200000010a4000000c000028af000001024000000c01000016")
    
    CER=HDRItem()
    CER.appId=0
    CER.flags=0x80
    CER.cmd=dictCOMMANDname2code('Capabilities-Exchange')
    initializeHops(CER)
    msg=createReq(CER,CER_avps)
    return msg

#------------------------------------------------------
#-- DWR: Diameter-Watchdog-Request definition        --
#------------------------------------------------------
def DWR(o_host,o_realm):
    # o_host   => Origin-Host
    # o_realm  => Origin-Realm
    
    #--- AVPs for DWR ---
    DWR_avps=[]
    DWR_avps.append(encodeAVP("Origin-Host",o_host))
    DWR_avps.append(encodeAVP("Origin-Realm",o_realm))
    
    DWR=HDRItem()
    DWR.appId=0
    DWR.flags=0x80
    DWR.cmd=dictCOMMANDname2code('Device-Watchdog')
    initializeHops(DWR)
    msg=createReq(DWR,DWR_avps)
    return msg

#------------------------------------------------------
#-- DPR: Disconnect-Peer-Request definition          --
#------------------------------------------------------
def DPR(o_host,o_realm):
    # o_host   => Origin-Host
    # o_realm  => Origin-Realm
    
    #--- AVPs for DPR ---
    DPR_avps=[]
    DPR_avps.append(encodeAVP("Origin-Host",o_host))
    DPR_avps.append(encodeAVP("Origin-Realm",o_realm))
    #-- Disconnect-Cause:
    #--      0: REBOOTING
    #--      1: BUSY
    #--      2: DO_NOT_WANT_TO_TALK_TO_YOU
    DPR_avps.append(encodeAVP("Disconnect-Cause",DPR_DO_NOT_WANT_TO_TALK_TO_YOU))
    
    DPR=HDRItem()
    DPR.appId=0
    DPR.flags=0x80
    DPR.cmd=dictCOMMANDname2code('Disconnect-Peer')
    initializeHops(DPR)
    msg=createReq(DPR,DPR_avps)
    return msg

#------------------------------------------------------
#-- PGyI: Gy CCR-I (Initial)                    --
#------------------------------------------------------
def PGyI(session_id,o_host,state,msisdn,imsi,apn):
    # Command Code                              -> always 272: Credit-Control -> from the dictionary
    # ApplicationId                             -> always   4: Diameter Credit Control Application (DCCA)
    # AVP: Session-Id(263)
    # AVP: Auth-Application-Id(258)
    # AVP: Origin-Host(264)
    # AVP: Origin-Realm(296)
    # AVP: Destination-Realm(283)
    # AVP: Service-Context-Id(461)              -
    # AVP: CC-Request-Type(416)                 -> always 1: INITIAL_REQUEST
    # AVP: CC-Request-Number(415)               -> always 0
    # AVP: User-Name(1)                         
    # AVP: Orgin-State-Id(278)
    # AVP: Event-Timestamp(55)
    # AVP: Subscriton-Id(443)                   -> Type 0: MSISDN
    # AVP: Subscriton-Id(443)                   -> Type 1: IMSI
    # AVP: Multiple-Service-Indicator(455)      -> always 1
    # AVP: User-Equipment-Info(458)
    # AVP: 3GPP-Charging-Id(2)
    # AVP: 3GPP-PDP-Type(3)
    # AVP: 3GPP-GPRS-Negotiated-QoS-Profile(5)
    # AVP: 3GPP-GGSN-MCC-MNC(9)
    # AVP: 3GPP-NSAPI(10)
    # AVP: Called-Station-Id(30)
    # AVP: 3GPP-Selection-Mode(12)
    # AVP: 3GPP-Charging-Characteristics(13)
    # AVP: 3GPP-SGSN-MCC-MCN(18)
    # AVP: 3GPP-MS-TimeZone(23)
    # AVP: 3GPP-User-Location-Info(22)
    # AVP: 3GPP-RAT-Type(21)
    # AVP: Framed-IP-Address(8)
    # AVP: 3GPP-CG-Address(4)
    # AVP: 3GPP-SGSN-Address(6)
    # AVP: 3GPP-GGSN-Address(7)
    # AVP: Route-Record(282)
    
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
    CCR_avps.append("000001ca0000002c000001cb0000000c00000000000001cc0000001833353630353730393035373531363031")
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",123454))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))    
    #-- CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","UTMS"))
    CCR_avps.append("0000000580000023000028af30382d343430393030303030343139303030303134376200")
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC",MCC_MNC))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC",MCC_MNC))
    #-- 3GPP-Timezone
    CCR_avps.append("000000178000000e000028af0a000000")
    #-- 3GPP-User-Location-Info
    CCR_avps.append("0000001680000019000028af8217f60135df17f601055931d7000000")
    #--                  00000016C0000017000028AF3731363130353633353136
    #--              0000001680000019000028af8217f60135df17f601055931d7000000
    #-- CCR_avps.append(encodeAVP("3GPP-User-Location-Info","71601563516"))
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","1004"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","10.56.38.128"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.128.65.81"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","200.108.101.81"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","200.108.101.192"))
    CCR_avps.append(encodeAVP("Route-Record",o_host))

    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)    
       
    return msg

#------------------------------------------------------
#-- PGyU: Gy CCR-U (Update)                     --
#------------------------------------------------------
def PGyU(session_id,o_host,state,msisdn,imsi,apn,ratinggroup,requestnumber,usedquota,reportingreason):
    # Command Code                              -> always 272: Credit-Control -> from the dictionary
    # ApplicationId                             -> always   4: Diameter Credit Control Application (DCCA)
    # AVP: Session-Id(263)
    # AVP: Auth-Application-Id(258)
    # AVP: Origin-Host(264)
    # AVP: Origin-Realm(296)
    # AVP: Destination-Realm(283)
    # AVP: Service-Context-Id(461)              
    # AVP: CC-Request-Type(416)                 -> always 2: UPDATE_REQUEST
    # AVP: CC-Request-Number(415)
    # AVP: Destination-Host
    # AVP: User-Name(1)                        
    # AVP: Orgin-State-Id(278)
    # AVP: Event-Timestamp(55)
    # AVP: Subscriton-Id(443)                   -> Type 0: MSISDN
    # AVP: Subscriton-Id(443)                   -> Type 1: IMSI
    # AVP: Multiple-Service-Indicator(455)      -> always 1
    # AVP: Multiple-Service-Credit-Control(456)
    #      AVP: Requested-Service-Unit(437)
    #      AVP: Used-Service-Unit(446)
    #      AVP: Rating-Group(432)
    #      AVP: 3GPP-Reporting-Reason(872)    
    # AVP: User-Equipment-Info(458)
    # AVP: 3GPP-Charging-Id(2)
    # AVP: 3GPP-PDP-Type(3)
    # AVP: 3GPP-GPRS-Negotiated-QoS-Profile(5)
    # AVP: 3GPP-GGSN-MCC-MNC(9)
    # AVP: 3GPP-NSAPI(10)
    # AVP: Called-Station-Id(30)
    # AVP: 3GPP-Selection-Mode(12)
    # AVP: 3GPP-Charging-Characteristics(13)
    # AVP: 3GPP-SGSN-MCC-MCN(18)
    # AVP: 3GPP-MS-TimeZone(23)
    # AVP: 3GPP-User-Location-Info(22)
    # AVP: 3GPP-RAT-Type(21)
    # AVP: Framed-IP-Address(8)
    # AVP: 3GPP-CG-Address(4)
    # AVP: 3GPP-SGSN-Address(6)
    # AVP: 3GPP-GGSN-Address(7)
    # AVP: Route-Record(282)
    
    CCR_avps=[]
    CCR_avps.append(encodeAVP("Session-Id", session_id))
    CCR_avps.append(encodeAVP("Auth-Application-Id",DIAMETER_GY_APPLICATION_ID))
    CCR_avps.append(encodeAVP("Origin-Host",o_host))
    CCR_avps.append(encodeAVP("Origin-Realm",GY_ORIGIN_REALM))
    CCR_avps.append(encodeAVP("Destination-Realm",GY_DESTINATION_REALM))
    CCR_avps.append(encodeAVP("Service-Context-Id",GY_SERVICE_CONTEXT_ID))
    CCR_avps.append(encodeAVP("CC-Request-Type",2))                                   #-- 2: UPDATE_REQUEST
    CCR_avps.append(encodeAVP("CC-Request-Number",requestnumber))        
    CCR_avps.append(encodeAVP("User-Name",GY_USER_NAME))
    CCR_avps.append(encodeAVP("Origin-State-Id",state))
    CCR_avps.append(encodeAVP("Event-Timestamp", int(time.time()) ))    
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",0),encodeAVP("Subscription-Id-Data",msisdn)]))
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",1),encodeAVP("Subscription-Id-Data",imsi  )]))
    CCR_avps.append(encodeAVP("Multiple-Services-Indicator",1))                       #-- 1: Always MSCC enabled
    if requestnumber==1:
        CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Requested-Service-Unit",""),encodeAVP("Rating-Group",ratinggroup)]))
    else:
        CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Requested-Service-Unit",""),encodeAVP("Used-Service-Unit",[encodeAVP("CC-Total-Octets",usedquota)]),encodeAVP("Rating-Group",ratinggroup),encodeAVP("Reporting-Reason",reportingreason)]))
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",123454))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))    
    #-- CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","UTMS"))
    CCR_avps.append("0000000580000023000028af30382d343430393030303030343139303030303134376200")
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC",MCC_MNC))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC",MCC_MNC))
    #-- 3GPP-Timezone
    CCR_avps.append("000000178000000e000028af0a000000")
    #-- 3GPP-User-Location-Info
    CCR_avps.append("0000001680000019000028af8217f60135df17f601055931d7000000")
    #--                  00000016C0000017000028AF3731363130353633353136
    #--              0000001680000019000028af8217f60135df17f601055931d7000000
    #-- CCR_avps.append(encodeAVP("3GPP-User-Location-Info","71600563516"))
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","1004"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","10.56.38.128"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.128.65.81"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","200.108.101.81"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","200.108.101.192"))
    CCR_avps.append(encodeAVP("Route-Record",o_host))

    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)    
       
    return msg

#------------------------------------------------------
#-- PGyT: Gy CCR-T (Terminate)                  --
#------------------------------------------------------
def PGyT(session_id,o_host,state,msisdn,imsi,apn,ratinggroup,requestnumber,usedquota):
    # Command Code                              -> always 272: Credit-Control -> from the dictionary
    # ApplicationId                             -> always   4: Diameter Credit Control Application (DCCA)
    # AVP: Session-Id(263)
    # AVP: Auth-Application-Id(258)
    # AVP: Origin-Host(264)
    # AVP: Origin-Realm(296)
    # AVP: Destination-Realm(283)
    # AVP: Service-Context-Id(461)              
    # AVP: CC-Request-Type(416)                 -> always 3: TERMINATION_REQUEST
    # AVP: CC-Request-Number(415)
    # AVP: Destination-Host
    # AVP: User-Name(1)                         
    # AVP: Orgin-State-Id(278)
    # AVP: Event-Timestamp(55)
    # AVP: Subscriton-Id(443)                   -> Type 0: MSISDN
    # AVP: Subscriton-Id(443)                   -> Type 1: IMSI
    # AVP: Termination-Cause(295)               -> always 1: DIAMETER_LOGOUT
    # AVP: Multiple-Service-Indicator(455)      -> always 1: MULTIPLE_SERVICES_SUPPORTED
    # AVP: Multiple-Service-Credit-Control(456)
    #      AVP: Used-Service-Unit(446)
    #      AVP: Rating-Group(432)
    #      AVP: 3GPP-Reporting-Reason(872)      -> always 2: FINAL
    # AVP: User-Equipment-Info(458)
    # AVP: 3GPP-Charging-Id(2)
    # AVP: 3GPP-PDP-Type(3)
    # AVP: 3GPP-GPRS-Negotiated-QoS-Profile(5)
    # AVP: 3GPP-GGSN-MCC-MNC(9)
    # AVP: 3GPP-NSAPI(10)
    # AVP: Called-Station-Id(30)
    # AVP: 3GPP-Selection-Mode(12)
    # AVP: 3GPP-Charging-Characteristics(13)
    # AVP: 3GPP-SGSN-MCC-MCN(18)
    # AVP: 3GPP-MS-TimeZone(23)
    # AVP: 3GPP-User-Location-Info(22)
    # AVP: 3GPP-RAT-Type(21)
    # AVP: Framed-IP-Address(8)
    # AVP: 3GPP-CG-Address(4)
    # AVP: 3GPP-SGSN-Address(6)
    # AVP: 3GPP-GGSN-Address(7)
    # AVP: Route-Record(282)
    
    CCR_avps=[]
    CCR_avps.append(encodeAVP("Session-Id", session_id))
    CCR_avps.append(encodeAVP("Auth-Application-Id",DIAMETER_GY_APPLICATION_ID))
    CCR_avps.append(encodeAVP("Origin-Host",o_host))
    CCR_avps.append(encodeAVP("Origin-Realm", GY_ORIGIN_REALM))
    CCR_avps.append(encodeAVP("Destination-Realm",GY_DESTINATION_REALM))
    CCR_avps.append(encodeAVP("Service-Context-Id", GY_SERVICE_CONTEXT_ID))
    CCR_avps.append(encodeAVP("CC-Request-Type",3))                                   #-- 3: TERMINATION_REQUEST
    CCR_avps.append(encodeAVP("CC-Request-Number",requestnumber))
    CCR_avps.append(encodeAVP("User-Name",GY_USER_NAME))
    CCR_avps.append(encodeAVP("Origin-State-Id",state))
    CCR_avps.append(encodeAVP("Event-Timestamp", int(time.time()) ))    
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",0),encodeAVP("Subscription-Id-Data",msisdn)]))
    CCR_avps.append(encodeAVP("Subscription-Id",[encodeAVP("Subscription-Id-Type",1),encodeAVP("Subscription-Id-Data",imsi  )]))
    CCR_avps.append(encodeAVP("Termination-Cause",1))
    CCR_avps.append(encodeAVP("Multiple-Services-Indicator",1))                       #-- 1: Always MSCC enabled
    CCR_avps.append(encodeAVP("Multiple-Services-Credit-Control",[encodeAVP("Used-Service-Unit",[encodeAVP("CC-Total-Octets",usedquota)]),encodeAVP("Rating-Group",ratinggroup),encodeAVP("Reporting-Reason",2)]))
    CCR_avps.append(encodeAVP("3GPP-Charging-Id",123454))
    CCR_avps.append(encodeAVP("3GPP-PDP-Type",0))    
    #-- CCR_avps.append(encodeAVP("3GPP-GPRS-Negotiated-QoS-profile","UTMS"))
    CCR_avps.append("0000000580000023000028af30382d343430393030303030343139303030303134376200")
    CCR_avps.append(encodeAVP("3GPP-GGSN-MCC-MNC",MCC_MNC))
    CCR_avps.append(encodeAVP("3GPP-NSAPI","5"))
    CCR_avps.append(encodeAVP("Called-Station-Id",apn))
    CCR_avps.append(encodeAVP("3GPP-Selection-Mode","0"))
    CCR_avps.append(encodeAVP("3GPP-Charging-Characteristics","0100"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-MCC-MNC",MCC_MNC))
    #-- 3GPP-Timezone
    CCR_avps.append("000000178000000e000028af0a000000")
    #-- 3GPP-User-Location-Info
    CCR_avps.append("0000001680000019000028af8217f60135df17f601055931d7000000")
    #--                  00000016C0000017000028AF3731363130353633353136
    #--              0000001680000019000028af8217f60135df17f601055931d7000000
    #-- CCR_avps.append(encodeAVP("3GPP-User-Location-Info","71610563516"))
    CCR_avps.append(encodeAVP("3GPP-RAT-Type","1004"))
    CCR_avps.append(encodeAVP("Framed-IP-Address","10.56.38.128"))
    CCR_avps.append(encodeAVP("3GPP-CG-Address","10.128.65.81"))
    CCR_avps.append(encodeAVP("3GPP-SGSN-Address","200.108.101.81"))
    CCR_avps.append(encodeAVP("3GPP-GGSN-Address","200.108.101.192"))
    CCR_avps.append(encodeAVP("Route-Record",o_host))

    CCR=HDRItem()
    CCR.appId=4
    CCR.flags=0xc0
    CCR.cmd=dictCOMMANDname2code('Credit-Control')
    initializeHops(CCR)
    msg=createReq(CCR,CCR_avps)    
       
    return msg
    
def create_Session_Id(o_host):
    IDENTITY="test.3gppnetwork.org"
    
    #The Session-Id MUST be globally and eternally unique
    #<DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
    now=datetime.datetime.now()
    ret=o_host+";"
    ret=ret+str(now.year)[2:4]+"%02d"%now.month+"%02d"%now.day
    ret=ret+"%02d"%now.hour+"%02d"%now.minute+";"
    ret=ret+"%02d"%now.second+str(now.microsecond)+";"
    ret=ret+IDENTITY[2:16]
    return ret
    