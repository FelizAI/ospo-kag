---
title: "Technical Blueprint"
---

The purpose of this document is to detail the goals and guidelines for the Observability team. The focus is on our principles and our goals for the next five years.

## Team Principles

### Observability for GitLab, not just SaaS Platforms

We are better when we work together.

Although our main mandate is to support GitLab's SaaS Platforms, we actively share knowledge with other teams at GitLab and other customers and build tools and frameworks that work for everyone.

### Self-Service, Discoverability and Accessibility

We favor providing repeatable self-service opportunities to those who use our stack over doing the work ourselves, which increases efficiency for everyone.
These opportunities are easy to use and easy to discover for our users.
Internal users can improve the observability of our platform and access observability data freely, through higher level means (dashboards, reports, etc.) and lower-level well-defined interfaces to underlying data.

### Improve the product with the tools we create when possible

Not all of what we do belongs in the product, but some of it might!

In line with our [Dogfooding philosophy](/handbook/product/product-processes/dogfooding-for-r-d/), we go beyond the SaaS context and consider what we can offer upstream to other GitLab customers.
Similarly, we prefer using GitLab's own features and tools when they fit our requirements.

### Tool Portability

GitLab's SaaS Infrastructure is complex.

We aim to provide observability solutions that are portable or tool agnostic to efficiently deliver a similar and more cohesive experience across our different platforms.

### We implement against Standards

The observability space is a mature and competitive industry, meaning there are usually many different (open source) tools to choose from that have their own benefits and nuances.

We opt for industry accepted standards and implementations, which reinforces our principle of portability.

### Platform-First Approach

Build reusable components, not point solutions. Transform observability into a unified platform that provides self-service access to all observability data with consistent data structures and query interfaces.

We treat the observability services and tools we build as internal products with external-quality standards. This means:

- **Documentation**: Our tools and services are documented as thoroughly as any product you would purchase or use externally
- **Reliability**: We maintain the same quality standards for internal tools that we would expect from any production service
- **User Experience**: We design interfaces and workflows that are intuitive and require minimal tribal knowledge to use effectively
- **Support**: We provide clear support channels and maintain comprehensive troubleshooting resources

## Goals

This is an aspirational list of goals that we would like to achieve in the next five years and should be used as a source of inspiration for project planning and roadmap creation.

### Theme 1: Improve how we work with other teams at GitLab

We are faster together.  If we improve how we work with other teams at GitLab, we make their jobs and our jobs easier, and we can focus on new and additional problems.

#### Goals within this theme

- Determine who our internal customers are and make certain that we're meeting their needs by soliciting feedback
- Determine other observability tools and who is using them and who owns them (Sentry, Tableau, etc)
- Dogfood the Monitor:Observability tracing tool for GitLab.com
- Collaborate with Dedicated to help create and integrate Observability Units
- Support the observability components of Cells and other GitLab initiatives
- Work with other teams (SIRT, business analytics, finops, etc) to de-duplicate logging and metrics and define scope of what goes where
- Improve customer experience for error budgets to make it easier for stage groups to focus on the problems in the code, not the problems in the tooling.
- Expand error budgets to additional teams/environments (e.g. staging environment, Dedicated and include Infrastructure teams)
- Expand capacity planning to additional teams/environments (e.g. ops and staging environment, Dedicated, etc.)
- Create an observability Single Pane of Glass (SPOG)

### Theme 2: Make it easier for teams to onboard to the observability stack

Adding a new service to the observability stack today is a complicated and not well understood process.  Adding new metrics to the source side is also only partially understood.  We should create as the right tools and abstractions to make it so that all our customers can self-service onboarding to the system.  This will also have the benefit that the system will become easier to maintain.

#### Goals within this theme

- Provide reference tooling for teams to onboard themselves to the observability stack (helm charts, cloud run configs)
- Create reusable abstractions that can be used for a wide variety of systems within GitLab and are easy to self-service
- Improve our cardinality of metrics and educate teams on the best practices, making it easy to do the right thing and hard to do the wrong thing, and create a feedback loop to help iterate over improvements
- Create well understood patterns to add metrics at the source side (LabKit, etc)

### Theme 3: Make the observability stack easier to manage and maintain

In order to work efficiently, we make data driven decisions on the health of our system, improve the ease of use for ourselves and for other teams, and make certain that we're focusing on self-service.

#### Goals within this theme

- Set SLOs for availability and correctness of observability tools (metrics, logging, capacity planning, etc)
- Set SLOs for mean time for changes to take effect for metrics and observability deployments
- Use capacity planning to forecast saturation for all aspects of the observability stack
- Improve deployment tooling for observability deployments (helm files, deployment tools, etc)
- Split the runbooks repository into smaller, self contained repositories
- Create a cost effective and easy to manage logging solution
- Push capacity planning as far left as possible (docs on how to use it, live grafana views, etc)
- Create a system to audit metrics, logs and dashboards to delete data that no one uses

### Theme 4: Improve our ability to answer FAQ from the past and unknown questions for the future

We've had a number of situations where lack of observability into aspects of our environment has cost us time, money, and availability.  We need to constantly iterate to improve how we are able to observe our environment by providing appropriate tools and data to the teams who own the services.

#### Goals within this theme

- Increased redis key analysis to better understand how we use Redis

 We have had multiple incidents and multiple issues where a subset of keys have either been unused and were wasted space or grew substantially without anyone realizing it until it was too late.  We also have very little knowledge of which teams own which pieces of data within redis which makes additional analysis even harder.  We need to improve our ability to understand how we're using shared data resources so that we improve how we use them.

- Improve database analysis and observability

