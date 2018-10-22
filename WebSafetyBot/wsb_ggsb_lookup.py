import keys
import requests
def checkWebsite(website):
    # Dict with potential http status
    http_status = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        500: "Internal Server Error",
        503: "Service Unavailable",
        504: "Gateway Timeout"
    }
    api_key = keys.api_key
    # Google Safebrowsing v4 lookup
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    # Build payload to match Google SafeBrowsing formatting
    payload = {'client': {'clientId': "websafetybot", 'clientVersion': "0.0.1"},
               'threatInfo': {'threatTypes': ["MALWARE","SOCIAL_ENGINEERING",
                                              "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE",
                                              "POTENTIALLY_HARMFUL_APPLICATION"],
                              'platformTypes': ["ANY_PLATFORM"],
                              'threatEntryTypes': ["URL"],
                              'threatEntries': [{'url': website}]}}
    params = {'key': api_key}
    r = requests.post(url, params=params, json=payload)
    status_code = r.status_code
    #if json response has body
    if(http_status[status_code] != "OK"):
        return (http_status[status_code], "ERROR")
    if(r.json() != {}):
        ##Response format is:
        # {
        #     "matches": [{
        #         "threatType": "MALWARE",
        #         "platformType": "WINDOWS",
        #         "threatEntryType": "URL",
        #         "threat": {"url": "http://www.urltocheck1.org/"},
        #         "threatEntryMetadata": {
        #             "entries": [{
        #                 "key": "malware_threat_type",
        #                 "value": "landing"
        #             }]
        #         },
        #         "cacheDuration": "300.000s"
        #     }, {
        #         "threatType": "MALWARE",
        #         "platformType": "WINDOWS",
        #         "threatEntryType": "URL",
        #         "threat": {"url": "http://www.urltocheck2.org/"},
        #         "threatEntryMetadata": {
        #             "entries": [{
        #                 "key": "malware_threat_type",
        #                 "value": "landing"
        #             }]
        #         },
        #         "cacheDuration": "300.000s"
        #     }]
        # }
        #Get matches from json, [0] is first list, ["threatType"] gets threatType dict
        r_threatType = r.json()["matches"][0]["threatType"]
        return (http_status[status_code], r_threatType)
    return (http_status[status_code], "SAFE")