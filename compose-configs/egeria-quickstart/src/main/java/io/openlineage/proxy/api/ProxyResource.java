/*
/* Copyright 2018-2024 contributors to the OpenLineage project
/* SPDX-License-Identifier: Apache-2.0
*/

package io.openlineage.proxy.api;

import static jakarta.ws.rs.core.MediaType.APPLICATION_JSON;

import io.openlineage.proxy.service.ProxyService;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.container.AsyncResponse;
import jakarta.ws.rs.container.Suspended;
import jakarta.ws.rs.core.Response;
import lombok.NonNull;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Path("/api/v1/lineage")
public class ProxyResource {
  private final ProxyService service;

  public ProxyResource(@NonNull final ProxyService service) {
    this.service = service;
  }

  @POST
  @Consumes(APPLICATION_JSON)
  public void proxyEvent(
      @Valid String eventAsString, @Suspended final AsyncResponse asyncResponse) {
    service
        .proxyEventAsync(eventAsString)
        .whenComplete(
            (result, err) -> {
              if (err != null) {
                log.error("Failed to proxy OpenLineage event!", err);
                asyncResponse.resume(Response.status(500).build());
              } else {
                asyncResponse.resume(Response.status(200).build());
              }
            });
  }
}
