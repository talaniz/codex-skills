"""Local, bounded workflow operations. No network, commits, merges or authorization."""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit

RECORD = 'harness/milestone.json'

def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError('Git operation failed: ' + args[0])
    return result.stdout.strip()

def root(repo):
    p = Path(repo).resolve(strict=True)
    if Path(git(p, 'rev-parse', '--show-toplevel')).resolve() != p:
        raise ValueError('Use the repository root')
    return p

def safe(repo, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError('Invalid repository path')
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or '.git' in p.parts or str(p) != relative:
        raise ValueError('Unsafe repository path')
    current = repo
    for part in p.parts:
        current /= part
        if current.is_symlink():
            raise ValueError('Symlink paths are not supported')
    if not current.resolve().is_relative_to(repo):
        raise ValueError('Path escaped repository')
    return current

def inspect(repo):
    repo = root(repo)
    return {'head':git(repo,'rev-parse','HEAD'),
            'branch':git(repo,'branch','--show-current'),
            'dirty':bool(git(repo,'status','--porcelain','--untracked-files=all')),
            'worktrees':git(repo,'worktree','list','--porcelain')}

def load_record(repo, head):
    git(repo, 'ls-files', '--error-unmatch', '--', RECORD)
    data = json.loads(safe(repo, RECORD).read_text())
    required = {'id','status','recorded_by','reviewed_head','required_checks','checks','reviews','files'}
    if not isinstance(data, dict) or not required <= data.keys():
        raise ValueError('Missing milestone fields')
    if data['status'] != 'completed' or not isinstance(data['recorded_by'],str) or not data['recorded_by'].strip():
        raise ValueError('Main must record completion first')
    if not isinstance(data['id'],str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',data['id']):
        raise ValueError('Invalid milestone ID')
    reviewed = data['reviewed_head']
    if not isinstance(reviewed,str) or not re.fullmatch(r'[0-9a-f]{40}',reviewed):
        raise ValueError('Invalid reviewed head')
    git(repo,'merge-base','--is-ancestor',reviewed,head)
    changed = git(repo,'diff','--name-only',reviewed,head,'--').splitlines()
    if any(p != RECORD for p in changed):
        raise ValueError('Only the completion record may change after reviewed HEAD')
    reviews=data['reviews']
    if not isinstance(reviews,list) or len(reviews)!=2 or {r.get('role') for r in reviews if isinstance(r,dict)}!={'code','e2e'}:
        raise ValueError('Both independent reviews required')
    identities=[]
    for r in reviews:
        if r.get('head')!=reviewed or r.get('verdict')!='sign-off' or not isinstance(r.get('reviewer'),str) or not r['reviewer'].strip() or not isinstance(r.get('evidence'),str) or not r['evidence'].startswith('https://'):
            raise ValueError('Missing exact-head review evidence')
        identities.append(r['reviewer'])
    if len(set(identities+[data['recorded_by']]))!=3:
        raise ValueError('Reviewers must be distinct from each other and main')
    required_checks=data['required_checks']
    if not isinstance(required_checks,list) or not required_checks or any(not isinstance(n,str) or not n.strip() for n in required_checks) or len(set(required_checks))!=len(required_checks):
        raise ValueError('Explicit required checks needed')
    checks=data['checks']
    if not isinstance(checks,list) or len(checks)!=len(required_checks) or any(not isinstance(c,dict) for c in checks) or {c.get('name') for c in checks}!=set(required_checks) or any(c.get('head')!=reviewed or c.get('status')!='passed' for c in checks):
        raise ValueError('Required checks have not passed at reviewed HEAD')
    return data

def link_target(repo, source, target):
    url=urlsplit(target)
    if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
        return None
    return (repo/source).parent.joinpath(unquote(url.path)).resolve()

def rewrite(repo, source, destination, text, moves):
    mapping={safe(repo,a).resolve():safe(repo,b) for a,b in moves.items()}
    # Refuse syntax this intentionally small rewriter cannot interpret safely.
    pattern = r'(!?\[[^\]\n]*\]\()([^()\n]*)\)'
    if text.count('](') != len(re.findall(pattern, text)):
        raise ValueError('Nested or escaped Markdown links are unsupported')
    for code in re.findall(r'(```.*?```|~~~.*?~~~|`[^`\n]*`)', text, re.S):
        if '](' in code:
            raise ValueError('Markdown link syntax in code examples requires manual review')
    for target in re.findall(r'<([^<>\s]+)>', text):
        resolved = link_target(repo, source, target)
        if resolved in mapping or (source != destination and resolved is not None):
            raise ValueError('Affected autolink unsupported')
    # References and HTML are left untouched unless they reference a moving record.
    for target in re.findall(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)',text,re.M)+re.findall(r'(?:href|src)=["\']([^"\']+)',text):
        resolved = link_target(repo, source, target)
        if resolved in mapping or (source != destination and resolved is not None):
            raise ValueError('Affected reference/HTML link unsupported; use a simple inline link')
    def replace(match):
        target=match.group(2)
        original=link_target(repo,source,target)
        if original is None:
            return match.group(0)
        if re.search(r'[\s<>\\]',target):
            raise ValueError('Inline links with titles, spaces or escapes are unsupported')
        url=urlsplit(target)
        new_target=mapping.get(original,original)
        if source==destination and original not in mapping:
            return match.group(0)
        relative=os.path.relpath(new_target,(repo/destination).parent).replace(os.sep,'/')
        suffix=('?'+url.query if url.query else '')+('#'+url.fragment if url.fragment else '')
        return match.group(1)+quote(relative,safe='/._-')+suffix+')'
    return re.sub(r'(!?\[[^\]\n]*\]\()([^()\n]*)\)',replace,text)

def preview(repo):
    repo=root(repo)
    state=inspect(repo)
    if state['dirty'] or not state['branch']:
        raise ValueError('Archive requires a clean repository on a named branch')
    data=load_record(repo,state['head'])
    paths=data['files']
    prefix=f"harness/active/{data['id']}/"
    if not isinstance(paths,list) or not paths or len(paths)>1000 or any(not isinstance(p,str) for p in paths) or len(set(paths))!=len(paths):
        raise ValueError('Explicit unique milestone files required')
    tracked=set(git(repo,'ls-files','-z').split('\0'))
    moves={}
    for source in paths:
        src=safe(repo,source)
        if not source.startswith(prefix) or src.suffix not in ('.md','.json','.txt') or not src.is_file() or source not in tracked:
            raise ValueError('Archive only tracked declared milestone records')
        destination=source.replace(prefix,f"harness/archive/{data['id']}/",1)
        if safe(repo,destination).exists():
            raise ValueError('Archive destination already exists')
        moves[source]=destination
    edits={}
    for source in sorted(tracked):
        if not source.endswith('.md'):continue
        file=safe(repo,source)
        if file.stat().st_size>2*1024*1024:raise ValueError('Markdown file exceeds 2 MiB bound')
        old=file.read_text()
        destination=moves.get(source,source)
        new=rewrite(repo,source,destination,old,moves)
        if new!=old:edits[destination]=new
    plan={'head':state['head'],'record':data,'moves':moves,'edits':edits}
    plan['digest']=hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()
    return plan

def write_bytes(path, data):
    path.write_bytes(data)

def apply(repo,digest,reason):
    repo=root(repo)
    if not isinstance(reason,str) or not reason.strip() or len(reason)>1000:
        raise ValueError('Explicit bounded operator reason required')
    plan=preview(repo)
    if digest!=plan['digest']:
        raise ValueError('Preview changed; inspect a new preview before applying')
    touched=set(plan['moves'])|set(plan['moves'].values())|set(plan['edits'])|{RECORD}
    originals={p:safe(repo,p).read_bytes() if safe(repo,p).exists() else None for p in touched}
    new_dirs=[]
    try:
        for source,destination in plan['moves'].items():
            dest=safe(repo,destination)
            missing=[];parent=dest.parent
            while not parent.exists():missing.append(parent);parent=parent.parent
            for directory in reversed(missing):directory.mkdir();new_dirs.append(directory)
            safe(repo,source).rename(dest)
        for name,content in plan['edits'].items():write_bytes(safe(repo,name),content.encode())
        record={**plan['record'],'status':'archived','archive':{'head':plan['head'],'digest':digest,'reason':reason,'moves':plan['moves']}}
        write_bytes(safe(repo,RECORD),(json.dumps(record,indent=2)+'\n').encode())
    except Exception:
        # Best effort on caught errors. Not a crash-safe or concurrent-writer transaction.
        for name,content in originals.items():
            p=safe(repo,name)
            if content is None:p.unlink(missing_ok=True)
            else:p.write_bytes(content)
        for directory in reversed(new_dirs):directory.rmdir()
        raise
    return {'archived':plan['record']['id'],'digest':digest,'changes':sorted(touched)}
