---
name: "[SKILL_NAME]"
tags: ["[tag1]", "[tag2]", "[tag3]"]
intent: "[Detailed description of when to use this skill. Include trigger phrases, user requests, symptoms, and specific use cases. Be thorough - this field is critical for discovery.]"
version: "1.0.0"
languages: all
# Optional fields:
# risk_level: low | medium | high
# requires_confirmation: false
# script_first: false  # Set to true for bulk/iterative operations (see SCRIPT-FIRST-DIRECTIVE.md)
---

# [SKILL_NAME]

## Usage

[Brief explanation of what this skill does and the core principle. 2-3 sentences covering what, why, and when.]

**Use this skill when:**
- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

**Don't use when:**
- [Exclusion case 1]
- [Exclusion case 2]

<!-- Include this section if script_first: true in frontmatter -->
<!-- ## Script-First Directive

**SCRIPT-FIRST EXECUTION REQUIRED**

Do not execute this task row-by-row or chat turn-by-turn. Instead:

1. Write a Python/Bash script that:
   - Iterates through all inputs
   - Applies the required logic
   - Handles errors gracefully
   - Prints a final summary

2. Execute the script once

3. Return only the summary to the conversation

### Script Template

```python
#!/usr/bin/env python3
results = []
for item in items:
    result = process(item)
    results.append(result)

successes = sum(1 for r in results if r.success)
print(f"Processed {len(results)} items: {successes} succeeded")
```

### Expected Output Format

```
Processed: N items
Succeeded: X
Failed: Y
```
-->

## Examples

User: "[Common phrasing of request]"
Agent: [Exact action or response - be specific about commands, files, or steps]

User: "[Variation or edge case phrasing]"
Agent: [Appropriate response for this variation]

User: "[Another common scenario]"
Agent: [Response demonstrating skill application]

## Implementation

### Quick Reference

| Task | Command/Action |
|------|----------------|
| [Common task 1] | `[command or action]` |
| [Common task 2] | `[command or action]` |

### Step-by-Step

1. **[First step]**
   ```bash
   # Example command with comments
   [command here]
   ```

2. **[Second step]**
   [Instructions and code if applicable]

3. **[Third step]**
   [Instructions and code if applicable]

### Common Mistakes

**[Mistake description]**
- Problem: [What goes wrong]
- Fix: [How to correct it]

**[Another mistake]**
- Problem: [What goes wrong]
- Fix: [How to correct it]

## Additional Notes

[Any additional context, related skills, or advanced usage tips]

---

**Remember:** [Key takeaway or principle for this skill]
