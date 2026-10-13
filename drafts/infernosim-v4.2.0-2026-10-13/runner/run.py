import datetime,json,os,pathlib,platform,subprocess,sys
root=pathlib.Path('/tmp/arc-inferno-runner-20261013')
label=sys.argv[1]; argv=sys.argv[2:]
out=root/label;out.mkdir(parents=True,exist_ok=False)
env={'PATH':str(root/'go/bin')+':/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),'GOPATH':str(root/'gopath'),'GOCACHE':str(root/'gocache'),'GOTOOLCHAIN':'local','GOPROXY':'https://goproxy.cn','EVIDENCE_DIR':str(out/'evidence')}
for d in ['home','tmp','gopath','gocache']:(root/d).mkdir(exist_ok=True)
meta={'argv':argv,'cwd':'/tmp/arc-inferno-source-20261013','environment':env,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'source_sha':'f26b5522bbb20f2904d7534b879fa2896bdf1302'}
(out/'command.json').write_text(json.dumps(meta,indent=2)+'\n')
with (out/'stdout').open('wb') as stdout,(out/'stderr').open('wb') as stderr:
 p=subprocess.run(argv,env=env,cwd=meta['cwd'],stdout=stdout,stderr=stderr)
(out/'exit').write_text(str(p.returncode)+'\n');print(label,p.returncode)
sys.exit(p.returncode)
