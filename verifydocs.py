from passporteye import read_mrz
import requests
from fuzzywuzzy import fuzz

def verify_npi(npi):
    try:
        npi_request = requests.get(f'https://npiregistry.cms.hhs.gov/api/?number={npi}&version=2.1')
        npi_json = npi_request.json()
        if npi_json.get('result_count'):
            npi_data = npi_json.get('results')
        else:
            return {'message':'NPI NOT FOUND','payload':None}
        if npi_data:
            record = npi_data[0]
            data = {'message':'NPI FOUND','payload':{}}
            if record.get('enumeration_type') and record.get('enumeration_type') == 'NPI-1':
                data['payload']['last_name'] = record['basic']['last_name'].lower()
                data['payload']['first_name'] = record['basic']['first_name'].lower()
                data['payload']['gender'] = record['basic']['gender']
            elif record.get('enumeration_type') == 'NPI-2':
                data['payload']['last_name'] = record['basic']['authorized_official_last_name'].lower()
                data['payload']['first_name'] = record['basic']['authorized_official_first_name'].lower()
                data['payload']['gender'] = None
            else:
                try:
                    data['payload']['last_name'] = record['basic']['last_name'].lower()
                    data['payload']['first_name'] = record['basic']['first_name'].lower()
                except:
                    return {'message':'NPI PARSE ERROR','payload':None}
            return data
        else:
            return {'message':'NPI NOT FOUND','payload':None}
    except:
        return {'message':'CRITICAL ERROR','payload':None}

def validate_passport(url,force_flag=False,threshold=70,url_type=True):
    if url_type:
        try:
            passport_image = requests.get(url).content
        except:
            return {'message':'URL ERROR','payload':None}
    else:
        passport_image=url
    try:
        passport_details = read_mrz(passport_image).to_dict()
        if passport_details:
            if passport_details['valid_score'] > threshold or force_flag:
                dob = None
                if passport_details.get('valid_date_of_birth'):
                    dob = passport_details['date_of_birth']
                return {'message':'VALIDATED','payload':{'last_name':passport_details['surname'].lower(),'first_name':passport_details['names'].lower(),'gender':passport_details['sex'].lower(),'dob':dob}}
            else:
                return {'message':'NOT CONFIDENT','payload':None}
        else:
            return {'message':'PARSING ERROR','payload':None}
    except:
        return {'message':'SCANNING ERROR','payload':None}


def compare(Str1,Str2,exact=False):
    if exact:
        if Str1 == Str2:
            return 1
        else:
            return 0
    Ratio = fuzz.ratio(Str1.lower(),Str2.lower())
    Partial_Ratio = fuzz.partial_ratio(Str2.lower(),Str1.lower())
    if Ratio >= 70 or Partial_Ratio >= 70:
        return 1
    else:
        return 0

def validate(url,npi,dob=None,url_type=True):
    valid_passport = validate_passport(url,url_type=url_type)
    valid_npi = verify_npi(npi)
    npi_data = valid_npi['payload']
    passport_data = valid_passport['payload']
    if npi_data and passport_data:
        veracity = 0
        truth = 0
        if npi_data.get('first_name') and passport_data.get('first_name'):
            truth+=1
            veracity+=compare(npi_data['first_name'],passport_data['first_name'])
        if npi_data.get('last_name') and passport_data.get('last_name'):
            truth+=1
            veracity+=compare(npi_data['last_name'],passport_data['last_name'])
        if npi_data.get('gender') and passport_data.get('gender'):
            truth+=1
            veracity+=compare(npi_data['gender'],passport_data['gender'],exact=True)
        if passport_data.get('dob') and dob:
            truth+=1
            veracity+=compare(npi_data['dob'],dob,exact=True)
        if truth > 1 and veracity/truth > .5:
            return {'valid':1,'payload':None}
        else:
            return {'valid':0,'payload':None}
    elif npi_data:
        return {'valid':0,'payload':valid_passport}
    elif passport_data:
        return {'valid':0,'payload':valid_npi}
    else:
        return {'valid':0,'payload':[valid_passport,valid_npi]}

def validate(url,npi,dob=None,url_type=True):
    valid_passport = validate_passport(url,url_type=url_type)
    valid_npi = verify_npi(npi)
    npi_data = valid_npi['payload']
    passport_data = valid_passport['payload']
    if npi_data and passport_data:
        veracity = 0
        truth = 0
        if npi_data.get('first_name') and passport_data.get('first_name'):
            truth+=1
            veracity+=compare(npi_data['first_name'],passport_data['first_name'])
        if npi_data.get('last_name') and passport_data.get('last_name'):
            truth+=1
            veracity+=compare(npi_data['last_name'],passport_data['last_name'])
        if npi_data.get('gender') and passport_data.get('gender'):
            truth+=1
            veracity+=compare(npi_data['gender'],passport_data['gender'],exact=True)
        if passport_data.get('dob') and dob:
            truth+=1
            veracity+=compare(npi_data['dob'],dob,exact=True)
        if truth > 1 and veracity/truth > .5:
            return {'valid':1,'payload':None}
        else:
            return {'valid':0,'payload':None}
    elif npi_data:
        return {'valid':0,'payload':valid_passport['message']}
    elif passport_data:
        return {'valid':0,'payload':valid_npi['message']}
    else:
        return {'valid':0,'payload':valid_passport['message'] + ' & ' + valid_npi['message']}