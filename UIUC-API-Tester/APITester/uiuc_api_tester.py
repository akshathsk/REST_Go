import openai
import os
import json
import sys
import requests
import re
import traceback
import ast
import collections
from functools import (partial,
                       singledispatch)
from itertools import chain
from typing import (Dict,
                    List,
                    TypeVar)
import time
import re
import random
from difflib import SequenceMatcher
from collections import MutableMapping
from functools import partial
from random import randint
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

crumbs = True
def flatten(dictionary, parent_key=False, separator='.'):
    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            if not value.items():
                items.append((new_key,None))
            else:
                items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            if len(value):
                for k, v in enumerate(value):
                    items.extend(flatten({str(k): v}, new_key, separator).items())
            else:
                items.append((new_key,None))
        else:
            items.append((new_key, value))
        
    return dict(items)

def string_helper(json_dict):
    string_sequence = json_dict['sequence']
    string_sequence = string_sequence.replace("[", "", 1)
    string_sequence = string_sequence[::-1].replace("]", "", 1)[::-1]
    string_sequence = string_sequence.split('], [')
    string_sequence[0] = string_sequence[0].lstrip('[')
    string_sequence[-1] = string_sequence[-1].rstrip(']')

    return string_sequence

# helper function for similarity check
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# helper function to delete certain params
def delete_key(json_obj, key_to_delete):
    if isinstance(json_obj, dict):
        for key in list(json_obj.keys()):
            if key_to_delete in key:
                del json_obj[key]
            else:
                delete_key(json_obj[key], key_to_delete)
    elif isinstance(json_obj, list):
        for item in json_obj:
            delete_key(item, key_to_delete)


def randints(count, *randint_args):
    ri = partial(randint, *randint_args)
    return [(ri(), ri()) for _ in range(count)]



def getBodyForUrl(urlToFind, previousResponse, GPTcontent, isFormData):
    exmple = ''
    try:
        print(urlToFind)
        for ms in microservices:
            host = ms['host']
            methodToRequestMap = ms['methodToRequestMap']
            for key in methodToRequestMap:
                if (key == "POST"):
                    requestList = methodToRequestMap[key]
                    for ele in requestList:
                        url = host + ele['url']
                        if (urlToFind == url):
                            if 'example' not in ele:
                                return "",exmple, isFormData
                            if 'contentType' in ele:
                                if ele['contentType'] == "FORM_DATA":
                                    isFormData = True
                            try:
                                exmple = ele['example']
                                exmple = json.loads(exmple)
                            except:
                                exmple = ''
                                pass

                            if not previousResponse:
                                # print("previousResponse")
                                # print(previousResponse)
                                print("skeleton to GPT")
                                print(ele['example'])
                                if 'prompt' not in ele.keys():
                                    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system",
                                                "content": "You are an assistant that provides sample json data for HTTP POST requests. These are a sequence of HTTP requests so please use the same context in subsequent requests"},
                                            {"role": "user", "content": "using the same context provide one json data that follows the key value information in : {0}. Don't add any additional attributes and respond with only a json without additional information.".format(
                                                ele['example'])},
                                            {"role": "user", "content": "For values that could not be found from above context, use {} for the same. For dates use the format: yyyy-MM-dd'T'HH:mm:ss. Add +1 country code for phone numbers only if phone number is present in the json struture given. Return strong passwords for password field only if password is present in the json context given. Please provide full form values for all attributes in provided json structure".format(
                                                GPTcontent)}
                                        ]
                                    )
                                else:
                                    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system",
                                                "content": "You are an assistant that provides sample json data for HTTP POST requests. These are a sequence of HTTP requests so please use the same context in subsequent requests"},
                                            {"role": "user", "content": "using the same context provide one json data that follows the key value information in: {0}. Use {1} as reference to substitute for values in required places. Don't add any additional attributes and respond with only a json without additional information.".format(
                                                ele['example'], ele['prompt'])},
                                            {"role": "user", "content": "For values that could not be found from above context, use {} for the same. For dates use the format: yyyy-MM-dd'T'HH:mm:ss. Add +1 country code for phone numbers only if phone number is present in the json struture given. Return strong passwords for password field only if password is present in the json context given. Please provide full form values for all attributes in provided json structure".format(
                                                GPTcontent)}
                                        ]
                                    )
                                content = response['choices'][0]['message']['content']
                                # print(content)
                                content_json = content.split("{", 1)[1]
                                content_json = "{" + content_json.rsplit("}", 1)[0] + "}"
                                print("GPT content")
                                print(content_json)
                                content_json = json.loads(content_json)
                                print("GENERATED JSON FROM GPT")
                                print(content_json)
                                return content_json, exmple, isFormData
                            else:
                                # print("previousResponse")
                                # print(previousResponse)
                                print("skeleton to GPT")
                                print(ele['example'])
                                if 'prompt' not in ele.keys():
                                    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system",
                                                "content": "You are a helpful assistant that provides sample json data for HTTP POST requests. These are a sequence of HTTP requests so please use the same context in subsequent requests"},
                                            {"role": "user", "content": "The previous POST request returned the json: {0}".format(
                                                previousResponse)},
                                            {"role": "user", "content": "using the same context and reusing the attribute values from the previous response, provide one json data that follows the json structure: {0}. Don't add any additional attributes and respond with only a json without additional information.".format(
                                                ele['example'])},
                                            {"role": "user", "content": "For values that could not be found from above context, use {} for the same. For dates use the format: yyyy-MM-dd'T'HH:mm:ss. Add +1 country code for phone numbers only if phone number is present in the json struture given. Return strong passwords for password field only if password is present in the json context given. Please provide full form values for all attributes in provided json structure".format(
                                                GPTcontent)}
                                        ]
                                    )
                                else:
                                    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system",
                                                "content": "You are a helpful assistant that provides sample json data for HTTP POST requests. These are a sequence of HTTP requests so please use the same context in subsequent requests"},
                                            {"role": "user", "content": "The previous POST request returned the json: {0} and some fields need to be populated with values in {1}".format(
                                                previousResponse, ele['prompt'])},
                                            {"role": "user", "content": "using the same context and reusing the attribute values from the previous response, provide one json data that follows the json structure: {0}. Don't add any additional attributes and respond with only a json without additional information.".format(
                                                ele['example'])},
                                            {"role": "user", "content": "For values that could not be found from above context, use {} for the same. For dates use the format: yyyy-MM-dd'T'HH:mm:ss. Add +1 country code for phone numbers only if phone number is present in the json struture given. Return strong passwords for password field only if password is present in the json context given. Please provide full form values for all attributes in provided json structure".format(
                                                GPTcontent)}
                                        ]
                                    )
                                content = response['choices'][0]['message']['content']
                                # print("content")
                                # print(content)
                                content_json = content.split("{", 1)[1]
                                print(content_json)
                                content_json = "{" + \
                                    content_json.rsplit("}", 1)[0] + "}"
                                print("GPT content")
                                print(content_json)
                                content_json = json.loads(content_json)
                                print("GENERATED JSON FROM GPT")
                                print(content_json)
                                return content_json,exmple, isFormData
    except Exception as e:
        print(traceback.format_exc())
    return '',exmple,isFormData




