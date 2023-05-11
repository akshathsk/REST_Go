## Generate Swagger during project building

* `OpenAPI` (formerly known as `Swagger`) is an open standard for defining and documenting APIs. It uses a JSON or YAML format to describe the endpoints, operations, parameters, responses, and other details of an API.

* For project we selected in the very first period of this semetser, we used `spring security fox` plugins to generate the `swagger` files by setting up a separate thread of service to scan through all the available API endpoints of the entire system during system set up, here is the instructions of how to do so:

    1. Add the `Springfox` dependencies to the project's build configuration file. For example, if the project is using Maven, add the following to the `pom.xml` file:
        
        ```
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>${springfox.version}</version>
        </dependency>
        <dependency>
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>${springfox.version}</version>
        </dependency>
        ```
    
    2. Create a `Docket` bean in projects' Spring configuration class to enable `Swagger` in the Spring application:

        ```
        // Here it scans all the API endpoints under "com.example.controllers"
        @Configuration
        @EnableSwagger2
        public class SwaggerConfig {
            @Bean
            public Docket api() {
                return new Docket(DocumentationType.SWAGGER_2)
                    .select()
                    .apis(RequestHandlerSelectors.basePackage("com.example.controllers"))
                    .paths(PathSelectors.any())
                    .build();
            }
        }
        ```

    3. Start the Spring application and navigate to `http://localhost:{port_number}/swagger-ui.html` in web browser to view the generated Swagger documentation.

        * Here the `port_number` refers to the service port number

    * We have generated `swagger` files for `ftgo-application`, `day-trader`, and `lakesideMutual` projects

----

* Current all of the projects in `REST_Go` have pre-developed `swagger files`:
    * Here are the cooresponding swagger files' location:
        * `REST_Go`: 
            * `https://github.com/codingsoo/REST_Go/tree/master/doc`
            * `https://raw.githubusercontent.com/randomqwerqwer/issta/main/features_swagger.json`

* Reasons not to use auto swagger genertion tools again for `REST_Go`:

    1. The integration process might cause unexpected bugs or excceptions during the execution, and therefore might cost us much time in debugging.

    2. `REST_Go` has already provided us 20 projects already with `swagger` files, spending extra time in exploring and extending auto-swagger generation tools seems unworthy.

* For more detailed explanation, please refer to [Swagger Doc](https://swagger.io/specification/)