package org.uiuc;

import com.google.gson.Gson;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.parser.OpenAPIV3Parser;
import java.io.IOException;
import java.io.FileWriter;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;

import io.swagger.v3.oas.models.media.Schema;
import io.swagger.oas.inflector.examples.models.Example;
import io.swagger.oas.inflector.examples.ExampleBuilder;
import com.fasterxml.jackson.databind.module.SimpleModule;
import io.swagger.oas.inflector.processors.JsonNodeExampleSerializer;
import io.swagger.util.Json;
import org.uiuc.dto.swagger.Endpoints;
import org.uiuc.dto.swagger.Request;
import java.io.File;
import java.util.stream.Collectors;

import static java.util.Objects.nonNull;
import static org.uiuc.dto.swagger.Request.*;

public class Main {
  public static void main(String[] args) throws IOException {

    String path = args[0];
    String output = args[1];
    List<Endpoints> endpoints = new ArrayList<>();
    File file = new File(path);
    OpenAPI swagger = new OpenAPIV3Parser().read(path);
    Map<String, Schema> definitions = swagger.getComponents().getSchemas();
    Endpoints endpoint = new Endpoints();
    endpoint.setMicroservice(file.getName().split("\\.")[0]);
    String hostUrl = swagger.getServers().get(0).getUrl();
    if(hostUrl.charAt(hostUrl.length()-1) == '/'){
      hostUrl = hostUrl.substring(0, hostUrl.length()-1);
    }
    endpoint.setHost(hostUrl);
    Map<String, List<Request>> methodToRequestMap = new HashMap<>();
    swagger
        .getPaths()
        .forEach(
            (k, v) -> {
              if (v.getGet() != null) {
                Request request = new Request();
                AtomicReference<String> str = new AtomicReference<>(k);
                if (v.getGet().getParameters() != null && v.getGet().getParameters().size() > 0) {
                  v.getGet()
                      .getParameters()
                      .forEach(
                          param -> {
                            if (param.getIn().equals("query")) {
                              if (str.get().contains("{") && !str.get().contains("?")) {
                                str.set(
                                    str.get()
                                        + "?"
                                        + param.getName()
                                        + "={"
                                        + param.getName()
                                        + "}");
                              } else if (!str.get().contains("{")) {
                                str.set(
                                    str.get()
                                        + "?"
                                        + param.getName()
                                        + "={"
                                        + param.getName()
                                        + "}");
                              } else {
                                str.set(
                                    str.get()
                                        + "&"
                                        + param.getName()
                                        + "={"
                                        + param.getName()
                                        + "}");
                              }
                            }
                          });
                }
                request.setUrl(str.get());
                if (!methodToRequestMap.containsKey("GET")) {
                  List<Request> list = new ArrayList<>();
                  list.add(request);
                  methodToRequestMap.put("GET", list);
                } else {
                  methodToRequestMap.get("GET").add(request);
                }
              }
              if (v.getPut() != null) {
                Request request = new Request();
                request.setUrl(k);
                if (v.getPut().getRequestBody() != null
                    && v.getPut().getRequestBody().getContent().values().stream()
                        .findFirst()
                        .isPresent()) {
                  String bodyRef =
                      v.getPut().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .get$ref();
                  Map<String, Schema> nonBodyParams = v.getPut().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .getProperties();
                  if(nonNull(bodyRef)){
                    request.setBody(bodyRef);
                    String obj[] = bodyRef.split("/");
                    String finalObj = obj[obj.length - 1];
                    request.setExample(getExampleJson(definitions, finalObj));
                    request.setContentType(REQUEST_BODY_CONTENT_TYPE);
                  }
                  else if(nonNull(nonBodyParams) && !nonBodyParams.isEmpty()){
                    Map<String, Object> paramAndExample = nonBodyParams.values().stream()
                            .collect(Collectors.toMap(Schema::getName, param -> getExampleForFormData(param.getType())));
                    SimpleModule simpleModule = new SimpleModule().addSerializer(new JsonNodeExampleSerializer());
                    Json.mapper().registerModule(simpleModule);
                    request.setExample(Json.pretty(paramAndExample));
                    request.setContentType(FORM_DATA_CONTENT_TYPE);
                  }
                  if (!methodToRequestMap.containsKey("PUT")) {
                    List<Request> list = new ArrayList<>();
                    list.add(request);
                    methodToRequestMap.put("PUT", list);
                  } else {
                    methodToRequestMap.get("PUT").add(request);
                  }
                }
              }
              if (v.getPost() != null) {
                Request request = new Request();
                request.setUrl(k);
                if (v.getPost().getRequestBody() != null) {
                  String bodyRef =
                      v.getPost().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .get$ref();
                  Map<String, Schema> nonBodyParams = v.getPost().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .getProperties();
                  if (nonNull(bodyRef)) {
                    request.setBody(bodyRef);
                    String obj[] = bodyRef.split("/");
                    String finalObj = obj[obj.length - 1];
                    request.setExample(getExampleJson(definitions, finalObj));
                    request.setContentType(REQUEST_BODY_CONTENT_TYPE);
                  }
                  // Get formData params
                  else if(nonNull(nonBodyParams) && !nonBodyParams.isEmpty()){
                    Map<String, Object> paramAndExample = nonBodyParams.values().stream()
                            .collect(Collectors.toMap(Schema::getName, param -> getExampleForFormData(param.getType())));
                    SimpleModule simpleModule = new SimpleModule().addSerializer(new JsonNodeExampleSerializer());
                    Json.mapper().registerModule(simpleModule);
                    request.setExample(Json.pretty(paramAndExample));
                    request.setContentType(FORM_DATA_CONTENT_TYPE);
                  }
                }
                if (!methodToRequestMap.containsKey("POST")) {
                  List<Request> list = new ArrayList<>();
                  list.add(request);
                  methodToRequestMap.put("POST", list);
                } else {
                  methodToRequestMap.get("POST").add(request);
                }
              }
              if (v.getDelete() != null) {
                Request request = new Request();
                request.setUrl(k);
                if (!methodToRequestMap.containsKey("DELETE")) {
                  List<Request> list = new ArrayList<>();
                  list.add(request);
                  methodToRequestMap.put("DELETE", list);
                } else {
                  methodToRequestMap.get("DELETE").add(request);
                }
              }
              if (v.getPatch() != null) {
                Request request = new Request();
                request.setUrl(k);
                if (v.getPatch().getRequestBody() != null) {
                  String bodyRef =
                      v.getPatch().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .get$ref();
                  Map<String, Schema> nonBodyParams = v.getPatch().getRequestBody().getContent().values().stream()
                          .findFirst()
                          .get()
                          .getSchema()
                          .getProperties();
                  if(nonNull(bodyRef)){
                    request.setBody(bodyRef);
                    String obj[] = bodyRef.split("/");
                    String finalObj = obj[obj.length - 1];
                    request.setExample(getExampleJson(definitions, finalObj));
                    request.setContentType(REQUEST_BODY_CONTENT_TYPE);
                  }
                  else if(nonNull(nonBodyParams) && !nonBodyParams.isEmpty()){
                    Map<String, Object> paramAndExample = nonBodyParams.values().stream()
                            .collect(Collectors.toMap(Schema::getName, param -> getExampleForFormData(param.getType())));
                    SimpleModule simpleModule = new SimpleModule().addSerializer(new JsonNodeExampleSerializer());
                    Json.mapper().registerModule(simpleModule);
                    request.setExample(Json.pretty(paramAndExample));
                    request.setContentType(FORM_DATA_CONTENT_TYPE);
                  }
                }
                if (!methodToRequestMap.containsKey("PATCH")) {
                  List<Request> list = new ArrayList<>();
                  list.add(request);
                  methodToRequestMap.put("PATCH", list);
                } else {
                  methodToRequestMap.get("PATCH").add(request);
                }
              }
            });
    endpoint.setMethodToRequestMap(methodToRequestMap);

    endpoints.add(endpoint);
    Gson gson = new Gson();
    System.out.println(gson.toJson(endpoints));
    FileWriter writer = new FileWriter(output + "/output.json");
    writer.write(gson.toJson(endpoints));
    writer.close();
  }

  private static String getExampleJson(Map<String, Schema> definitions, String pojo) {
    Schema model = definitions.get(pojo);
    Example example = ExampleBuilder.fromSchema(model, definitions);
    SimpleModule simpleModule = new SimpleModule().addSerializer(new JsonNodeExampleSerializer());
    Json.mapper().registerModule(simpleModule);
    return Json.pretty(example);
  }

  private static Object getExampleForFormData(String dataType){
    if(dataType.equalsIgnoreCase("string")){
      return "example_string";
    }
    else if(dataType.toLowerCase().contains("int")){
      return 1;
    }
    return "example_string";
  }
}
