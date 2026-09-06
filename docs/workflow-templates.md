# Organization workflow templates

These seven GitHub starter templates are based on the organization's existing workflows. Each YAML file has matching `.properties.json` metadata for the Actions catalog.

## Catalog and customization

| Template | Shared pattern | Required adaptation |
| --- | --- | --- |
| [Node CI](../workflow-templates/node-ci.yml) | Checkout, Node setup/cache, npm install, quality checks | Preserve Node version, working directories, lockfiles, real scripts, security gates, and test artifacts |
| [GitHub Pages](../workflow-templates/pages.yml) | Build/stage, upload Pages artifact, protected deployment | Insert the real build/copy steps, set SITE_DIRECTORY, and preserve quality gates, CNAME, and post-deploy jobs |
| [Azure Static Web Apps](../workflow-templates/azure-static-web-apps.yml) | Production upload, trusted PR preview, PR-close cleanup | Set app/API/output paths, build prerequisites, token mappings, environment names, smoke tests, and dependencies |
| [Terraform validation](../workflow-templates/terraform-validate.yml) | Setup Terraform, fmt, backend-free init, validate | Preserve version, root-module matrix, example source rewrites, Terraform tests, and TFLint |
| [Terraform Checkov](../workflow-templates/terraform-checkov.yml) | IaC scan and findings artifact | Set scan directory, configuration/exclusions, external-module needs, and the current soft/hard-fail policy |
| [Stale maintenance](../workflow-templates/stale-maintenance.yml) | Scheduled stale issue/PR processing | Preserve schedule, thresholds, exemptions, and labels; run dry-run before enabling |
| [Dependabot auto-merge](../workflow-templates/dependabot-auto-merge.yml) | Verified metadata, update-class filtering, queued merge | Preserve approved ecosystems/cadence and required checks/reviews; explicitly enable after review |

The Pages starter intentionally fails until a real site is staged. Node CI intentionally fails if required scripts are absent: adapt its commands instead of hiding missing checks. Terraform validation is a baseline, not a replacement for plans, tests, TFLint, or deployment approval.

## Adoption

1. Merge the templates PR into this repository's default branch. Check the organization's Actions catalog and account/plan access in the consuming repository.
2. Open **Actions → New workflow**, select the applicable organization template, and customize it in a branch. Alternatively, copy the YAML from `workflow-templates/` into the consuming repository's `.github/workflows/`; replace every `$default-branch` with the actual branch name when copying manually.
3. Follow that repository's adoption issue. Where a workflow mixes shared and specialized jobs, adapt only the matching jobs in place rather than replacing the entire file.
4. Preserve workflow/job names used by required checks, trigger/path filters, job `needs`, deployment environments, and secret mappings. Update required-check configuration only as an explicitly reviewed migration step.
5. Test a representative internal PR and a fork/Dependabot PR where applicable. Run deploy verification only in an authorized environment, then confirm production gating and preview cleanup.
6. Disable/remove overlapping jobs only after equivalent checks pass. Never run two copies of deployment, stale-item, branch-cleanup, or auto-merge automation.
7. Record the source template commit and local differences in the consuming workflow. Roll back by reverting the adoption commit and restoring the previous workflow/check configuration.

These are **copied workflow templates**, not `workflow_call` reusable workflows. Updating this repository does not automatically update existing copies. Review action-version and policy updates through consuming-repository PRs. A later reusable-workflow extraction can centralize maintenance once stable interfaces and deployment boundaries have been proven.

Templates do not inherit other repositories' secrets, settings, environments, or branch protection.

## Opt-in controls

### Static Web Apps

Map `AZURE_STATIC_WEB_APPS_API_TOKEN` to the correct app in both the upload and close jobs. Existing environment-scoped tokens must remain correctly scoped; preserve current environment names where they differ from the starter's `production` and `preview`.

Set `SWA_ENABLE_PREVIEWS=true` only when trusted same-repository preview deployment is configured. Fork and Dependabot PRs receive no deployment credentials; retain separate secret-free CI for them. Close-preview does not checkout PR code. Disabling previews does not remove already-existing Azure preview environments.

### Stale maintenance

Scheduled runs require `STALE_AUTOMATION_ENABLED=true`. Manual dispatch defaults to `dry_run=true`, which uses the action's `debug-only` mode.

Issue aging is disabled in the starter; PR aging defaults to 30 days plus 7 days before closure. Copy the repository's approved thresholds and messages before enabling. Preserve repositories that intentionally never stale/close issues. Ensure stale/exemption labels exist. Branch deletion is not part of this template because existing age, prefix, merged-status, and protection policies differ.

### Dependabot auto-merge

The starter requires all of the following:

- `DEPENDABOT_AUTOMERGE_ENABLED=true`.
- A verified Dependabot PR from the same repository with the `automerge` label.
- A minor or patch update in the allowed ecosystem list. `DEPENDABOT_AUTOMERGE_ECOSYSTEMS` is a JSON array, defaulting to `["github-actions"]`.
- Repository auto-merge enabled and reviewed required status checks/reviews.

The metadata-only `pull_request_target` job never checks out or runs PR code. It queues a squash merge for the expected head commit and does not approve reviews or bypass protection. **If no effective requirements are configured, `--auto` can merge immediately.** Verify protections before enabling the variable.

Keep Terraform provider updates manual in repositories where a provider-floor change is a breaking release. Do not replace a monthly merge window with event-driven merging without a separate policy decision. If existing approved bot review behavior must be retained, implement it explicitly without executing PR code and document that choice in the adoption PR.

## Validation and action updates

Run from the repository root with Python, PyYAML 6.0.3, and actionlint 1.7.12 available:

```sh
python scripts/validate_workflow_templates.py --actionlint /path/to/actionlint
git diff --check
```

The validation workflow installs the pinned actionlint release and verifies its SHA-256 checksum. The script checks catalog pairing, metadata, duplicate YAML keys, workflow structure, explicit read-only top-level permissions, action SHA pins, timeouts, and privileged metadata-only action selection. It runs actionlint after replacing the default-branch placeholder with `main`, `master`, and `release/stable`.

ShellCheck and pyflakes integration are disabled so this gate has no implicit tooling dependencies. This is static validation, not deployment or runtime verification. Pinning an action entrypoint does not pin every dependency or container image that action may download.

When updating a pin, resolve the upstream tag to its commit, review release notes/runner requirements, update the version comment, and rerun validation. Use GitHub-hosted Ubuntu runners unless a consuming repository has verified compatible self-hosted runners.

## References

- [GitHub workflow templates](https://docs.github.com/en/actions/how-tos/reuse-automations/create-workflow-templates)
- [Reusable workflows and their different update model](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [actionlint](https://github.com/rhysd/actionlint)
