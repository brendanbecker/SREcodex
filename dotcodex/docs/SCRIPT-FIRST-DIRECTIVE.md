# Script-First Directive

This document defines the standardized directive text for skills that require script-based execution instead of chat-based iteration.

## Standard Directive Text

Add the following block to skills that involve iteration, bulk operations, or multi-step workflows:

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

| Indicator | Threshold | Example |
|-----------|-----------|---------|
| Bulk operations | N > 10 items | Restart N pods, delete N resources |
| Large data processing | > 1000 lines | Parse log files, process CSVs |
| Multi-resource queries | N > 5 resources | Check status of N services |
| Sequential multi-step | > 3 steps | Deploy + verify + rollback |
| Any iteration | Loop required | For-each operations |

## Why Script-First?

### The Problem with Chat Iteration

| Approach | 50 Pods | Failure Mode |
|----------|---------|--------------|
| Chat-based | 50 separate commands | Timeout, context overflow |
| Script-first | 1 script, 1 execution | Summary returned |

### Benefits

1. **Parallel Execution**: Async operations run concurrently
2. **Filtered Results**: Only summary enters context, not raw data
3. **Explicit Control Flow**: Loops, conditionals, error handling in code
4. **Skill Composition**: Multiple tools orchestrated in one script
5. **Reliability**: No timeout from iterative commands

## Implementation Checklist

When adding the directive to a skill:

- [ ] Add directive block to the SKILL.md after "Usage" section
- [ ] Set `script_first: true` in YAML frontmatter
- [ ] Include at least one script template in Examples section
- [ ] Specify expected summary format
- [ ] Note any error handling requirements

## Template Section for Skills

Add this section structure to script-first skills:

```markdown
## Script-First Directive

**SCRIPT-FIRST EXECUTION REQUIRED**

[Standard directive text above]

### Script Template

```python
#!/usr/bin/env python3
"""
Purpose: [What this script does]
Input: [Expected inputs]
Output: [Summary format]
"""

def main():
    results = []
    errors = []

    for item in get_items():
        try:
            result = process(item)
            results.append(result)
        except Exception as e:
            errors.append(f"{item}: {e}")

    # Summary only
    print(f"Processed: {len(results)}")
    print(f"Errors: {len(errors)}")
    if errors:
        print("Failed items:", errors[:5])  # First 5 only

if __name__ == "__main__":
    main()
```

### Expected Output Format

```
Processed: 47 items
Succeeded: 45
Failed: 2
Failed items: [pod-abc, pod-xyz]
```
```

## Reference

Based on Anthropic's "Programmatic Tool Calling" pattern:
> "Claude writes code that calls multiple tools, processes their outputs, and controls what information actually enters its context window."

See: https://www.anthropic.com/engineering/advanced-tool-use
