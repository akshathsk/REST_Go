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
<to_be_added_by_chinmay>
#### Output
<to_be_added_by_chinmay>

## 2. Enum generation using it with Unified Swagger
### Generating enum
<to_be_added_by_chinmay>

### Using enum with unified json

## 3. Running the tool with the help of GPT 3.5 APIs and generated Unified Swagger