from fuzzywuzzy import fuzz
import csv
import datetime
import time

columns = {}


def get_status_score(status, dissolution):
    score = 0
    if dissolution != 'NULL':
        disstime = time.strptime(dissolution, '%b %d %Y %H:%M %p')
        dissolution = datetime.date(disstime.tm_year, disstime.tm_mon, disstime.tm_mday)
        print dissolution
    else:
        return 1.0

    if 'Active' in status and 'Inactive' not in status:
        score += 1.0
    else:
        score += 0.8
        if dissolution.year < datetime.date.today().year - 20:
            score -= 0.35
        elif dissolution.year < datetime.date.today().year - 10:
            score -= 0.3
        elif dissolution.year < datetime.date.today().year - 5:
            score -= 0.2
        elif dissolution.year < datetime.date.today().year - 3:
            score -= 0.1

    return score


def get_branch_score(branch):
    if 'None' in branch:
        return 1.0
    else:
        return 0.8


with open("/Users/JohnBowers/Desktop/project-folder/CRP_Projects/OC_Test/scoretest_in2.tsv", 'rU') as fi:
    org_r = csv.reader(fi, dialect="excel-tab")
    fo = open("/Users/JohnBowers/Desktop/project-folder/CRP_Projects/OC_Test/scoretest_out.csv", 'wb')
    writer = csv.writer(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for index, column in enumerate(next(org_r, None)):
        columns[column] = index

    header = sorted(columns.keys(), key=lambda key: columns[key])
    header.append("matchScore")
    header.append("adScore")

    writer.writerow(header)

    for row in org_r:
        adScore = 0
        if ('None' in row[columns['OC_address']]) or row[columns['CRP_address']] is '':
            adScore = 0
        else:
            adScore = fuzz.token_set_ratio(row[columns['OC_address']], row[columns['CRP_address']])

        statScore = get_status_score(row[columns['status']], row[columns['OC_Dissolution_date']])
        branchScore = get_branch_score(row[columns['branch']])

        matchScore = round(branchScore * statScore * ((adScore + float(row[columns['score']])*1.5) / 2.5))
        row.append(matchScore)
        row.append(adScore)
        row.append(statScore)
        writer.writerow(row)

fo.close()
