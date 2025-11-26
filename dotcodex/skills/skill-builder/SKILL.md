---
name: Skill Builder
tags: ["skill", "create", "template", "workflow", "pattern", "reusable", "document", "technique", "instructions", "metadata"]
intent: "Guide for creating new skills following best practices. Use when user asks to 'create a skill', 'make a skill', 'document a technique', 'capture a workflow', or 'add instructions for future sessions'. Also triggers when you discover a reusable pattern worth standardizing, when user says 'write this down for next time', or when a process keeps recurring and should be formalized."
version: "1.0.0"
languages: all
---

# Skill Builder

## Usage

This skill teaches you how to create new skills properly. Skills are reusable instruction sets that extend your capabilities with specialized knowledge, workflows, and best practices.

**Core principle:** Write skills that future instances of Codex can discover and apply without human intervention.

**Use this skill when:**
- User asks to "create a skill" or "make a skill"
- You discover a technique that should be reusable
- User wants to document a workflow or pattern
- You're asked to "write this down for next time"
- A process keeps recurring and should be standardized

**Don't use when:**
- Creating one-off solutions specific to a single project
- Documenting project-specific code (use project docs instead)
- The technique is already well-documented elsewhere

## What Makes a Good Skill

**Good skills are:**
- ✅ Reusable across multiple projects
- ✅ Clear and actionable (step-by-step)
- ✅ Discoverable (rich metadata)
- ✅ Self-contained (all info needed to use it)

**Don't create skills for:**
- ❌ One-off solutions
- ❌ Project-specific code (that goes in project docs)
- ❌ Things already well-documented elsewhere
- ❌ Personal preferences without broad applicability

## Examples

User: "Can you write down how we debugged that async issue so we don't forget next time?"
Agent: Create a new skill at `dotcodex/skills/async-debugging/SKILL.md` with YAML frontmatter containing name, tags, and intent. Include step-by-step debugging process and examples of common async issues.

User: "I keep doing this same git workflow. Can you make it a skill?"
Agent: Ask clarifying questions about trigger phrases and edge cases, then create a skill with rich `tags` for discovery and concrete examples in the `## Examples` section.

User: "Create a skill for handling environment variables"
Agent: Create `dotcodex/skills/env-var-handling/SKILL.md` with tags like ["env", "environment", "config", "secrets", ".env"], detailed intent covering when to use it, and Q&A examples demonstrating proper usage.

## SKILL.md Structure

Every skill must have this structure:

```markdown
---
name: "Human-Readable Skill Name"
tags: ["keyword1", "keyword2", "keyword3"]
intent: "Comprehensive description of when to use this skill. Include trigger phrases, user requests, symptoms, and specific use cases."
version: "1.0.0"
languages: all
---

# Skill Name

## Usage
2-3 sentence explanation of what this skill does and the core principle.
- When to use (bullet list)
- When NOT to use

## Examples
User: "[Common request phrasing]"
Agent: [Exact action or response]

User: "[Edge case or variation]"
Agent: [Appropriate response]

## Implementation
Step-by-step instructions with code examples.

## Common Mistakes (optional)
- ❌ Problem description
- ✅ How to fix it
```

See `dotcodex/docs/SKILL-SCHEMA.md` for the complete schema specification.

## The Critical YAML Frontmatter

The YAML section at the top is **critical for discovery**. Codex finds skills by matching patterns in these fields.

### Required Fields

**`name:`** - Human-readable title
- Use Title Case: "Time Awareness" not "time-awareness"
- Descriptive: "UV Python Workflow" not just "UV"

**`tags:`** - Keywords for search/discovery
- Include trigger words and synonyms
- Minimum 3 tags recommended
- Include related tools and concepts

**`intent:`** - When to use (MOST IMPORTANT)
- Combines what the skill does with when to trigger it
- Be extremely specific about user phrases
- Include error messages and symptoms
- More detail = better discovery

### Optional Fields

