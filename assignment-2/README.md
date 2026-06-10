<br>
<br>

## Overview

Overall, the way I completed Assignment #2 is to use a FastAPI API server on the first service on port 80, and since the second service is forbidden to expose any port and therefore forbidden to use another HTTP server like the first service, I implemented the second service using Docker's IPC (Inter-Process Communication) instead.

The deployment code as well as test code has been automated using Make:

```bash
# Build, run via Docker Compose, and test (output shown below).
make assignment-2
```

Under the hood, the way this works is by first building the two Docker images
using their respective `Dockerfile`; then deploying them with Docker Compose's
`ipc: "shareable"` flag on so that the two services can talk to each other via
one of the Python's Standard Library modules called
`multiprocessing.shared_memory.ShareableList`.

<br>

## Example

```
❯ curl http://127.0.0.1/romeo-and-juliet/thy --silent | jq
[
  "draw thy tool; here comes of the house of montagues.",
  "how? turn thy back and run?",
  <SNIP>
  "to press before thy father to a grave?",
  "o brother montague, give me thy hand."
]
❯ curl http://127.0.0.1/romeo-and-juliet/love --silent | jq
[
  "a pair of star-cross’d lovers take their life;",
  "the fearful passage of their death-mark’d love",
  <SNIP>
  "their course of love, the tidings of her death.",
  "that heaven finds means to kill your joys with love!"
]
❯ curl http://127.0.0.1/romeo-and-juliet/delicious --silent | jq
[
  "is loathsome in his own deliciousness,"
]
❯ curl http://127.0.0.1/romeo-and-juliet/food --silent | jq
[
  "shut up in prison, kept without my food,",
  "farewell, buy food, and get thyself in flesh.",
  "and in despite, i’ll cram thee with more food."
]
```

<br>
