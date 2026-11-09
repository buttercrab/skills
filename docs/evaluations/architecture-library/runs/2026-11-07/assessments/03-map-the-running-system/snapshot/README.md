# Ink intake
The public gateway stores uploaded documents in the database and publishes every upload to an event stream. A separate parser service runs in Region B. Results are pushed to browser clients over persistent sockets. All services have multiple replicas and are active-active across both regions.

Architecture maintained: 2025-06-01.
