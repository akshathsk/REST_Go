import json
import sys

def recursivePrompt(prompt, enum, jsnData):
    try:
        for key in jsnData.keys():
            if type(jsnData[key]) == list:
                for value in jsnData[key]:
                    recursivePrompt(prompt, enum, value)
            elif isinstance(jsnData[key], dict):
                recursivePrompt(prompt, enum, jsnData[key])
            
            for enum_keys in enum.keys():
                if key.lower() in enum_keys.lower() or  enum_keys.lower() in key.lower():
                    prompt.append('{} should be filled with one among {}'.format(key, enum[enum_keys]))
                    
    except Exception as e:
        pass
    return prompt

if __name__ == "__main__":

    service = sys.argv[1]

    # get swagger json
    try:
        f = open('../input/swagger/'+str(service)+'_swagger.json')
        data = json.load(f)
    except:
        data = {}

    # get enum 
    try:
        f = open('../input/enum-props/output_enum_'+str(service)+'.json')
        enum = json.load(f)
    except:
        enum = {}

    target = 'example'
    for jsonsArray in data:
        httpjson = jsonsArray['methodToRequestMap']
        for methods in httpjson:
                httpcontent = httpjson[methods]
                for content in httpcontent:
                    prompt = []
                    if target in content.keys():
                            customData =  content[target]
                            try:
                                jsnData = json.loads(customData)
                                content['prompt'] = []
                                prompt = recursivePrompt(prompt, enum, jsnData)
                                if prompt:
                                    for val in prompt:
                                        content['prompt'].append(val)
                                    
                                    content['prompt'].append("For other relevant values, use the following json as reference: {}".format(enum))
                            except:
                                pass                       


    with open('../output/uiuc-api-tester-'+str(service)+'.json', 'w') as f:
        json.dump(data, f)