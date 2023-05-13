import sys
import time
import subprocess
import os


def blackbox(swagger, port, service):
    curdir = os.getcwd()
    subprocess.run("cd UIUC-API-Tester/open-api-processor/target && java -jar open-api-processor-1.0-SNAPSHOT-jar-with-dependencies.jar " +
                   swagger + " " + curdir + "/UIUC-API-Tester/input/swagger" + " " + service, shell=True)
    subprocess.run(
        'cd UIUC-API-Tester/APITester && python3 integrate_enum.py '+str(service)+'', shell=True)
    subprocess.run('cd UIUC-API-Tester/APITester && python3 uiuc_api_tester.py '+str(service) +
                   ' '+str(enable_gpt_logs)+' '+runs+' > logs/restgpt_log_'+str(port)+'.txt', shell=True)
    print("restgpt tool ended")


if __name__ == "__main__":
    # this is only for blackbox. Please do not use this for whitebox testing
    global enable_gpt_logs
    global runs

    port = sys.argv[1]
    service = sys.argv[2]

    try:
        enable_gpt_logs = sys.argv[3]
        if enable_gpt_logs.lower() == 'true':
            enable_gpt_logs = True
    except:
        enable_gpt_logs = False

    runs = sys.argv[4]

    curdir = os.getcwd()

    # start the service
    subprocess.run("python3 run_service.py " + service +
                   " " + str(port) + " blackbox", shell=True)
    print("service: " + service +
          " has been started. You can check the same with tmux ls command in a new terminal")

    # initate jacoco agent
    cov_session = service + "_cov"
    subprocess.run("tmux new -d -s " + cov_session +
                   " sh get_cov.sh " + str(port), shell=True)
    print("jacoc agent initated")

    base_path = "UIUC-API-Tester/input/input_swagger/"

    blackbox(base_path+service, port, service)