def getParamFromAlreadyGeneratedValues(allJsonKeyValues, param):
    print("param: "+ param)
    paramSet = set()
    for i in allJsonKeyValues:
        for j in i:
            if len(paramSet) > 10:
                break
            param_new  = param
            if param_new[-1] =='s':
                param_new = param_new[:-1]
            if param_new.lower() in j.lower() or j.lower() in param_new.lower() or similar(j.lower(),param_new.lower()) > 0.85:
                paramSet.add(i[j])
    return paramSet


def getParamFromChatGPT(postUrl, param, allJsonKeyValues):
    response2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                     "content": "You are working with HTTP POST request URLs. You will only provide a single word output."},
            {"role": "user", "content": "Can you give one valid path param value for the {} param in the POST URL {} without any other information. If you are unable to generate a value provide one unique identifier without any other information or text.Do not use abbreviations. Output should be a single word.".format(
                param, postUrl)}
        ]
    )

    content2 = response2['choices'][0]['message']['content']
    if content2.endswith("."):
        content2 = content2[:-1]

    if "\"" in content2 or "\'" in content2:
        match = re.search(
            r'"([^"]*)"', content2) or re.search(r"'([^']*)'", content2)
        content2 = match.group(1)

    data = {}
    data[param] = content2
    allJsonKeyValues.append(flatten(data))

    print(allJsonKeyValues)
    return content2


