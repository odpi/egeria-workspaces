<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Secrets Store files (omsecrets)

Files with the file extension of `omsecrets` contain a *secrets store*.  This contains one or more collections of 
related secrets that are consumed by Egeria's connectors when they are accessing resources on remote systems/cloud services.
Typically, each collection of secrets within the secrets store is for a particular remote service/system.

The format of the secrets store is YAML, which organizes information as a set of nested properties.
This property nesting is implemented using indentation.

There are different types of security mechanisms that are in use in today's systems.
The secrets store therefore supports different types of secrets.

Below is an example of a secrets store file.
There are three secret collections in the store: `apache-atlas-server-1`, `unity-catalog-on-databricks` and `egeria-view-server`.

```yaml
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.

secretsCollections:
  collectionName:
    refreshTimeInterval: 10
    secrets:
      secretProperty1: secretValue1
      secretProperty2: secretValue2
      secretProperty3: secretValue3
  View Server:view-server[b5423a9c-24d1-4d90-9bc1-5ae358eb7826]:
    refreshTimeInterval: 60
    tokenAPI:
      httpRequestType: POST
      url: https://localhost:9443/api/token
      contentType: application/json
      requestBody:
        userId: viewnpa
        password: secret
  Databricks Unity Catalog Server:Databricks UC:
    refreshTimeInterval: 60
    secrets:
      accessToken: mytoken
```

The `apache-atlas-server-1` collection has two properties: `userId` and `password`.  This is for a server that uses basic authentication/authorization.  The userId and password values supplied are used to log Egeria into the server.

The `unity-catalog-on-databricks` has one property called `accessToken`.  This is set to the bearer token to use on the REST API requests to the server.

Finally, `egeria-view-server` has a description of an API to dynamically return a token (`tokenAPI`).
The token API is specified as an HTTP request type (eg `GET` or `POST`),
a URL, content type and a request body.
The connector running in Egeria will issue the appropriate HTTP request to the supplied URL with the requested request body attached.
It expects a bearer token in the response and this token is then used on subsequent REST API request to the remote server to access its resources.




