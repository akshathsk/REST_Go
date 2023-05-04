import sys
import time
import subprocess
import os


def blackbox(swagger, port, service):
    curdir = os.getcwd()
    subprocess.run("cd UIUC-API-Tester/open-api-processor/target && java -jar open-api-processor-1.0-SNAPSHOT-jar-with-dependencies.jar " + swagger + " " + curdir + "/UIUC-API-Tester/input/swagger" + " " +service, shell=True)
    subprocess.run('cd UIUC-API-Tester/APITester && python3 integrate_enum.py '+str(service)+'', shell=True)
    print("uiuc tool started")
    subprocess.run('cd UIUC-API-Tester/APITester && python3 uiuc_api_tester.py '+str(service)+' > logs/uiuc_test_'+str(port)+'.txt', shell=True)
    # subprocess.run('cd UIUC-API-Tester/APITester && python3 uiuc_api_tester.py '+str(service)+'', shell=True)
    print("uiuc tool ended")


if __name__ == "__main__":
    # this is only for blackbox. Please do not use this for whitebox testing
    port = sys.argv[1]
    service = sys.argv[2]

    curdir = os.getcwd()
    # services = ["market","user-management", "cwa-verification","ncs", "proxyprint", "restcountries", "scout-api", "erc20-rest-service", "person-controller", "rest-study", "spring-batch-rest", "project-tracking-system"]
    

    # for service in services:
        # start the service
    subprocess.run("python3 run_service.py " + service + " " + str(port) + " blackbox", shell=True)
    print("service: "+ service + " has been started. You can check the same with tmux ls command in a new terminal")

    # initate jacoco agent
    cov_session = service + "_cov"
    subprocess.run("tmux new -d -s " + cov_session + " sh get_cov.sh " + str(port), shell=True)
    print("jacoc agent initated")

    if service == "features-service":
        blackbox(os.path.join(curdir, "doc/features_swagger.json"), port, service)
    elif service == "news":
        blackbox(os.path.join(curdir, "doc/news_swagger.json"), port, service)
    elif service == 'scs':
        blackbox(os.path.join(curdir, "doc/scs_swagger.json"), port, service)
    elif service == 'ocvn':
        blackbox(os.path.join(curdir, "doc/ocvn_swagger.json"), port, service)
    elif service == 'languagetool':
        blackbox(os.path.join(curdir, "doc/languagetool_swagger.json"), port, service)
    elif service == 'genome-nexus':
        blackbox(os.path.join(curdir, "doc/genome_swagger.json"), port, service)
    elif service == 'problem-controller':
        blackbox(os.path.join(curdir, "doc/problem_swagger.json"), port, service)
    elif service == "ncs":
        blackbox(os.path.join(curdir, "doc/ncs_swagger.json"), port, service)
    elif service == "proxyprint":
        blackbox(os.path.join(curdir, "doc/proxyprint_swagger.json"), port, service)
    elif service == "restcountries":
        blackbox(os.path.join(curdir, "doc/restcountries_openapi.yaml"), port, service)
    elif service == "scout-api":
        blackbox(os.path.join(curdir, "doc/scout_swagger.json"), port, service)
    elif service == "erc20-rest-service":
        blackbox(os.path.join(curdir, "doc/erc20_swagger.json"), port, service)
    elif service == "person-controller":
        blackbox(os.path.join(curdir, "doc/person_swagger.json"), port, service)
    elif service == "rest-study":
        blackbox(os.path.join(curdir, "doc/rest_swagger.json"), port, service)
    elif service == "spring-batch-rest":
        blackbox(os.path.join(curdir, "doc/springbatch_openapi.yaml"), port, service)
    elif service == "user-management":
        blackbox(os.path.join(curdir, "doc/user_swagger.json"), port, service)
    elif service == "cwa-verification":
        blackbox(os.path.join(curdir, "doc/cwa_openapi.yaml"), port, service)
    elif service == "market":
        blackbox(os.path.join(curdir, "doc/market_swagger.json"), port, service)
    elif service == "project-tracking-system":
        blackbox(os.path.join(curdir, "doc/project_swagger.json"), port, service)
    elif service == "spring-boot-sample-app":
        blackbox(os.path.join(curdir, "doc/springboot_swagger.json"), port, service)
    else:
        print("select proper service")

        # port = port + 10


