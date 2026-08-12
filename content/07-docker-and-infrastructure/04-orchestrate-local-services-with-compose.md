# Orchestrate Local Services with Compose

## Learning objectives

By the end of this lesson, you will be able to:

- describe a multi-container application declaratively;
- use service names, networks, volumes, health checks, and dependencies;
- inspect the effective configuration and lifecycle; and
- avoid assuming that startup order means readiness.

## Compose describes an application model

A Compose file defines services and their configuration, plus shared networks, volumes, configs, and secrets. `docker compose up` reconciles those definitions into containers and related resources. It is useful for local development, tests, and some deployments; it is not a universal replacement for every production orchestrator.

Compose creates a default network and registers service names in internal DNS. A service should connect to `api:8080`, not a changing container IP. Only publish ports that the host or external clients need.

## Dependencies have different meanings

A dependency can express creation order. It does not necessarily mean the dependency is ready to serve. A database process may start before it accepts queries. Add a meaningful health check and make the application itself tolerate dependency restart and temporary unavailability.

Health checks should be cheap, bounded, and reflect required function. They should not create business side effects. A liveness-style check asks whether restart may help; a readiness-style check asks whether traffic should be sent. Docker health status is one signal, not a complete availability design.

## Free local practice

Use the `Dockerfile` and `app.py` from lesson 2. Create `compose.yaml`:

```yaml
services:
  api:
    build: .
    ports:
      - "127.0.0.1:8080:8080"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/', timeout=2)"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 2s

  check:
    build: .
    depends_on:
      api:
        condition: service_healthy
    command: ["python", "-c", "import urllib.request; print(urllib.request.urlopen('http://api:8080/').read().decode())"]
```

Run and inspect:

```bash
docker compose config
docker compose up --build
docker compose ps
docker compose logs api
docker compose down
```

Run `check` again with `docker compose run --rm check`. Remove the health condition, add a startup delay to the API, and observe why creation order alone can race.

## Configuration rules

- Commit the Compose file and a non-secret `.env.example`, not actual secrets.
- Use named volumes for persistent service data.
- Use separate internal networks to reduce unnecessary reachability.
- Set restart policies deliberately; restarts can hide persistent failure loops.
- Inspect `docker compose config` to see interpolation and the effective model, but avoid exposing secrets in shared output.
- Use `docker compose down -v` only when intentionally deleting named project volumes.

## Completion criteria

- [ ] The effective Compose configuration renders successfully.
- [ ] The client reaches the API by service name without a published client port.
- [ ] The health check is bounded and side-effect free.
- [ ] You demonstrated startup order versus service readiness.
- [ ] Teardown preserves or deletes data only according to an explicit decision.

## References

- [Docker Compose](https://docs.docker.com/compose/) - official entry point for the application model, lifecycle, installation, and reference.
- [Compose Application Model](https://docs.docker.com/compose/intro/compose-application-model/) - official explanation of services, networks, volumes, configs, secrets, and projects.
- [Networking in Compose](https://docs.docker.com/compose/how-tos/networking/) - official service discovery, default networks, port distinctions, updates, and debugging.
- [Compose `depends_on`](https://docs.docker.com/reference/compose-file/services/#depends_on) - exact semantics for creation order and health-based dependency conditions.

## Continue

Next: [Harden, Observe, and Debug Containers](05-harden-observe-and-debug-containers.md)
