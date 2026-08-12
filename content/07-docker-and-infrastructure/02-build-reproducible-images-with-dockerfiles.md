# Build Reproducible Images with Dockerfiles

## Learning objectives

By the end of this lesson, you will be able to:

- explain build context, instructions, layers, and cache;
- write a small Dockerfile with predictable startup behavior;
- reduce image size and accidental data inclusion; and
- distinguish build-time arguments from runtime configuration and secrets.

## A Dockerfile is a build recipe

The builder receives a Dockerfile and a build context. Instructions create image configuration and filesystem layers. Common instructions include:

- `FROM` selects a base and starts a stage;
- `WORKDIR` establishes the working directory;
- `COPY` copies files from the build context;
- `RUN` executes a build step;
- `ENV` sets image environment defaults;
- `USER` selects the runtime user;
- `EXPOSE` documents a listening port but does not publish it; and
- `CMD` or `ENTRYPOINT` defines startup behavior.

The build context is data the builder can access. Exclude Git history, secrets, dependency caches, and unrelated large files with `.dockerignore`. Never assume deleting a secret in a later layer removes it from earlier layers or build records.

## Arrange layers for correctness and cache reuse

Build cache reuses a step when its instruction and relevant inputs have not changed. Copy dependency manifests and install dependencies before copying frequently changed source when the ecosystem supports it. Combine commands when atomic cleanup matters, but do not compress everything into an unreadable line.

Use multi-stage builds when compilation needs tools that the runtime does not. Copy only the final artifact into a smaller runtime stage. Pin dependencies and base-image versions according to your update process; tags alone can move.

## Define process behavior explicitly

Exec-form `CMD`, such as `CMD ["python", "app.py"]`, avoids an extra shell and improves signal handling. The main process should log to stdout/stderr, handle termination, and exit nonzero when startup fails.

Build arguments and environment variables are not secret stores. Secret mounts provided by BuildKit can expose a value to one build step without intentionally recording it in the image, but the step itself must not copy or print it.

## Free local practice

Create `app.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"status":"ok"}\n'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
```

Create `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-alpine
WORKDIR /app
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
```

Create `.dockerignore` containing `.git`, `.env`, `__pycache__`, and `*.log`, then:

```bash
docker build -t course-api:0.1 .
docker run --rm -d --name course-api -p 127.0.0.1:8080:8080 course-api:0.1
curl http://127.0.0.1:8080/
docker stop course-api
docker history course-api:0.1
```

Change one source line, rebuild, and explain which steps reused cache.

## Completion criteria

- [ ] The image builds and returns the expected local response.
- [ ] The build context excludes secrets and unrelated files.
- [ ] You distinguish `EXPOSE` from publishing with `-p`.
- [ ] Startup uses exec-form `CMD`.
- [ ] You inspected layers and explained cache behavior after a source change.

## References

- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/) - authoritative instructions, forms, variables, mounts, health checks, and `.dockerignore` behavior.
- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/) - official recommendations on bases, context, cache, multi-stage builds, pinning, and ephemeral containers.
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/) - official guide to separating build tooling from runtime images.
- [Build Secrets](https://docs.docker.com/build/building/secrets/) - official guidance for secret and SSH mounts during builds.

## Continue

Next: [Configure Runtime, Storage, and Networks](03-configure-runtime-storage-and-networks.md)
