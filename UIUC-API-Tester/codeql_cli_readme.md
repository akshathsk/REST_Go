# Run `codeql queries` by Command Line

1. Install `codeql cli` dependency:

    1. Download `codeql zip package` from [`codeql repo`](https://github.com/github/codeql-cli-binaries/releases)

        * The zip file could be obtained using command 
            * `wget https://github.com/github/codeql-cli-binaries/releases/download/v2.6.2/codeql-linux64.zip`
        * If the url is expired, please refer to the repo for the latest url

    2. Extract the `codeql-linux64.zip` to machine instance

        * The zip file could be extracted using command
            * `unzip codeql-linux64.zip`

    3. Add `codeql cli` dependency to `PATH` variable

        * `export PATH=$PATH:/path/to/codeql/cli/dependency/`
        * The installation could be verified by typing in
            * `codeql version`
            * Sample output
                * `CodeQL command-line toolchain release 2.13.0. ...`

----

2. Generate `codeql database` for target project

    1. Move to target project folder
        * `cd /path/to/target/project/folder`

    2. Generate `codeql database` using following command

        * `codeql database create /path/to/store/database --language={project_language} --command='{project_build_script}' --overwrite`
        * Sample command to analyze `Java` project build using `Maven` and store database under `~/codeql` folder
            * `codeql database create ~/codeqlDB --language=java --command='mvn clean install -DskipTests' --overwrite`
                
----

3. Set up `codeql query dependency`

    1. Create a `qlpack.yml` for the codebase environment
        * Have to define `name`, `version`, and `dependency`
        * Sample scrpit for `Java`:<br>
            * ```
                name: getting-started/codeql-extra-queries-java
                version: 0.0.0
                dependencies:
                    codeql/java-all: "*"
                ```

    2. Install the `qlpack` using command line
        * `codeql pack install`
            
----

4. Run `codeql query` and store the result

    1. Developed a `codeql query script`
        * Sample script (`enum-extract.ql`)<br>
            * ```
                /**
                * @name Empty block
                * @kind problem
                * @problem.severity warning
                * @id java/example/empty-block
                */

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
            * Please refer to [`codeql doc`](https://docs.github.com/en/code-security/codeql-cli/using-the-codeql-cli/creating-codeql-query-suites) for further detailed info

    2. Use command `codeql query run --database=/path/to/codeqlDB /path/to/query.ql`
        * Sample script <br>
            `codeql query run --database=./codeqlDB ./enum-extract.ql`
        * Sample outcome
            * ```
                | col0  |    col1    |                                                col2                                                |                                                         col3                                                         |
                +-------+------------+----------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
                | Roles | ROLE_USER  | /home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java | file:///home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java:49:7:49:11 |
                | Roles | ROLE_STAFF | /home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java | file:///home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java:49:7:49:11 |
                | Roles | ROLE_ADMIN | /home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java | file:///home/kobenorriswu/REST_Go/services/jdk11/market/market-core/src/main/java/market/domain/Role.java:49:7:49:11 |
                ```
----
