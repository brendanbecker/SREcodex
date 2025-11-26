# FEAT-004: Script-First Programmatic Orchestration

## Objective

Implement the "Programmatic Tool Calling" pattern to handle high-volume operations and multi-skill composition through script generation rather than chat-based iteration.

## Background

### The Problem

Chat-based iteration fails for complex tasks:

| Scenario | Chat Approach | Failure Mode |
|----------|---------------|--------------|
| Restart 50 pods | 50 separate commands | Timeout, context overflow |
| Parse 1GB logs | Stream line by line | Token limit exceeded |
| Deploy + verify + rollback | 3 sequential skills | State lost between turns |

### The Solution (Anthropic's Programmatic Tool Calling)

> "Claude writes code that calls multiple tools, processes their outputs, and controls what information actually enters its context window."

Benefits:
- **Parallel execution**: Async operations run concurrently
- **Filtered results**: Only summary enters context, not raw data
- **Explicit control flow**: Loops, conditionals, error handling in code
- **Skill composition**: Multiple tools orchestrated in one script

### Example: Budget Compliance Check

**Chat approach** (fails): Fetch 2,000 expense line items -> context overflow

**Script approach** (works):
```python
async def check_compliance():
    teams = await get_teams()
    expenses = await asyncio.gather(*[get_expenses(t) for t in teams])
    budgets = await asyncio.gather(*[get_budget(t) for t in teams])

    violations = [e for e, b in zip(expenses, budgets) if e > b]
    return f"Found {len(violations)} budget violations"  # Only summary returned
```

## Implementation Plan

### Section 1: Enable Workspace Write Mode

**File**: `dotcodex/config.toml`

Update execution environment to allow script creation:

```toml
[execution_environment]
# Allow agent to write and execute scripts in workspace
sandbox_mode = "workspace-write"

# Script execution settings
[scripts]
allowed_extensions = [".py", ".sh", ".js"]
execution_timeout = 300  # 5 minutes max
cleanup_after_run = true  # Remove temp scripts after execution
```

### Section 2: Define Script-First Directive

Create a standardized directive to add to high-volume skills.

**File**: `dotcodex/docs/SCRIPT-FIRST-DIRECTIVE.md`

```markdown
# Script-First Directive

## Standard Directive Text

Add this to skills that involve iteration, bulk operations, or multi-step workflows:

---

**SCRIPT-FIRST EXECUTION REQUIRED**

Do not execute this task row-by-row or chat turn-by-turn. Instead:

1. Write a Python/Bash script that:
   - Iterates through all inputs
   - Applies the required logic
   - Handles errors gracefully
   - Prints a final summary

2. Execute the script once

3. Return only the summary to the conversation

**Example**:
```python
#!/usr/bin/env python3
results = []
for item in items:
    result = process(item)
    results.append(result)

successes = sum(1 for r in results if r.success)
print(f"Processed {len(results)} items: {successes} succeeded")
```

---

## When to Apply

Apply this directive to skills involving:
- Bulk operations (restart N pods, delete N resources)
- Log/data parsing (process large files)
- Multi-resource queries (check status of N services)
- Sequential multi-step workflows
- Any operation where N > 10
```

### Section 3: Identify Skills Requiring Directive

Audit existing and planned skills. Add directive to those matching criteria.

**Candidates** (examples):

| Skill | Reason |
|-------|--------|
| `k8s/bulk-restart` | Restart multiple deployments |
| `k8s/pod-cleanup` | Delete pods matching pattern |
| `logs/cloudwatch-search` | Parse large log volumes |
| `aws/ec2-inventory` | Query many instances |
| `db/migration-batch` | Run multiple migrations |
| `monitoring/alert-triage` | Process alert backlog |

**Checklist file**: `dotcodex/docs/SCRIPT-FIRST-SKILLS.md`

```markdown
# Skills Requiring Script-First Directive

## Applied
- [ ] k8s/bulk-restart
- [ ] k8s/pod-cleanup
- [ ] logs/cloudwatch-search

## Pending Review
- [ ] aws/ec2-inventory
- [ ] db/migration-batch
- [ ] monitoring/alert-triage

## Not Applicable
- k8s/single-pod-restart (single item)
- db/connection-test (single operation)
```

### Section 4: Create Orchestration Skill

**File**: `dotcodex/skills/core/orchestrator/SKILL.md`

A meta-skill for composing multiple skills into workflows:

```markdown
---
name: "Workflow Orchestrator"
tags: ["core", "composition", "workflow", "multi-skill", "scripting"]
intent: "Use this when a task requires combining multiple skills or executing a multi-step workflow. Write a script that orchestrates the skills together."
always_load: false
---

# Skill: Workflow Orchestrator

## Purpose

Compose multiple skills into a single executable workflow when a task requires:
- Sequential skill execution (do A, then B, then C)
- Conditional logic (if A fails, do B instead)
- Parallel execution (do A and B simultaneously)
- Result aggregation (combine outputs from multiple skills)

## Usage

When you identify a task requiring multiple skills:

1. **Discover** needed skills via Librarian
2. **Plan** the workflow (sequence, conditions, parallelism)
3. **Write** a Python script that orchestrates the skills
4. **Execute** the script once
5. **Return** the aggregated summary

## Template

```python
#!/usr/bin/env python3
"""
Workflow: [Description]
Skills: [skill-a], [skill-b], [skill-c]
"""
import subprocess
import json

def run_skill_a():
    # Implementation from skill-a
    pass

def run_skill_b(input_from_a):
    # Implementation from skill-b
    pass

def run_skill_c(input_from_b):
    # Implementation from skill-c
    pass

