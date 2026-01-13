---
title: Unified Security Risk Management Program
---

## Purpose

The Unified Security Risk Management (USRM) program ensures consistent identification, documentation, prioritization, treatment, and tracking of security observations, recommendations, and findings to improve efficiency, enable holistic visibility, and increase adoption rates of security recommendations. The process will also act as an input to security risk management processes across the org allowing for quicker decision making.

## Scope

The program is designed to support any Security Division recommendations, findings, and observations. The onboarding of different sources into the USRM process will be deployed through a phased approach to ensure proper standardization and successful adoption across teams. These sources will then be mapped to individual STORM risks.

Coverage includes identified sources:

| # | Project | Team | USRM Phase | Finding Coordinator | Issue Template |
|:-:| :------ | :--: |-----------| :--: |----------------|
| 1 | [Compliance Observations](https://gitlab.com/gitlab-com/gl-security/security-assurance/security-compliance-commercial-and-dedicated/observation-management/-/issues) | Sec Compliance | Phase 1 | Observation Manager | Existing or USRM |
| 2 | [Security Policy Exceptions](https://gitlab.com/gitlab-com/gl-security/security-assurance/governance-and-field-security/governance/security-governance/-/issues?sort=created_date&state=all&label_name%5B%5D=ExceptionRequest&first_page_size=100) | Security Governance | Phase 1 | @davoudtu | Existing |
| 3 | [Product Risk Register](https://gitlab.com/gitlab-com/gl-security/security-assurance/security-risk-team/storm-risk-register/-/issues/?sort=created_asc&state=opened&label_name%5B%5D=Department%3A%3AProduct%20Security&first_page_size=100) | ProdSec | Phase 1 | @jrinaudo | Existing or USRM |
| 4 | [TPRM Security Notices](https://gitlab.com/gitlab-com/gl-security/security-assurance/security-risk-team/third-party-vendor-security-management/-/issues/?sort=created_date&state=opened&label_name%5B%5D=TPRM%3ASecurity%20Notice&first_page_size=100) | Sec Risk | Phase 1 | Risk Manager |  Existing or USRM |
| 5 | [Vulnerabilities](https://gitlab.com/groups/gitlab-com/gl-security/product-security/vulnerability-management/-/issues/?sort=created_asc&state=opened&label_name%5B%5D=bug%3A%3Avulnerability&first_page_size=100) | Vuln Mgmt. | TBD | TBD  |  TBD |
| 6 | Incidents | SIRT | TBD |  TBD | TBD |
| 7 | [Red Team Recommendations (~RTRec::)](https://gitlab.com/gitlab-com/gl-security/security-operations/leadership/-/wikis/OffSec-Recommendations-Dashboard) | Red Team | Phase 1 | @madlake | USRM |
| 8 | [Inventory findings](https://gitlab.com/gitlab-com/gl-security/product-security/inventory/-/issues) | Sec Architecture | TBD | @kylesmith2 | TBD |
| 9 | [Wiz Findings](https://app.wiz.io/p/production) | InfraSec | TBD | TBD | TBD |
| 10 | [Threat Intel Recommendations (~TIRec::)](https://gitlab.com/gitlab-com/gl-security/security-operations/leadership/-/wikis/OffSec-Recommendations-Dashboard) | Threat Intel | Phase 1 | @madlake | TBD |
| 11 | Signals Engineering (~SET::Signals-Improvement, SET::Detection-New, SET::Signal-Gap) | Signals Engineering | TBD | TBD |TBD |
| 12 | [GitLab vulnerabilities](https://gitlab.com/gitlab-org/gitlab/-/issues/?sort=created_date&state=opened&label_name%5B%5D=bug%3A%3Avulnerability&first_page_size=100) | AppSec/Multiple | TBD |  TBD | TBD |
| 13 | Data Security Recommendations (~DataSec::consult) | DataSec | TBD |  TBD | TBD |
| 14 | Corp Sec Recommendations (~corpsec-metric::consult and ~corpsys-gitlab-com) | CorpSec | TBD |   TBD | TBD |
| 15 | Trust and Safety Contributions (~"Trust and Safety contribution") | T&S | TBD | TBD |  TBD |
| 16 | [Security Reviews](https://gitlab.com/gitlab-com/gl-security/product-security/infrastructure-security/bau/-/issues/?sort=created_asc&state=all&search=Security+review&first_page_size=100&show=eyJpaWQiOiI0OTYiLCJmdWxsX3BhdGgiOiJnaXRsYWItY29tL2dsLXNlY3VyaXR5L3Byb2R1Y3Qtc2VjdXJpdHkvaW5mcmFzdHJ1Y3R1cmUtc2VjdXJpdHkvYmF1IiwiaWQiOjEzNjYzMDUzOH0%3D) | InfraSec | TBD  | TBD  | USRM |

## Roles and Responsibilities

| Role            | RACI | Responsibility                                                        |
|-----------------|------|-----------------------------------------------------------------------|
| Finding Identifier | C | Consults with business stakeholders on the security finding, provides expert recommendations, and determines which stakeholders should be involved in remediation. Must validate remediation mitigates finding identified. |
| Remediation Manager | R | Responsible for executing the remediation plan, including confirming assignees, setting due dates, and fine-tuning remediation activities to meet requirements identified in the recommendation. |
| Business Risk Owner | A | Accountable for the overall risk related to the finding. Can make decisions on whether to remediate or accept the risk. |
| Security Risk Owner | I | Informed of the finding identification, remediation plan, and progress. |
| Finding Coordinator | R | Responsible for ensuring the USRM process is followed correctly, monitoring that service level commitments are met, and escalating when necessary. |

### Authority Matrix

When security findings are identified, the following management levels must be informed based on priority. These managers have authority to intervene if they disagree with the proposed remediation approach or determine an alternative treatment is more appropriate.

| Finding Priority | Business Risk Owner Authority Level | Security Risk Owner Authority Level |
|---------------|--------------------------------|--------------------------------|
| **Low (Priority 4)** | Manager level | Manager level (from originating security team) |
| **Medium (Priority 3)** | Director level | Director level (from originating security team) |
| **High (Priority 2)** | VP level | VP level (from originating security team) |
| **Critical (Priority 1)** | VP level | VP level (from originating security team) |

## Procedure

The USRM workflow can be seen below:

![USRM Workflow](/images/security/usrm_workflow.png)

### Service Level Commitments

These commitments establish standardized timing expectations for each phase of the process. They ensure consistent response times across all security teams and provide clear expectations to business stakeholders regarding when they can expect actions and responses during the finding lifecycle.

| Phase | Duration |
|-------|----------|
| Issue Opened | - |
| Remediation Plan | 4 business days |
| Monitoring Setup | 2 business day |
| Remediation/Closure | Based on finding source and priority |

### Identification

Each team in Security has their own defined workflows. One of the outputs of these workflows is a finding being identified that requires action or remediation. In order to normalize findings in order to assess priority, the following steps should be completed.

Once identified, the finding should be opened in a issue following the team's standard format and issue templates. The finding identifier is responsible for opening an issue in the related GitLab project. The finding identifier fills out all necessary information, remediation recommendations and submits the finding to the remediation manager for validation. The finding coordinator is responsible for managing the finding through the lifecycle. This includes ensuring linkages associated risk issues, validating the finding with the Remediation Manager, tracking all remediation progress and updating the GitLab issue with current information and status updates. Each finding will be assigned a risk rating, which should drive the priority of remediation.

#### USRM Issue Template

A standardized [USRM finding template](https://gitlab.com/gitlab-com/gl-security/security-templates/-/blob/main/.gitlab/issue_templates/usrm-template.md) is available for teams to use when creating security findings. This template ensures consistency across all USRM-tracked findings and includes all required fields for proper tracking and management.

**Key Guidelines:**

- Teams with existing issue templates can continue using them if they include all USRM required fields and labels
- The USRM template should be used for sources without existing templates
- All findings, regardless of template used, must include the required USRM labels for tracking and reporting

#### Drafting Finding Description Guidance

The description should include the who, what, when, where, why, and how related to the finding. As a review step, if you knew nothing about this finding could you understand the finding, how it was identified, and the effect it has on objectives? Consider leveraging the 4Cs model:

- Condition - current state
- Criteria - desired state based on policy, requirement, control, regulation, etc.
- Cause - root cause of the observation
- Consequence - actual or potential effect on objectives/assets

For additional helpful risk drafting guidance from the Prod Sec department can be found [here](/handbook/security/product-security/security-platforms-architecture/risk-register/well-articulated-prodsec-risks/#what-makes-a-well-articulated-risk).

#### Required Labels

Required labels need to be applied to enable prioritization and reporting and metrics. These labels are as follows:

| Label Category | Options | Usage |
|----------------|---------|-------|
| **Workflow Status** | `USRM Workflow::Finding Identified`, `USRM Workflow::Remediation Plan`, `USRM Workflow::Monitoring`, `USRM Workflow::Closed` | Process tracking |
| **Department**|`Department:[department-name]`| To identify department that owns the risk for Corporate findings |
| **Group**|`group:[group-name]`| To identify product that owns the risk for Product findings |
| **Priority** | `priority::1`, `priority::2`, `priority::3`, `priority::4` | Aligns with GitLab standard priority framework. Use either priority/severity labels OR risk rating labels, not both |
| **Severity** | `severity::1`, `severity::2`, `severity::3`, `severity::4` | Aligns with GitLab standard severity framework. Use either priority/severity labels OR risk rating labels, not both |
| **Risk Rating** | `RiskRating::Critical`, `RiskRating::High`,`RiskRating::Moderate`,`RiskRating::Low`| Alternative to severity and priority to rate risks|
| **Risk Treatment** | `risk-treatment::remediate`, `risk-treatment::accept` | Indicates whether risk will be remediated or formally accepted |
| **STORM Risk** | `STORM RISK:#` | To enable risk mapping reporting |
| **Finding Coordinator** | `FindingCoordinator::@team member` | To identify the coordinator responsible for monitoring the finding through the USRM process |

#### Optional Labels

| Label Category | Options | Usage |
|----------------|---------|-------|
| **System** | `system:[system-name]` | For affected systems |
| **Fiscal Year and Quarter** | `FY25-Q3`, `FY25-Q4` | Planning alignment |
| **Escalation** | `escalated::level-1`, `escalated::level-2` | When escalated |
| **Product Group** | `group::authorization` | For action owning group |

#### Issue Status & Alert Labels

These labels are applied either automatically by triage bot or manually by the Finding Coordinator to track issues requiring attention:

| Label | When Applied | Applied By | When to Remove |
|-------|--------------|------------|----------------|
| `stale` | No updates for 30 days | Triage Bot (automatic) | When issue is updated with progress |
| `overdue` | Issue is past its due date | Triage Bot (automatic) | When due date is extended or work completed |
| `Blocked` | Progress cannot continue due to external dependencies, resource constraints, or technical obstacles beyond team's control | Finding Coordinator (manual) | When blockers are removed |
| `Missing_Labels` | Required labels are missing from the issue | Triage Bot (automatic) | When all required labels are applied |
| `Missing_Assignee` | Issue has no assignee after 48 hours of creation | Triage Bot (automatic) | When assignee is added |
| `missing_duedate` | Issue older than 7 days without a due date | Triage Bot (automatic) | When due date is set |

### Risk Rating

Many teams (example [SIRT](/handbook/security/security-operations/sirt/severity-matrix/)) have existing risk assessment methodologies. For those that don't, please use the standardized GitLab [priority](https://docs.gitlab.com/development/labels/#priority-labels) and [severity](https://docs.gitlab.com/development/labels/#severity-labels) framework, adapted for security division requirements below:

<details><summary>Priority and Severity Framework</summary>

#### Priority Rating (Business Impact and Urgency)

| Priority | Label | Criteria | Target Resolution | Notification | Equivalent Mappings |
|----------|-------|----------|-------------------|--------------|-------------------|
| **1 (Critical)** | `priority::1` | Urgent security threat requiring immediate action regardless of team capacity | 30 days maximum | Immediate escalation to Security leadership | StORM Critical (26-30), Vulnerability Critical (CVSS 9.0-10.0) |
| **2 (High)** | `priority::2` | High impact security issue that will be addressed soon with dedicated capacity | 60-90 days | Security management notification within 24 hours | StORM High (21-25), Vulnerability High (CVSS 7.0-8.9) |
| **3 (Medium)** | `priority::3` | Important security improvements that may compete with other priorities | 90-120 days | Standard team lead notification | StORM Medium (11-20), Vulnerability Medium (CVSS 4.0-6.9) |
| **4 (Low)** | `priority::4` | Security enhancements with no designated timeline | No specific timeline | Standard backlog management | StORM Low (1-10), Vulnerability Low (CVSS 0.1-3.9) |

#### Severity Rating (Technical Impact and Complexity)

| Severity | Label | Definition | Examples | Remediation SLO |
|----------|-------|------------|----------|-----------------|
| **1 (Blocker)** | `severity::1` | Security issue that completely blocks normal operations or causes data loss | System compromise with no workaround, active data breach, critical control failure | Immediate mitigation required |
| **2 (Critical)** | `severity::2` | Security issue with significant impact but complex workaround available | Critical vulnerabilities with limited exploit scenarios, major compliance gaps | 30 days for Critical vulnerabilities |
| **3 (Major)** | `severity::3` | Security issue with moderate impact and reasonable workaround | Medium vulnerabilities, process improvements, minor compliance issues | 90 days for vulnerabilities |
| **4 (Minor)** | `severity::4` | Security enhancement or minor issue with minimal impact | Best practice improvements, documentation updates, low-priority recommendations | 180 days for vulnerabilities |

#### Risk Assessment Guidelines

When assigning priority and severity ratings, consider these factors:

**Priority Assessment Factors**:

- **Business Impact**: Effect on operations, customers, and revenue
- **Regulatory Requirements**: Compliance deadlines and obligations
- **Stakeholder Urgency**: Leadership and customer expectations
- **Resource Availability**: Team capacity and competing priorities

**Severity Assessment Factors**:

- **Technical Impact**: System functionality and security posture
- **Scope of Affected Systems**: Number and criticality of impacted assets
- **Exploitability**: Ease of exploitation or occurrence
- **Compensating Controls**: Existing mitigations that reduce severity

</details>

### Recommendations

Recommendations reflect how the finding will be addressed. ISO 31000 recommends applying one or more of the following approaches to treating risks:

- Avoid - Deciding not to start or continue with an activity that gives rise to the risk, or removing the risk source altogether
- Mitigate - Introducing controls that reduce either the likelihood of the risk occurring or the impact.
- Transfer - Sharing the risk with a third-party through contracts, outsourcing, or insurance.
- Accept - Making an informed decision to take the risk.

Recommendations should:

- Address the root cause - If this can't be done, the recommendation should reduce the likelihood or impact of the risk.
- Be low-context.
- Achievable – Realistic given available resources, skills, and constraints.
- Actionable – Clearly states what needs to be done, by whom, and when.

Additional helpful guidance from the Red Team can be found [here](/handbook/security/security-operations/red-team/how-we-operate/#security-recommendations-across-gitlab).

### Remediation Plan

Using your recommendation, work with the appropriate owner group to develop a [SMART](/handbook/security/critical-projects/#smart-and-not-an-okr) remediation plan.

### Business Risk & Security Risk Owner

Once the remediation plan is documented, both the Business Risk Owner and Security Risk Owner must be informed.

**Business Risk Owner:**

- Accountable for the overall risk presented by the finding and response decision
- Must be informed of the identified fionding and proposed remediation plan
- Has authority to approve the remediation approach or request modifications
- Can choose to formally accept the risk if remediation is not feasible or justified

**Security Risk Owner:**

- Represents the originating security team that identified the finding
- Reviews the proposed remediation plan to ensure it adequately addresses the security recommendation
- Provides technical validation and security acknowledgment
- Escalates concerns if the remediation approach leaves significant residual risk

Tagging both owners in the GitLab issue ensures proper visibility and accountability, which greatly increases the likelihood that the risk will be appropriately addressed.

### Risk Acceptance

There may be instances where we decide to accept risk rather than avoid, mitigate, or transfer it. If risk acceptance is desired for a security finding, the remediation owner must provide:

1. **Risk Description**: Clear statement of the risk
2. **Business Justification**: Why acceptance is necessary
3. **Compensating Controls**: What mitigations are in place to reduce exposure
4. **Expected Duration**: How long acceptance is needed (maximum is 24 months based on risk rating)
5. **Residual Risk**: What risk remains after compensating controls

The finding coordinator validates that acceptance is appropriate based on our risk tolerance and compliance/regulatory obligations. Approvals are required from the department's management team per the [Authority Matrix](/handbook/security/security-observations-risk-management.md#authority-matrix).

Once approved, apply the `risk-acceptance::active` label and the appropriate risk level label. **The issue remains open** as an active risk acceptance that will be tracked and periodically reviewed.

#### Periodic Review Schedule

The finding coordinator performs periodic reviews at these intervals:

| Risk Level | Review Frequency |
|------------|------------------|
| Critical | Every 6 months |
| High | Every 12 months |
| Medium | Every 18 months |
| Low | Every 24 months |

For each review, the finding coordinator will:

1. Evaluate if original conditions still exist
2. Assess whether severity has changed
3. Review changes to threat landscape or business environment
4. Confirm acceptance justification remains valid
5. Evaluate if remediation options have become available
6. Verify compensating controls are still effective

### Security Acknowledgment

Security will validate that the following is in place:

- Treatment plan or risk acceptance
- Due date for follow-up/remediation testing
- Required labels
- Monitoring in place
- Finding is mapped to related risk issue

### Monitoring

### Recommendation Quality and Escalation

To ensure findings from security teams are accurate, current, and properly managed, we leverage [triage bot](https://gitlab.com/gitlab-org/ruby/gems/gitlab-triage). This bot will support issue quality, nudging/escalation, and timely resolution of security findings across the division.

### Finding Coordinator

The Finding Coordinator is responsible for ensuring findings remain active, current, and have defined remediation timelines. These tasks are aided by the triage bot policies. They will also initiate escalations and ensure blockers are cleared. The finding coordinator role is filled by members of the SecCompliance and SecRisk teams. For more detailed responsibilities and procedures of the finding coordinator, please review the collapsed sections below.

<details>
  <summary>Finding Coordinator Responsibilities</summary>

#### Overview

This runbook provides instructions for Finding Coordinators to manage finding issues through the USRM lifecycle. Follow these procedures to ensure findings progress through each phase and meet service level commitments.

#### Phase 1: Finding Identified (USRM Workflow::Finding Identified)

**When:** A new security finding (issue) is created

**Actions:**

1. Verify the issue has been created with the finding template
2. Confirm the Finding Identifier has completed all required fields in the issue template:

   - Issue title providing high level overview of finding
   - Description of finding (using 4Cs model)
   - Risk of not remediating
   - RACI Stakeholders table with specific team members
   - Recommendation
   - Priority & Severity checkboxes selected
3. Apply initial workflow label and verify all [required labels](#required-labels) are present:

   - `USRM Workflow::Finding Identified`
   - `Department:[department-name]`
   - `priority::1-4`
   - `severity::1-4`
   - `STORM RISK:#`
   - `FindingCoordinator::@team member`
4. Verify all RACI stakeholders are tagged in the issue
5. Confirm issue is linked to appropriate STORM Risk issue
6. Verify exit criteria Step 1 is complete

**Escalation triggers:**

- Issue is incomplete or missing critical information after 1 business day
- Finding Identifier is unresponsive to requests for clarification

---

#### Phase 2: Remediation Plan Documentation (USRM Workflow::Remediation Plan)

**When:** Finding has been identified with complete information and stakeholders tagged

**Actions:**

1. Verify Remediation Manager has been assigned (from RACI table)
2. Monitor for completion of detailed remediation plan (SLC: 4 business days from issue creation)
3. Verify the remediation plan includes:

   - Remediation step table with owners, due dates, and status OR
   - Linked epic/issue for tracking remediation elsewhere
   - Issue due date is set and aligns with priority-based SLOs
4. Update workflow label to `USRM workflow:Remediation Plan`
5. Verify exit criteria Step 2 is complete

**Escalation triggers:**

- Remediation plan not documented after 4 business days
- Remediation Manager not assigned after 2 business days
- Due date not set or doesn't align with priority SLOs
- Remediation plan lacks sufficient detail or clear ownership

---

#### Phase 3: Monitoring (USRM Workflow::Monitoring)

**When:** Remediation plan is approved and work has begun

**Actions:**

1. Update workflow label to `USRM Workflow::Monitoring`
2. Monitor issue for regular progress updates (at minimum monthly)
3. Track against due date and priority-based SLOs
4. Watch for triage bot alerts:

   - `stale` label (no updates for 30 days)
   - `overdue` label (past due date)
   - `Missing_Assignee` label
   - `missing_duedate` label
   - `Missing_Labels` label
5. Address triage bot alerts promptly with assignees
6. Update STORM Risk issue with progress as needed

**Escalation triggers:**

- Issue becomes stale (30+ days without updates)
- Issue is overdue without extension approval
- Remediation blocked with no clear path forward
- Assignee becomes unresponsive
- Due date will be missed and no communication from Remediation Manager

---

#### Phase 4: Remediation Complete & Closure (USRM Workflow::Closed)

**When:** Remediation Manager indicates work is complete

**Actions:**

1. Tag Finding Identifier for validation
2. Verify Finding Identifier has:

   - Validated remediation is complete
   - Confirmed remediation mitigates the original finding
   - Documented remediation evidence in the issue
3. Confirm all required labels are present
4. Close the issue
5. Update related STORM Risk issue to reflect closure
6. Remove any temporary labels (`stale`, `overdue`, etc.)

**Escalation triggers:**

- Finding Identifier cannot validate remediation
- Remediation evidence is insufficient
- Finding Identifier is unresponsive to validation request

---

#### Risk Acceptance Path - Monitoring

**When:** Issue has `risk-acceptance::active` label

**Actions:**

1. Schedule periodic reviews based on priority:

   - Critical: Every 6 months
   - High: Every 12 months
   - Medium: Every 18 months
   - Low: Every 24 months
2. At each review period:

   - Create comment in issue requesting review
   - Tag Business Risk Owner and Security Risk Owner
   - Verify risk conditions, compensating controls still valid
   - Update risk acceptance documentation
   - Assess if remediation is now feasible
3. Issue remains open until remediated or risk no longer exists

**Escalation triggers:**

- Risk conditions have changed significantly
- Compensating controls are no longer effective
- Regulatory/compliance requirements now mandate remediation
- Risk acceptance period exceeds maximum duration (24 months for lowest priority)

---

#### USRM Label Reference

| Label | When to Apply | When to Remove |
|-------|---------------|----------------|
| `USRM Workflow::Finding Identified` | Security finding has been discovered and documented with all required fields complete (description, recommendation, RACI, priority/severity) | When Remediation Manager begins documenting detailed remediation plan (apply `Remediation Plan` label) |
| `USRM Workflow::Remediation Plan` | Remediation Manager is documenting detailed remediation plan with steps, owners, and due dates | When remediation work begins and issue enters active monitoring (apply `Monitoring Active` label) |
| `USRM Workflow::Monitoring` | Remediation work is underway with active progress monitoring - awaiting completion and validation | When Finding Identifier validates remediation complete (apply `Closed` label) |
| `USRM Workflow::Closed` | Security finding has been fully remediated and validated as resolved | N/A - Terminal state |

---

</details>

#### Required Triage Bot Policies

All security teams generating findings must implement the following automated policies in their respective projects:

1. **Stale Issue Nudging**

Policy: Automated nudging when issues remain inactive

- Trigger: Issues without updates for 30 days
- Action: After 30 days of inactivity, add `stale` label and add comment requesting status update and tag assignee
- Exception: Issues labeled `ignore` or `blocked` are excluded

<details>
  <summary>Example Policy</summary>

  ```yaml
  - name: Nudge stale issues
    conditions:
      issue_type: issue
      forbidden_labels:
        - stale
        - <blocked team label here>
      state: opened
      date:
          attribute: updated_at
          condition: older_than
          interval_type: months
          interval: 1
      actions:
          redact_confidential_resources: false
          comment: |
             {{author}} This issue has not been updated in 1 month.

              If this issue is still relevant, please provide an update and/or update the workflow status.

              The `stale` label has been applied to help track issues requiring attention.
          labels:
            - stale
```

</details>

1. **Missing Assignee Management**

Policy: All finding issues must have designated owners

- Trigger: Issues without assignees after 48 hours of creation
- Action: Add `needs-assignee` label
- Exception: Issues in backlog milestone may remain unassigned

<details>
  <summary>Example Policy</summary>

  ```yaml
    - name: Alert when issue has no assignees
      conditions:
        issue_type: issue
        forbidden_labels:
            - Missing_Assignee
        ruby: resource[:assignees].empty?
        state: opened
      actions:
          redact_confidential_resources: false
          comment: |
            {{author}}, This issue is missing an assignee.
          labels:
            - Missing_Assignee
    - name: Remove Missing_Assignee label when there are assignees
      conditions:
        issue_type: issue
        labels:
            - Missing_Assignee
        ruby: |
            !resource[:assignees].empty?
        state: opened
        actions:
          remove_labels:
            - Missing_Assignee
  ```

</details>

1. **Past Due Issue Tracking**

Policy: Overdue issues require immediate attention and justification

- Trigger: Issues past their due date
- Action: Add `overdue` label and comment requesting updated timeline
- Exception: Issues with approved timeline extensions (documented in comments)

<details>
  <summary>Example Policy</summary>

  ```yaml
    - name: Comment on past due issues
      conditions:
        state: opened
        issue_type: issue
        forbidden_labels:
            - overdue
            - bot-ignore
        ruby: |
            past_due_date?
        actions:
          redact_confidential_resources: false
          comment: |
            {{author}} This issue is past due. Please review and update the timeline or mark as completed.
          labels:
            - overdue
  ```

</details>

1. **Due Date Enforcement**

Policy: All finding issues must have realistic timelines

- Trigger: Issues older than 7 days without due dates
- Action: Add `needs-due-date` label and request timeline from assignee
- Exception: Research or discovery issues may use milestone dates instead

<details>
  <summary>Example Policy</summary>

  ```yaml
    - name: Comment no due date issues
      conditions:
        state: opened
        issue_type: issue
        forbidden_labels:
            - missing_duedate
        ruby: resource[:due_date].nil?
      actions:
          redact_confidential_resources: false
          comment: |
            {{author}} This issue has no due date. Please review and update the timeline or mark as completed.
          labels:
            - missing_duedate
  ```

</details>

1. **Required Labels Enforcement**

Policy: All finding issues must have required labels for metrics and reporting

- Trigger: Required label is missing from issue
- Action: Add `missing-label` label and tag assignee for action
- Exceptions: Issues in backlog are ignored

<details>
  <summary>Example Policy</summary>

  ```yaml
    - name: Alert when an issue is missing required labels
      conditions:
        issue_type: issue
        forbidden_labels:
            - Missing_Labels
            - bot-ignore
        ruby: |
            [" list labels"].any? { |rl| !resource[:labels].any? { |l| l.start_with?(rl) } }
        state: opened
        actions:
          redact_confidential_resources: false
          comment: |
            {{author}} this issue does not have an appropriate project work labels.

            Please label it accordingly based on the Labeling Guide). The following labels are missing:
            #{ [" list labels"].map{ |rl| "- #{ rl } #{ resource[:labels].any?{ |l| l.start_with?(rl) } ? ':white_check_mark:' : ':x:' }"}.join("\n") }

            Once you add the missing labels, please remove the `Missing_Labels` label. If you are not a member of SecCompliance, please kindly ignore this message.
          labels:
            - Missing_Labels
  ```

</details>

### Remediation and Closure

The Finding Identifier is responsible for validating that the remediation is completed and effectively mitigates the finding. Once validated, the issue can be closed with appropriate documentation of the remediation evidence.

## References

### Support Channels

Please reach out to `#security-help` in slack, or tag the team managing the issue in the respective issue.

### Internal Documentation

- [Unified Security Risk Management Epic](https://gitlab.com/groups/gitlab-com/gl-security/security-assurance/-/epics/153)
- [Security Risk Sources](https://internal.gitlab.com/handbook/security/#security-risk-sources)
- [GitLab Issue Triage Guidelines](/handbook/product-development/how-we-work/issue-triage/)
- [StORM Program Procedures](/handbook/security/security-assurance/security-risk/storm-program/)
- [Observation Management Procedure](/handbook/security/security-assurance/observation-management-procedure/)
- [Vulnerability Resolution SLAs](/handbook/security/product-security/vulnerability-management/sla/)
- [GitLab Security Handbook](/handbook/security/)
