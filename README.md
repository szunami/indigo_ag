## Transport Take Home Exercise

This repository contains source code for Sam Szuflita's application to Indigo Ag.

This code was tested against `Python 3.9.4` and `Flask 2.0.1`. Other tools and dependencies are described in `requirements.txt`.

### Commands

Run debug server:
```
FLASK_APP=app.main flask run
```

Run integration tests (Note: these use a rolling window of 1 second):
```
pytest
```

`get.http` and `post.http` contain sample HTTP requests that I used while developing this solution.

### Source overview

All relevant logic for this application lives in `main.py`. At a high level, the application stores a list of `(timestamp, value)` tuples and a cached sum per `key`. On `POST`, a new value is appended to the appropriate list and the sum is updated. On `GET`, the app removes any values that are more than `window` old (default is 1 hour) and subtracts their value from the cached sum.

This design optimizes for a case in which the `POST` operation is more performance sensitive than the `GET`. The `POST` requires a constant number of operations, while a `GET` requires reading through N values to purge them. In my experience, it is much more likely that this kind of `POST` will wind up in a hot loop in code, and the `GET` will mostly happen when we are loading a dashboard. Given this, I chose to remove stale values in the `GET` request.