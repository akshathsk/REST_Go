# UIUC API Tester - RestGPT
RestGPT automatically tests the REST based projects with the help of GPT3.5 APIs. 
This document gives detailed description of the flow of the tool and its working.
For running the tool, follow the below sections in order.

## Installations
Run the commands below to install dependencies. This project requires python3.
- ```pip3 install openai```
- ```pip3 install pandas```
- ```pip3 install hashlib```
- ```pip3 install openpyxl```
- ```pip3 install xlsxwriter```

## Enum generation

#### Already Generated enums
For the projects under study, we have generated the enums at this [location](https://github.com/akshathsk/REST_Go/tree/UIUC-API-Tester/UIUC-API-Tester/input/enum-props)
</br>
To generate enums for new project, please follow below sections.
#### Requirements
To generate enums for a service, we need to have CodeQL setup on the system.
Please refer to CodeQL official docs to set up it on your system: https://codeql.github.com/

#### How to Run
- Import codebase as database in CodeQL. Sample query to import database: </br>
Execute this query at root directory of project - </br>
``codeql database create <location_of_folder_where_database_needs_to_be_stored> --language=java``
- This will create folder at root directory of project with name as ``<path_till_root_location>-codeql>``
- Open VSCode (assuming CodeQL extension is installed on VSCode)
- Import the database by selecting folder generated in above step ``<path_till_root_location>-codeql>``
- Select the imported Database as target database in CodeQL
- Execute this codeQL query: 
```
import java

from EnumType e

where 
  e.getFile().getAbsolutePath().matches("%src/main/java%")

select 
  e.getName(),
  e.getAnEnumConstant(),
  e.getFile().getAbsolutePath(),
  e.getLocation()
```

- Store the generated results as csv at ```UIUC-API-Tester/input/codeql_csv/``` with filename ```{service_name}_results.csv``` . Here service name can also be interpretted as project name (the project for which codeql was run). The final path will look like ```UIUC-API-Tester/input/codeql_csv/{service_name}_results.csv```

- Generate the enum in json format from the CSV by navigating to ```UIUC-API-Tester/APITester``` and running the command ```python3 codeql_enum_analysis.py {service_name}```.

- This script will generate a json file in the location ```UIUC-API-Tester/input/enum-props/output_enum_{service_name}.json``` with the enum information.




## Running the tool

### Configure openAI key and generating unified swagger generating jar

For setup execute the command ``python3 uiuc_tool_setup.py <openai_api_key>`` under the ```RESTGO/``` directory scope.

### Automated

To run all the script at once with a single python file, run the command ```python3 uiuc_tool_tester.py {port} {service_name} {enable_gpt_logs} {runs}```. Here, ```enable_gpt_logs``` should be filled with ```True/False``` and ```runs``` indicates the number of times the tool should run for one execution. This is defaulted to 10 if no input is given. 

### Manually

To run all scripts manually, follow the steps below.

#### 1. Unified Swagger File generation

##### Purpose 
This module generates a ``<servicename>_swagger.json`` file which is derived from swagger file 
of the application. This generated file along with enum generated from ``Step-2``, generates 
a json file which has all endpoints, their call-type, example object of request body, query param.
These examples of request body are used in ``Step-3`` to pass it to GPT as a context.

##### Requirements
1. ``Java-11``
2. Swagger file of respective project
3. Codebase - ``UIUC-API-Tester/open-api-processor``

##### How to Run
1. ``cd target``
2. Execute - </br>
``java -jar open-api-processor-1.0-SNAPSHOT-jar-with-dependencies.jar <path_to_folder_with_project_swagger> <path_to_output_folder> <project_name>``
3. Step-3 will generated ``<project_name>_swagger.json`` at ``<path_to_output_folder>`` location

##### Sample Input and Output

###### Input
Sample input of swagger file: [features_swagger.json](https://github.com/akshathsk/REST_Go/blob/UIUC-API-Tester/doc/features_swagger.json)
###### Output
Sample output of unified swagger file: [features-service_swagger.json](https://github.com/akshathsk/REST_Go/blob/UIUC-API-Tester/UIUC-API-Tester/input/swagger/features-service_swagger.json)


#### 2. Using enum with unified json
The project uses the enum's to replace certain attributes in the body during the request. Our tool already takes the unified swagger as input and to simplify the process, we integrate the enum to that swagger. to do that,

- Make sure to complete step - Unified Swagger File generation
- Navigate to the location ```UIUC-API-Tester/APITester``` and run the enum integration script using the command ```python3 integrate_enum.py {service_name}```
- This script will read the swagger and the enums, and integrate it in a way that chatGPT can understand.
- on successful execution of the script, the final swagger will be generated in the location ```UIUC-API-Tester/output/``` with the name ```uiuc-api-tester-{service_name}.json```. This json will be the input for the main tool script.

#### 3. Start the service and jacoco
Before we begin with the execution of our tool, we need to start the service and jacoco agent.
- Navigate to the root of the RESTGO project which is ```RESTGO/```. If you are in the ``UIUC-API-Tester`` directory, the command would be ```cd ..```
- Execute the following command ```python3 run_service.py {service_name} {port_number} blackbox```. Please make sure to check the spelling of the service name and also to make a note of the port number.
- Next, execute the shell script that brings up jacoco agent with the command ```sh get_cov.sh {port_number}```. Make sure to give the same port number. This step will start the jacoco agent and it generates the coverage for every 10 minutes in a executable file in the ```RESTGO/``` location with the name ```jacoco_{port_number}_{minute_number}.exe```. Here, ```minute_number``` will have values ```1,2,3,4,5,6``` indicating the jacoco executable generation for ```10,20,30,40,50,60``` minutes. Please , complete step 4 (next step) as soon as possible after starting the jacoco agent.
- The jacoc agent runs for 60 minutes and then we can generate the report.


#### 4. Running the tool with the help of GPT 3.5 APIs and generated Unified Swagger
After successful completion of previous steps, we will have the final swagger ready in the location ```UIUC-API-Tester/output/uiuc-api-tester-{service_name}.json```, service running and the jacoco agent started. Now we are ready to run our tool.

- Navigate to the location ```UIUC-API-Tester/APITester``` and run the script using the command ```python3 uiuc_api_tester.py {service_name} {enable_gpt_logs - True/False} {runs} > logs/restgpt_log__{port_number}.txt```. Here, ```runs``` indicates the number of times the tool should run for one execution. This is defaulted to 10 if no input is given. The tool will generate 2 files as it runs.

- The first file is the GPT logs for re-using the GPT produced data. This log file will be genereted in the location ```UIUC-API-Tester/APITester/gptlogs/{service_name}.txt```.

- The second file is the logs generated by the tool. This file will be generated in the location ```UIUC-API-Tester/APITester/logs/restgpt_logs_{port_number}.txt```

- For REST API testing we use track 1 of the python script.

- For microservices, we run track 2 also of the python script. For this, input the reverse topological ordering in the location ```UIUC-API-Tester/input/Sequence/{service}.json```


## Generating the report
After the jacoco agent is run for 1 hour, we should be able to see 6 jacoco executables in the ```RESTGO/``` directory. 
- create a directory using the command ```mkdir data```
- Navigate into data using ```cd data``` and create a folder for each service using ```mkdir {service_name}```
- from the root directory ```RESTGO/``` , run the command ```pytho3 report.py {port} {name} {tool_name}```.
- This will generate a csv file called ```res.csv``` with the coverage report at the location ```RESTGO/data/{service_name}/res.csv```


## formatting all results to one excel
For comparison, inorder to ease the process, there is a script that can iterate though all the ```res.csv``` from each service and the respective tool. This will ouput a file in the ```RESTGO/``` directoy with the name ```{tool_name}_results_{date}.xlsx```. 

- Make sure that ```RESTGO/data``` directory exists. If not, please follow steps from above properly. 
- To achieve this, from ```RESTGO/``` directory, run the command ```python3 tool_report.py {tool_name}```.
- Incase this is running on a VM, xlsx formats might be difficult to open in editors like vi . So we can scp the excel file to the local machine using the command ```scp user@remote:<path>/<filename>  <location in local machine>```

