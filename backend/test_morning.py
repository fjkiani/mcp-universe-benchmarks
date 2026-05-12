import os
os.environ['DEMO_MOCK_MODE'] = 'true'
os.environ['DATABASE_URL'] = 'sqlite:///./test_morning.db'

from database.session import init_db
init_db()  # Create all tables before any requests

from fastapi.testclient import TestClient
from main import app

c = TestClient(app)
tests = []

# 1. Health
r = c.get('/health')
tests.append(('health', r.status_code == 200, r.json().get('status')))

# 2. Domains
r = c.get('/api/v1/governance/domains')
d = r.json()
tests.append(('domains', r.status_code == 200 and len(d) > 0, f'{len(d)} domains'))

# 3. Stats
r = c.get('/api/v1/governance/stats')
tests.append(('stats', r.status_code == 200, str(r.json())))

# 4. Register agent
r = c.post('/api/v1/governance/agents/register', json={
    'name': 'morning-test', 'model': 'gpt-4o',
    'agent_type': 'react', 'mcp_tools': ['search'], 'risk_tier': 'medium'
})
tests.append(('register_agent', r.status_code == 200, r.json().get('agent_id', '')[:12]))

# 5. List agents
r = c.get('/api/v1/governance/agents')
tests.append(('list_agents', r.status_code == 200, f'{len(r.json())} agents'))

# 6. Certify
domain = list(d.keys())[0]
r = c.post('/api/v1/governance/certify', json={
    'agent_name': 'morning-test', 'model': 'gpt-4o', 'domain': domain
})
run_id = r.json().get('run_id', '')
tests.append(('certify', r.status_code == 200 and bool(run_id), f'run={run_id[:8]}'))

# 7. Run status
r = c.get(f'/api/v1/governance/certify/{run_id}')
tests.append(('run_status', r.status_code == 200, r.json().get('status')))

# 8. Full report
r = c.get(f'/api/v1/governance/certify/{run_id}/report')
rpt = r.json()
grade = rpt.get('grade', 'ERR')
score = rpt.get('overall_score', 0)
tests.append(('report', r.status_code == 200 and 'grade' in rpt, f'grade={grade} score={score}%'))

# 9. Reports list
r = c.get('/api/v1/governance/reports')
data = r.json()
tests.append(('reports_list', r.status_code == 200,
              f'{len(data["db_reports"])} db + {len(data["historical_reports"])} historical'))

# 10. Trap tasks
import json
from pathlib import Path
trap_dir = Path('../domains/governance_traps/tasks')
trap_files = list(trap_dir.glob('*.json'))
all_valid = True
for f in trap_files:
    task = json.loads(f.read_text())
    if not all(k in task for k in ['category', 'question', 'evaluators']):
        all_valid = False
        break
tests.append(('trap_tasks', all_valid and len(trap_files) == 8, f'{len(trap_files)}/8 tasks valid'))

# Print results
print()
all_pass = True
for name, ok, detail in tests:
    icon = 'PASS' if ok else 'FAIL'
    print(f'  [{icon}] {name:<22} {detail}')
    if not ok:
        all_pass = False

print()
if all_pass:
    print('  === ALL 10 TESTS PASSED — READY FOR MORNING ===')
else:
    print('  === SOME TESTS FAILED ===')

# Cleanup test db
import os as _os
try:
    _os.remove('test_morning.db')
except Exception:
    pass
