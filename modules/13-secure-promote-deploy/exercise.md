# Exercise — Secure, promote and deploy

Run task oci:package and task oci:inspect with ORAS installed. With published container dependencies, generate real SBOMs and run the policy gate. Then follow docs/deployment.md to pull a promoted digest, deploy, discover, describe, inspect its package, execute, monitor and retrieve results. Record the artifact digest and successful job id.

From the repository root:

```console
task supply-chain:check
```

Expected outcome: Local package inspection succeeds. A configured ZOO environment can execute the promoted package; deployment requires an accessible staged input and server credentials.

Compare [the solution](solution.md). Return to [the module](README.md).
