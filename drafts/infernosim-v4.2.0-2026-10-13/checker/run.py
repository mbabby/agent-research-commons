import datetime,json,os,pathlib,platform,subprocess,sys
root=pathlib.Path('${CHECKER_ROOT}')
label=sys.argv[1]; argv=sys.argv[2:]
out=root/label;out.mkdir(parents=True,exist_ok=False)
for d in ['home','tmp']:(root/d).mkdir(exist_ok=True)
env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'CHECKER_EVIDENCE':str(out/'evidence')}
meta={'argv':argv,'cwd':str(root),'environment':env,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'source_sha':'f26b5522bbb20f2904d7534b879fa2896bdf1302'}
(out/'command.json').write_text(json.dumps(meta,indent=2)+'\n')
with (out/'stdout').open('wb') as stdout,(out/'stderr').open('wb') as stderr:
 p=subprocess.run(argv,env=env,cwd=meta['cwd'],stdout=stdout,stderr=stderr)
(out/'exit').write_text(str(p.returncode)+'\n');print(label,p.returncode)
sys.exit(p.returncode)
