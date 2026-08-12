# Build a Cloud Mental Model

## Learning objectives

By the end of this lesson, you will be able to:

- explain the essential characteristics of cloud computing;
- compare IaaS, PaaS, and SaaS by responsibility rather than branding;
- reason about regions, zones, scalability, availability, and cost; and
- model a cloud system locally before opening a paid account.

## Cloud is an operating model

Cloud computing is not merely "someone else's computer." The NIST definition identifies on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service. These properties explain why cloud systems can be provisioned quickly and billed by consumption.

Three service models move the responsibility boundary:

| Model | Provider commonly manages | Customer still manages |
| --- | --- | --- |
| IaaS | physical facilities, network, servers, virtualization | operating system, runtime, application, data, access configuration |
| PaaS | IaaS layers plus operating system and managed runtime | application, data, identities, service configuration |
| SaaS | complete hosted application | users, access policy, entered data, tenant configuration, appropriate use |

Managed does not mean responsibility-free. A provider may patch a database engine while the customer still controls who can read the records and how long data is retained.

## Location is part of the design

A **region** is a geographic area. A **zone** is an isolated deployment area within a region. Exact definitions vary by provider, so consult the selected service's documentation.

Placement creates tradeoffs:

- closer resources reduce latency;
- multiple failure domains can improve availability;
- cross-region transfer can add cost and complexity;
- data residency and legal obligations can restrict location; and
- a zonal resource may not survive a zone failure without replication.

Scalability means handling a changing workload. Availability means being usable when required. Durability means retaining data correctly over time. They are related but not interchangeable.

## Measured service creates cost risk

Cloud cost is a product of dimensions such as time, requests, stored bytes, transferred bytes, replicas, logs, and premium support. A free tier is a pricing rule, not a safety boundary. Before provisioning anything, set a budget, define teardown steps, and understand whether idle resources incur charges.

Use a simple estimate:

```text
monthly cost = fixed resources + usage + storage + network egress + observability + margin
```

The exact provider calculator changes, but the habit of listing cost drivers transfers.

## Free local practice

Design a study-tracker system with four logical components: browser, API, relational database, and file backup.

1. Draw the request and data flows.
2. Assign each component to IaaS, PaaS, or SaaS in two alternative designs.
3. Mark customer and provider responsibilities.
4. Identify one zonal failure, one regional failure, and one credential compromise.
5. Write a local analogue for every component: static HTML, a local process, SQLite, and a copied database file.
6. List at least five possible cloud cost drivers without creating an account.

The goal is architecture reasoning, not a provider deployment.

## Completion criteria

- [ ] You can name and explain the five NIST cloud characteristics.
- [ ] Your responsibility matrix includes data and identity management.
- [ ] You distinguish scalability, availability, and durability with examples.
- [ ] Your design includes failure domains, teardown, and cost drivers.

## References

- [NIST SP 800-145: The Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final) - primary public definition of characteristics, service models, and deployment models.
- [Google Cloud overview](https://docs.cloud.google.com/docs/overview) - concrete explanation of services, projects, resources, regions, and zones; the concepts transfer across providers.
- [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) - provider documentation illustrating how security responsibilities change by service type.
- [FinOps Framework](https://www.finops.org/framework/) - openly available framework for managing cloud value, usage, and accountability.

## Continue

Next: [Protect Accounts, Data, and Decisions](05-protect-accounts-data-and-decisions.md)
