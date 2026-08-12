# Configure Runtime, Storage, and Networks

## Learning objectives

By the end of this lesson, you will be able to:

- separate image defaults from runtime configuration;
- choose between writable layers, bind mounts, volumes, and temporary filesystems;
- distinguish container ports from published host ports; and
- diagnose service connectivity using names and network membership.

## Build once, configure at runtime

An image should be reusable across development, test, and deployment. Supply environment-specific values when creating the container. Validate required configuration at startup and fail clearly when it is missing.

Environment variables are convenient but may be visible through process or container inspection and inherited by child processes. Do not treat them as automatically secure. Use the deployment environment's secret mechanism, narrow file permissions, and redaction in logs. Never bake secrets into images.

## Choose storage by lifecycle

- **Writable container layer:** temporary changes coupled to that container; removed with it.
- **Bind mount:** a specific host path mounted into a container; useful for development and host-managed files, but strongly couples host layout and permissions.
- **Named volume:** Docker-managed persistent storage, reusable across container replacement.
- **tmpfs mount:** memory-backed temporary data on supported systems; disappears when the container stops.

Mounts can hide files already present at the target path inside the image. Back up important volumes and test restoration. A volume outliving a container is persistence, not automatically a backup.

## Understand network scopes

`EXPOSE 8080` documents that the image listens on port 8080. `-p 127.0.0.1:8088:8080` publishes host loopback port 8088 to container port 8080. Binding to `127.0.0.1` limits access more than binding every host interface.

On a user-defined bridge network, containers can discover one another by container or service name. From one container, `localhost` refers to itself. To reach another container, use that service's network name and container port.

## Free local practice

Create a volume and network, then run the prior image:

```bash
docker volume create course-data
docker network create course-net
docker run --rm -d --name course-api --network course-net \
  -e COURSE_MODE=practice \
  --mount type=volume,src=course-data,dst=/data \
  -p 127.0.0.1:8080:8080 course-api:0.1
docker run --rm --network course-net curlimages/curl:latest \
  http://course-api:8080/
docker network inspect course-net
docker volume inspect course-data
docker stop course-api
```

Explain why the client uses `course-api:8080`, while the host uses `127.0.0.1:8080`. Repeat with an intentionally wrong `localhost:8080` inside the client container and retain the error as diagnostic evidence.

## Completion criteria

- [ ] You classify four storage mechanisms by lifecycle and ownership.
- [ ] You distinguish persistence from backup.
- [ ] You distinguish image `EXPOSE`, container port, and published host port.
- [ ] Two containers communicate by name on a user-defined network.
- [ ] You explain why `localhost` failed inside the separate client container.

## References

- [Docker Storage](https://docs.docker.com/engine/storage/) - official overview of writable layers, volumes, bind mounts, tmpfs, and storage drivers.
- [Volumes](https://docs.docker.com/engine/storage/volumes/) - official volume lifecycle, mounting, backup, and sharing documentation.
- [Docker Networking](https://docs.docker.com/engine/network/) - official overview of network drivers, port publishing, DNS, and container connectivity.
- [Manage Secrets Securely in Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/) - official discussion of secret files, per-service access, and the risks of storing sensitive data in environment variables, images, or source.

## Continue

Next: [Orchestrate Local Services with Compose](04-orchestrate-local-services-with-compose.md)
