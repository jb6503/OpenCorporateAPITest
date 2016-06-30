import requests
import csv
import pprint
import unicodedata
import opencorporatelib as ocl

count = 1
hits = 0
matches = 0
rows = 0
organizations = 0

def try_unicode(data):
    try:
        ascii = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
        return ascii
    except TypeError:
        return "None Found"

def check_for_data(data):
    datalist = []
    if data != None:
        if data['most_recent']:
            try:
                for datum in data['most_recent']:
                    if "CompanyAddress" in datum['datum']['data_type']:
                        addition = datum['datum']['description']
                        datalist.append(addition)
                return datalist
            except TypeError as e:
                print e
    else:
        return None







CRP_Orgs_f = open("/Users/JohnBowers/Desktop/project-folder/CRP_Projects/OC_Test/Old/orgnames_tsv_sample_rest.tsv", 'rU')
org_r = csv.reader(CRP_Orgs_f, dialect='excel-tab')

orgnames = []
next(org_r, None)

for row in org_r:
    orgnames.append([row[1], row[6].lower()])
    organizations += 1

outfile = open("/Users/JohnBowers/Desktop/project-folder/CRP_Projects/OC_Test/Output_test.csv", 'wb')
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['Correct?', 'CRPName', 'State', 'ID', 'PossibleMatch', 'Score', 'URL', 'Status', 'Branch',
                 'Address', 'Incorporation', 'Dissolution', 'Type'])
output = []


for org in orgnames:
    try:
        payload = {"query": org[0]}
        recResp = requests.get(ocl.reconcile(org[1]), params=payload)
        recJson = recResp.json()
        print str(count) + ": " + str(payload["query"])
        print recJson

        for result in recJson['result']:

            if hits > 9:
                hits = 0
                break

            try:
                lookupResp = requests.get(ocl.lookup(result["id"]))
                lookupJson = lookupResp.json()
                lookupInfo = lookupJson["results"]["company"]
                toWrite = ['', org[0], org[1].upper(), try_unicode(result["id"]), try_unicode(result["name"]),
                           result["score"], try_unicode(result["uri"]), try_unicode(lookupInfo["current_status"]),
                           try_unicode(lookupInfo["branch_status"]),
                           try_unicode(lookupInfo["registered_address_in_full"]),
                           try_unicode(lookupInfo["incorporation_date"]), try_unicode(lookupInfo["dissolution_date"]),
                           try_unicode(lookupInfo["company_type"])]

                if check_for_data(lookupInfo["data"]) is not None:
                    toWrite.extend(check_for_data(lookupInfo["data"]))
                    writer.writerow(toWrite)
                else:
                    writer.writerow(toWrite)

                rows += 1
            except requests.exceptions.RequestException as e:
                print e
                continue
            except ValueError as e:
                print e
                continue
            hits += 1
        if hits > 0:
            matches += 1

        hits = 0

    except requests.exceptions.RequestException as e:
        print e
        continue
    except ValueError as e:
        print e
        continue
    count += 1

print "%d candidates returned for %d matches against %d organizations." % (rows, matches, organizations)

outfile.close()
CRP_Orgs_f.close()

