
## For Managed identity flow
- Managed Endpoint is created with SAI or UAI. 
- User containers with dependencies are deployed in Managed Deployment. 
- When `ManagedIdentityCredential().get_token()` is invoked from inside the deployment container, call routes via `http://10.0.0.4:8911/v1/token/msi/xds` uri all time to fetch a token for caller. 
- This is an internal URI which is available in sidecar containers.

- **Note**:
    - If Managed endpoint is cearted with SAI, then managed identity token is fetched for the SAI inside user contaier deployment.
    - If Managed endpoint is cearted with UAI, then managed identity token is fetched for the UAI inside user contaier deployment.

- As internal host is reached from deployment level, its suitable for deployments which has `egress-public-network-access` flag value as `disabled`, where PNA is disabled with private endpoint for own vnet. For `enabled`, the `get_token()` api call will also work fine.

Managed endpoint logs the following internal api calls if debug logs are enabled.

```
2025-12-29 04:35:40,079 [managed_identity] : DEBUG    [75] Obtaining token via managed identity on Azure App Service
2025-12-29 04:35:40,080 [_universal] : INFO     [75] Request URL: 'http://10.0.0.4:8911/v1/token/msi/xds?api-version=REDACTED&resource=REDACTED'
Request method: 'GET'
Request headers:
    'X-IDENTITY-HEADER': 'REDACTED'
    'Metadata': 'REDACTED'
    'User-Agent': 'azsdk-python-identity/1.25.1 Python/3.9.23 (Linux-6.8.0-1041-azure-x86_64-with-glibc2.31)'
No body was attached to the request
2025-12-29 04:35:40,451 [_universal] : INFO     [75] Response status: 200
Response headers:
    'Content-Type': 'application/json'
    'Date': 'Mon, 29 Dec 2025 04:35:40 GMT'
    'Transfer-Encoding': 'chunked'
2025-12-29 04:35:40,452 [token_cache] : DEBUG    [75] event={
    "client_id": null,
    "data": {},
    "params": {},
    "response": {
        "access_token": "********",
        "expires_in": 86399,
        "refresh_in": 43199,
        "resource": "https://management.azure.com",
        "token_type": "Bearer"
    },
    "scope": [
        "https://management.azure.com"
    ],
    "token_endpoint": "https://mir-user-pod-2f93b24399b24ae18c821a0beb026e67000000/managed_identity"
}
2025-12-29 04:35:40,452 [msal_managed_identity_client] : INFO     [75] AppServiceCredential.get_token succeeded
2025-12-29 04:35:40,452 [decorators] : INFO     [75] ManagedIdentityCredential.get_token succeeded
```

## For Service Principal identity flow
- Managed Endpoint is created with SAI. 
- User containers with dependencies are deployed in Managed Deployment. 
- When `ClientSecretCredential().get_token()` is invoked from inside the deployment container, call routes via `https://login.microsoftonline.com/<<tenant_id>>` uri all time to fetch a token for caller. 
- This is an external URI which is reached outside the deployment boundaries.

- As external host is reached from deployment level, its suitable for deployments which has `egress-public-network-access` flag value as `enabled`. For `disabled`, the `get_token()` api call will break.

Managed endpoint logs the following internal api calls if debug logs are enabled.

