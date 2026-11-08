"""Record the user-pinned ARIS reviewer route and its saved response."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json

ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('skill')
    ap.add_argument('agent')
    ap.add_argument('prompt_file')
    ap.add_argument('--response')
    ap.add_argument('--run',default='2026-11-01_paper_draft')
    ap.add_argument('--entry',default='001-review')
    args=ap.parse_args()
    dest=ROOT/'.aris'/'traces'/args.skill/args.run
    dest.mkdir(parents=True,exist_ok=True)
    now=datetime.now(timezone.utc).isoformat()
    base={'skill':args.skill,'model':'gpt-6.1-sol','reasoning_effort':'high',
          'route_override':'explicit user instruction: gpt-6.1-sol high only',
          'review_independence':'same-family','acceptance_status':'provisional',
          'agent_id':args.agent,'timestamp_utc':now}
    prompt=(ROOT/args.prompt_file).read_text(encoding='utf-8')
    (dest/(args.entry+'.request.json')).write_text(json.dumps({**base,'tool':'spawn_agent','prompt':prompt},indent=2)+'\n',encoding='utf-8')
    response=ROOT/args.response if args.response else None
    status='completed' if response and response.is_file() else 'pending'
    if response and response.is_file():
        (dest/(args.entry+'.response.md')).write_bytes(response.read_bytes())
    (dest/(args.entry+'.meta.json')).write_text(json.dumps({**base,'status':status},indent=2)+'\n',encoding='utf-8')
    (dest/'run.meta.json').write_text(json.dumps({**base,'executor':'codex','project_dir':str(ROOT)},indent=2)+'\n',encoding='utf-8')
    print(str(dest))

if __name__=='__main__':main()
