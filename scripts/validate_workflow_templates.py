#!/usr/bin/env python3
"""Validate catalog pairing, YAML, pinned actions, and materialized workflow syntax."""

import argparse
import copy
import json
import re
import subprocess
import tempfile
from pathlib import Path

import yaml


class WorkflowLoader(yaml.SafeLoader):
    """Keep 'on' as a string while retaining YAML true/false booleans."""


WorkflowLoader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for key, rules in WorkflowLoader.yaml_implicit_resolvers.items():
    WorkflowLoader.yaml_implicit_resolvers[key] = [
        rule for rule in rules if rule[0] != 'tag:yaml.org,2002:bool'
    ]
WorkflowLoader.add_implicit_resolver(
    'tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$', re.I), list('tTfF')
)


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


WorkflowLoader.add_constructor('tag:yaml.org,2002:map', unique_mapping)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_workflow(path):
    content = path.read_text()
    data = yaml.load(content, Loader=WorkflowLoader)
    require(isinstance(data, dict), f'{path}: expected workflow mapping')
    require('on' in data and 'jobs' in data, f'{path}: missing events/jobs')
    require(data.get('permissions') == {'contents': 'read'},
            f'{path}: use read-only top-level permissions; grant writes per job')
    privileged = 'pull_request_target' in data['on']
    for job_id, job in data['jobs'].items():
        require('timeout-minutes' in job, f'{path}:{job_id}: missing timeout')
        for step in job.get('steps', []):
            action = step.get('uses')
            if action:
                require(re.fullmatch(r'[^@]+@[0-9a-f]{40}', action),
                        f'{path}: action must use full commit SHA: {action}')
                if privileged:
                    require(action.startswith('dependabot/fetch-metadata@'),
                            f'{path}: privileged metadata workflow cannot checkout/run PR code')
            if 'run' in step:
                require('${{' not in step['run'],
                        f'{path}: pass expression values through env instead of shell interpolation')
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--actionlint', required=True, help='Path to actionlint executable')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    catalog = root / 'workflow-templates'
    templates = sorted(catalog.glob('*.yml'))
    metadata = sorted(catalog.glob('*.properties.json'))
    require(templates, 'No templates found')
    require({p.stem for p in templates} == {p.name.removesuffix('.properties.json') for p in metadata},
            'Template/metadata files are not paired')
    names = set()
    with tempfile.TemporaryDirectory(prefix='workflow-templates-') as folder:
        materialized = []
        for template in templates:
            properties = json.loads(template.with_suffix('.properties.json').read_text())
            for key in ('name', 'description'):
                require(isinstance(properties.get(key), str) and properties[key].strip(),
                        f'{template}: missing metadata {key}')
            require(properties['name'] not in names, 'Duplicate catalog display name')
            names.add(properties['name'])
            for pattern in properties.get('filePatterns', []):
                re.compile(pattern)
            content = validate_workflow(template)
            for branch in ('main', 'master', 'release/stable'):
                target = Path(folder) / (template.stem + '-' + branch.replace('/', '-') + '.yml')
                target.write_text(content.replace('$default-branch', branch))
                materialized.append(str(target))
        own_workflows = sorted((root / '.github' / 'workflows').glob('*.yml'))
        for workflow in own_workflows:
            validate_workflow(workflow)
        subprocess.run(
            [args.actionlint, '-shellcheck=', '-pyflakes=', *materialized,
             *map(str, own_workflows)], check=True, cwd=root
        )
    print(f'Validated {len(templates)} template/metadata pairs, '
          f'{len(materialized)} branch substitutions, and {len(own_workflows)} repository workflows.')
    print('Static validation only: no deploy, apply, issue update, or merge was executed.')


if __name__ == '__main__':
    main()