def processPostID(allJsonKeyValues, postUrl, postUrlIDVariation,microservices, logger_helper):
    if "{" not in postUrl:
        postUrlIDVariation.add(postUrl)
    else:
        for ms in microservices:
            host = ms['host']
            methodToRequestMap = ms['methodToRequestMap']
            for key in methodToRequestMap:
                if (key == "POST"):
                    requestList = methodToRequestMap[key]
                    for ele in requestList:
                        url = host + ele['url']
                        print(ele)
                        if (postUrl == url):
                            if 'pathParamExample' in ele.keys():
                                resp = ele['pathParamExample']
                                resp = json.loads(resp)
                                var = postUrl
                                for key in resp.keys():
                                    var = var.replace("{"+key+"}", str(resp[key]))
                                print(type(postUrlIDVariation))
                                postUrlIDVariation.add(var)
                                 

        allParams = re.findall('\{.*?\}', postUrl)
        print("URL PARAMS")
        print(allParams)
        for param in allParams:
            paramValues = getParamFromAlreadyGeneratedValues(
                allJsonKeyValues, param)
            if len(paramValues) == 0:
                paramFromChatGPT = getParamFromChatGPT(
                    postUrl, param, allJsonKeyValues)
                if (len(paramFromChatGPT) > 0):
                    stringVal = str(paramFromChatGPT)
                    tmp = postUrl
                    postUrl = postUrl.replace(param, stringVal)
                    postUrlIDVariation.add(postUrl)
                else:
                    tmp = postUrl
                    if "id" in param.lower():
                        postUrl = postUrl.replace(param, "1")
                        postUrlIDVariation.add(postUrl)
                    else:
                        postUrl = postUrl.replace(param, "")
                        postUrlIDVariation.add(postUrl)
            else:
                for p in paramValues:
                    tmp = postUrl
                    stringVal = str(p)
                    postUrl = postUrl.replace(param, stringVal)
                    postUrlIDVariation.add(postUrl)


def processGetRequests(allJsonKeyValues, getUrl, tmp, allIdFields,microservices, logg_helper):
    print(type(tmp), tmp)
    if "{" not in getUrl:
        tmp.add(getUrl)
    else:
        for ms in microservices:
            host = ms['host']
            methodToRequestMap = ms['methodToRequestMap']
            for key in methodToRequestMap:
                if (key == "GET"):
                    requestList = methodToRequestMap[key]
                    for ele in requestList:
                        url = host + ele['url']
                        print(ele)
                        if (getUrl == url):
                            if 'pathParamExample' in ele.keys():
                                resp = ele['pathParamExample']
                                resp = json.loads(resp)
                                var = getUrl
                                for key in resp.keys():
                                    var = var.replace("{"+key+"}", str(resp[key]))
                                print(type(tmp))
                                tmp.add(var)

        allParams = re.findall('{(.+?)}', getUrl)
        print("after regex")
        print(allParams)
        for param in allParams:
            paramValues = getParamFromAlreadyGeneratedValues(
                allJsonKeyValues, param)
            print(paramValues)
            for p in paramValues:
                url = getUrl
                url = url.replace("{"+param+"}", str(p))
                tmp.add(url)
                paramOnly = param.replace("{", "").replace("}", "")
                if paramOnly not in allIdFields:
                    allIdFields[paramOnly] = paramValues
                else:
                    allIdFields[paramOnly].update(paramValues)


def replaceAdditionalParams(processedUrls, logger_helper):
    try:
        remove = []
        add = []
        for url in processedUrls:
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": "You are generating HTTP GET request url"},
                        {"role": "user", "content": "Replace the params between braces in the url {} with one realistic example value. Provide only the url as a response without any explanation.".format(
                                                    url)}
                    ]
                )
            remove.append(url)
            add.append(response['choices'][0]['message']['content'])
        for j in remove:
            processedUrls.remove(j)
        for j in add:
            processedUrls.append(j)

    except Exception as e:
        print(traceback.format_exc())
    
    return processedUrls[0] if processedUrls else []


def getPutValuesForJson(jsonStr, idJsonLoad):
    content_json = ''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that provides sample json data for HTTP PUT requests using the same context as the previous POST and GET requests."},
                {"role": "user", "content": "using the same context and reusing the id fields from the json {} provide one json data that follows the json structure: {}. Don't add any additional attributes and respond with only a json without additional information.".format(
                                            idJsonLoad, jsonStr)},
                {"role": "user", "content": "Using the same context, substitute existing attributes present in the json with United States related data for each field and don't add additional attributes to the json and return only the json response without any extra text."}
            ]
        )
        content = response['choices'][0]['message']['content']
        content_json = content.split("{", 1)[1]
        content_json = "{" + \
            content_json.rsplit("}", 1)[0] + "}"
        content_json = json.loads(content_json)
        print("Generated Json")
        print(content_json)
        return content_json
    except Exception as e:
        print(traceback.format_exc())
    return content_json


