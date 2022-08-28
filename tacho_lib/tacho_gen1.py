from dataclasses import dataclass, field
from enum import Enum

################################################################################
# Refer to XXXX.pdf p.280                                                      #
################################################################################
# DF  - Dedicated File. A DF can contain other files (DF or EF)                #
# EF  - Elementary File                                                        #
# FID - File ID                                                                #
# IC  - Integrated Circuit                                                     #
# ICC - Integrated Circuit Card                                                #
# MF  - Master File (root DF)                                                  #
# VU  -  Vehicle Unit                                                          #
################################################################################

################################################################################
# Constants                                                                    #
################################################################################
class eFID(Enum):
    MF                         = {"name": "MF"                           , "fid": bytes([0x3F, 0x00])}
    ICC                        = {"name": "EF ICC"                       , "fid": bytes([0x00, 0x02])}
    IC                         = {"name": "EF IC"                        , "fid": bytes([0x00, 0x05])}
    DIR                        = {"name": "EF DIR"                       , "fid": bytes([0x2F, 0x00])}
    ATR_INFO                   = {"name": "EF ATR/INFO"                  , "fid": bytes([0x2F, 0x01])}
    EXTENDED_LENGTH            = {"name": "EF EXTENDED_LENGTH"           , "fid": bytes([0x00, 0x06])}
    TACHOGRAPH                 = {"name": "DF Tachograph"                , "fid": bytes([0x05, 0x00])}
    APPLICATION_IDENTIFICATION = {"name": "EF Application_Identification", "fid": bytes([0x05, 0x01])}
    CARD_CERTIFICATE           = {"name": "EF Card_Certificate"          , "fid": bytes([0xC1, 0x00])}
    CA_CERTIFICATE             = {"name": "EF CA_Certificate"            , "fid": bytes([0xC1, 0x08])}
    IDENTIFICATION             = {"name": "EF Identification"            , "fid": bytes([0x05, 0x20])}
    CARD_DOWNLOAD              = {"name": "EF Card_Download"             , "fid": bytes([0x05, 0x0E])}
    DRIVING_LICENSE_INFO       = {"name": "EF Driving_License_Info"      , "fid": bytes([0x05, 0x21])}
    EVENTS_DATA                = {"name": "EF Events_Data"               , "fid": bytes([0x05, 0x02])}
    FAULTS_DATA                = {"name": "EF Faults_Data"               , "fid": bytes([0x05, 0x03])}
    DRIVER_ACTIVITY_DATA       = {"name": "EF Driver_Activity_Data"      , "fid": bytes([0x05, 0x04])}
    VEHICLE_USED               = {"name": "EF Vehicle_Used"              , "fid": bytes([0x05, 0x05])}
    PLACES                     = {"name": "EF Places"                    , "fid": bytes([0x05, 0x06])}
    CURRENT_USAGE              = {"name": "EF Current_Usage"             , "fid": bytes([0x05, 0x07])}
    CONTROL_ACTIVITY_DATA      = {"name": "EF Control_Activity_Data"     , "fid": bytes([0x05, 0x08])}
    SPECIFIC_CONDITIONS        = {"name": "EF Specific_Conditions"       , "fid": bytes([0x05, 0x22])}

    def seek(fid_to_seek):
        for fid in eFID:
            if fid.value["fid"] == fid_to_seek:
                return True
        return False

    def get_name(fid_to_seek):
        for fid in eFID:
            if fid.value["fid"] == fid_to_seek:
                return fid.value["name"]
        return

TSC_145 = bytes([0x61, 0x08, 0x4F, 0x06, 0xFF,
                 0x54, 0x41, 0x43, 0x48, 0x4F,
                 0x61, 0x08, 0x4F, 0x06, 0xFF,
                 0x53, 0x4D, 0x52, 0x44, 0x54])
