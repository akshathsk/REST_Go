#!/bin/bash

codeql_cli_dir="$HOME/codeql"
codeql_pak_dir="$HOME"
codeql_query_path="$HOME/enum-extract.ql"
codeql_dbs_dir="$HOME/codeqlDBs"
codeql_res_dir="$HOME/codeqlRes"
rest_go_dir="$HOME/REST_Go"

export PATH=$PATH:$codeql_cli_dir/

# # Detect whether qlpack.yml exists
# if [ -e "$codeql_pak_dir/qlpack.yml" ]; then
#     # If so, install the dependency
#     echo "qlpack.yml detected, start installing dependencies ..."
#     codeql pack install
# else
#     echo "qlpack.yml not detected, stopping script ..."
#     exit 1
# fi

# Detect whether query.ql exists
if [ -e "$codeql_query_path" ]; then
    echo "Target codeql query file detected"
else
    echo "Target codeql query file not detected, stopping script ..."
    exit 1
fi

# Detect whether codeql database storage folder exists
if [ -d "$codeql_dbs_dir" ]; then
    # If so, remove all the content and the folder recursively
    echo "CodeQLDBs already exists. Removing ..."
    rm -rf "$codeql_dbs_dir"
fi
# Create the codeql database storage folders
mkdir "$codeql_dbs_dir"
mkdir "$codeql_dbs_dir/evo_jdk8"
mkdir "$codeql_dbs_dir/jdk8"
mkdir "$codeql_dbs_dir/jdk11"
echo "CodeQLDBs created."

# Detect whether codeql results storage folder exists
if [ -d "$codeql_res_dir" ]; then
    # If so, remove all the content and the folder recursively
    echo "CodeQLRes already exists. Removing ..."
    rm -rf "$codeql_res_dir"
fi
# Create the codeql database storage folders
mkdir "$codeql_res_dir"
mkdir "$codeql_res_dir/evo_jdk8"
mkdir "$codeql_res_dir/jdk8"
mkdir "$codeql_res_dir/jdk11"
echo "CodeQLRes created."

# codeql_query_evo_jdk8_art_project() {
#     # Obtain project name from command line
#     project_name=$1
#     # Load Java 8 environment
#     cd $rest_go_dir
#     . ./java8.env
#     cd $rest_go_dir/services/evo_jdk8/cs/rest/artificial/$project_name
#     codeql database create $codeql_dbs_dir/evo_jdk8/$project_name --language=java --command='mvn clean compile' --overwrite
#     codeql query run --database=$codeql_dbs_dir/evo_jdk8/$project_name $codeql_query_path | tee $codeql_res_dir/evo_jdk8/$project_name.res
# }

# codeql_query_evo_jdk8_ori_project() {
#     # Obtain project name from command line
#     project_name=$1
#     # Load Java 8 environment
#     cd $rest_go_dir
#     . ./java8.env
#     cd $rest_go_dir/services/evo_jdk8/cs/rest/original/$project_name
#     codeql database create $codeql_dbs_dir/evo_jdk8/$project_name --language=java --command='mvn clean compile' --overwrite
#     codeql query run --database=$codeql_dbs_dir/evo_jdk8/$project_name $codeql_query_path | tee $codeql_res_dir/evo_jdk8/$project_name.res
# }

# codeql_query_jdk8_project() {
#     # Obtain project name from command line
#     project_name=$1
#     # Load Java 8 environment
#     cd $rest_go_dir
#     . ./java8.env
#     cd $rest_go_dir/services/jdk8/$project_name
#     codeql database create $codeql_dbs_dir/jdk8/$project_name --language=java --command='mvn clean compile' --overwrite
#     codeql query run --database=$codeql_dbs_dir/jdk8/$project_name $codeql_query_path | tee $codeql_res_dir/jdk8/$project_name.res
# }

codeql_query_java_gradle_project() {
    # Obtain project name from command line
    project_name=$1
    project_path=$2
    project_java_version=$3

    cd $rest_go_dir
    if [ $project_java_version == "8" ]; then
        . ./java8.env
    elif [ $project_java_version == "11" ]; then
        . ./java11.env
    else 
        echo "Unsupport Java Version: $project_java_version"
        exit 2
    fi
    
    codeql_db_path=$4
    codeql_res_path=$5

    cd $project_path
    codeql database create $codeql_db_path --language=java --command='gradle build' --overwrite
    codeql query run --database=$codeql_db_path $codeql_query_path | tee $codeql_res_path
}

codeql_query_java_mvn_project() {
    # Obtain project name from command line
    project_name=$1
    project_path=$2
    project_java_version=$3

    cd $rest_go_dir
    if [ $project_java_version == "8" ]; then
        . ./java8.env
    elif [ $project_java_version == "11" ]; then
        . ./java11.env
    else 
        echo "Unsupport Java Version: $project_java_version"
        exit 2
    fi
    
    codeql_db_path=$4
    codeql_res_path=$5

    cd $project_path
    codeql database create $codeql_db_path --language=java --command='mvn clean compile' --overwrite
    codeql query run --database=$codeql_db_path $codeql_query_path | tee $codeql_res_path
}

# codeql_query_jdk11_project() {
#     project_name=$1
#     # Load Java 8 environment
#     cd $rest_go_dir
#     . ./java8.env
#     cd $rest_go_dir/services/jdk8/$project_name
#     codeql database create $codeql_dbs_dir/jdk8/$project_name --language=java --command='mvn clean compile' --overwrite
#     codeql query run --database=$codeql_dbs_dir/jdk8/$project_name $codeql_query_path | tee $codeql_res_dir/jdk8/$project_name.res
# }