```
2025-12-29 05:18:09,943 [authority] : DEBUG    [75] Initializing with Entra authority: https://login.microsoftonline.com/<<tenant_id>>
2025-12-29 05:18:09,944 [_universal] : INFO     [75] Request URL: 'https://login.microsoftonline.com/<<tenant_id>>/v2.0/.well-known/openid-configuration'
Request method: 'GET'
Request headers:
    'User-Agent': 'azsdk-python-identity/1.25.1 Python/3.9.23 (Linux-6.8.0-1041-azure-x86_64-with-glibc2.31)'
No body was attached to the request
2025-12-29 05:18:10,229 [_universal] : INFO     [75] Response status: 200
Response headers:
    'Cache-Control': 'max-age=86400, private'
    'Content-Type': 'application/json; charset=utf-8'
    'Strict-Transport-Security': 'REDACTED'
    'X-Content-Type-Options': 'REDACTED'
    'Access-Control-Allow-Origin': 'REDACTED'
    'Access-Control-Allow-Methods': 'REDACTED'
    'P3P': 'REDACTED'
    'x-ms-request-id': 'de4c5b3d-4f8d-4c8e-9887-93ecc8360701'
    'x-ms-ests-server': 'REDACTED'
    'x-ms-srs': 'REDACTED'
    'Content-Security-Policy-Report-Only': 'REDACTED'
    'X-XSS-Protection': 'REDACTED'
    'Set-Cookie': 'REDACTED'
    'Date': 'Mon, 29 Dec 2025 05:18:09 GMT'
    'Content-Length': '1964'
..
..
..
2025-12-29 05:18:10,230 [application] : DEBUG    [75] Broker enabled? None
2025-12-29 05:18:10,230 [application] : DEBUG    [75] Region to be used: None
2025-12-29 05:18:10,233 [telemetry] : DEBUG    [75] Generate or reuse correlation_id: a71e2e80-7d7b-4ede-bd16-ffb0b7d82f6a
2025-12-29 05:18:10,233 [_universal] : INFO     [75] Request URL: 'https://login.microsoftonline.com/<<tenant_id>>/oauth2/v2.0/token'
Request method: 'POST'
Request headers:
    'Accept': 'application/json'
    'x-client-sku': 'REDACTED'
    'x-client-ver': 'REDACTED'
    'x-client-os': 'REDACTED'
    'x-ms-lib-capability': 'REDACTED'
    'client-request-id': 'REDACTED'
    'x-client-current-telemetry': 'REDACTED'
    'x-client-last-telemetry': 'REDACTED'
    'User-Agent': 'azsdk-python-identity/1.25.1 Python/3.9.23 (Linux-6.8.0-1041-azure-x86_64-with-glibc2.31)'
A body is sent with the request
2025-12-29 05:18:10,393 [_universal] : INFO     [75] Response status: 200
Response headers:
    'Cache-Control': 'no-store, no-cache'
    'Pragma': 'no-cache'
    'Content-Type': 'application/json; charset=utf-8'
    'Expires': '-1'
    'Strict-Transport-Security': 'REDACTED'
    'X-Content-Type-Options': 'REDACTED'
    'P3P': 'REDACTED'
    'client-request-id': 'REDACTED'
    'x-ms-request-id': 'de4c5b3d-4f8d-4c8e-9887-93ecce360701'
    'x-ms-ests-server': 'REDACTED'
    'x-ms-clitelem': 'REDACTED'
    'x-ms-srs': 'REDACTED'
    'Content-Security-Policy-Report-Only': 'REDACTED'
    'X-XSS-Protection': 'REDACTED'
    'Set-Cookie': 'REDACTED'
    'Date': 'Mon, 29 Dec 2025 05:18:09 GMT'
    'Content-Length': '1864'
2025-12-29 05:18:10,394 [token_cache] : DEBUG    [75] event={
    "client_id": "<<client_id>>",
    "data": {
        "claims": null,
        "scope": [
            "https://management.azure.com/.default"
        ]
    },
    "environment": "login.microsoftonline.com",
    "grant_type": "client_credentials",
    "params": null,
    "response": {
        "access_token": "********",
        "expires_in": 86399,
        "ext_expires_in": 86399,
        "refresh_in": 43199,
        "token_type": "Bearer"
    },
    "scope": [
        "https://management.azure.com/.default"
    ],
    "token_endpoint": "https://login.microsoftonline.com/<<tenant_id>>/oauth2/v2.0/token"
}
2025-12-29 05:18:10,394 [get_token_mixin] : INFO     [75] ClientSecretCredential.get_token succeeded
```

## How to run samples?
- For SAI based azureml managed endpoint, follow notebook - [online-endpoint-sai-upload.ipynb](online-endpoint-sai-upload.ipynb).
- For UAI based azureml managed endpoint, follow notebook - [online-endpoint-uai-upload.ipynb](online-endpoint-uai-upload.ipynb).
- For SP based azureml managed endpoint, follow notebook - [online-endpoint-sp-upload.ipynb](online-endpoint-sp-upload.ipynb).

