# Skills Requiring Script-First Directive

This checklist tracks which skills need the Script-First directive based on their bulk operation or multi-step workflow requirements.

## Criteria for Inclusion

A skill requires the Script-First directive if it involves:
- Bulk operations (N > 10 items)
- Large data processing (> 1000 lines)
- Multi-resource queries (N > 5 resources)
- Sequential multi-step workflows (> 3 steps)
- Any loop-based iteration

## Existing Skills

### Applied

- [x] `document-parser` - Multi-document comparison and batch parsing
  - Reason: Parses multiple large documents, compares structures
  - Added: 2025-11-26

### Pending Application

- [ ] `skill-builder` - Bulk skill migration/creation
  - Reason: When migrating multiple skills to new schema format
  - Priority: Low (rare use case)

### Not Applicable

- `core/librarian` - Single search operation
- `time-awareness` - Single date/time query
- `uv-python` - Individual Python operations

## Planned Skills (Future)

### High Priority (Core SRE Operations)

- [ ] `k8s/bulk-restart` - Restart multiple deployments
  - Reason: Iterates through N deployments
  - Example: "Restart all deployments in namespace X"

- [ ] `k8s/pod-cleanup` - Delete pods matching pattern
  - Reason: Bulk delete operation
  - Example: "Delete all Evicted pods"

- [ ] `k8s/health-check-all` - Check health of multiple services
  - Reason: Multi-resource query
  - Example: "Which services are unhealthy?"

### Medium Priority (Observability)

- [ ] `logs/cloudwatch-search` - Parse large log volumes
  - Reason: Large data processing
  - Example: "Find all ERROR lines in yesterday's logs"

- [ ] `logs/multi-service-grep` - Search logs across services
  - Reason: Multi-resource aggregation
  - Example: "Find 'timeout' errors across all services"

- [ ] `monitoring/alert-triage` - Process alert backlog
  - Reason: Bulk operation on alerts
  - Example: "Acknowledge all P3 alerts older than 24h"

### Lower Priority (Infrastructure)

- [ ] `aws/ec2-inventory` - Query many instances
  - Reason: Multi-resource query
  - Example: "List all stopped instances by age"

- [ ] `aws/security-group-audit` - Audit security groups
  - Reason: Bulk audit operation
  - Example: "Find all SGs with 0.0.0.0/0 ingress"

- [ ] `db/migration-batch` - Run multiple migrations
  - Reason: Sequential multi-step workflow
  - Example: "Apply all pending migrations"

- [ ] `db/table-stats` - Gather stats across tables
  - Reason: Multi-resource query
  - Example: "Show size of all tables over 1GB"

## Tracking Updates

| Date | Skill | Action | Notes |
|------|-------|--------|-------|
| 2025-11-26 | document-parser | Identified | Multi-doc comparison |
| 2025-11-26 | Initial list | Created | Based on FEAT-004 spec |

## How to Add New Skills to This List

1. Evaluate against the criteria above
2. Add to appropriate section (Applied/Pending/Not Applicable/Planned)
3. Document the reason for inclusion
4. Update tracking table
5. When implementing, add directive to SKILL.md and set `script_first: true`

## Verification

When marking a skill as "Applied":
- [ ] SKILL.md contains Script-First directive block
- [ ] YAML frontmatter has `script_first: true`
- [ ] Examples section includes script template
- [ ] Summary format is specified
