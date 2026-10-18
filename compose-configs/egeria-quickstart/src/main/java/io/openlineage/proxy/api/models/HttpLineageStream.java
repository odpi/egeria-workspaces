/*
/* Copyright 2018-2024 contributors to the OpenLineage project
/* SPDX-License-Identifier: Apache-2.0
*/

package io.openlineage.proxy.api.models;

import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.client.Client;
import jakarta.ws.rs.client.ClientBuilder;
import jakarta.ws.rs.client.Entity;
import jakarta.ws.rs.client.Invocation;
import jakarta.ws.rs.core.HttpHeaders;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import lombok.NonNull;
import lombok.extern.slf4j.Slf4j;

/** HttpLineageStream pushes events to http endpoint */
@Slf4j
public class HttpLineageStream extends LineageStream {

  private final String url;
  private final String apiKey;
  private Invocation.Builder invocation;

  public HttpLineageStream(@NonNull final HttpConfig httpConfig) {
    super(Type.HTTP);
    this.url = httpConfig.getUrl();
    this.apiKey = httpConfig.getApiKey();
    ClientBuilder cb = ClientBuilder.newBuilder();
    Client client = cb.build();
    this.invocation = client.target(this.url).request(MediaType.APPLICATION_JSON);
    if (this.apiKey != null && this.apiKey.trim().length() > 0) {
      this.invocation = this.invocation.header(HttpHeaders.AUTHORIZATION, "Bearer " + this.apiKey);
    }
  }

  @Override
  public void collect(@NonNull String eventAsString) {
    eventAsString = eventAsString.trim();
    try {
      Response response = this.invocation.post(Entity.json(eventAsString));
      int status = response.getStatus();
      log.debug("Received lineage event: {} \n response code: {}", eventAsString, status);
    } catch (WebApplicationException ex) {
      log.error("Exception occurred during HttpLineageStream's collect() call.");
      log.error(ex.getMessage());
    }
  }
}
