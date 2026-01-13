---
title: GitLab Dedicated Overview
category: GitLab Dedicated
description: "GitLab Dedicated Support overview."
---

### Overview

[GitLab Dedicated](https://docs.gitlab.com/subscriptions/gitlab_dedicated/), from a support perspective, works as a combination of SaaS and Self-Managed. Customers have full Admin access to the instance, but no access to the infrastructure, nor to the backend configurations. This workflow captures the differences, and details of providing support for GitLab Dedicated.

When working on GitLab Dedicated tickets, a good mental model to follow is to determine if the issue is an Application issue or an Infrastructure issue.

- If you're dealing with an Application issue, that is, the issue is within the GitLab application, then you can treat it like a Self-Managed instance while being mindful of the [features that are not available for GitLab Dedicated](https://docs.gitlab.com/subscriptions/gitlab_dedicated/#unavailable-features).
- If it's an infrastructure issue, you'll want to consider engaging with the SREs by opening a [Request for Help](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicated), checking [for incidents](https://gitlab.com/gitlab-com/gl-infra/gitlab-dedicated/incident-management/-/issues/?type%5B%5D=incident), or [raising one yourself](#raise-a-dedicated-incident). The [runbooks](https://gitlab.com/gitlab-com/gl-infra/gitlab-dedicated/team/-/tree/main/runbooks) used by the SREs may be useful additional context.

Use the [SaaS, Self-Managed and Dedicated Troubleshooting tables](/handbook/support/workflows/saas_sm_cheatsheet/) to learn more about the differences between `gitlab.com`, self-managed and GitLab Dedicated.

If you'd like to work on GitLab Dedicated tickets, consider [creating an issue using the template](https://gitlab.com/gitlab-com/support/support-training/-/issues/new?issuable_template=GitLab%20Dedicated) in Support Training, and reading the [GitLab Dedicated engineering overview](https://gitlab-com.gitlab.io/gl-infra/gitlab-dedicated/team/engineering/overview.html) (GitLab internal only).

Below is a list of other GitLab Dedicated Support workflow pages. This is list
is a temporary measure to workaround the lack of until workflow categories are reintroduced

- [GitLab Dedicated Logs](/handbook/support/workflows/dedicated_logs/)
- [GitLab Dedicated Observability and Monitoring (Grafana)](/handbook/support/workflows/dedicated_instance_health/)
- [GitLab Dedicated Switchboard Troubleshooting](/handbook/support/workflows/dedicated_switchboard/)
- [Hosted runners for GitLab Dedicated](dedicated_runners.md)

Here are links to other pages about GitLab Dedicated around GitLab:

- Docs: [Configure GitLab Dedicated](https://docs.gitlab.com/administration/dedicated/)
- Product: [Glossary of Switchboard terms](https://about.gitlab.com/direction/platforms/switchboard/glossary/)
- Infrastructure: [GitLab Dedicated internal docs](https://gitlab-com.gitlab.io/gl-infra/gitlab-dedicated/team/) (GitLab internal only)
- CSM: [Engaging with GitLab Dedicated Customers](https://internal.gitlab.com/handbook/customer-success/csm/gitlab-dedicated/) (GitLab internal only)

### Handling tickets that are not about GitLab the product but related to how we handle the infrastructure

Handling GitLab Dedicated tickets should be approached the same way as other tickets: use the docs, the handbook and the various issue trackers to help address the customer request. Anything that is related to our provisioning of the tenant or how we manage the infrastructure requires a different approach:

- check the docs and the handbook
- point the customer to the [GitLab Trust Center](https://trust.gitlab.com/?product=gitlab-dedicated) at `trust.gitlab.com` for inquiries related to compliance
- point the customer to their CSM for any questions not addressed by the GitLab Trust Center

### Test and reproduction on GitLab Dedicated instance

GitLab Support has access to a GitLab Dedicated instance for testing and problem
reproduction purposes. This instance can be accessed at the following URLs:

- GitLab: https://dedicatedtestsandbox.gitlab-private.org
- OpenSearch: https://opensearch.dedicatedtestsandbox.gitlab-private.org/_dashboards
- Grafana: https://grafana.dedicatedtestsandbox.gitlab-private.org
- Switchboard: https://console.gitlab-private.org/tenants/40

To receive an invite to the GitLab Dedicated instance, ask Armin, Daphne, Wade or Wei-Meng in [#support_gitlab-dedicated](https://gitlab.enterprise.slack.com/archives/C058LM1RL3V).

You can also request an assigned GitLab Duo Enterprise seat.

### Conducting a test

When running a test on the GitLab Support Dedicated instance,

- consider whether your test can be conducted in an instance deployed in the [Sandbox Cloud Realm](/handbook/company/infrastructure-standards/realms/sandbox/)
- communicate about it on the Slack channel [#support_gitlab-dedicated](https://gitlab.enterprise.slack.com/archives/C058LM1RL3V)
- revert your changes when you are done

As the test instance is shared within the GitLab Support team, post a message at the beginning of a test with an estimate duration if the test is likely to impact the performance of the instance.
Upon test completion, revert your changes and use the emoji `:done:` to show the test is completed and the instance has been restored to the previous state.

This instance is deployed to the [`Test` environment](https://gitlab.com/gitlab-com/gl-infra/gitlab-dedicated/team/-/tree/main#deployed-environments).

### Administrative access to a Dedicated instance

The GitLab Dedicated team does **not** have administrative access to the [Admin Area](https://docs.gitlab.com/administration/) in the GitLab application on Dedicated instances and neither does the GitLab Support team. Select individuals in the customer organization do have access to the **Admin Area**. Any support requests that require a GitLab instance administrator to make a change in the Admin Area, for example resetting 2FA, has to be performed by the appropriate team within the customer organization.

### Sharing internal logs, data & graphs

We should not visually or physically share internal logs, data and graphs
with GitLab Dedicated customers by default. Examples of things we should
not share include, but are not limited to, screenshots of graphs, copied
log entries, and raw log dumps.

For avoidance of doubt:

- Internal logs refers to [logs not generated by the GitLab application](/handbook/support/workflows/dedicated_logs/#sharing-logs).
- Internal data and graphs include all data available in Grafana.
Here is some background to understand why:

1. GitLab Dedicated comes with a Sevice Level Availability SLO, which if not
   met results in financial penalties for GitLab.
1. Capacity is limited for the GitLab Dedicated engineering teams as of October
   2023. The teams want to spend the majority of their time on engineering
   tasks and avoid spending time answering non-critical customer questions.

Sharing internal logs, data and graphs without adequate context and explanation
may cause customers to misinterpret the provided information, creating more
work for *all* teams involved and, in the worst case, cause unnecessary damage
to GitLab's relationship with the customer.

If you assess that sharing such internal logs, data and graphs with the
customer would create results for the customer and for GitLab, consult with a
Director of Support. Be aware that a formal process for this is still being
defined, and that there will be delays as approvals are currently ad hoc.

### Working with logs

Working with logs [has been moved](/handbook/support/workflows/dedicated_logs/)

### Working with Grafana

Working with Grafana [has been moved](/handbook/support/workflows/dedicated_instance_health/)

### View instance metadata

Use the Switchboard app. More information can be found in the [Switchboard workflow](/handbook/support/workflows/dedicated_switchboard/).

#### Feature Flags are not supported

In GitLab Dedicated, [feature flags](https://docs.gitlab.com/subscriptions/gitlab_dedicated/#available-features) are not supported, meaning we do not able enable/disable a feature flag for a Dedicated instance. When customers request feature flags to be modified in the GitLab Rails console, the GitLab Support team should:

- create or find an issue in the appropriate issue tracker about making this feature generally available (without a feature flag).
- notify the [appropriate Product Manager](/handbook/product/categories/) in the issue with a comment that followed the [feedback template](/handbook/product/product-management/#feedback-template).
- notify the customer that we [don't keep tickets open](https://about.gitlab.com/support/general-policies/#we-dont-keep-tickets-open-even-if-the-underlying-issue-isnt-resolved) even if the underlying issue isn't resolved.
- check whether the customer has any questions about the next steps.

Support team members with questions can check in the [`#support_gitlab-dedicated`](https://gitlab.enterprise.slack.com/archives/C058LM1RL3V) Slack channel for additional guidance.

### Feature proposals

GitLab Dedicated feature proposal issues should be created in the **Public** [`gitlab-org/gitlab` issue tracker](https://gitlab.com/gitlab-org/gitlab/-/issues/?sort=created_date&state=opened&first_page_size=100). Mention the Product Manager when opening a feature proposal issue. Use the [feedback template](/handbook/product/product-management/#feedback-template) to register a customer's interest in the feature proposal.

### Configuration changes

GitLab Dedicated uses the [Cloud Native Hybrid reference architecture](https://docs.gitlab.com/administration/reference_architectures/10k_users/#cloud-native-hybrid-reference-architecture-with-helm-charts-alternative). Instance implementation and changes are done via the [instrumentor project](https://gitlab.com/gitlab-com/gl-infra/gitlab-dedicated/instrumentor).

If it's an emergency, [raise a Dedicated incident](#raise-a-dedicated-incident).

When any changes are required besides those listed below, raise [an issue with `SupportRequestTemplate-GitLabDedicated`](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicated).

#### Inbound (Forward) PrivateLink Request

Inbound Private Link configuration is now available for the [customer to self-serve in Switchboard](https://docs.gitlab.com/administration/dedicated/configure_instance/network_security/#inbound-private-link) and should no longer require support engagement.

#### Outbound (Reverse) PrivateLink Request

Customers can [self-serve outbound private link configuration](https://docs.gitlab.com/administration/dedicated/configure_instance/network_security/#outbound-private-link) in Switchboard without engaging support.

#### IP Allowlist Request

In most cases, customers should use **Switchboard** to [update the IP allowlist](https://docs.gitlab.com/administration/dedicated/configure_instance/network_security/#ip-allowlist) for their GitLab Dedicated instance. If this is not possible:

1. Ask the customer to provided the [required information](https://docs.gitlab.com/administration/dedicated/configure_instance/network_security/#ip-allowlist) in the ticket. In this case, it's a comma-separated list of IP addresses.
1. Open a [Request for Help issue](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicated) and confirm that the `support::request-for-help`) in the GitLab Dedicated issue tracker.

##### SCIM / OIDC with IP Allowlist request

Customers who use the IP allowlist may request to enable the SCIM or OIDC endpoints to the internet. This is a simple on/off toggle but must be performed by the Environment Automation team:

1. Open a [Request for Help issue](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicated) in the GitLab Dedicated issue tracker. (Confirm that the `support::request-for-help` label has been applied)

#### SAML Request

1. Ask the customer to provided the [required information](https://docs.gitlab.com/administration/dedicated/configure_instance/authentication/saml/#add-a-saml-provider-with-a-support-request) in the ticket. In this case, it's a SAML configuration block or can be a list of information provided by a customer.
1. Open a new [SAML Config Request issue](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicatedSAMLConfigRequest) and confirm that the `support::request-for-help` label is added.
1. Add the customer provided information and match it with the required formatting.

#### Application Logs Request

See [Granting customers access to application logs](/handbook/support/workflows/dedicated_logs/#granting-customers-access-to-application-logs)

### Filing issues

In cases where Customer Support need to interact with Dedicated engineers to gather information or debug a problem at tenant's request (when Grafana or OpenSearch do not suffice), raise an issue in the [Request for Help issue tracker](https://gitlab.com/gitlab-com/request-for-help/-/issues/) using [the `Request for Help` template](https://gitlab.com/gitlab-com/request-for-help/-/issues/new?issuable_template=SupportRequestTemplate-GitLabDedicated).

RFH have an [SLA](https://gitlab-com.gitlab.io/gl-infra/gitlab-dedicated/team/runbooks/on-call.html#sla) of three working days for all severity levels. For severity 1 and 2 issues based on [Support definition](https://about.gitlab.com/support/#definitions-of-support-impact), consider [raising a Dedicated incident](#raise-a-dedicated-incident). Ask in Slack `#support_gitlab-dedicated` if you are unsure.

During the course of the investigation, you may realize that you need to escalate a Request for Help (RFH) issue to another team. You should follow the existing process to [formally request help from another group in the GitLab Development Team](/handbook/support/workflows/how-to-get-help/#how-to-formally-request-help-from-the-gitlab-development-team). When doing this:

- Summarize the investigation thus far and make sure the ask for the team you are escalating to is clear
- Apply the `~workflow-infra::Escalated` label to the RFH issue in the GitLab Dedicated issue tracker

### Handling GitLab Dedicated emergencies

GitLab Dedicated customer emergencies follow the same process to
[triage the emergency request](/handbook/support/workflows/customer_emergencies_workflows/#triage-the-emergency-request)
as all other customer emergencies.

If the customer is reporting an availability or performance issue:

1. Look up the customer on [Dedicated Switchboard](dedicated_switchboard.md#accessing-switchboard). In the **Overview** tab, check if there are any **Active incidents**.
1. If there is a relevant open incident:
   - Inform the customer that the GitLab Dedicated infrastructure team is actively investigating.
   - Get in touch with the Dedicated SRE on-call and determine if the customer needs to be involved
     with troubleshooting.
   - Assist the customer and the Dedicated SRE as necessary.
1. If there isn't an open incident, [raise a Dedicated incident](#raise-a-dedicated-incident).

#### Understanding Tenant Status in Switchboard

The Switchboard Overview page displays real-time status information about each GitLab Dedicated instance. Refer to the Dedicated Switchboard workflows to [Understand Tenant Status Indicators](dedicated_switchboard.md#understanding-tenant-status-indicators).

#### Raise a Dedicated incident

When raising a GitLab Dedicated incident, you must complete all three steps:

1. [Declare a Dedicated incident through Slack](../../engineering/infrastructure-platforms/incident-management/_index.md#reporting-an-incident).
   - Provide the `internal_reference` and `tenant_id` (also known as identifier) of the customer by referring to [Dedicated Switchboard](dedicated_switchboard.md#accessing-switchboard).
1. In the incident channel that is automatically created on Slack, provide a summary of the current state.
1. Dedicated incidents declared do not automatically page EOCs, unlike for GitLab.com. Proceed to [escalate the incident to the GitLab Dedicated Engineer On-Call](#escalate-to-gitlab-dedicated-engineer-on-call).

You are now done raising the incident!

#### Escalate to GitLab Dedicated Engineer On-Call

Sometimes, you may need to escalate to the GitLab Dedicated Engineer On-Call (GDEOC), which is a GitLab Dedicated SRE, to get their immediate attention on an urgent Dedicated issue or an incident. 

Escalate to the GDEOC by paging them. Select **dedicated EOC** as the **On-Call Teams** when you:

- Click on the button **📟 Escalate to someone** in the Slack channel, or
- Type `/inc escalate` into the Slack channel.

#### Engaging the GitLab Dedicated CMOC

If the nature of the emergency reaches the point where we only need to provide async status updates
to the customer, consider engaging the [GitLab Dedicated Communications Manager on Call](/handbook/support/workflows/dedicated_cmoc)
to take over.