################################################################################
# Header                                                                       #
################################################################################
@dataclass
class cHeader:
    fid:         bytearray = bytearray([0x00] * 2)
    appendix:    bytearray = bytearray([0x00] * 1)
    data_length: bytearray = bytearray([0x00] * 2)
################################################################################
# EF ICC                                                                       #
################################################################################
@dataclass
class cCardIccIdentification:
    clockStop:                bytearray = bytearray([0x00] * 1)
    cardExtendedSerialNumber: bytearray = bytearray([0x00] * 8)
    cardApprovalNumber:       bytearray = bytearray([0x20] * 8)
    cardPersonaliserID:       bytearray = bytearray([0x00] * 1)
    embedderIcAssemblerID:    bytearray = bytearray([0x00] * 5)
    icIdentifier:             bytearray = bytearray([0x00] * 2)

@dataclass
class cEF_ICC:
    Header:                cHeader = cHeader(eFID.ICC.value["fid"])
    CardIccIdentification: cCardIccIdentification = cCardIccIdentification()
################################################################################
# EF IC                                                                        #
################################################################################
@dataclass
class cCardChipIdentification:
    icSerialNumber:           bytearray = bytearray([0x00] * 4)
    icManufacturingReference: bytearray = bytearray([0x00] * 4)

@dataclass
class cEF_IC:
    Header:                 cHeader = cHeader(eFID.IC.value["fid"])
    CardChipIdentification: cCardChipIdentification = cCardChipIdentification()
################################################################################
# EF DIR                                                                       #
################################################################################
@dataclass
class cEF_DIR:
    Header:  cHeader = cHeader(eFID.DIR.value["fid"])
    Data:    bytearray = bytearray([0x00] * 20)
################################################################################
# EF ATR/INFO                                                                  #
################################################################################
@dataclass
class cEF_ATR_INFO:
    Header: cHeader = cHeader(eFID.ATR_INFO.value["fid"])
    Data:   bytearray = bytearray([0x00] * 128)
################################################################################
# EF EXTENDED_LENGTH                                                           #
################################################################################
@dataclass
class cEF_Extended_Length:
    Header: cHeader = cHeader(eFID.EXTENDED_LENGTH.value["fid"])
    Data:   bytearray = bytearray([0x00] * 3)
################################################################################
# EF ApplicationIdentification                                                 #
################################################################################
@dataclass
class cDriverCardApplicationIdentification:
    typeOfTachographCardId:  bytearray = bytearray([0x00] * 3)
    cardStructureVersion:    bytearray = bytearray([0x00] * 2)
    noOfEventsPerType:       bytearray = bytearray([0x00] * 1)
    noOfFaultsPerType:       bytearray = bytearray([0x00] * 1)
    activityStructureLength: bytearray = bytearray([0x00] * 2)
    noOfCardVehicleRecords:  bytearray = bytearray([0x00] * 2)
    noOfCardPlaceRecords:    bytearray = bytearray([0x00] * 1)

@dataclass
class cEF_Application_Identification:
    Header:                              cHeader = cHeader(eFID.APPLICATION_IDENTIFICATION.value["fid"])
    DriverCardApplicationIdentification: cDriverCardApplicationIdentification = cDriverCardApplicationIdentification()
################################################################################
# EF Card_Certificate                                                          #
################################################################################
@dataclass
class cEF_Card_Certificate:
    Header:          cHeader = cHeader(eFID.CARD_CERTIFICATE.value["fid"])
    CardCertificate: bytearray = bytearray([0x00] * 194)
################################################################################
# EF CA_Certificate #
################################################################################
@dataclass
class cCA_Certificate:
    Header:                 cHeader = cHeader(eFID.CA_CERTIFICATE.value["fid"])
    MemberStateCertificate: bytearray = bytearray([0x00] * 194)
