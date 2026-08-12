# Protect Accounts, Data, and Decisions

## Learning objectives

By the end of this lesson, you will be able to:

- apply a practical baseline for account and device security;
- classify data before placing it in a cloud or AI service;
- distinguish authentication, authorization, encryption, and backup; and
- evaluate digital claims with traceable evidence.

## Start with identity

Authentication establishes who or what is making a request. Authorization determines what that identity may do. A valid login does not imply permission to every record.

For personal and project accounts:

- use unique passwords generated and stored by a password manager;
- enable phishing-resistant multifactor authentication where available;
- save recovery codes offline in a protected location;
- keep operating systems, browsers, and tools updated; and
- treat urgent requests for credentials or code execution as hostile until independently verified.

API keys and tokens are credentials too. Store them outside source files, grant the smallest useful scope, rotate them after suspected exposure, and avoid printing them in logs.

## Classify before sharing

Use a small data inventory:

| Field | Source | Sensitivity | Purpose | Retention | Allowed destinations |
| --- | --- | --- | --- | --- | --- |
| email | user | personal | account notice | 90 days | approved mail provider |
| API token | provider | secret | authentication | until rotation | secret store only |
| study note | learner | internal | learning | as needed | local repository |

Do not send confidential work, personal identifiers, health or financial data, access credentials, or third-party copyrighted material to an AI service merely because the interface is convenient. Check the service terms, data controls, organizational policy, and applicable law. When possible, replace real data with minimal synthetic examples.

## Separate controls

- **Encryption in transit** protects data while connections carry it.
- **Encryption at rest** protects stored media under specified threat assumptions.
- **Authorization** limits permitted operations.
- **Backups** create recoverable copies.
- **Logging** provides evidence of events.

One control does not substitute for another. Encrypted deletion is still deletion; encrypted data exposed to an overprivileged account is still accessible; a backup that has never been restored is an assumption.

## Think critically about digital claims

For a technical or AI-generated claim:

1. separate the exact claim from persuasive language;
2. identify what evidence would confirm or falsify it;
3. prefer the governing specification, official documentation, source code, or original paper;
4. check version and publication date;
5. reproduce a minimal example where feasible; and
6. state remaining uncertainty.

Search snippets and generated answers are leads, not evidence. A citation is useful only when the linked source actually supports the nearby claim.

## Free local practice: local security review

Review `digital-literacy-lab` without uploading it anywhere:

```bash
git status --short
git log --oneline --all
git grep -n -i -E 'password|secret|token|api[_-]?key' -- . ':!*.md'
```

Then write `security-review.md` containing:

- assets worth protecting;
- likely threats;
- current controls;
- one recovery test;
- data that must not leave the device; and
- three prioritized improvements.

Use obviously fake credentials if you need test strings. Never paste a real secret into the lab.

## Completion criteria

- [ ] You can distinguish authentication from authorization.
- [ ] Your data inventory includes purpose, retention, and allowed destinations.
- [ ] You identified one preventive, one detective, and one recovery control.
- [ ] You verified a technical claim against a primary or official source.
- [ ] No real credential appears in the practice repository or its history.

## References

- [Secure Our World](https://www.cisa.gov/secure-our-world) - CISA's public baseline on phishing, strong unique passwords, password managers, MFA, and software updates.
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework) - voluntary framework for identifying and managing privacy risk.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) - practical guidance on secret lifecycle, storage, rotation, auditing, and access.
- [SIFT: The Four Moves](https://hapgood.us/2019/06/19/sift-the-four-moves/) - publicly available method for investigating online claims by stopping, tracing, finding coverage, and locating original context.

## Continue

Next module: [Frame Problems for AI](../03-ai-fundamentals/01-frame-problems-for-ai.md)
