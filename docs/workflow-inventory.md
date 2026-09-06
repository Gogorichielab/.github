# Workflow inventory and migration scope

Reviewed 2026-09-06 from each repository's default-branch snapshot.

## Coverage

- 24 repositories: 20 active and 4 archived.
- 48 workflow YAML files across 17 repositories; 47 files are in active repositories.
- Two generated agentic workflow lockfiles were inspected as generated output and are not migration targets.
- Seven repositories have no workflow YAML on their default branch.
- No repository-local `action.yml` or `action.yaml` definitions were found.
- 13 active repositories have matching adoption work: 9 public and 4 private.
- Workflow enabled/disabled state could not be retrieved through the available connector endpoint. A file's presence is not evidence that it is enabled. Verify state during adoption and do not reactivate intentionally disabled automation.

Coverage includes workflow triggers, job dependencies, permissions, action references, build/deploy paths, schedules, and available repository instructions. It does not include runtime execution, secret values, environment settings, or a complete organization ruleset audit. Non-default branches were not exhaustively audited; reconcile them before migration.

## Common patterns

Counts below are distinct repositories using the named action family, with versions combined. Generated agentic internals are excluded from these counts.

| Pattern/action family | Repositories | Decision |
| --- | ---: | --- |
| Checkout | 17 | Shared baseline; pin entrypoint and disable persisted credentials for build jobs |
| Node setup | 7 | Node CI starter for application/lint jobs; preserve specialized build/release jobs |
| General artifact upload | 6 | Preserve each consumer's report paths and retention |
| Pages configure/upload/deploy | 5 (one archived) | Pages starter; four active adoption targets |
| Stale processing | 5 | Stale starter; preserve each repository's policy |
| GitHub script | 5 | Scripts perform different operations; do not generalize solely because they use the same action |
| Terraform setup | 4 | Backend-free validation starter; cloud plans/applies stay local |
| Azure Static Web Apps deploy | 4 | SWA upload/preview-close starter |
| Dependabot metadata | 3 | Metadata-only auto-merge starter with explicit policy controls |
| Checkov | 2 | IaC scan starter with local artifact output |
| TFLint | 2 | Retain version/plugin and directory-specific behavior in consumers |

Multiple versions coexist, including checkout v2/v4/v5/v6/v7 and stale v9/v11. The new templates pin verified upstream commits with version comments. This is an adoption starting point, not a claim that every older action is broken.

## Public repository decisions

| Repository | Workflow files reviewed | Adoption |
| --- | ---: | --- |
| [Mainroad](https://github.com/Gogorichielab/Mainroad) | 1 | Node CI for the lint job; keep the Hugo compatibility matrix |
| [PPCollection](https://github.com/Gogorichielab/PPCollection) | 4 | Node CI, Pages, stale; preserve release, Docker, security, and smoke workflows |
| [mutli-tz](https://github.com/Gogorichielab/mutli-tz) | 2 | Pages; preserve build/changelog and monthly Dependabot cadence |
| [swearjar](https://github.com/Gogorichielab/swearjar) | 4 | SWA and stale; retain Function App/configuration and Azure preview-cleanup workflows |
| [nugget-tracker](https://github.com/Gogorichielab/nugget-tracker) | 3 | SWA and stale; preserve beacon injection, branch policies, and nightly application operation |
| [AMERICASTRONGFAMILYFEST](https://github.com/Gogorichielab/AMERICASTRONGFAMILYFEST) | 1 | Pages with the existing static-file staging list; no Node/bundler |
| [splcf1](https://github.com/Gogorichielab/splcf1) | 1 | Pages with spellcheck gate and explicit public-file staging |
| [terraform-azurerm-scaffold](https://github.com/Gogorichielab/terraform-azurerm-scaffold) | 2 | Terraform validation and Dependabot; preserve local-source example validation and provider-review policy |
| [terraform-grafana-influxdb-ds-module](https://github.com/Gogorichielab/terraform-grafana-influxdb-ds-module) | 5 | Add Terraform validation alongside TFLint; adopt Dependabot filtering; release remains separate |
| [gun-db](https://github.com/Gogorichielab/gun-db) | 4 | Keep specialized Python checks, Copilot setup, and release scripts; no matching migration in this tranche |
| [.github](https://github.com/Gogorichielab/.github) | 0 existing | Hosts templates and gains template-validation CI in this PR |
| [drip](https://github.com/Gogorichielab/drip) | 1 | Archived; Pages pattern recorded, no adoption issue or reactivation |
| [Gogorichie2020](https://github.com/Gogorichielab/Gogorichie2020) | 0 | Archived; no migration |
| [Azure-Inventory-Workbook](https://github.com/Gogorichielab/Azure-Inventory-Workbook) | 0 | Archived; no migration |

Private repository details stay in their own adoption issues. Of the ten private repositories, four have matching migration work, two retain specialized workflows, three active repositories have no workflows, and one is archived with no workflows.

## Preserve specialized behavior

- Release implementations differ: semantic-release, release-please, conventional changelog, custom tags, container publishing/signing, and module releases are not interchangeable.
- Branch cleanup differs in prefixes, inactivity periods, merged-PR checks, and protection handling. Keep it separate from the stale template.
- Backend credentials, Azure OIDC, Terraform plans/applies/drift, database schema deployment, and application-specific schedules remain local.
- Existing manual or disabled automation must not be enabled just because a template has a trigger.
- Generated `.lock.yml` workflows must be changed through their source/compiler if necessary, not hand-edited.
- Adoption issues are implementation work, not evidence that the consuming repositories have already migrated.

See [the adoption guide](workflow-templates.md) for templates, controls, validation, rollback, and the copied-template update model.
