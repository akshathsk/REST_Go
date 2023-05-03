Inorder to execute the RESTGPT tool , the following scripts need to be present in the project ( starting from root directiory RESTGO/)
1. uiuc_tool_tester.py
2. report.py
3. run_service.py
4. get_cov.sh
5. docs/(swagger files for each service)
6. UIUC-API-Tester/API-Tester/integrate_enum.py
7. UIUC-API-Tester/API-Tester/uiuc_api_tester.py
8. UIUC-API-Tester/input/enum-props/(enum json for each service)
9. UIUC-API-Tester/swagger/(processed swagger for each service)


STEPS:
1. run ```tmux ls``` to check that all services are down
2. run ```tmux kill-sess -t {session name}``` to kill services that are not required
3. select a 4 digit port number ( unique per service and please remember it)
4. run ```python3 uiuc_tool_tester.py {port} {service}```
5. after 1 hr, there will be 6 jacoco.exe in the home directory (RESTGO/) with the corresponding port name
6. before creating report, please run ```sudo mkdir data``` , ```cd data``` and ```sudo mkdir {service name}``` for each service.
7. run ```python3 report.py {port} {service} {tool name to store result}```
8. This will create a directory with the name of the tool under data/{service name} and store the result
9. run ```cd data/{service}/{tool}``` and ```vi res.cs``` to check the results
10. logs of tool will be stores in UIUC-API-Tester/API-Tester/logs/uiuc_test_{port}.txt



Things to remember:
Some projects like genome-nexus, problem-controller, person-controller, spring-batch-rest have issues with docker.
They cannot re-use a docker image and therefore, when the service is run for the second time, we face error. To overcome that, find the docker image and run the following command
1. ```sudo docker stop {image}```
2. ```sudo docker rm {image} ```

Then please run as per above steps.

