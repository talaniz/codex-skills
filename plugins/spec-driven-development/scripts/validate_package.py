#!/usr/bin/env python3
"""Validate this self-contained bundle without third-party packages or installation."""
import ast
import json
import re
import sys
from pathlib import Path

EXPECTED={'ideate','build-author','pre-dev-prep','tdd','pr-author','merge-manager','close-milestone'}

def validate(root):
    root=Path(root).resolve()
    manifest=json.loads((root/'.codex-plugin/plugin.json').read_text())
    assert manifest['name']==root.name=='spec-driven-development','Plugin identity mismatch'
    assert re.fullmatch(r'\d+\.\d+\.\d+',manifest['version']),'Invalid version'
    assert manifest['skills']=='./skills/' and manifest['author']['name'],'Missing metadata'
    assert {p.name for p in (root/'skills').iterdir() if p.is_dir()}==EXPECTED,'Expected seven entrypoints'
    for name in EXPECTED:
        path=root/'skills'/name/'SKILL.md';text=path.read_text()
        assert re.match(r'---\nname: '+re.escape(name)+r'\ndescription: .+\n---\n',text),'Invalid skill metadata: '+name
        ui=(path.parent/'agents/openai.yaml').read_text()
        assert '$'+name in ui,'Default prompt must invoke skill'
    for file in root.rglob('*'):
        assert not file.is_symlink(),'Package symlinks unsupported'
        if file.suffix=='.py':ast.parse(file.read_text(),filename=str(file))
        if file.suffix!='.md':continue
        text=re.sub(r'```.*?```','',file.read_text(),flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            if '://' in target or target.startswith('#'):continue
            resolved=(file.parent/target.split('#')[0]).resolve()
            assert resolved.is_relative_to(root) and resolved.is_file(),'Missing/outside bundled reference: '+target
    print('Validated seven skills, plugin metadata, bundled references and Python syntax')

if __name__=='__main__':
    try:validate(Path(__file__).resolve().parents[1])
    except (AssertionError,ValueError,KeyError,OSError,SyntaxError) as e:
        print('Invalid package: '+str(e),file=sys.stderr);sys.exit(1)
