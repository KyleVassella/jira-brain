# PROJ-110: Rate limit the public REST API
Status: In Progress | Type: Feature | Fix version: 2.5.0
Add per-API-key rate limiting of 1,000 requests per hour to the public REST API.
Implemented as a token bucket in Redis. Responses include X-RateLimit-Remaining and
Retry-After headers. Exceeding the limit returns HTTP 429.
