# UIUC API Tester - RestGPT
RestGPT automatically tests the REST based projects with the help of GPT3.5 APIs. 
This document gives detailed description of the flow of the tool and its working.
The tool mainly consists of three major modules - 
1. Unified Swagger File generation
2. Enum generation and its use with unified swagger
3. Running the tool with the help of GPT 3.5 APIs

## 1. Unified Swagger File generation

### Purpose 
This module generates a ``<servicename>_swagger.json`` file which is derived from swagger file 
of the application. This generated file along with enum generated from ``Step-2``, generates 
a json file which has all endpoints, their call-type, example object of request body, query param.
These examples of request body are used in ``Step-3`` to pass it to GPT as a context.

### Requirements
1. ``Java-11``
2. Swagger file of respective project
3. Codebase - ``UIUC-API-Tester/open-api-processor``

### How to Run
1. Go to root location of ``UIUC-API-Tester/open-api-processor`` and execute ``mvn clean package``
2. ``cd target``
3. Execute - </br>
``java -jar open-api-processor-1.0-SNAPSHOT-jar-with-dependencies.jar <path_to_folder_with_project_swagger> <path_to_output_folder> <project_name>``
4. Step-3 will generated ``<project_name>_swagger.json`` at ``<path_to_output_folder>`` location

### Sample Input and Output

#### Input
Sample input of swagger file: [features_swagger.json](https://github.com/akshathsk/REST_Go/blob/UIUC-API-Tester/doc/features_swagger.json)
#### Output
Sample output of unified swagger file: [features-service_swagger.json](https://github.com/akshathsk/REST_Go/blob/UIUC-API-Tester/UIUC-API-Tester/input/swagger/features-service_swagger.json)

## 2. Enum generation using it with Unified Swagger
### Generating enum

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

``<<<<SURAJ PLEASE UPDATE README FROM THIS POINT>>>>>``
- Store the generated results as csv at ...
### Using enum with unified json

## 3. Running the tool with the help of GPT 3.5 APIs and generated Unified Swagger