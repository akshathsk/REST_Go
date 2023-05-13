package org.uiuc.dto.swagger;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class Request {

  public static String FORM_DATA_CONTENT_TYPE = "FORM_DATA";
  public static String REQUEST_BODY_CONTENT_TYPE = "REQUEST_BODY";
  String url;
  String body;
  String example;
  String contentType;
  String pathParamExample;
}