**`version:`** - Semantic version (default: "1.0.0")

**`languages:`** - Which languages/contexts apply
- `all` for universal skills
- `["python", "javascript"]` for language-specific

**`risk_level:`** - `low`, `medium`, or `high` for risky operations

**`requires_confirmation:`** - `true` for destructive operations

### Example of Good vs Bad intent

❌ **Bad - Too vague:**
```yaml
intent: "For git workflows"
```

✅ **Good - Specific triggers:**
```yaml
intent: "Manage multiple git worktrees for parallel feature development. Use when working on multiple features simultaneously, when you need to preserve work-in-progress, when switching contexts frequently, when you see 'detached HEAD' state, or when user mentions 'git worktrees'."
```

## Step-by-Step Skill Creation Process

### Step 1: Identify the Pattern

Ask yourself:
- What technique/pattern did we just use?
- Would this be useful again in a different context?
- Can it be generalized?
- Is it already well-documented elsewhere?

### Step 2: Choose a Name

Use this format:
- Action-based: "debugging-with-logs", "creating-tests"
- Pattern-based: "condition-based-waiting"
- Clear and searchable: "git-worktree-workflow"

Avoid:
- Generic names: "helper", "utils"
- Abbreviations: "db-mgmt"
- Unclear references: "the-pattern"

### Step 3: Write Discovery Metadata

This is THE MOST IMPORTANT part. Write `when_to_use` with:

**Include specific triggers:**
- Error messages: "ENOENT", "Cannot find module"
- Symptoms: "flaky tests", "race conditions"
- Keywords: "async", "parallel", "concurrent"
- User phrases: "how do I...", "keep getting..."

**Include context:**
- When in the workflow: "before writing code", "when debugging"
- Project types: "React projects", "CLI tools"
- Situations: "when tests are slow", "when merging is difficult"

### Step 4: Write Clear Instructions

**Use imperative mood:**
- ✅ "Run this command"
- ❌ "You should run this command"

**Number steps:**
1. First do this
2. Then do this
3. Finally do this

**Show code examples inline:**
```bash
# Good examples are commented and complete
git worktree add ../feature-branch feature-branch
```

**Explain WHY, not just WHAT:**
```markdown
## Why condition-based waiting works

Polling with conditions is more reliable than fixed timeouts because...
```

### Step 5: Add Examples

Include 2-3 real-world examples:
- Simple case
- Edge case
- Common variation

Make them **concrete** - actual code, actual commands, actual scenarios.

### Step 6: Document Common Mistakes

Every skill should have this section:
```markdown
## Common Mistakes

❌ **Mistake:** Description of what goes wrong
✅ **Fix:** How to do it correctly

❌ **Mistake:** Another common error
✅ **Fix:** The right approach
```

### Step 7: Create the File

```bash
# Create skill directory (DOTCODEX_DIR defaults to ../dotcodex)
default_dotcodex="${DOTCODEX_DIR:-$(cd .. && pwd)/dotcodex}"
skills_dir="${default_dotcodex}/skills"
mkdir -p "${skills_dir}/skill-name"

# Create SKILL.md file
cat > "${skills_dir}/skill-name/SKILL.md" <<'EOF'
[paste your skill content here]
EOF

# Verify it appears
codex-skills list

# Test loading it
codex-skills use skill-name
```

## Skill Templates by Type

### Technique Skill (How-to)

For teaching a specific technique or method.

**Focus on:**
- Clear step-by-step process
- Code examples
- Before/after comparisons

**Example:** time-awareness, systematic-debugging

### Pattern Skill (Conceptual)

For teaching a way of thinking or mental model.

**Focus on:**
- The principle/concept
- When to apply it
- Recognition patterns

**Example:** defensive-programming, separation-of-concerns

### Workflow Skill (Process)

For multi-step processes or workflows.

**Focus on:**
- Ordered steps
- Decision points
- Checkpoints