def main():
    # Orchestration logic
    result_a = run_skill_a()

    if result_a.success:
        result_b = run_skill_b(result_a.output)
        result_c = run_skill_c(result_b.output)
    else:
        print(f"Workflow aborted: {result_a.error}")
        return

    # Summary only
    print(f"Workflow complete: {result_c.summary}")

if __name__ == "__main__":
    main()
```

## Examples

**User**: "Deploy the new version and verify it's healthy, rollback if not"
**Agent**: This requires deploy + health-check + rollback skills. Writing orchestration script...

```python
#!/usr/bin/env python3
def main():
    # Step 1: Deploy
    deploy_result = kubectl_apply("deployment.yaml")
    if not deploy_result.success:
        print(f"Deploy failed: {deploy_result.error}")
        return

    # Step 2: Wait and verify
    time.sleep(30)
    health = check_health("/health", retries=3)

    # Step 3: Rollback if unhealthy
    if not health.ok:
        rollback_result = kubectl_rollback("deployment")
        print(f"Rolled back due to health check failure: {health.error}")
    else:
        print(f"Deployment successful. Health: {health.status}")

main()
```

**User**: "Find all pods in CrashLoopBackOff and restart their deployments"
**Agent**: This requires pod-status + bulk-restart skills. Writing orchestration script...

```python
#!/usr/bin/env python3
import subprocess
import json

def get_crashloop_pods():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-A", "-o", "json"],
        capture_output=True, text=True
    )
    pods = json.loads(result.stdout)["items"]
    return [p for p in pods if "CrashLoopBackOff" in str(p.get("status", {}))]

def restart_deployment(namespace, deployment):
    subprocess.run(["kubectl", "rollout", "restart", f"deployment/{deployment}", "-n", namespace])

def main():
    crashloop_pods = get_crashloop_pods()
    deployments = set((p["metadata"]["namespace"], p["metadata"]["labels"].get("app"))
                      for p in crashloop_pods)

    for ns, deploy in deployments:
        if deploy:
            restart_deployment(ns, deploy)

    print(f"Restarted {len(deployments)} deployments for {len(crashloop_pods)} crashed pods")

main()
```
```

### Section 5: Update Skill Template

**File**: `dotcodex/templates/SKILL.template.md`

Add optional script-first section:

```markdown
---
name: "[Skill Name]"
tags: ["tag1", "tag2"]
intent: "[When to use this skill]"
script_first: false  # Set to true for bulk/iterative operations
---

# Skill: [name]

## Usage
[How to use this skill]

## Script-First Directive (if applicable)
<!-- Include if script_first: true -->
**SCRIPT-FIRST EXECUTION REQUIRED**
[Standard directive text]

## Examples
[Few-shot examples]

## Implementation
[The executable payload]
```

### Section 6: Documentation

**File**: `dotcodex/docs/PROGRAMMATIC-ORCHESTRATION.md`

```markdown
# Programmatic Orchestration Guide

## Overview

SREcodex uses the "Script-First" pattern for complex operations. Instead of executing commands one at a time through chat, the agent writes a script that handles the entire workflow.

## When Script-First Applies

| Indicator | Example |
|-----------|---------|
| Bulk operations | "Restart all pods in namespace X" |
| Large data processing | "Find errors in yesterday's logs" |
| Multi-step workflows | "Deploy, verify, and rollback if needed" |
| Composition | Tasks requiring multiple skills |

## How It Works

1. Agent recognizes task matches script-first criteria
2. Agent writes Python/Bash script
3. Script executes with full logic (loops, conditions, error handling)
4. Only summary returns to conversation

## Benefits

- **Reliability**: No timeout from iterative commands
- **Efficiency**: Parallel execution where possible
- **Context control**: Raw data stays in script, summary in chat
- **Composition**: Multiple skills combined naturally

## Reference

Based on Anthropic's "Programmatic Tool Calling" pattern.
See: https://www.anthropic.com/engineering/advanced-tool-use
```

## Deliverables

| File | Purpose |
|------|---------|
| `dotcodex/config.toml` | Enable workspace-write sandbox |
| `dotcodex/docs/SCRIPT-FIRST-DIRECTIVE.md` | Standard directive text |
| `dotcodex/docs/SCRIPT-FIRST-SKILLS.md` | Checklist of skills needing directive |
| `dotcodex/docs/PROGRAMMATIC-ORCHESTRATION.md` | Pattern documentation |
| `dotcodex/skills/core/orchestrator/SKILL.md` | Composition meta-skill |
| Updated `SKILL.template.md` | Add script_first field |

## Acceptance Criteria

- [ ] config.toml updated with `sandbox_mode = "workspace-write"`
- [ ] Script-First directive documented with standard text
- [ ] At least 3 existing/planned skills identified for directive
- [ ] Orchestrator skill created with composition examples
- [ ] SKILL.template.md updated with `script_first` field
- [ ] End-to-end test: Agent writes and executes script for bulk operation
- [ ] End-to-end test: Agent composes 2+ skills into single workflow script

## Testing Plan

### Manual Tests

1. **Bulk Operation Test**
   - Request: "List all pods in CrashLoopBackOff across all namespaces"
   - Expected: Agent writes script, executes once, returns summary
   - Verify: No iterative kubectl calls in chat

2. **Composition Test**
   - Request: "Check which services are unhealthy and restart them"
   - Expected: Agent combines health-check + restart skills in one script
   - Verify: Single script handles discovery + action

3. **Large Data Test**
   - Request: "Find all ERROR lines in /var/log/app.log and group by error type"
   - Expected: Agent writes parsing script, returns grouped summary
   - Verify: Full log content never enters chat context

### Validation Criteria

- Script executes successfully
- Only summary (not raw data) appears in response
- Execution completes within timeout (300s)
- Temp scripts cleaned up after run
