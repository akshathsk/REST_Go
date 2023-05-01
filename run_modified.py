import sys
import time
import subprocess


def process(services, base_cov_port, tool):
    for i in range(len(services)):
        cov_port = base_cov_port + i*10
        print("Running " + tool + " for " + services[i] + ": " + str(cov_port))
        session = tool + '_' + services[i]
        cov_session = services[i] + "_cov"
        with open("run_logger.txt", 'a+') as f:
            sentence = "running " + str(session) + " on port: "+ str(cov_port)
            f.write(sentence)
        subprocess.run("tmux new -d -s " + cov_session + " sh get_cov.sh " + str(cov_port), shell=True)
        subprocess.run("tmux new -d -s " + session + " 'timeout " + str(time_limit) + "h python3 run_tool.py " + tool + ' ' + services[i] + ' ' + str(cov_port) + "'", shell=True)

    time.sleep(300)
    time.sleep(int(time_limit) * 60 * 60)
    print("stop all script started")
    subprocess.run("sh stop_all.sh", shell=True)
    for i in range(len(services)):
        subprocess.run("tmux kill-sess -t " + services[i], shell=True)
        subprocess.run("tmux kill-sess -t " + services[i] + "_cov", shell=True)
        subprocess.run("tmux kill-sess -t " + tool + '_' + services[i], shell=True)


if __name__ == "__main__":
    tool = sys.argv[1]
    service = str(sys.argv[2])
    time_limit = 1
    base_cov_port = int(sys.argv[3])

    # base_cov_port = 8010
    #services = ["scout-api","restcountries","languagetool","features-service","erc20-rest-service","ocvn","genome-nexus",]
    #services = ["proxyprint","scs", "ncs", "news", "genome-nexus", "person-controller", "problem-controller", "rest-study", "spring-batch-rest", "spring-boot-sample-app", "user-management", "cwa-verification", "market", "project-tracking-system"]
    #services = ["features-service","market","user-management", "cwa-verification","ncs", "proxyprint", "restcountries", "scout-api", "erc20-rest-service","scs", "person-controller", "problem-controller", "rest-study", "spring-batch-rest", "spring-boot-sample-app", "project-tracking-system","languagetool","news", "ocvn"]
    # services = ["news", "languagetool", "scs", "problem-controller", "genome-nexus", "ocvn"]
    index = 0
    service_numbers = 20
    # print(len(services))
    while index < 1:
        # print(services[index:index+1])
        # process(services[index:index+1], base_cov_port, tool)
        print(service)
        process([service], base_cov_port, tool)
        base_cov_port = base_cov_port + 50
        index= index + 1