################################################################################
# EF Identification                                                            #
################################################################################
@dataclass
class cCardIdentification:
    cardIssuingMemberState: bytearray = bytearray([0x00] * 1)
    cardNumber:             bytearray = bytearray([0x20] * 16)
    cardIssuingAuthor:      bytearray = bytearray([0x00] + [0x20] * 35)
    cardIssueDate:          bytearray = bytearray([0x00] * 4)
    cardValidityBegin:      bytearray = bytearray([0x00] * 4)
    cardExpiryDate:         bytearray = bytearray([0x00] * 4)

@dataclass
class cCardHolderName:
    holderSurname:    bytearray = bytearray([0x00] + [0x20] * 35)
    holderFirstNames: bytearray = bytearray([0x00] + [0x20] * 35)

@dataclass
class cDriverCardHolderIdentification:
    cardHolderName:              cCardHolderName = cCardHolderName()
    cardHolderBirthDate:         bytearray = bytearray([0x00] * 4)
    cardHolderPreferredLanguage: bytearray = bytearray([0x20] * 2)

@dataclass
class cEF_Identification:
    Header:                         cHeader = cHeader(eFID.IDENTIFICATION.value["fid"])
    CardIdentification:             cCardIdentification = cCardIdentification()
    DriverCardHolderIdentification: cDriverCardHolderIdentification = cDriverCardHolderIdentification()
################################################################################
# EF Card_Download                                                             #
################################################################################
@dataclass
class cEF_Card_Download:
    Header:           cHeader = cHeader(eFID.CARD_DOWNLOAD.value["fid"])
    LastCardDownload: bytearray = bytearray([0x00] * 4)
################################################################################
# EF Driving_License_Info                                                      #
################################################################################
@dataclass
class cCardDrivingLicenseInformation:
    drivingLicenseIssuingAuthority: bytearray = bytearray([0x00] + [0x20] * 35)
    drivingLicenseIssuingNation:    bytearray = bytearray([0x00] * 1)
    drivingLicenseNumber:           bytearray = bytearray([0x20] * 16)

@dataclass
class cEF_Driving_License_Info:
    Header:                        cHeader = cHeader(eFID.DRIVING_LICENSE_INFO.value["fid"])
    CardDrivingLicenseInformation: cCardDrivingLicenseInformation = cCardDrivingLicenseInformation()
################################################################################
# EF Events_Data                                                               #
################################################################################
@dataclass
class cEventVehicleRegistration:
    vehicleRegistrationNation: bytearray = bytearray([0x00] * 1)
    vehicleRegistrationNumber: bytearray = bytearray([0x00] + [0x20] * 13)

@dataclass
class cCardEventRecord:
    eventType:      bytearray = bytearray([0x00] * 1)
    eventBeginTime: bytearray = bytearray([0x00] * 4)
    eventEndTime:   bytearray = bytearray([0x00] * 4)
    eventVehicleRegistration: cEventVehicleRegistration = cEventVehicleRegistration()

@dataclass
class cCardEventData:
    cardEventRecords: list[cCardEventRecord] = field(default_factory=lambda: [cCardEventRecord()] * 12)

@dataclass
class cEF_Events_Data:
    Header:        cHeader = cHeader(eFID.EVENTS_DATA.value["fid"])
    CardEventData: cCardEventData = cCardEventData()
################################################################################
# EF Faults_Data                                                               #
################################################################################
@dataclass
class cFaultVehicleRegistration:
    vehicleRegistrationNation: bytearray = bytearray([0x00] * 1)
    vehicleRegistrationNumber: bytearray = bytearray([0x00] + [0x20] * 13)

@dataclass
class cCardFaultRecord:
    faultType:      bytearray = bytearray([0x00] * 1)
    faultBeginTime: bytearray = bytearray([0x00] * 4)
    faultEndTime:   bytearray = bytearray([0x00] * 4)
    faultVehicleRegistration: cFaultVehicleRegistration = cFaultVehicleRegistration()

@dataclass
class cCardFaultData:
    CardFaultRecords: list[cCardFaultRecord] = field(default_factory=lambda: [cCardEventRecord()] * 12)

