import sys
import os
import subprocess
import json

if __name__ == "__main__":
    curdir = os.getcwd()
    chat_gpt_api_key = {"apikey": sys.argv[1]}

    print("Building Unified Swagger Generation Code")
    subprocess.run("cd UIUC-API-Tester/open-api-processor && mvn clean package", shell=True)
    print("Setting ChatGPT API key")
    config_file_path = os.path.join(curdir, "UIUC-API-Tester/input/constants.json")
    with open(config_file_path, 'w+') as fd:
        fd.write(json.dumps(chat_gpt_api_key))