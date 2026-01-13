---
title: "Cloud Spanner Region Configuration for Topology Service"
owning-stage: "~devops::tenant-scale"
group: cells-infrastructure
creation-date: "2025-05-08"
authors: ["@a_richter"]
coach:
approvers: []
toc_hide: true
---

{{< engineering/design-document-header >}}

The Topology Service in the Cells architecture requires a highly available database with strong consistency guarantees. Cloud Spanner offers both [regional](https://cloud.google.com/spanner/docs/instance-configurations#regional-configurations) and [multi-regional](https://cloud.google.com/spanner/docs/instance-configurations#multi-region-configurations) configurations.
For our implementation, we need to determine the optimal configuration that balances performance, disaster recovery capabilities, and cost.

Key considerations:

- Client side latency example HTTP Router -> Topology Service.
- Server side latency inter spanner communication such as the Paxos replication.
- Disaster recovery needs and resilience against regional outages.
- Cost implications for different configurations.
- [SLAs](https://cloud.google.com/spanner/sla) provided by Google.

Multi-regional configurations under consideration:

- `nam3`: Read-write replicas in east of US, and optional replicas in Europe and Asia
- `nam11`: Read-write replicas across multiple North American regions
- `nam-eur-asia3`: Read-write across North America, and read only across Europe and Asia

## Client Side Latency Testing

We tested the latency between various GCP regions and the current Topology Service hosted in us-east1/us-central1 to mimic our production environment where HTTP Router can send requests to it from all over the globe.
Testing was performed using GCP VMs running k6 load testing tool, which provides an indication of cross-region latency patterns.

Test VMs were created in the following regions:

- asia-east1-a (n1-standard-4)
- europe-west1-b (n1-standard-4)
- us-east1 (n1-standard-4)
- us-central1 (n1-standard-4)

The k6 test script made POST requests to the Topology Service's `/v1/classify` endpoint with a single [virtual user](https://grafana.com/docs/k6/latest/reference/glossary/#virtual-user) over 30 seconds.

<details>
<summary>K6s Latency Testing Methodology</summary>

See this [Comment](https://gitlab.com/gitlab-com/content-sites/handbook/-/merge_requests/13198#note_2517912631) for further details

<pre><code>import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1, // Number of virtual users
  duration: '30s', // Test duration
};

export default function() {
  const url = 'https://topology-rest.runway.gitlab.net/v1/classify';
  const payload = JSON.stringify({
    type: "CELL_ID",
    value: "2"
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = http.post(url, payload, params);

  // Check if the request was successful
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
}
</code></pre>

</details>

### Results

**Baseline Configuration (us-east1/us-central1 deployment):**

| Run     | us-east1    | europe-west1-b | asia-east1-c |
| ------- | ----------- | -------------- | ------------ |
| 1       | 11.57ms     | 105.69ms       | 182.41ms     |
| 2       | 11.27ms     | 106.12ms       | 188.10ms     |
| 3       | 12.04ms     | 105.12ms       | 182.79ms     |
| **Avg** | **11.63ms** | **105.64ms**   | **184.43ms** |

**Multi-Regional Configuration (us-east1/us-central1/europe-west1/asia-east1 deployment):**

| Run     | us-east1    | europe-west1 | asia-east1  | us-central1 |
| ------- | ----------- | ------------ | ----------- | ----------- |
| 1       | 14.35ms     | 17.59ms      | 11.48ms     | 31.30ms     |
| 2       | 14.82ms     | 18.12ms      | 11.23ms     | 32.87ms     |
| 3       | 13.92ms     | 17.21ms      | 11.79ms     | 30.76ms     |
| **Avg** | **14.36ms** | **17.64ms**  | **11.50ms** | **31.64ms** |

### Analysis

The latency testing reveals significant improvements for international regions when using multi-regional deployment:

- **Europe latency improvement**: 83% reduction (105.64ms → 17.64ms)
- **Asia latency improvement**: 94% reduction (184.43ms → 11.50ms)
- **US East Coast**: Slight increase (11.63ms → 14.36ms) due to distributed routing

These results demonstrate that while our proposed `nam11` configuration serves North American users well, there would be substantial performance benefits for future EU or Asia-based deployments if we migrate to `nam-eur-asia3`.

## Server Side Latency

Spanner uses [Paxos for replication](https://cloud.google.com/spanner/docs/replication). In multi-regional a successful write means that it's done on both regions.
Both regions need to have low latency between them to speed up the writes.
The `Performance Dashboard` below shows that the least amount of latency is
between `us-east1` and `us-east4` which are the regions for `nam3`.

![Latency between zone pairs](/images/cells/latency_between_zone_pairs.png)

[source](<https://console.cloud.google.com/net-intelligence/performance/global-dashboard?referrer=search&inv=1&invt=Ab2uwg&project=gitlab-staging-1&pageState=(%22performanceDashboardTraffic%22:(%22v%22:%22internal%22),%22performanceDashboardMetric%22:(%22v%22:%22latency%22),%22pdNetworkTierState%22:(%22n%22:%22NETWORK_TIER_UNSPECIFIED%22),%22globalPerformanceDashboardRegions%22:(%22regions%22:%22%5B%5C%22us-central1%5C%22,%5C%22us-east1%5C%22,%5C%22us-east4%5C%22%5D%22),%22performanceDashboardRegions%22:(%22regions%22:%22%5B%5D%22))>)

## Decision

We will base our instance configuration off [`nam3`](https://cloud.google.com/spanner/docs/instance-configurations#multi-region-configurations) with the following
modification:

- `us-east1` as primary instead of `us-east4`: Our primary region is `us-east1`
- Additional Read-only replicas: HTTP Router is globally distributed this means Topology service also needs to be, to improve latency for classification. This means we need additional read-only replicas.

| Read-Write Regions               | Read-Only Regions                             | Witness Region | Optional Read Only Region         |
| -------------------------------- | --------------------------------------------- | -------------- | --------------------------------- |
| `us-east1` (primary), `us-east4` | `us-west2`, `asia-southeast1`, `europe-west1` | us-central1    | `asia-southeast2`, `europe-west2` |

We will rely on Google's default encryption for data at rest, which is automatically enabled, rather than implementing Customer-Managed Encryption Keys (CMEK).

## Consequences

When we change the topology of Spanner this will trigger an [instance move](https://cloud.google.com/spanner/docs/move-instance).
Using terraform can result into data loss since it will re-create the instance,
but if we add read-replicas right before we [add Legacy Cell to Cells Cluster](https://gitlab.com/groups/gitlab-com/gl-infra/-/epics/1625) there would be no data loss.

### Benefits

1. Reduced Costs up until we need it: We can start small and expand while not
   changing the read-write topology.
1. Least server side latency for writes.
1. Ability to expand to other contents like Europe and Asia for client side
   latency.
1. Less maintenance overhead with encryption keys compared to CMEK

## Alternatives Considered

### Alternative 1: `nam-eur-asia3`

**Context**: Read-write in `us-east1` and `us-central1` with out-of-the-box
read-only regions.

**Decision**: Not ideal for server side latency, and high cost from the start
with little regional expandability.

### Alternative 2: `nam11`

**Context**: Read-write in `us-east1` and `us-central1` with a single optional
read-only regions.

**Decision**: Not ideal for server side latency with little regional expandability.

## Cost Analysis

| Configuration                                                                                                                                                                                              | Compute    | Replication | Total Cost |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------- | ---------- |
| [nam3](https://cloud.google.com/products/calculator?hl=en&dl=CjhDaVF3TnpjNVlqZ3paQzFoTldJNExUUmxNVGd0T0RBek9TMWhaR00yTlRNMVpUSTRaRElRQVE9PRAOGiRDRENBM0ZENy0zQ0Y5LTQ1MkQtQkJBMi04NUZGNjU1RUVBM0U)          | $12,138.60 | $888.18     | $13,026.78 |
| [nam11](https://cloud.google.com/products/calculator?hl=en&dl=CjhDaVEzTVRoaE1HTTBNQzB6TldJM0xUUXpNemt0T0dRMU55MDBaVEpqWVdZeE9UTXpPV0VRQVE9PRAOGiRDRENBM0ZENy0zQ0Y5LTQ1MkQtQkJBMi04NUZGNjU1RUVBM0U)         | $11,702.50 | $888.18     | $12,590.68 |
| [nam-eur-asia3](https://cloud.google.com/products/calculator?hl=en&dl=CjhDaVF3WmpJNE5qZzVOQzFrWldVeUxUUTBObUl0WWpFMll5MWxPV000TURKa05qWm1ZamdRQVE9PRAiGiQ1Rjc1REQ3Ny0xREQzLTQ5MEEtOEYwNy02NjVGNUI1QTRFMEU) | $20,751.58 | $1937.12    | $22,688.70 |

This estimate is based on:

- 5 nodes of compute capacity
- 1 TB of SSD storage
- 10 GB of data written/modified per hour
- Enterprise Plus Edition