@dataclass
class cEF_Faults_Data:
    Header:        cHeader = cHeader(eFID.FAULTS_DATA.value["fid"])
    CardFaultData: cCardFaultData = cCardFaultData()
################################################################################
# EF Driver_Activity_Data                                                      #
################################################################################
@dataclass
class cCardDriverActivity:
    activityPointerOldestDayRecord: bytearray = bytearray([0x00] * 2)
    activityPointerNewestRecord:    bytearray = bytearray([0x00] * 2)
    activityDailyRecords:           bytearray = bytearray([0x00] * 13776)

@dataclass
class cEF_Driver_Activity_Data:
    Header:             cHeader = cHeader(eFID.DRIVER_ACTIVITY_DATA.value["fid"])
    CardDriverActivity: cCardDriverActivity = cCardDriverActivity()
################################################################################
# EF Vehicle_Used                                                              #
################################################################################
@dataclass
class cVehicleRegistration:
    vehicleRegistrationNation: bytearray = bytearray([0x00] * 1)
    vehicleRegistrationNumber: bytearray = bytearray([0x00] + [0x20] * 13)

@dataclass
class cCardVehicleRecord:
    vehicleOdometerBegin: bytearray = bytearray([0x00] * 3)
    vehicleOdometerEnd:   bytearray = bytearray([0x00] * 3)
    vehicleFirstUse:      bytearray = bytearray([0x00] * 4)
    vehicleLastUse:       bytearray = bytearray([0x00] * 4)
    vehicleRegistration:  cVehicleRegistration = cVehicleRegistration()
    vuDataBlockCounter:   bytearray = bytearray([0x00] * 2)

@dataclass
class cCardVehiclesUsed:
    vehiclePointerNewestRecord: bytearray = bytearray([0x00] * 2)
    cardVehicleRecords: list[cCardEventRecord] = field(default_factory=lambda: [cCardVehicleRecord()] * 200)

@dataclass
class cEF_Vehicle_Used:
    Header:           cHeader = cHeader(eFID.VEHICLE_USED.value["fid"])
    CardVehiclesUsed: cCardVehiclesUsed = cCardVehiclesUsed()
################################################################################
# EF Places                                                                    #
################################################################################
@dataclass
class cPlaceRecord:
    entryTime:                bytearray = bytearray([0x00] * 4)
    entryTimeDailyWorkPeriod: bytearray = bytearray([0x00] * 1)
    dailyWorkPeriodCountry:   bytearray = bytearray([0x00] * 1)
    vehicleOdometerValue:     bytearray = bytearray([0x00] * 3)

@dataclass
class cCardPlaceDailyWorkPeriod:
    placePointerNewestRecord: bytearray = bytearray([0x00] * 1)
    placeRecords: list[cPlaceRecord] = field(default_factory=lambda: [cPlaceRecord()] * 112)

@dataclass
class cEF_Places:
    Header:                   cHeader = cHeader(eFID.PLACES.value["fid"])
    CardPlaceDailyWorkPeriod: cCardPlaceDailyWorkPeriod = cCardPlaceDailyWorkPeriod()
################################################################################
# EF Current_Usage                                                             #
################################################################################
@dataclass
class cSessionOpenVehicle:
    vehicleRegistrationNation: bytearray = bytearray([0x00] * 1)
    vehicleRegistrationNumber: bytearray = bytearray([0x00] + [0x20] * 13)

@dataclass
class cCardCurrentUse:
    sessionOpenTime:    bytearray = bytearray([0x00] * 4)
    sessionOpenVehicle: cSessionOpenVehicle = cSessionOpenVehicle()

@dataclass
class cEF_Current_Usage:
    Header:         cHeader = cHeader(eFID.CURRENT_USAGE.value["fid"])
    CardCurrentUse: cCardCurrentUse = cCardCurrentUse()
