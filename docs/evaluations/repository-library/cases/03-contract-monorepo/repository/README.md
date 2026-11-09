# Harbor workspace
`contracts/event.json` owns the wire shape. `tools/generate.py` regenerates the committed Python event class. Gateway and Python SDK have independent release schedules. The console is an internal gateway client and deploys with the gateway.

A change to contract fields requires checking both consumers. Latest checked-in SDK version is 2.3.0; latest gateway version is 0.18.0. The snapshot does not contain registry or deployment state.
