---
name: "Workflow Orchestrator"
tags: ["core", "composition", "workflow", "multi-skill", "scripting", "orchestration", "automation"]
intent: "Use this when a task requires combining multiple skills or executing a multi-step workflow. Write a script that orchestrates the skills together. Triggers when you recognize tasks like 'do A then B', 'check X and if bad do Y', or any request requiring sequential or conditional skill execution."
script_first: true
version: "1.0.0"
languages: ["python", "bash"]
---

# Workflow Orchestrator

## Usage

Compose multiple skills into a single executable workflow when a task requires:
- Sequential skill execution (do A, then B, then C)
- Conditional logic (if A fails, do B instead)
- Parallel execution (do A and B simultaneously)
- Result aggregation (combine outputs from multiple skills)

**Use this skill when:**
- Task mentions multiple operations in sequence
- Request includes conditional logic ("if X then Y")
- Need to combine outputs from different sources
- Single-skill execution would require multiple chat turns

**Don't use when:**
- Task requires only one skill
- Operations are independent (no shared context)
- Simple queries with no workflow logic

## Script-First Directive

**SCRIPT-FIRST EXECUTION REQUIRED**

Do not execute multi-skill tasks turn-by-turn. Instead:

1. Write a Python/Bash script that:
   - Calls each skill's operations in sequence
   - Handles errors and conditional branching
   - Aggregates results from all steps
   - Prints a final summary

2. Execute the script once

3. Return only the summary to the conversation

## Script Location

**Write ephemeral scripts to `dotcodex/scratch/`**

This directory is gitignored and designated for temporary orchestration scripts.

```bash
# Example: write script to scratch directory
cat > dotcodex/scratch/workflow_$(date +%s).py << 'EOF'
#!/usr/bin/env python3
# ... script content ...
EOF

# Execute
python3 dotcodex/scratch/workflow_*.py

# Clean up (optional - directory is gitignored)
rm dotcodex/scratch/workflow_*.py
```

**When to keep scripts:**
- Reusable workflows → move to `dotcodex/scripts/`
- Skill-specific utilities → move to skill's `scripts/` subdirectory
- One-off operations → leave in scratch (auto-ignored)

## Orchestration Workflow

1. **Discover** needed skills via Librarian
2. **Plan** the workflow (sequence, conditions, parallelism)
3. **Write** a Python script that orchestrates the skills
4. **Execute** the script once
5. **Return** the aggregated summary

## Quick Reference

| Pattern | Use Case | Script Structure |
|---------|----------|------------------|
| Sequential | A then B then C | `result_a = do_a(); result_b = do_b(result_a)` |
| Conditional | If A fails, do B | `if not result_a.success: do_b()` |
| Parallel | A and B together | `asyncio.gather(do_a(), do_b())` |
| Aggregation | Combine A + B | `summary = merge(result_a, result_b)` |

## Script Template

```python
#!/usr/bin/env python3
"""
Workflow: [Description]
Skills: [skill-a], [skill-b], [skill-c]
"""
import subprocess
import json

def run_skill_a():
    """Implementation from skill-a"""
    # Replace with actual skill logic
    pass

def run_skill_b(input_from_a):
    """Implementation from skill-b"""
    # Replace with actual skill logic
    pass

def run_skill_c(input_from_b):
    """Implementation from skill-c"""
    # Replace with actual skill logic
    pass

def main():
    results = {"steps": [], "errors": []}

    # Step 1: Skill A
    try:
        result_a = run_skill_a()
        results["steps"].append({"skill": "a", "status": "success"})
    except Exception as e:
        results["errors"].append(f"Skill A failed: {e}")
        print(f"Workflow aborted at step 1: {e}")
        return

    # Step 2: Skill B (conditional on A)
    if result_a.get("success"):
        try:
            result_b = run_skill_b(result_a.get("output"))
            results["steps"].append({"skill": "b", "status": "success"})
        except Exception as e:
            results["errors"].append(f"Skill B failed: {e}")

    # Step 3: Skill C
    try:
        result_c = run_skill_c(result_b.get("output"))
        results["steps"].append({"skill": "c", "status": "success"})
    except Exception as e:
        results["errors"].append(f"Skill C failed: {e}")

    # Summary only
    print(f"Workflow complete: {len(results['steps'])} steps succeeded")
    if results["errors"]:
        print(f"Errors: {results['errors']}")

if __name__ == "__main__":
    main()
```

## Examples

User: "Deploy the new version and verify it's healthy, rollback if not"
Agent: This requires deploy + health-check + rollback skills. Writing orchestration script...

```python
#!/usr/bin/env python3
"""
Workflow: Deploy with health check and rollback
Skills: k8s/deploy, k8s/health-check, k8s/rollback
"""
import subprocess
import time

def kubectl_apply(manifest):
    result = subprocess.run(
        ["kubectl", "apply", "-f", manifest],
        capture_output=True, text=True
    )
    return {"success": result.returncode == 0, "output": result.stdout, "error": result.stderr}

def check_health(endpoint, retries=3):
    for i in range(retries):
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", endpoint],
            capture_output=True, text=True
        )
        if result.stdout == "200":
            return {"ok": True, "status": "healthy"}
        time.sleep(10)
    return {"ok": False, "status": "unhealthy", "error": f"Failed after {retries} retries"}

def kubectl_rollback(deployment):
    result = subprocess.run(
        ["kubectl", "rollout", "undo", f"deployment/{deployment}"],
        capture_output=True, text=True
    )
    return {"success": result.returncode == 0}

def main():
    # Step 1: Deploy
    deploy_result = kubectl_apply("deployment.yaml")
    if not deploy_result["success"]:
        print(f"Deploy failed: {deploy_result['error']}")
        return

    # Step 2: Wait and verify
    time.sleep(30)
    health = check_health("http://service/health", retries=3)

    # Step 3: Rollback if unhealthy
    if not health["ok"]:
        rollback_result = kubectl_rollback("my-deployment")
        print(f"Rolled back due to health check failure: {health['error']}")
    else:
        print(f"Deployment successful. Health: {health['status']}")

if __name__ == "__main__":
    main()
```

