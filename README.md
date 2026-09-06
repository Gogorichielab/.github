# Gogorichie Lab Organization Defaults

This repository hosts organization-level Copilot agents and the public [organization profile](profile/README.md). Supported community health defaults can also be maintained here when added.

## Workflow templates

The [workflow template catalog and adoption guide](docs/workflow-templates.md) provides shared starters for Node CI, GitHub Pages, Azure Static Web Apps, Terraform validation, Checkov scanning, stale maintenance, and Dependabot auto-merge. See the [workflow inventory](docs/workflow-inventory.md) for the patterns and migration scope.

Templates are copied into consuming repositories; changes here do not automatically update existing copies.

## Agent catalog

| Agent | Use it for | Scope |
| --- | --- | --- |
| [DevOps Agent](agents/devops-agent.agent.md) | CI/CD, infrastructure configuration, and deployment planning | Validates changes and separates configuration edits from live operations |
| [Documentation Agent](agents/docs-agent.agent.md) | Accurate guides and README updates | Follows the target repository's documentation layout and stack |
| [Test Scout](agents/qe-eng.agent.md) | Test design, regression coverage, and test reliability | Preserves assertions and reports actual execution results |
| [Refactor Mate](agents/refactor-eng.agent.md) | Structural refactoring and internal migrations | Preserves behavior and public compatibility |
| [Security Agent](agents/security-eng.agent.md) | Security review and requested remediation | Reports evidence and severity; does not itself enforce merge policy |
| [UI Engineer](agents/ui-eng.agent.md) | Frontend behavior, accessibility, and visual improvements | Uses existing patterns and distinguishes observed checks from recommendations |
| [Universal Janitor](agents/janitor.agent.md) | Small cleanup and proven dead-code removal | Protects regression coverage and operational resources |
| [Devils Advocate](agents/devils-advocate.agent.md) | Proposal stress-testing and design debate | Manually selected; read-only; supports bounded reviews |
| [Repo Architect Agent](agents/repo-architect.agent.md) | Repository instructions and host-specific agent setup | Uses portable AGENTS.md guidance and correct profile/skill layouts |

## Using the agents

Organization-level profiles belong in root `agents/` in this `.github` repository. Repository-specific Copilot profiles belong in that repository's `.github/agents/`. Availability depends on the host, account, and organization settings; verify discovery in your intended client.

The profiles use explicit tool lists. Editing roles include shell access for validation; those lists are not security sandboxes. Docs, QE, and UI include the Playwright namespace for supported browser work. DevOps and Security include the GitHub namespace for repository context. Only tools available in the host can be used; unsupported tools must be reported, not simulated.

Devils Advocate intentionally omits editing and execution tools and disables automatic model invocation. All profiles inherit the host's model choice.

Filenames use `.agent.md` consistently. The six former plain `.md` files retain their identifier before the suffix, preserving GitHub's filename-based identity; update any direct links or local copies that reference their old paths. Display names are retained.

## Repository instructions

[AGENTS.md](AGENTS.md) describes how to maintain this repository, including validation and PR expectations. It is separate from the agent profiles: it governs this repository and does not automatically provide organization-wide instructions to other repositories.

Each agent reads the target repository's own root and applicable nested `AGENTS.md` files and existing contribution guidance. Repository-specific commands and conventions belong there. Keep human onboarding in the README and detailed agent guidance in `AGENTS.md`.

## Validation

There is no application build or test suite in this repository. For profile changes, review YAML frontmatter, tool selections, identifiers, links, and instruction consistency, then run the Git checks in [AGENTS.md](AGENTS.md).

Validate discovery and representative behavior in the intended Copilot or OpenCode client separately. A successful static check does not establish runtime compatibility or merge enforcement.

## References

- [AGENTS.md format and guidance](https://agents.md/)
- [Creating organization-level Copilot agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents)
- [Copilot configuration and tool aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
