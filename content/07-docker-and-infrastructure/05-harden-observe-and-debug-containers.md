# Harden, Observe, and Debug Containers

## Learning objectives

By the end of this lesson, you will be able to:

- apply least privilege to a container build and runtime;
- collect logs, health, resource, and provenance evidence;
- diagnose common container failures systematically; and
- define promotion and rollback criteria for an image.

## Containers are a security boundary that needs defense in depth

Reduce capabilities and attack surface:

- use a minimal, trusted base and update it deliberately;
- run as a non-root user when the application permits it;
- avoid `--privileged`, host namespaces, and the Docker socket;
- drop Linux capabilities and add only those proven necessary;
- make the root filesystem read-only when feasible;
- mount only required data, with read-only access where possible;
- set CPU and memory limits appropriate to the environment;
- keep secrets out of images and logs; and
- scan dependencies and record image provenance.

The Docker daemon is highly privileged in ordinary rootful mode. Access to its socket is effectively administrative control over the host. Rootless mode reduces some daemon and runtime risk but does not remove application vulnerabilities.

## Observe the process, not just container status

"Running" means the main process has not exited. It does not prove correct service. Capture:

- structured stdout/stderr logs with request IDs;
- health and dependency status;
- CPU, memory, network, and storage use;
- restart and exit counts;
- image digest, configuration, and deployment time; and
- application metrics tied to user outcomes.

Apply retention and redaction. More logs can increase cost and privacy risk.

## Diagnose in layers

1. Is the expected container present and running?
2. What exit code and error do logs show?
3. Is runtime configuration present and valid?
4. Is the process listening on the expected interface and port?
5. Is the port published only where intended?
6. Do DNS and network membership match the design?
7. Are mounts present with correct ownership and permissions?
8. Are resource limits or health checks causing termination?
9. Does the exact image work in a minimal isolated test?

Change one variable and retain evidence.

## Free local practice: harden the local API

Update the Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-alpine
RUN addgroup -S app && adduser -S -G app app
WORKDIR /app
COPY --chown=app:app app.py .
USER app
EXPOSE 8080
CMD ["python", "app.py"]
```

Rebuild, then run:

```bash
docker build --pull -t course-api:0.2 .
docker run --rm -d --name hardened-api \
  --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  --cap-drop ALL --memory 128m --cpus 0.5 \
  -p 127.0.0.1:8080:8080 course-api:0.2
docker top hardened-api
docker stats --no-stream hardened-api
docker inspect hardened-api
curl http://127.0.0.1:8080/
docker stop hardened-api
```

Document which controls are visible in inspection and what they do not protect against. Define a rollback to image `0.1` by immutable image ID or digest, not by assuming a tag never moved.

## Completion criteria

- [ ] The service works as a non-root user with all capabilities dropped.
- [ ] The root filesystem is read-only and required temporary writes are explicit.
- [ ] You captured logs, process identity, health, resource, and image evidence.
- [ ] Your diagnostic checklist distinguishes process, configuration, network, storage, and resource failures.
- [ ] Promotion and rollback refer to a verified immutable image identity.

## References

- [Docker Security](https://docs.docker.com/engine/security/) - official overview of namespaces, daemon attack surface, capabilities, and related controls.
- [Rootless Mode](https://docs.docker.com/engine/security/rootless/) - official explanation and setup for running daemon and containers without root privileges.
- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/) - official guidance for trusted bases, rebuilding, pinning, cache, multi-stage builds, and CI.
- [Docker Scout: Image Analysis](https://docs.docker.com/scout/explore/analysis/) - official documentation for package inventories, vulnerabilities, and image policy evidence.
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) - publicly described consensus benchmark for securing Docker environments; access terms may require registration.

## Continue

Next module: [Understand MCP Architecture and Lifecycle](../08-model-context-protocol/01-understand-mcp-architecture-and-lifecycle.md)
