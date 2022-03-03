# Testing the API and rate limits service deployed

## Query to the API:
```
http://localhost:8000/customers/search?nameprefix=papa.sarr@wave.com
```

Returns:
```
{"data":{"customers":[{"id":7,"name":"Fatou Sene"}]}}
```
## Ratelimit deployment
At /envoy-ratelimit there are the manifests to deploy ratelimit, you can check the deployment runs at the k8s cluster.
To simplify I have added Redis inside the ratelimit POD, but the data is lost when the POD restarts. To be properly done, should have a PVC and all PVC "protections" from autoscaler, or use GCE Redis service.

## Query to ratelimit
```
curl -X POST http://localhost:8080/json \
--data-binary @- << EOF
{
  "domain": "support-dashboard",
  "descriptors": [
    {
      "entries": [
        {
          "key": "endpoint",
          "value": "/customers/search"
        }
      ]
    },
    {
      "entries": [
        {
          "key": "endpoint",
          "value": "/customers/search"
        },
        {
          "key": "user",
          "value": "Fatou Sene"
        }
      ]
    }
  ]
}
EOF
```

Response:
```
{"overallCode":"OK","statuses":[{"code":"OK"}]}
```

# Python coding
At /python/support there are the 2 versions:
- ratelimit-check-middleware: where the API code is modified L48-L70
- ratelimit-check-middleware:
  The customer request goes with POST to http://middlewahre:5000/api-rate-limit and this middleware forwards the request to wave API if the request in not throttling rate limits.

I haven't packed with poetry al dependencies nor pushed the image.

# Final notes
I didn't have time to pack all dependencies of the middleware because all the confusion with envoy talked with Kamal. 
Honestly I see a lot of details in the test and from my humble point of view should be more focused exercice specially on how to implement rate limits as I thought I had to use envoy proxy or ISTIO ad I dedicated a lot of time to this until I asked.