---

User: "Find all pods in CrashLoopBackOff and restart their deployments"
Agent: This requires pod-status + bulk-restart skills. Writing orchestration script...

```python
#!/usr/bin/env python3
"""
Workflow: Find crashed pods and restart deployments
Skills: k8s/pod-status, k8s/bulk-restart
"""
import subprocess
import json

def get_crashloop_pods():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True, text=True
    )
    pods = json.loads(result.stdout)["items"]
    crashed = []
    for p in pods:
        statuses = p.get("status", {}).get("containerStatuses", [])
        for cs in statuses:
            waiting = cs.get("state", {}).get("waiting", {})
            if waiting.get("reason") == "CrashLoopBackOff":
                crashed.append(p)
                break
    return crashed

def restart_deployment(namespace, deployment):
    result = subprocess.run(
        ["kubectl", "rollout", "restart", f"deployment/{deployment}", "-n", namespace],
        capture_output=True, text=True
    )
    return result.returncode == 0

def main():
    # Step 1: Find crashed pods
    crashloop_pods = get_crashloop_pods()

    # Step 2: Extract unique deployments
    deployments = set()
    for p in crashloop_pods:
        ns = p["metadata"]["namespace"]
        labels = p["metadata"].get("labels", {})
        deploy = labels.get("app") or labels.get("app.kubernetes.io/name")
        if deploy:
            deployments.add((ns, deploy))

    # Step 3: Restart each deployment
    restarted = 0
    for ns, deploy in deployments:
        if restart_deployment(ns, deploy):
            restarted += 1

    # Summary
    print(f"Found {len(crashloop_pods)} pods in CrashLoopBackOff")
    print(f"Restarted {restarted}/{len(deployments)} deployments")

if __name__ == "__main__":
    main()
```

---

User: "Check which services are unhealthy and create JIRA tickets for each"
Agent: This requires health-check + jira-create skills. Writing orchestration script...

```python
#!/usr/bin/env python3
"""
Workflow: Health check and ticket creation
Skills: monitoring/health-check, integrations/jira-create
"""
import subprocess
import json
import requests

JIRA_URL = "https://company.atlassian.net"
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")

def get_service_health():
    # Example: query Kubernetes services
    result = subprocess.run(
        ["kubectl", "get", "endpoints", "-A", "-o", "json"],
        capture_output=True, text=True
    )
    endpoints = json.loads(result.stdout)["items"]
    unhealthy = []
    for ep in endpoints:
        subsets = ep.get("subsets", [])
        if not subsets or not subsets[0].get("addresses"):
            unhealthy.append({
                "name": ep["metadata"]["name"],
                "namespace": ep["metadata"]["namespace"]
            })
    return unhealthy

def create_jira_ticket(service):
    payload = {
        "fields": {
            "project": {"key": "OPS"},
            "summary": f"Service unhealthy: {service['name']}",
            "description": f"Service {service['name']} in namespace {service['namespace']} has no healthy endpoints.",
            "issuetype": {"name": "Bug"},
            "priority": {"name": "High"}
        }
    }
    response = requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        json=payload,
        headers={"Authorization": f"Bearer {JIRA_TOKEN}"}
    )
    return response.status_code == 201

def main():
    # Step 1: Check health
    unhealthy = get_service_health()

    # Step 2: Create tickets
    tickets_created = 0
    for svc in unhealthy:
        if create_jira_ticket(svc):
            tickets_created += 1

    # Summary
    print(f"Found {len(unhealthy)} unhealthy services")
    print(f"Created {tickets_created} JIRA tickets")

if __name__ == "__main__":
    main()
```

## Common Mistakes

**Executing skills turn-by-turn instead of scripting**
- Problem: Context overflow, timeout, lost state between turns
- Fix: Always write a script that handles the full workflow

**Not handling errors between steps**
- Problem: Workflow fails silently or continues with bad state
- Fix: Add try/except blocks, check return values, abort or branch on failure

**Returning raw data instead of summary**
- Problem: Raw output fills context window
- Fix: Process data in script, return only counts/summaries

**Forgetting to discover skills first**
- Problem: Write script without knowing what operations are available
- Fix: Use Librarian to search for needed skills before writing orchestration

## Integration with Librarian

Before writing an orchestration script:

1. Identify needed capabilities
2. Search: `codex-skills search "capability description"`
3. Load relevant skills
4. Extract the core operations from each skill
5. Compose into orchestration script

## Parallel Execution Pattern

For independent operations that can run concurrently:

```python
import asyncio

async def main():
    # Run health checks in parallel
    results = await asyncio.gather(
        check_service_a(),
        check_service_b(),
        check_service_c(),
        return_exceptions=True
    )

    healthy = sum(1 for r in results if r.get("healthy"))
    print(f"Health check: {healthy}/{len(results)} services healthy")

asyncio.run(main())
```

---

**Remember:** One script, one execution, one summary. Never iterate through chat turns for multi-step workflows.
