# 07. Docker and Infrastructure

Move from container concepts to reproducible images, runtime configuration, storage, networks, Compose, hardening, observability, debugging, backup, and rollback. The emphasis is operational evidence, not merely starting a container.

## Before you begin

Complete [Module 06](../06-web-apis-and-webhooks/index.md). Install Docker Engine or Docker Desktop if your machine supports it; retain a written architecture exercise if container execution is unavailable.

## Lessons

1. [Understand Images and Containers](01-understand-images-and-containers.md)
2. [Build Reproducible Images with Dockerfiles](02-build-reproducible-images-with-dockerfiles.md)
3. [Configure Runtime, Storage, and Networks](03-configure-runtime-storage-and-networks.md)
4. [Orchestrate Local Services with Compose](04-orchestrate-local-services-with-compose.md)
5. [Harden, Observe, and Debug Containers](05-harden-observe-and-debug-containers.md)

## Suggested artifact

Deliver a small Compose stack with pinned images, health checks, non-root execution, named storage, isolated networks, secret-free configuration, structured logs, and a tested backup-and-restore runbook.

## Practice lab

[Docker Health Stack](https://github.com/velrino/course/tree/master/labs/docker-health-stack) turns those controls into an executable local service and health-check exercise.

## Continue

Use these local service boundaries while building an integration protocol in [Module 08: Model Context Protocol](../08-model-context-protocol/index.md).
