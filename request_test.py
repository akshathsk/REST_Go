import requests
import openai
import os
import json
import re
import traceback
import collections
from functools import (partial,
                       singledispatch)
from itertools import chain
from typing import (Dict,
                    List,
                    TypeVar)
import time
import re

from collections import MutableMapping
crumbs = True
def flatten(dictionary, parent_key=False, separator='.'):


    items = []
    for key, value in dictionary.items():
        # if crumbs: print('checking:',key)
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            if not value.items():
                # if crumbs: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
            else:
                items.extend(flatten(value, new_key, separator).items())
        elif isinstance(value, list):
            # if crumbs: print(new_key,': list found')
            if len(value):
                for k, v in enumerate(value):
                    items.extend(flatten({str(k): v}, new_key, separator).items())
            else:
                # if crumbs: print('Adding key-value pair:',new_key,None)
                items.append((new_key,None))
        else:
            # if crumbs: print('Adding key-value pair:',new_key,value)
            items.append((new_key, value))
    return dict(items)




url7 = "http://localhost:50112/api/problem"
# url6 = "http://localhost:50112/api/problem/0gn547"
# myobj = {'authorId': '1', 'country': 'USA', 'creationTime': '2022-03-31T15:30:00-07:00','newsId':'32' ,'text': 'This is a sample text message.'}
myobj = {'code': '0gn547', 'title': 'Test Title'}
# resp = requests.get(url6)
# headers = {'Content-type': 'application/vnd.tsdes.news+json;charset=UTF-8;version=2'}
resp= requests.post(url7, json = myobj)
print(resp)
print(resp.status_code)
print(resp.text)
allJsonKeyValues = []
# print(resp.json())
resp_2 = resp.json()
limit = 0