################################################################################
# EF Control_Activity_Data                                                     #
################################################################################
@dataclass
class cControlCardNumber:
    cardType:               bytearray = bytearray([0x00] * 1)
    cardIssuingMemberState: bytearray = bytearray([0x00] * 1)
    cardNumber:             bytearray = bytearray([0x20] * 16)

@dataclass
class cControlVehicleRegistration:
    vehicleRegistrationNation: bytearray = bytearray([0x00] * 1)
    vehicleRegistrationNumber: bytearray = bytearray([0x00] + [0x20] * 13)

@dataclass
class cCardControlActivityDataRecord:
    controlType:                bytearray = bytearray([0x00] * 1)
    controlTime:                bytearray = bytearray([0x00] * 4)
    controlCardNumber:          cControlCardNumber = cControlCardNumber()
    controlVehicleRegistration: cControlVehicleRegistration = cControlVehicleRegistration()
    controlDownloadPeriodBegin: bytearray = bytearray([0x00] * 4)
    controlDownloadPeriodEnd:   bytearray = bytearray([0x00] * 4)

@dataclass
class cEF_Control_Activity_Data:
    Header:                        cHeader = cHeader(eFID.CONTROL_ACTIVITY_DATA.value["fid"])
    CardControlActivityDataRecord: cCardControlActivityDataRecord = cCardControlActivityDataRecord()
################################################################################
# SpecificConditionRecord                                                      #
################################################################################
@dataclass
class cSpecificConditionRecord:
    entryTime:             bytearray = bytearray([0x00] * 4)
    SpecificConditionType: bytearray = bytearray([0x00] * 1)

@dataclass
class cEF_Specific_Conditions:
    Header:                   cHeader = cHeader(eFID.SPECIFIC_CONDITIONS.value["fid"])
    SpecificConditionRecords: list[cSpecificConditionRecord] = field(default_factory=lambda: [cSpecificConditionRecord()] * 56)
################################################################################
# DF Tachograph                                                                #
################################################################################
@dataclass
class cDF_Tachograph:
    Header:                        cHeader = cHeader(eFID.TACHOGRAPH.value["fid"])
    EF_Application_Identification: cEF_Application_Identification = cEF_Application_Identification()
    EF_Card_Certificate:           cEF_Card_Certificate = cEF_Card_Certificate()
    CA_Certificate:                cCA_Certificate = cCA_Certificate()
    EF_Identification:             cEF_Identification = cEF_Identification()
    EF_Card_Download:              cEF_Card_Download = cEF_Card_Download()
    EF_Driving_License_Info:       cEF_Driving_License_Info = cEF_Driving_License_Info()
    EF_Events_Data:                cEF_Events_Data = cEF_Events_Data()
    EF_Faults_Data:                cEF_Faults_Data = cEF_Faults_Data()
    EF_Driver_Activity_Data:       cEF_Driver_Activity_Data = cEF_Driver_Activity_Data()
    EF_Vehicle_Used:               cEF_Vehicle_Used = cEF_Vehicle_Used()
    EF_Places:                     cEF_Places = cEF_Places()
    EF_Current_Usage:              cEF_Current_Usage = cEF_Current_Usage()
    EF_Control_Activity_Data:      cEF_Control_Activity_Data = cEF_Control_Activity_Data()
    EF_Specific_Conditions:        cEF_Specific_Conditions = cEF_Specific_Conditions()

################################################################################
# MF                                                                           #
################################################################################
@dataclass
class cMF:
    Header:             cHeader = cHeader(eFID.MF.value["fid"])
    EF_ICC:             cEF_ICC = cEF_ICC()
    EF_IC:              cEF_IC = cEF_IC()
    EF_DIR:             cEF_DIR = cEF_DIR()
    EF_ATR_INFO:        cEF_ATR_INFO = cEF_ATR_INFO()
    EF_Extended_Length: cEF_Extended_Length = cEF_Extended_Length()
    DF_Tachograph:      cDF_Tachograph = cDF_Tachograph()