# # Load Java 8 environment
# cd $rest_go_dir
# . ./java8.env

# # # Can't generate Enum for erc20-rest-service as Codeql could not 
# # codeql_query_java8_project erc20-rest-service
# codeql_query_java8_project genome-nexus
# codeql_query_java8_project person-controller
# codeql_query_java8_project problem-controller
# codeql_query_java8_project rest-study
# codeql_query_java8_project spring-batch-rest
# codeql_query_java8_project spring-boot-sample-app
# codeql_query_java8_project user-management
codeql_query_java_gradle_project erc20-rest-service $rest_go_dir/services/jdk8/erc20-rest-service 8 $codeql_dbs_dir/jdk8/erc20-rest-service $codeql_res_dir/jdk8/erc20-rest-service.res
codeql_query_java_mvn_project genome-nexus $rest_go_dir/services/jdk8/genome-nexus 8 $codeql_dbs_dir/jdk8/genome-nexus $codeql_res_dir/jdk8/genome-nexus.res
codeql_query_java_mvn_project person-controller $rest_go_dir/services/jdk8/person-controller 8 $codeql_dbs_dir/jdk8/person-controller $codeql_res_dir/jdk8/person-controller.res
codeql_query_java_mvn_project problem-controller $rest_go_dir/services/jdk8/problem-controller 8 $codeql_dbs_dir/jdk8/problem-controller $codeql_res_dir/jdk8/problem-controller.res
codeql_query_java_mvn_project rest-study $rest_go_dir/services/jdk8/rest-study 8 $codeql_dbs_dir/jdk8/rest-study $codeql_res_dir/jdk8/rest-study.res
codeql_query_java_mvn_project spring-batch-rest $rest_go_dir/services/jdk8/spring-batch-rest 8 $codeql_dbs_dir/jdk8/spring-batch-rest $codeql_res_dir/jdk8/spring-batch-rest.res
codeql_query_java_mvn_project spring-boot-sample-app $rest_go_dir/services/jdk8/spring-boot-sample-app 8 $codeql_dbs_dir/jdk8/spring-boot-sample-app $codeql_res_dir/jdk8/spring-boot-sample-app.res
codeql_query_java_mvn_project user-management $rest_go_dir/services/jdk8/user-management 8 $codeql_dbs_dir/jdk8/user-management $codeql_res_dir/jdk8/user-management.res

# codeql_query_evo_jdk8_art_project ncs
# codeql_query_evo_jdk8_art_project news
# codeql_query_evo_jdk8_art_project scs
codeql_query_java_mvn_project ncs $rest_go_dir/services/evo_jdk8/cs/rest/artificial/ncs 8 $codeql_dbs_dir/evo_jdk8/ncs $codeql_res_dir/evo_jdk8/ncs.res
codeql_query_java_mvn_project news $rest_go_dir/services/evo_jdk8/cs/rest/artificial/news 8 $codeql_dbs_dir/evo_jdk8/news $codeql_res_dir/evo_jdk8/news.res
codeql_query_java_mvn_project scs $rest_go_dir/services/evo_jdk8/cs/rest/artificial/scs 8 $codeql_dbs_dir/evo_jdk8/scs $codeql_res_dir/evo_jdk8/scs.res

# codeql_query_evo_jdk8_ori_project features-service
# codeql_query_evo_jdk8_ori_project languagetool
# codeql_query_evo_jdk8_ori_project proxyprint
# codeql_query_evo_jdk8_ori_project restcountries
# codeql_query_evo_jdk8_ori_project scout-api
codeql_query_java_mvn_project features-service $rest_go_dir/services/evo_jdk8/cs/rest/original/features-service 8 $codeql_dbs_dir/evo_jdk8/scout-api $codeql_res_dir/evo_jdk8/features-service.res
codeql_query_java_mvn_project languagetool $rest_go_dir/services/evo_jdk8/cs/rest/original/languagetool 8 $codeql_dbs_dir/evo_jdk8/languagetool $codeql_res_dir/evo_jdk8/languagetool.res
codeql_query_java_mvn_project proxyprint $rest_go_dir/services/evo_jdk8/cs/rest/original/proxyprint 8 $codeql_dbs_dir/evo_jdk8/proxyprint $codeql_res_dir/evo_jdk8/proxyprint.res
codeql_query_java_mvn_project restcountries $rest_go_dir/services/evo_jdk8/cs/rest/original/restcountries 8 $codeql_dbs_dir/evo_jdk8/restcountries $codeql_res_dir/evo_jdk8/restcountries.res
codeql_query_java_mvn_project scout-api $rest_go_dir/services/evo_jdk8/cs/rest/original/scout-api 8 $codeql_dbs_dir/evo_jdk8/scout-api $codeql_res_dir/evo_jdk8/scout-api.res

codeql_query_java_mvn_project cwa-verification $rest_go_dir/services/jdk11/cwa-verification 11 $codeql_dbs_dir/jdk11/cwa-verification $codeql_res_dir/jdk11/cwa-verification.res
codeql_query_java_mvn_project market $rest_go_dir/services/jdk11/market 11 $codeql_dbs_dir/jdk11/market $codeql_res_dir/jdk11/market.res
codeql_query_java_mvn_project project-tracking-system $rest_go_dir/services/jdk11/project-tracking-system 11 $codeql_dbs_dir/jdk11/project-tracking-system $codeql_res_dir/jdk11/project-tracking-system.res