#!/usr/bin/env python3
"""Preview by default; apply only with the exact digest and caller's authorization."""
import argparse
import json
import sys
from workflow import preview, apply

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True)
    parser.add_argument('--apply',metavar='DIGEST')
    parser.add_argument('--reason')
    args=parser.parse_args()
    try:
        if args.apply:result=apply(args.repo,args.apply,args.reason)
        else:
            plan=preview(args.repo)
            result={k:plan[k] for k in ('head','digest','moves')}
            result['edited_files']=list(plan['edits'])
        print(json.dumps(result,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError) as error:
        print('Archive refused: '+str(error),file=sys.stderr)
        return 1
if __name__=='__main__':sys.exit(main())
