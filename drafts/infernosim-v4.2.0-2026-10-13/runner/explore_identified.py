import json,subprocess
r='/tmp/arc-inferno-runner-20261013';app='/tmp/arc-inferno-source-20261013/examples/concurrencylab/app.py'
for mode in ['unsafe','safe']:
 label='identified-'+mode
 argv=['/usr/bin/python3',r+'/run.py',label,r+'/infernosim','agent','explore',r+'/incident','--causal-graph',r+'/graph.json','--seed','7100','--schedule-budget','100','--budget','200','--max-faults','2','--boundary-timeout','5s','--setup-command-json',json.dumps(['/usr/bin/python3',app,'--scenario','retry','--setup']),'--check-command-json',json.dumps(['/usr/bin/python3',r+'/check_identified.py']),'--check-ids','database,filesystem','--report-dir',r+'/'+label+'/reports','--','/usr/bin/python3',app,'--scenario','retry','--mode',mode]
 subprocess.run(argv)
