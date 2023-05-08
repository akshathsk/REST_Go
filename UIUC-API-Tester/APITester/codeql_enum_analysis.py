import re
import json
import sys

def process():

    values = {}
    f = open('../input/codeql_csv/'+str(service)+'_results.csv', "r")
    for line in f.readlines():
        line = line.split(',')
        if len(line)>1:
            const = line[0]
            const = const.replace('"', '')
            val = line[1]
            if const in values.keys():
                values[const].append(val.strip())
            else:
                values[const] = [val.strip()]


    with open('../input/enum-props/output_enum_'+str(service)+'.json', "w") as myfile:
        json.dump(values, myfile)


if __name__ == "__main__":
    global service
    service = sys.argv[1]
    process()