Database scale is a core problem for us and our engineering teams are dealing with regular and also not so well known problems due to the scale of the database systems we run. They need database observability tech beyond what you'd usually expect to aid database analysis and getting insights into scaling bottlenecks we need to resolve.

- Provide the ability to answer unknown questions with the data we presently have

### Theme 5: Improve external customer experiences

- Availability reflects the customer experience
- Create a toolchest for self-managed customers so that they can use the knowledge we have
- Create a capacity planning tool for self-managed customers

## Current State Analysis

### Pain Points

- **Data Inconsistency**: 500 errors are named differently across metrics, logs, and traces
- **Tribal Knowledge Dependency**: Deep expertise required to navigate multiple tools
- **Poor Discoverability**: No unified entry point for observability data
- **Configuration Complexity**: Stage groups cannot easily own their observability configuration
- **Limited Correlation**: Difficult to trace issues across the full stack
- **Gaps in Coverage**: Missing observability for HAProxy, Cloudflare, client-side components

### Current Architecture Limitations

- Multiple query interfaces without standardization
- No consistent data structure or naming conventions
- Isolated data silos (metrics in Prometheus, logs in Elasticsearch, no distributed tracing)
- Manual correlation between different observability signals

## Platform Vision

This technical architecture blueprint provides a roadmap for transforming GitLab's observability infrastructure into a unified, self-service platform that aligns with our team principles and strategic goals. The proposed architecture addresses current pain points while positioning GitLab to handle future scale and complexity requirements across all deployment models (SaaS, Dedicated, Self-managed).

Success depends on strong commitment to standards, careful attention to data consistency, and a focus on developer experience throughout the implementation process. By building observability as a platform, we enable teams across GitLab to move faster, debug more effectively, and deliver better experiences to our customers.

### Core Platform Definition

Transform observability from a collection of tools into a **unified platform** that provides:

- Self-service access to all observability data
- Consistent data structures and query interfaces
- End-to-end visibility across all GitLab components
- Ability to answer unknown unknowns through structured data collection

### Why We Need a Platform

- **Data Consistency**: Standardized naming conventions and structures across all observability signals
- **Discoverability**: Single entry point with unified search and correlation capabilities
- **Self-Service**: Enable stage groups to own their observability without deep platform knowledge
- **Reduced Friction**: Eliminate tribal knowledge requirements and complex tool navigation
- **Unknown Unknowns**: Structured data collection that enables exploratory analysis

### What This Unlocks

- Observability as a consistent product for all GitLab users
- Faster time to detect and time to recover for incidents, software bugs, and other debugging across the platform
- Higher availability for GitLab.com and other SaaS platforms through proactive observability that prevents issues before they occur, coupled with faster problem detection and resolution enabled by development teams' deeper understanding of a simpler observability stack."
- Less reliance on individuals with tribal knowledge and more ownership from stage groups
- Less frustration (all types of users) when trying to query observability components
- Ability to answer unknown unknowns and a set of standardized methods to record observability data so that it is easily findable
- Better reflection of the customer experience

## Target Architecture

### High-Level Architecture

#### Write path

![Observability Platform Write Path](/images/engineering/infrastructure-platforms/production-engineering/observability/write_path.png)

#### Read path

![Observability Platform Read Path](/images/engineering/infrastructure-platforms/production-engineering/observability/read_path.png)

#### Configuration

![Observability Platform Write Path](/images/engineering/infrastructure-platforms/production-engineering/observability/configuration.png)

### Core Components

#### 1. Discovery and Entry Layer

- **Service Catalog Integration**: Automatically generated service maps with observability metadata
- **Data Correlation**: Cross-signal search capabilities (find related metrics, logs, traces, profiles)
- **Role-Based Access**: Integrated with Okta

#### 2. Query Federation Engine

While we currently use a single application to display observability data, we envision building a unified data-access layer that serves as the foundation for a comprehensive observability data lake.

**Long-term Goals:**

- **Cross-Signal Correlation:** Automatic linking between metrics, logs, and traces
- **Query Translation:** Convert high-level queries to backend-specific formats
- **Caching Layer:** Intelligent caching for frequently accessed data

This federation engine would enable both visualization and direct programmatic access to all types of observability data across the organization. This represents our first step toward treating observability data as a strategic asset with lake-style access patterns.

#### 3. Data Processing Layer

- **Schema Enforcement**: Ensure consistent data structures across all signals
- **Enrichment Pipeline**: Add metadata, service information, and correlation IDs
- **Sampling and Filtering**: Intelligent data reduction while preserving signal quality
- **Format Standardization**: Convert all data to OpenTelemetry formats

#### 4. Data Storage Architecture

##### Metrics

- Long-term storage with configurable retention
- Federation across multiple clusters

##### Logs

- Structured logging with enforced schema
- Optimized for analytical queries
- Automatic correlation with traces and metrics

##### Distributed Tracing

- Complete request lifecycle tracking
- Integration with profiling data

#### Wide Events

- Structured event data for unknown unknowns
- Flexible schema for exploratory analysis
- Integration with business metrics

#### Continuinous Profiling

- Profiles captured from production processes
- Assists with debugging of complex saturation problems

#### 5. Collection and Instrumentation

##### Untrusted Aggregator

- Tool to collect client side metrics
- Will require complex security discussions
- We will need to investigate potential solutions

##### Application side instrumentation

- Use standard collectors when possible (Otel)
- Create GitLab-specific SDKs with sensible defaults
- Covered Experiences/Users Journeys defined using Labkit

##### Third Party Monitoring**

- Make it easier to monitor things we don't own (Cloudflare, LLMs, etc)
- Make it possible to correlate third party services to customer features through covered experiences and user journeys.

##### Observability Stack**

- Standardized way to add observability for GitLab systems
- Includes tenants (Cells, Dedicated) as well as one-off applications
