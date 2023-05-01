import re
import json

def process():
    file_str = ''
    # f = open("results.csv", "r")
    # for line in f.readlines():
    #     if line  and not line.isspace():
    #         file_str = file_str + line.rstrip()


    # constants = []

    # if "context.value" in file_str:
    #     regex_pattern = r'<Form\.Select.*?/>'
    #     mat = re.findall(regex_pattern, file_str)
    #     for form in mat:
    #         if "context.value" in form:
    #             regex_pattern = r'options=\{([^}]*)\}'
    #             dropdown = re.findall(regex_pattern, form)
    #             constants.append(dropdown[0])



    values = {}
    f = open("../input/codeql_results.csv", "r")
    for line in f.readlines():
        line = line.split(',')
        if len(line)>1:
            print(line)
            const = line[0]
            const = const.replace('"', '')
            print(const)
            val = line[1]
            print(val)
            if const in values.keys():
                values[const].append(val.strip())
            else:
                values[const] = [val.strip()]


    print(values)

    # f = open('output_enum_message_struct.json')
    # existing_json = json.load(f)

    # for const in constants:
    #     val = values[const]
    #     val = val.split('=')[1]
    #     lst = val.split(",")
    #     enum_list = []
    #     for st in lst:
    #         if "value" in st:
    #             values_between_quotes = re.findall('"([^"]*)"', st)
    #             if values_between_quotes[0]:
    #                 values_between_quotes = values_between_quotes[0].replace('\'', "\"")
    #                 enum_list.append(values_between_quotes)
        
    #     existing_json[const] = enum_list


    with open("output_enum_message_struct.json", "w") as myfile:
        json.dump(values, myfile)


if __name__ == "__main__":
    process()