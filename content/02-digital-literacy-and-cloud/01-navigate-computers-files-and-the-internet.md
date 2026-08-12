# Navigate Computers, Files, and the Internet

## Learning objectives

By the end of this lesson, you will be able to:

- distinguish an operating system, process, file, directory, and application;
- interpret absolute and relative paths;
- explain how a URL identifies a network resource; and
- gather basic diagnostic evidence before asking for help.

## A working mental model of a computer

An **operating system** manages hardware and provides services such as processes, files, networking, and permissions. An **application** is a program running through those services. A **process** is a particular running instance of a program. One program can have several processes, and a process can start child processes.

Files store bytes under names. A directory maps names to files and other directories. The file extension is a convention, not proof of content: renaming `report.json` to `report.png` does not convert JSON into an image. Tools infer formats from extensions, metadata, and sometimes the file's bytes.

An absolute path begins at a filesystem root and identifies a location independently of the current directory. A relative path is interpreted from the process's current working directory:

```text
/home/learner/project/data.json  # absolute on Linux
./data.json                      # relative to the current directory
../data.json                     # relative to the parent directory
```

Windows path syntax differs, but the ideas of root, separator, current directory, and parent directory remain.

## From a URL to a response

Consider:

```text
https://api.example.test:8443/v1/items?limit=10#results
```

- `https` is the scheme.
- `api.example.test` is the host name.
- `8443` is an explicit port.
- `/v1/items` is the path.
- `limit=10` is the query.
- `results` is a fragment interpreted by the client; it is normally not sent in the HTTP request.

At a high level, a client resolves a host name through DNS, opens a connection to an address and port, negotiates TLS for HTTPS, and exchanges HTTP messages. These layers matter during diagnosis. "The website is down" could mean name resolution failed, the connection was refused, TLS validation failed, the server returned an error, or the browser could not run the page.

## Capture facts before theories

A useful diagnostic note contains:

- the exact command or action;
- the working directory;
- the input, with secrets removed;
- complete error text;
- relevant tool and operating-system versions; and
- what changed since the last success.

Do not post access tokens, cookies, passwords, `.env` contents, or private customer data. Redact values while retaining key names and shapes when they matter.

## Free local practice

Open a terminal and create a disposable workspace:

```bash
mkdir -p digital-literacy-lab/docs
cd digital-literacy-lab
printf '{"course":"ai-agents","lessons":5}\n' > docs/course.json
pwd
ls -la
file docs/course.json
```

Without changing directories, predict which of these point to the same file, then verify with `ls`:

```text
docs/course.json
./docs/course.json
docs/../docs/course.json
../digital-literacy-lab/docs/course.json
```

Finally, take any public URL and label its scheme, host, port if explicit, path, query, and fragment. Do not need to visit it.

## Completion criteria

- [ ] You can explain program versus process in one example.
- [ ] You correctly resolved four relative paths from a known working directory.
- [ ] You labeled every relevant component of a URL.
- [ ] You produced a diagnostic note without exposing sensitive values.

## References

- [What is a URL?](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL) - MDN explanation of URL schemes, authority, paths, parameters, and fragments.
- [How the Web works](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works) - free overview of clients, servers, DNS, TCP/IP, HTTP, and component files.
- [The Linux Command Line](https://linuxcommand.org/tlcl.php) - freely downloadable book covering filesystems, commands, permissions, processes, and shell use.

## Continue

Next: [Use the Command Line and Git](02-use-the-command-line-and-git.md)