**Example:** git-worktree-workflow, code-review-process

### Reference Skill (Documentation)

For API docs, command references, syntax guides.

**Focus on:**
- Quick reference tables
- Command syntax
- Common operations

**Example:** docker-commands, regex-patterns

## Testing Your Skill

After creating a skill, test it:

### 1. Discovery Test
```bash
# Does it show up?
codex-skills list | grep -i "your-skill-name"
```

### 2. Loading Test
```bash
# Does it load properly?
codex-skills use your-skill-name
```

### 3. Format Test
- [ ] YAML frontmatter has `---` delimiters
- [ ] All required fields present
- [ ] No tabs in YAML (use spaces)
- [ ] Headers use `##` format
- [ ] Code blocks use triple backticks

### 4. Practical Test
- Start a new Codex session
- Create a situation where the skill should apply
- Does Codex discover and use the skill?
- Do the instructions work as expected?

## Common Mistakes When Creating Skills

### ❌ Vague when_to_use
```yaml
when_to_use: For testing
```
✅ **Better:**
```yaml
when_to_use: When writing unit tests, when tests are flaky, when you see "test timeout" errors, when mocking external dependencies
```

### ❌ No concrete examples
```markdown
Use the command with appropriate flags.
```
✅ **Better:**
```markdown
## Example
```bash
git worktree add ../feature-branch feature-branch
cd ../feature-branch
# Now you can work here independently
```
```

### ❌ Missing the "why"
```markdown
Run this command.
```
✅ **Better:**
```markdown
Run this command to avoid race conditions. Fixed timeouts fail when systems are slow; condition-based waiting adapts.
```

### ❌ Narrative instead of instructions
```markdown
Last week we had a bug where...
```
✅ **Better:**
```markdown
## Common Mistakes
When files are locked, you'll see EBUSY errors. Use graceful-fs to retry automatically.
```

## Skill Creation Checklist

When creating a new skill, verify:

**Discovery:**
- [ ] `when_to_use` includes specific trigger words
- [ ] `when_to_use` includes error messages if applicable
- [ ] `when_to_use` includes symptoms/situations
- [ ] Description is clear and specific
- [ ] Name is descriptive and searchable

**Content:**
- [ ] Overview explains core principle
- [ ] When to Use section is comprehensive
- [ ] Instructions are step-by-step and imperative
- [ ] Code examples are complete and commented
- [ ] Common mistakes section included
- [ ] Real-world examples provided

**Format:**
- [ ] YAML frontmatter properly formatted
- [ ] All required fields present
- [ ] Sections use ## headers
- [ ] Code uses triple backtick blocks
- [ ] No tabs in YAML (spaces only)

**Testing:**
- [ ] Appears in `codex-skills list`
- [ ] Loads with `codex-skills use skill-name`
- [ ] Actually helps with the intended task
- [ ] Can be found when needed

## Integration with Workflow

After creating a skill:

1. **Announce it:** Tell the user "I've created a new skill: [name]"
2. **Explain when to use it:** Summarize the triggers
3. **Offer to test:** "Would you like me to test loading this skill?"
4. **Document it:** Keep a project log of custom skills if relevant

## Example: Creating a Skill (Full Walkthrough)

**User asks:** "Can you write down how to handle environment variables properly so we don't forget next time?"

**You respond:**

"I'll create a skill for environment variable handling. Let me structure this properly..."

```bash
default_dotcodex="${DOTCODEX_DIR:-$(cd .. && pwd)/dotcodex}"
skills_dir="${default_dotcodex}/skills"
mkdir -p "${skills_dir}/env-var-handling"
```

