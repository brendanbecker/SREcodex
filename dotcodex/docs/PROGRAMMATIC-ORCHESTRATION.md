# Programmatic Orchestration Guide

## Overview

SREcodex uses the "Script-First" pattern for complex operations. Instead of executing commands one at a time through chat, the agent writes a script that handles the entire workflow.

This approach is based on Anthropic's "Programmatic Tool Calling" pattern:
> "Claude writes code that calls multiple tools, processes their outputs, and controls what information actually enters its context window."

## When Script-First Applies

| Indicator | Example |
|-----------|---------|
| Bulk operations | "Restart all pods in namespace X" |
| Large data processing | "Find errors in yesterday's logs" |
| Multi-step workflows | "Deploy, verify, and rollback if needed" |
| Skill composition | Tasks requiring multiple skills |
| Iterative operations | Any loop-based task |

## How It Works

1. Agent recognizes task matches script-first criteria
2. Agent writes Python/Bash script with full logic
3. Script executes with loops, conditions, error handling
4. Only summary returns to conversation

```
┌─────────────────────────────────────────────────────────────┐
│                    CHAT-BASED (FAILS)                       │
├─────────────────────────────────────────────────────────────┤
│  Turn 1: kubectl get pods...         → 500 lines output     │
│  Turn 2: kubectl restart pod-1...    → output               │
│  Turn 3: kubectl restart pod-2...    → output               │
│  ...                                                        │
│  Turn 50: kubectl restart pod-50...  → TIMEOUT/OVERFLOW     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   SCRIPT-FIRST (WORKS)                      │
├─────────────────────────────────────────────────────────────┤
│  Turn 1: Write script that:                                 │
│          - Gets all pods                                    │
│          - Filters for target pods                          │
│          - Restarts each in loop                            │
│          - Prints summary                                   │
│  Turn 2: Execute script → "Restarted 50/50 pods"           │
└─────────────────────────────────────────────────────────────┘
```

## Benefits

### Reliability
No timeout from iterative commands. Script runs to completion.

### Efficiency
Parallel execution where possible. Async operations run concurrently.

### Context Control
Raw data stays in script, only summary enters chat context.

### Composition
Multiple skills combined naturally in code.

### Error Handling
Explicit try/except, conditionals, and branching in script.

## Implementation

### Enabling Script-First

1. **Configuration**: `dotcodex/config.toml` enables workspace-write mode:
   ```toml
   [execution_environment]
   sandbox_mode = "workspace-write"
   ```

2. **Skill Marking**: Skills requiring script-first have `script_first: true` in YAML frontmatter

3. **Directive**: Script-first skills include the standard directive block

### The Script-First Directive

Add this to skills involving bulk operations:

```markdown
**SCRIPT-FIRST EXECUTION REQUIRED**

Do not execute this task row-by-row or chat turn-by-turn. Instead:

1. Write a Python/Bash script that:
   - Iterates through all inputs
   - Applies the required logic
   - Handles errors gracefully
   - Prints a final summary

2. Execute the script once

3. Return only the summary to the conversation
```

### Skills with Directive

See `SCRIPT-FIRST-SKILLS.md` for the full list. Key skills include:
- `document-parser` - Multi-document processing
- `core/orchestrator` - Multi-skill composition
- Planned: `k8s/bulk-restart`, `logs/cloudwatch-search`, etc.

## Orchestration Patterns

### Sequential Execution

```python
result_a = do_skill_a()
result_b = do_skill_b(result_a.output)
result_c = do_skill_c(result_b.output)
print(f"Complete: {result_c.summary}")
```

### Conditional Branching

```python
result = deploy()
if not result.success:
    rollback()
    print("Deployment failed, rolled back")
else:
    health = check_health()
    if not health.ok:
        rollback()
        print("Health check failed, rolled back")
    else:
        print("Deployment successful")
```

### Parallel Execution

```python
import asyncio

async def main():
    results = await asyncio.gather(
        check_service_a(),
        check_service_b(),
        check_service_c()
    )
    healthy = sum(1 for r in results if r.ok)
    print(f"{healthy}/{len(results)} services healthy")

asyncio.run(main())
```

### Error Aggregation

```python
results = []
errors = []

for item in items:
    try:
        result = process(item)
        results.append(result)
    except Exception as e:
        errors.append(f"{item}: {e}")

print(f"Processed {len(results)}, Failed {len(errors)}")
if errors:
    print(f"First 5 errors: {errors[:5]}")
```

## The Orchestrator Skill

For tasks requiring multiple skills, use `core/orchestrator`:

1. Discover needed skills via Librarian
2. Plan the workflow
3. Write orchestration script
4. Execute once
5. Return summary

See `skills/core/orchestrator/SKILL.md` for full documentation and examples.

## Testing Script-First

### Manual Test 1: Bulk Operation

**Request**: "List all pods in CrashLoopBackOff across all namespaces"

**Expected**: Agent writes script, executes once, returns summary

**Verify**: No iterative kubectl calls in chat

### Manual Test 2: Composition

**Request**: "Check which services are unhealthy and restart them"

**Expected**: Agent combines health-check + restart skills in one script

**Verify**: Single script handles discovery + action

### Manual Test 3: Large Data

**Request**: "Find all ERROR lines in /var/log/app.log and group by error type"

**Expected**: Agent writes parsing script, returns grouped summary

**Verify**: Full log content never enters chat context

## Validation Criteria

- [ ] Script executes successfully
- [ ] Only summary (not raw data) appears in response
- [ ] Execution completes within timeout (300s default)
- [ ] Temp scripts cleaned up after run (if `cleanup_after_run = true`)

## Related Documentation

- `SCRIPT-FIRST-DIRECTIVE.md` - Standard directive text
- `SCRIPT-FIRST-SKILLS.md` - Skills requiring the directive
- `skills/core/orchestrator/SKILL.md` - Multi-skill composition
- `config.toml` - Execution environment settings

## Reference

Based on Anthropic's "Programmatic Tool Calling" pattern.
See: https://www.anthropic.com/engineering/advanced-tool-use
