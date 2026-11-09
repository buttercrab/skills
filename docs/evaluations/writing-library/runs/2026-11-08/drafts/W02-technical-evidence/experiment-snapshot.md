# Synthetic snapshot — Cedar trial

Source label: [S1]. Frozen May 9. These are all the available measurements.

## Service and intervention
Cedar generates image previews from uploaded files. In the trial configuration it checked an in-memory result cache before rendering. A cache hit reused a previous preview. Cache misses still rendered. No other architecture details were recorded here.

## Logged windows
| Window | Configuration | Successful requests | Median latency | p95 latency | Cache-hit share |
|---|---|---:|---:|---:|---:|
| Monday 10:00–11:00 | cache off | 10,000 | 200 ms | 900 ms | not applicable |
| Tuesday 10:00–11:00 | cache on | 12,000 | 120 ms | 840 ms | 35% |

Each row summarizes all successful requests in its own window. The windows were not randomized or paired. The request mix and input sizes were not logged. Failed requests were excluded; failure counts were not recorded. No interval estimates were calculated. This packet has no CPU, memory, power, or energy measurements.

## Separate bench note
A separate service, Birch, ran a fixed repeated-input benchmark with a disk cache. Its median fell from 250 ms to 125 ms. Birch uses a different renderer. The benchmark has no Cedar requests. Source label: [S2].
