# WeTalk
Anonymous live chatting app.

## Benchmarks

| Users | Messages/s | CPU load (%) | Egress traffic (Mb/s) | Remarks |
| ------ | ------ | ------ | ------ | ------ |
| 0 | 0 | 0-1 | - | Server uses minimal resources
| 5 | 20 | 3 | 0.19 | Everything works as intended
| 10 | 40 | 4-6 | 0.80 | Everything works as intended
| 20 | 78 | 9-13 | 4 | Chat client experiences minimal lag 
| 40 | 154 | 14-23 | 10 | Chat clinet crashed
| 80 | 310 | 45-48 | 42 | Unable to use client
| 160 | 620 | 52-54 | 88 | Unable to use client
| 320 | 1240 | 54-58 | 180 | Server throws exceptions if all join at once