**You create:**
```markdown
---
name: Environment Variable Handling
description: Best practices for managing environment variables securely in applications
when_to_use: When setting up new projects, when you see hardcoded secrets, when configuring deployments, when user mentions "env vars" or ".env files", when debugging configuration issues
version: 1.0.0
languages: all
---

# Environment Variable Handling

## Overview
Proper environment variable management keeps secrets out of code, enables configuration across environments, and prevents security vulnerabilities.

## When to Use
- Starting a new project that needs configuration
- See hardcoded API keys or secrets in code
- Deploying to different environments (dev/staging/prod)
- User mentions environment variables or configuration
- Debugging "works on my machine" issues

## Core Pattern

❌ **Wrong:**
```python
API_KEY = "sk-abc123..."  # Hardcoded secret
DATABASE_URL = "postgres://localhost"
```

✅ **Right:**
```python
import os
API_KEY = os.environ.get('API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

## Implementation

1. **Create .env file for local development:**
```bash
cat > .env << 'EOF'
API_KEY=your-key-here
DATABASE_URL=postgres://localhost:5432/mydb
NODE_ENV=development
EOF
```

2. **Add .env to .gitignore:**
```bash
echo ".env" >> .gitignore
```

3. **Create .env.example template:**
```bash
cat > .env.example << 'EOF'
API_KEY=your-api-key-here
DATABASE_URL=your-database-url
NODE_ENV=development
EOF
```

4. **Load in application:**
```python
# Python
from dotenv import load_dotenv
load_dotenv()
```

```javascript
// Node.js
require('dotenv').config()
```

5. **Access variables:**
```python
import os
api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError("API_KEY not set")
```

## Common Mistakes

❌ **Committing .env to git**
- Add .env to .gitignore FIRST
- Check with: `git status` before committing

❌ **No validation**
```python
# Bad - fails silently
api_key = os.environ.get('API_KEY')
```

✅ **Validate required vars:**
```python
# Good - fails fast with clear error
api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError("API_KEY environment variable required")
```

❌ **Inconsistent naming**
- Use UPPER_SNAKE_CASE consistently
- Not `apiKey` or `api-key`

## Examples

**Example 1: Python Flask app**
```python
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DATABASE_URI'] = os.environ.get('DATABASE_URL')

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY must be set")
```

**Example 2: Node.js Express app**
```javascript
require('dotenv').config()

const app = express()
const PORT = process.env.PORT || 3000
const DB_URL = process.env.DATABASE_URL

if (!DB_URL) {
  throw new Error('DATABASE_URL must be set')
}
```

## Production Deployment

For production:
- Set env vars in hosting platform (Heroku, AWS, etc.)
- Never commit production secrets
- Use secret management tools for sensitive data
- Rotate secrets regularly

---

Remember: If it's a secret or configuration, it belongs in an environment variable, not in code.
```

**You save it:**
```bash
# Save the skill
cat > "${skills_dir}/env-var-handling/SKILL.md" <<'EOF'
[content above]
EOF
```

**You verify:**
```bash
codex-skills list
# Should show: Environment Variable Handling
```

**You announce:**
"I've created the 'env-var-handling' skill. It will activate whenever you mention environment variables, configuration, or when I see hardcoded secrets. You can load it anytime with `codex-skills use env-var-handling`."

## Advanced: Skill Families

Related skills can reference each other:

```markdown
## Related Skills

See also:
- `codex-skills use security-best-practices` for broader security patterns
- `codex-skills use docker-config` for containerized deployments
```

This creates a knowledge graph of interconnected skills.

## Meta-Skill: Using This Skill

**When user asks you to create a skill:**

1. Announce: "I'll create a new skill for [topic]"
2. Ask clarifying questions if needed:
   - What should trigger this skill?
   - What are common error messages?
   - What mistakes should we warn about?
3. Follow this skill's structure
4. Create the file in `${DOTCODEX_DIR:-../dotcodex}/skills/` (symlinked to `~/.codex/skills/`)
5. Verify with `codex-skills list`
6. Announce completion and when it will activate

**Remember:** You're creating instructions for your future self. Be clear, be specific, be helpful.

---

**This skill is itself an example of a well-structured skill. Use it as a template!**