def process_response_post(resp,url,body,GPTcontent,prevRespJson,allJsonKeyValues):
    try:
        try:
            resp_val = int(resp.text)
            if isinstance(resp_val, int):
                allJsonKeyValues.append({"id":resp_val})
                prevRespJson.append(str({"id":resp_val}))
                return 
        except:
            pass

        GPTcontent.append(body)
        id_gen = url.split("/")[-1]
        id_gen = id_gen[:-1]
        resp_json = {}
        try:
            resp = resp.json()
        except:
            resp = ""
        if resp != "" and resp:
            print("response")
            print(resp)
            for key in resp:
                if key == 'id':
                    resp_json[id_gen + key] = resp[key]
                else:
                    resp_json[key] = resp[key]

            print("flatten the data")
            print(resp_json)
            flatten_resp = flatten(resp_json)
            delete_key(flatten_resp, '_links')
            allJsonKeyValues.append(flatten_resp)
            prevRespJson.append(str(flatten_resp))
            print("prev")
            print(prevRespJson)
    
    except Exception as e:
        print(traceback.format_exc())


def pre_run(microservices, logger):
    # # authenticate using  username and password
    # authentication = {
    #     "email": "admin@example.com",
    #     "password": "1password"
    # }

    # #  get the auth token and customer id
    # login_url = "http://localhost:8080/auth"
    # resp = requests.post(login_url, json=authentication)
    token = ""  # resp.json()['token']
    print(token)
    allJsonKeyValues = []
    prevRespJson = []
    GPTcontent = []
    run(microservices, token, allJsonKeyValues, prevRespJson, GPTcontent, logger)


def run(microservices, token, allJsonKeyValues, prevRespJson, GPTcontent, logger):
    login_url = ""  # "http://localhost:8080/auth"
    finalReqs = {}
    finalReqs['POST'] = {}
    finalReqs['GET'] = {}
    finalReqs['PUT'] = {}
    finalReqs['DELETE'] = {}
    finalReqs['PATCH'] = {}
    const_no = str(random.randint(-5,6))
    const_no2 = '10001'
    const_str = "xyz"
    # const_no_neg = "-123"
    # const_no_big = "123456789012345678901234567890123456789012345678901234567890"
    # const_no_exp = "6.921106675869019E-34"

    for ms in microservices:
        host = ms['host']
        methodToRequestMap = ms['methodToRequestMap']
        for key in methodToRequestMap:
            if (key == "POST"):
                requestList = methodToRequestMap[key]
                for ele in requestList:
                    url = host + ele['url']
                    finalReqs['POST'][url] = ""
            elif (key == "GET"):
                requestList = methodToRequestMap[key]
                for ele in requestList:
                    url = host + ele['url']
                    finalReqs['GET'][url] = ""
            elif (key == "PUT"):
                requestList = methodToRequestMap[key]
                for ele in requestList:
                    if 'body' in ele:
                        url = host + ele['url']
                        exm = json.loads(ele['example'])
                        finalReqs['PUT'][url] = exm
            elif (key == "DELETE"):
                requestList = methodToRequestMap[key]
                for ele in requestList:
                    url = host + ele['url']
                    finalReqs['DELETE'][url] = ""
            elif (key == "PATCH"):
                requestList = methodToRequestMap[key]
                for ele in requestList:
                    if 'body' in ele:
                        url = host + ele['url']
                        exm = json.loads(ele['example'])
                        finalReqs['PATCH'][url] = exm
    
    print("ALL REQUESTS")
    print(finalReqs)


    urls = ",".join(finalReqs['POST'].keys())
    print("POST BEFORE ORDERING")
    print(urls)
    if urls:
        urlList = urls.split(",")
        if len(urlList) > 2:
            response2 = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are working with HTTP POST request URLs"},
                    {"role": "user", "content": "Can you logically order these POST URLs without any additional information as a comma separated line {}. Return only the urls as a comma separated string".format(
                        urls)}
                ]
            )

            content2 = response2['choices'][0]['message']['content']
            urlList = [x.strip() for x in content2.split(',')]

        if login_url in urlList:
            urlList.remove(login_url)
        print("LOGICAL ORDERING")
        print(urlList)

        logger_helper = {}
        for url in urlList:
            if url.endswith('.'):
                url = url[:-1]

            isFormData = False
            body_processed, body_def, isFormData = getBodyForUrl(url, prevRespJson, GPTcontent, isFormData)
            body_arr = []
            if body_processed:
                body_arr.append(body_processed)
            if body_def:
                body_arr.append(body_def)
            
            # newly added code for no body cases
            if len(body_arr) == 0:
                body = ""
                print("came here")
                postUrlIDVariation = set()
                processPostID(allJsonKeyValues, url,postUrlIDVariation,microservices, logger_helper)
                for postUrl in postUrlIDVariation:
                    if '{' not in postUrl:
                        print(" POST URL : " + postUrl)
                        try:
                            resp = {}
                            headers = {'X-Auth-Token': token}
                            if isFormData:
                                headers['Content-type'] ='application/x-www-form-urlencoded'
                                resp = requests.post(
                                    postUrl, json=body, headers=headers)
                            else:
                                resp = requests.post(postUrl, json=body, headers=headers)
                            print(resp.status_code)
                            if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)
                                
                            if resp.status_code == 401:
                                print("PROCESS 401")
                                try:
                                    f = open("../input/config.json")
                                    headers = json.load(f)
                                except:
                                    pass

                                if isFormData:
                                    headers['Content-type'] ='application/x-www-form-urlencoded'
                                    resp = requests.post(
                                        postUrl, json=body, headers=headers)
                                else:
                                    resp = requests.post(postUrl, json=body, headers=headers)
                                print("401 FOLLOW UP: " + str(resp.status_code))
                                if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                    process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)
                            

                        except Exception as e:
                            print(traceback.format_exc())

            # newly added code ended

            print("body arr")
            print(body_arr)
            for body in body_arr:
                print(body)
                if body:
                    print("body")
                    print(body)
                    if isinstance(body, list):
                        for bdy_json in body:
                            if isinstance(bdy_json, str):
                                continue
                            else:
                                print(bdy_json)
                                flatten_resp = flatten(bdy_json)
                                delete_key(flatten_resp, '_links')
                                allJsonKeyValues.append(flatten_resp)
                    else:
                        flatten_resp = flatten(body)
                        delete_key(flatten_resp, '_links')
                        allJsonKeyValues.append(flatten_resp)

                postUrlIDVariation = set()
                cov_url_no = ''
                cov_url_str = ''

                if '{' in url:
                    allParams = re.findall('{(.+?)}', url)
                    cov_url_no = url
                    cov_url_str = url
                    for param in allParams:
                        cov_url_no = cov_url_no.replace("{"+param+"}", const_no2)
                    postUrlIDVariation.add(cov_url_no)

                    for param in allParams:
                        cov_url_str = cov_url_str.replace("{"+param+"}", const_str)
                    postUrlIDVariation.add(cov_url_str)


                processPostID(allJsonKeyValues, url,postUrlIDVariation,microservices, logger_helper)


                print("new changes")
                print(postUrlIDVariation)

                for postUrl in postUrlIDVariation:
                    if "}" in postUrl:
                        print("came here")
                        postUrl = replaceAdditionalParams([postUrl], logger_helper)
                        print("postURL: "+ postUrl)
                    if '{' not in postUrl:
                        print(" POST URL : " + postUrl)
                        try:
                            resp = {}
                            headers = {'X-Auth-Token': token}
                            if isFormData:
                                headers['Content-type'] ='application/x-www-form-urlencoded'
                                resp = requests.post(
                                    postUrl, json=body, headers=headers)
                            else:
                                resp = requests.post(postUrl, json=body, headers=headers)
                            print(resp.status_code)
                            if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)
                                
                            if resp.status_code == 401:
                                print("PROCESS 401")
                                try:
                                    f = open("../input/config.json")
                                    headers = json.load(f)
                                except:
                                    pass

                                if isFormData:
                                    headers['Content-type'] ='application/x-www-form-urlencoded'
                                    resp = requests.post(
                                        postUrl, json=body, headers=headers)
                                else:
                                    resp = requests.post(postUrl, json=body, headers=headers)
                                print("401 FOLLOW UP: " + str(resp.status_code))
                                if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                    process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)
                            
                                # try to delete certain params like 'date' that can cause these errors
                            if resp.status_code == 400:
                                print("PROCESS 400")
                                body_new = body
                                delete_key(body_new, "date")
                                if isFormData:
                                    headers['Content-type'] ='application/x-www-form-urlencoded'
                                    resp = requests.post(
                                        postUrl, json=body_new, headers=headers)
                                else:
                                    resp = requests.post(postUrl, json=body_new, headers=headers)
                                print("401 FOLLOW UP: "+str(resp.status_code))
                                if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                    process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)
                                
                                # handle cases where Id's are default and dates are missmatched
                                if resp.status_code == 400:
                                    print("PROCESS FOLLOW UP 400")
                                    body_new = body
                                    delete_key(body_new, "date")
                                    delete_key(body_new, "Time")
                                    post_checker = postUrl.split("localhost:")[1]
                                    post_checker = post_checker.split("/")[1]
                                    keys_to_delete = []
                                    if isinstance(body_new, dict):
                                        for key in body_new.keys():
                                            if similar(key.lower(),"id") > 0.95:
                                                keys_to_delete.append(key)
                                            if similar(key.lower(),post_checker.lower())>0.60:
                                                keys_to_delete.append(key)
                                    
                                    for key in keys_to_delete:
                                        delete_key(body_new, key)
                                     
                                    print(body_new)
                                    if isFormData:
                                        headers['Content-type'] ='application/x-www-form-urlencoded'
                                        resp = requests.post(
                                            postUrl, json=body_new, headers=headers)
                                    else:
                                        resp = requests.post(postUrl, json=body_new, headers=headers)
                                    print("401 FOLLOW UP TWICE: "+str(resp.status_code))
                                    if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                                        process_response_post(resp, url,body,GPTcontent,prevRespJson,allJsonKeyValues)


                        except Exception as e:
                            print(traceback.format_exc())

            postUrlIDVariation = []

    # print("ALL VALUES ")
    # print(allJsonKeyValues)
    allIdFields = {}
    logger_helper = {}
    print("START GET REQUESTS")
    getUrlsProcessed = []

    # logically order the get requests
    ordered_url = []
    for url in finalReqs['GET'].keys():
        if "{" not in url:
            ordered_url.append(url)

    for url in finalReqs['GET'].keys():
        if "{" in url:
            ordered_url.append(url)

    getUrlsProcessed = ordered_url

    print("ALL GET URLS")
    print(getUrlsProcessed)
    for i in getUrlsProcessed:
        print("GET URL :" + i)
        tmp = set()
        cov_url_no = ''
        cov_url_str = ''

        if '{' in i:
            allParams = re.findall('{(.+?)}', i)
            cov_url_no = i
            cov_url_str = i
            for param in allParams:
                cov_url_no = cov_url_no.replace("{"+param+"}", const_no)
            tmp.add(cov_url_no)

            for param in allParams:
                cov_url_str = cov_url_str.replace("{"+param+"}", const_str)
            tmp.add(cov_url_str)

            random_int_neg = randint(-1*1000, 0)
            random_int_small = randint(1 , 1000)
            random_int_big = randint(10**5 , 10**10)
            random_int_deci = (randint(1 , 5000))/100
            random_integers = [random_int_neg,random_int_small,random_int_big,random_int_deci]
            for rnd in random_integers:
                print("random number generated: "+str(rnd))
                const_url = i
                for param in allParams:
                    const_url = const_url.replace("{"+param+"}", str(rnd))
                tmp.add(const_url)
            
            randomizer = ['121','-451','32','abcd','baab','xyz','and','for']
            random_url = i
            for param in allParams:
                random_url = random_url.replace("{"+param+"}", str(random.choice(randomizer)))
            tmp.add(random_url)
            print("url after random generation: "+ random_url)
        
        tmp.add(i)
        processGetRequests(allJsonKeyValues, i,
                           tmp, allIdFields,microservices, logger_helper)
        print("all URL's to query")
        try:
            for url in tmp:
                processed_url = replaceAdditionalParams([url], logger_helper)
                if '{' not in processed_url:
                    print("get url: " + processed_url)
                    headers = {'accept': '*/*'}
                    resp = requests.get(processed_url, headers=headers)
                    print(resp.status_code)
                    if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                        # print("response")
                        # print(resp.text)
                        try:
                            inter_json = resp.json()
                            prevRespJson.append(str(inter_json))
                            limit = 0 
                            if isinstance(inter_json, list):
                                for resp_jsn in inter_json:
                                    if resp_jsn is not None:
                                        if limit > 1:
                                            break
                                        flatten_resp = flatten(resp_jsn)
                                        delete_key(flatten_resp, '_links')
                                        size = len(flatten_resp)
                                        if size <= 100 and flatten_resp:
                                            allJsonKeyValues.append(flatten_resp)
                                            prevRespJson.append(str(flatten_resp))
                                        limit += 1
                            else:
                                flatten_resp = flatten(resp_jsn)
                                delete_key(flatten_resp, '_links')
                                size = len(flatten_resp)
                                if size <= 100 and flatten_resp:
                                    allJsonKeyValues.append(flatten_resp)
                                    prevRespJson.append(str(flatten_resp))
                        except:
                            pass

                    if resp.status_code == 401:
                        print("PROCESS 401")
                        try:
                            f = open("../input/config.json")
                            headers = json.load(f)
                            headers['accept'] = '*/*'
                        except:
                            pass
                        resp = requests.get(processed_url, headers=headers)
                        print("401 FOLLOW UP: "+str(resp.status_code))
                        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                            # print("response")
                            # print(resp.text)
                            try:
                                inter_json = resp.json()
                                prevRespJson.append(str(inter_json))
                                limit = 0 
                                if isinstance(inter_json, list):
                                    for resp_jsn in inter_json:
                                        if resp_jsn is not None:
                                            if limit > 1:
                                                break
                                            flatten_resp = flatten(resp_jsn)
                                            delete_key(flatten_resp, '_links')
                                            size = len(flatten_resp)
                                            if size <= 100 and flatten_resp:
                                                allJsonKeyValues.append(flatten_resp)
                                                prevRespJson.append(str(flatten_resp))
                                            limit += 1
                                else:
                                    flatten_resp = flatten(resp_jsn)
                                    delete_key(flatten_resp, '_links')
                                    size = len(flatten_resp)
                                    if size <= 100 and flatten_resp:
                                        allJsonKeyValues.append(flatten_resp)
                                        prevRespJson.append(str(flatten_resp))
                            except:
                                pass
                    
        except Exception as e:
            print(traceback.format_exc())

    print("START PUT REQUESTS")
    finalProcessedPutReqs = {}
    logger_helper = {}
    for k in finalReqs['PUT'].keys():
        putUrlsProcessed = set()
        processGetRequests(allJsonKeyValues, k,
                           putUrlsProcessed, allIdFields,microservices, logger_helper)
        putUrlsProcessed = list(putUrlsProcessed)
        replaceAdditionalParams(putUrlsProcessed, logger_helper)
        for j in putUrlsProcessed:
            finalProcessedPutReqs[j] = finalReqs['PUT'][k]

    idJsonDump = json.dumps(allIdFields, default=set_default)
    idJsonLoad = json.loads(idJsonDump)

    for i in finalProcessedPutReqs:
        if '{' not in i:
            print("PUT URL : " + i)
            body_processed = getPutValuesForJson(finalProcessedPutReqs[i], idJsonLoad)
            body_arr = []
            if body_processed:
                body_arr.append(body_processed)
            if finalProcessedPutReqs[i]:
                body_arr.append(finalProcessedPutReqs[i])

            for body in body_arr:
                try:
                    headers = {'accept': '*/*'}
                    resp = requests.put(i, json=body, headers=headers)
                    print(resp.status_code)
                    if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                        flatten_resp = flatten(resp.json())
                        delete_key(flatten_resp, '_links')
                        allJsonKeyValues.append(flatten_resp)
                        prevRespJson.append(str(flatten_resp))
                    
                    if resp.status_code == 401:
                        print("PROCESS 401")
                        try:
                            f = open("../input/config.json")
                            headers = json.load(f)
                            headers['accept'] = '*/*'
                        except:
                            pass

                        resp = requests.put(i, json=body, headers=headers) 
                        print("401 FOLLOW UP: " + str(resp.status_code))
                        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                            flatten_resp = flatten(resp.json())
                            delete_key(flatten_resp, '_links')
                            allJsonKeyValues.append(flatten_resp)
                            prevRespJson.append(str(flatten_resp))

                except Exception as e:
                    print(traceback.format_exc())

    print("START PATCH REQUESTS")
    finalProcessedPatchReqs = {}
    logger_helper = {}
    for k in finalReqs['PATCH'].keys():
        putUrlsProcessed = set()
        processGetRequests(allJsonKeyValues, k,
                           putUrlsProcessed, allIdFields,microservices, logger_helper)
        putUrlsProcessed = list(putUrlsProcessed)
        replaceAdditionalParams(putUrlsProcessed, logger_helper)
        for j in putUrlsProcessed:
            finalProcessedPatchReqs[j] = finalReqs['PATCH'][k]

    idJsonDump = json.dumps(allIdFields, default=set_default)
    idJsonLoad = json.loads(idJsonDump)
    print(idJsonLoad)

    for i in finalProcessedPatchReqs:
        if '{' not in i:
            print("patch url: "+ i)
            body_processed = getPutValuesForJson(finalProcessedPatchReqs[i], idJsonLoad)
            body_arr = []
            if body_processed:
                body_arr.append(body_processed)
            if finalProcessedPatchReqs[i]:
                body_arr.append(finalProcessedPatchReqs[i])

            for body in body_arr:
                try:
                    headers = {'accept': '*/*'}
                    resp = requests.patch(i, json=body, headers=headers)
                    print(resp.status_code)
                    # logger['PATCH'][logger_helper[i]][resp.status_code] += 1
                    # print("response: ")
                    # print(resp)
                    if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                        flatten_resp = flatten(resp.json())
                        delete_key(flatten_resp, '_links')
                        allJsonKeyValues.append(flatten_resp)
                        prevRespJson.append(str(flatten_resp))

                    if resp.status_code == 401:
                        print("PROCESS 401")
                        try:
                            f = open("../input/config.json")
                            headers = json.load(f)
                            headers['accept'] = '*/*'
                        except:
                            pass

                        resp = requests.patch(i, json=body, headers=headers) 
                        print("401 FOLLOW UP: " + str(resp.status_code))
                        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                            flatten_resp = flatten(resp.json())
                            delete_key(flatten_resp, '_links')
                            allJsonKeyValues.append(flatten_resp)
                            prevRespJson.append(str(flatten_resp))

                except:
                    print(traceback.format_exc())

    print("START DELETE REQUESTS")
    deleteUrlsProcessed = set()
    logger_helper = {}
    for k in finalReqs['DELETE'].keys():
        processGetRequests(allJsonKeyValues, k, deleteUrlsProcessed, allIdFields,microservices, logger_helper)

        deleteUrlsProcessed = list(deleteUrlsProcessed)
        replaceAdditionalParams(deleteUrlsProcessed, logger_helper)
        deleteUrlsProcessed = set(deleteUrlsProcessed)
        # logger_helper[deleteUrlsProcessed[-1]] = k
    
    # print(deleteUrlsProcessed)

    for i in deleteUrlsProcessed:
        if '{' not in i:
            print("DELETE URL :" + i)
            try:
                headers = {'accept': '*/*'}
                resp = requests.delete(i, json=body, headers=headers)
                print(resp.status_code)
                # logger['DELETE'][logger_helper[i]][resp.status_code] += 1
                # if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 204:
                #     prevRespJson.append(str(resp.json()))
                #     allJsonKeyValues.append(flatten(resp.json()))

                if resp.status_code == 401:
                    print("PROCESS 401")
                    try:
                        f = open("../input/config.json")
                        headers = json.load(f)
                        headers['accept'] = '*/*'
                    except:
                        pass
                    resp = requests.delete(i, json=body, headers=headers)
                    print("401 FOLLOW UP: " + str(resp.status_code))
                
            except:
                print(traceback.format_exc())


if __name__ == "__main__":
    # chat GPT code to get data suggestions
    service = port = sys.argv[1]
    time.sleep(100)
    openai.organization = os.getenv("OPENAI_ORGANIZATION")

    # read the pojo with the required data type ( please input the file location of struct.json)
    # please input the unified swagger json
    f = open('/home/amd/REST_Go/UIUC-API-Tester/output/uiuc-api-tester-'+str(service)+'.json')
    # f = open('output.json')
    microservices = json.load(f)
    logger_write = []

    # track 1
    for i in range(10):
        try:
            print("run started for : " + str(i))
            logger = {}
            logger['POST'] = {}
            logger['POST'] = {}
            logger['GET'] = {}
            logger['PUT'] = {}
            logger['DELETE'] = {}
            logger['PATCH'] = {}
            pre_run(microservices, logger)

        except Exception as e:
            print("this exception should not happen")
            print(traceback.format_exc())

    print(" track 1 done")

    # track 2
    # dependency_file = open('dependency.json')
    # json_dict = json.load(dependency_file)

    # if json_dict:
    #     string_sequence = string_helper(json_dict)
    #     string_list = [x.split(",") for x in string_sequence]

    #     for sequence in string_list:
    #         for i in range(1,3):
    #             # authenticate using  username and password
    #             authentication = {
    #                 "email": "admin@example.com",
    #                 "password": "1password"
    #             }

    #             #  get the auth token and customer id
    #             login_url = "http://localhost:8080/auth"
    #             resp = requests.post(login_url, json=authentication)
    #             token = resp.json()['token']
    #             allJsonKeyValues = []
    #             prevRespJson = []
    #             for service in sequence:
    #                 print(service)
    #                 for swagger_service in microservices:
    #                     if swagger_service['microservice'] in service.strip() or service.strip() in swagger_service['microservice']:
    #                         formatted_json = []
    #                         formatted_json.append(swagger_service)
    #                         try:
    #                             run(formatted_json, token, allJsonKeyValues, prevRespJson)
    #                         except Exception as e:
    #                             print("An exception occurred in track 2")
    #                             print(traceback.format_exc())
    #                             print(e)
