---
description: Workflow for creating system architecture documentation and ADRs from PRDs in spec-driven development
applyTo: "**/docs/**/system-architecture.md,**/docs/**/architecture-decisions/**/*.md,**/adr-*.md"
---

# System Architecture and ADR Creation Workflow

## Overview

System architecture design translates Product Requirements Documents (PRDs) into high-level system design, defining how multiple systems work together to deliver business value. Architecture Decision Records (ADRs) capture significant architectural choices and their rationale.

**Position in Spec-Driven Flow**: BRD → PRDs with User Stories → **System Architecture (with ADRs)** → SRDs → Implementation Tasks

## Prerequisites

Before creating system architecture, ensure you have:
- ✅ **Complete set of approved PRDs** covering all major feature domains
- ✅ **Business Requirements Document (BRD)** with constraints and objectives
- ✅ **Non-functional requirements** from PRDs consolidated
- ✅ **Technology constraints** and existing system inventory
- ✅ **Team structure and delivery timeline** understanding

## Process

### Step 1: Requirements Analysis and System Boundary Identification

1. **Analyze PRDs Collectively**
   - Identify common data entities across PRDs
   - Map user workflows that span multiple feature domains
   - Extract performance, security, and scalability requirements
   - Identify integration points with external systems

2. **Define System Boundaries**
   - Group related functionality into logical systems
   - Identify data ownership and responsibility boundaries
   - Define integration patterns between systems
   - Consider team ownership and development independence

3. **Extract Architectural Drivers**
   - **Quality Attributes**: Performance, security, scalability, availability
   - **Business Constraints**: Budget, timeline, regulatory requirements
   - **Technical Constraints**: Existing systems, technology choices, team skills
   - **Organizational Constraints**: Team structure, development process, deployment model

### Step 2: High-Level Architecture Design

#### System Decomposition
- **Identify Core Systems**: Based on business domain boundaries from PRDs
- **Define System Responsibilities**: What each system owns and manages
- **Map System Interactions**: How systems communicate and share data
- **Design Data Flow**: How information moves through the architecture

#### Integration Pattern Selection
- **Synchronous Communication**: REST APIs, GraphQL, gRPC
- **Asynchronous Communication**: Message queues, event streams, webhooks
- **Data Sharing**: Shared databases, data replication, event sourcing
- **User Interface Integration**: Micro-frontends, shared component libraries

### Step 3: System Architecture Document Structure

Create `system-architecture.md` with these **required sections**:

#### 1. Architecture Overview
- **Vision Statement**: High-level description of the system architecture
- **Architectural Principles**: Guiding principles for all design decisions
- **Context Diagram**: Visual representation of systems and external dependencies
- **Key Quality Attributes**: Primary non-functional requirements driving design

##### System Context Diagram (Required)
Include a high-level context diagram showing the relationship between systems and external entities:

```mermaid
C4Context
    title System Context Diagram
    
    Person(user, "User", "End user of the system")
    Person(admin, "Administrator", "System administrator")
    
    System(mainSystem, "Main System", "Core business application")
    System_Ext(authProvider, "Auth Provider", "External authentication service")
    System_Ext(paymentGateway, "Payment Gateway", "External payment processing")
    System_Ext(emailService, "Email Service", "External email delivery")
    
    Rel(user, mainSystem, "Uses", "HTTPS")
    Rel(admin, mainSystem, "Administers", "HTTPS")
    Rel(mainSystem, authProvider, "Authenticates users", "HTTPS/OAuth")
    Rel(mainSystem, paymentGateway, "Processes payments", "HTTPS/API")
    Rel(mainSystem, emailService, "Sends notifications", "HTTPS/API")
```

##### High-Level Architecture Diagram (Required)
Include a comprehensive architecture overview showing all systems and their relationships:

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Application]
        Mobile[Mobile App]
    end
    
    subgraph "API Gateway Layer"
        Gateway[API Gateway]
    end
    
    subgraph "Service Layer"
        Auth[Authentication Service]
        User[User Service]
        Data[Data Service]
        Notification[Notification Service]
    end
    
    subgraph "Data Layer"
        UserDB[(User Database)]
        DataDB[(Data Database)]
        Cache[(Redis Cache)]
    end
    
    subgraph "External Services"
        Email[Email Provider]
        SMS[SMS Provider]
        Analytics[Analytics Service]
    end
    
    UI --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> User
    Gateway --> Data
    Gateway --> Notification
    
    Auth --> UserDB
    User --> UserDB
    Data --> DataDB
    Auth --> Cache
    User --> Cache
    
    Notification --> Email
    Notification --> SMS
    Data --> Analytics
```

#### 2. System Inventory
```markdown
## System: [System Name]
**Purpose**: [Primary responsibility and business capability]
**Data Ownership**: [What data this system owns and manages]
**Key Interfaces**: [Primary APIs or interfaces exposed]
**Technology Stack**: [Chosen technologies and frameworks]
**Team Ownership**: [Which team owns this system]

### Core Responsibilities
- [Responsibility 1: Specific capability]
- [Responsibility 2: Specific capability]
- [Responsibility 3: Specific capability]

### External Dependencies
- [External System 1: What data/services are consumed]
- [External System 2: What data/services are consumed]

### Scaling Characteristics
- **Expected Load**: [User volume, transaction volume]
- **Growth Pattern**: [How load is expected to grow]
- **Scaling Strategy**: [Horizontal/vertical scaling approach]
```

#### 3. Integration Architecture

##### Communication Patterns
```markdown
## Integration: [System A] ↔ [System B]
**Pattern**: Synchronous/Asynchronous/Event-driven
**Protocol**: REST/GraphQL/gRPC/Message Queue
**Data Format**: JSON/Protobuf/Avro
**Authentication**: API Key/OAuth/JWT/mTLS

### Use Cases
- [Use Case 1: When this integration is used]
- [Use Case 2: When this integration is used]

### Error Handling
- [How failures are detected and handled]
- [Retry policies and circuit breaker patterns]
- [Fallback mechanisms]

### Performance Requirements
- **Response Time**: [Target response time]
- **Throughput**: [Expected requests per second]
- **Availability**: [Required uptime percentage]
```

##### System Interaction Diagrams (Required)
Include sequence diagrams for key system interactions:

```mermaid
sequenceDiagram
    participant User
    participant Gateway as API Gateway
    participant Auth as Auth Service
    participant UserSvc as User Service
    participant DB as Database
    participant Cache
    
    User->>Gateway: POST /login
    Gateway->>Auth: Validate credentials
    Auth->>DB: Query user data
    DB-->>Auth: User record
    Auth->>Cache: Store session
    Auth-->>Gateway: JWT token
    Gateway-->>User: Authentication response
    
    User->>Gateway: GET /profile (with JWT)
    Gateway->>Auth: Validate token
    Auth->>Cache: Check session
    Cache-->>Auth: Session valid
    Auth-->>Gateway: User authorized
    Gateway->>UserSvc: Get user profile
    UserSvc->>DB: Query profile data
    DB-->>UserSvc: Profile data
    UserSvc-->>Gateway: Profile response
    Gateway-->>User: User profile
```

##### Data Flow Diagrams (Required)
Show how data moves through the system:

```mermaid
flowchart LR
    subgraph "Data Sources"
        UI[User Interface]
        API[External APIs]
        Files[File Uploads]
    end
    
    subgraph "Processing Layer"
        Validator[Data Validator]
        Transformer[Data Transformer]
        Enricher[Data Enricher]
    end
    
    subgraph "Storage Layer"
        Primary[(Primary DB)]
        Analytics[(Analytics DB)]
        Archive[(Archive Storage)]
    end
    
    subgraph "Output Layer"
        Reports[Reports]
        Notifications[Notifications]
        Export[Data Export]
    end
    
    UI --> Validator
    API --> Validator
    Files --> Validator
    
    Validator --> Transformer
    Transformer --> Enricher
    
    Enricher --> Primary
    Enricher --> Analytics
    Primary --> Archive
    
    Primary --> Reports
    Analytics --> Reports
    Primary --> Notifications
    Primary --> Export
```

##### Data Architecture
- **Data Ownership**: Which system owns which data entities
- **Data Consistency**: How consistency is maintained across systems
- **Data Synchronization**: How data updates are propagated
- **Master Data Management**: How shared reference data is managed

##### Entity Relationship Diagrams (Required)
Include ER diagrams showing key data relationships across systems:

```mermaid
erDiagram
    User {
        string id PK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    Profile {
        string id PK
        string user_id FK
        string first_name
        string last_name
        string phone
        datetime created_at
        datetime updated_at
    }
    
    Order {
        string id PK
        string user_id FK
        decimal total_amount
        string status
        datetime created_at
        datetime updated_at
    }
    
    OrderItem {
        string id PK
        string order_id FK
        string product_id FK
        integer quantity
        decimal unit_price
    }
    
    Product {
        string id PK
        string name
        string description
        decimal price
        integer stock_quantity
        boolean is_active
    }
    
    User ||--|| Profile : "has"
    User ||--o{ Order : "places"
    Order ||--o{ OrderItem : "contains"
    Product ||--o{ OrderItem : "included in"
```

##### System State Diagrams (Where Applicable)
For systems with complex state management, include state diagrams:

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted : submit()
    Submitted --> UnderReview : assign_reviewer()
    UnderReview --> Approved : approve()
    UnderReview --> Rejected : reject()
    UnderReview --> Draft : request_changes()
    Rejected --> Draft : revise()
    Approved --> Published : publish()
    Published --> Archived : archive()
    Archived --> [*]
    
    note right of UnderReview
        Reviewer can approve,
        reject, or request changes
    end note
```

#### 4. Technology Stack

##### Technology Selection Matrix
```markdown
| Component | Technology Choice | Rationale | Alternatives Considered |
|-----------|------------------|-----------|------------------------|
| Backend Language | [Language] | [Why chosen] | [What else was considered] |
| Database | [Database] | [Why chosen] | [What else was considered] |
| Message Queue | [Technology] | [Why chosen] | [What else was considered] |
| Frontend Framework | [Framework] | [Why chosen] | [What else was considered] |
| API Gateway | [Technology] | [Why chosen] | [What else was considered] |
```

##### Infrastructure Architecture
- **Deployment Model**: Cloud/On-premise/Hybrid
- **Container Strategy**: Docker, Kubernetes, serverless
- **Database Strategy**: SQL/NoSQL choices and rationale
- **Caching Strategy**: Redis, CDN, application-level caching
- **Monitoring and Observability**: Logging, metrics, tracing tools

#### 5. Security Architecture

##### Security Patterns
- **Authentication**: How users and services authenticate
- **Authorization**: How access control is implemented
- **Data Protection**: Encryption at rest and in transit
- **Network Security**: Firewalls, VPNs, network segmentation
- **Secrets Management**: How sensitive configuration is handled

##### Compliance Requirements
- **Regulatory Requirements**: GDPR, HIPAA, SOC2, etc.
- **Data Residency**: Where data can be stored and processed
- **Audit Requirements**: What events must be logged and retained
- **Security Controls**: Required security measures and validations

#### 6. Deployment and Operations

##### Environment Strategy
- **Development Environment**: Local development setup
- **Testing Environments**: Integration, staging, performance testing
- **Production Environment**: Production deployment and scaling
- **Disaster Recovery**: Backup and recovery procedures

##### Deployment Architecture (Required)
Include deployment diagrams showing infrastructure and environment organization:

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer"
            LB[Application Load Balancer]
        end
        
        subgraph "Application Tier"
            App1[App Server 1]
            App2[App Server 2]
            App3[App Server 3]
        end
        
        subgraph "Database Tier"
            Primary[(Primary DB)]
            Replica1[(Read Replica 1)]
            Replica2[(Read Replica 2)]
        end
        
        subgraph "Cache Tier"
            Redis1[(Redis Primary)]
            Redis2[(Redis Replica)]
        end
        
        subgraph "Storage"
            S3[File Storage]
        end
    end
    
    Internet --> LB
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> Primary
    App2 --> Primary
    App3 --> Primary
    
    App1 --> Replica1
    App2 --> Replica2
    App3 --> Replica1
    
    App1 --> Redis1
    App2 --> Redis1
    App3 --> Redis1
    
    Redis1 --> Redis2
    Primary --> Replica1
    Primary --> Replica2
    
    App1 --> S3
    App2 --> S3
    App3 --> S3
```

##### DevOps and CI/CD
- **Build Pipeline**: How code is built and tested
- **Deployment Pipeline**: How code is deployed to environments
- **Configuration Management**: How environment-specific config is managed
- **Monitoring and Alerting**: How system health is monitored

##### CI/CD Pipeline Diagram (Required)
Show the complete build and deployment pipeline:

```mermaid
flowchart LR
    subgraph "Development"
        Dev[Developer]
        Git[Git Repository]
    end
    
    subgraph "CI Pipeline"
        Trigger[Webhook Trigger]
        Build[Build & Test]
        Security[Security Scan]
        Package[Package Artifacts]
    end
    
    subgraph "CD Pipeline"
        Deploy_Dev[Deploy to Dev]
        Test_Int[Integration Tests]
        Deploy_Stage[Deploy to Staging]
        Test_E2E[E2E Tests]
        Approve[Manual Approval]
        Deploy_Prod[Deploy to Production]
    end
    
    subgraph "Monitoring"
        Health[Health Checks]
        Metrics[Metrics Collection]
        Alerts[Alerting]
    end
    
    Dev --> Git
    Git --> Trigger
    Trigger --> Build
    Build --> Security
    Security --> Package
    Package --> Deploy_Dev
    Deploy_Dev --> Test_Int
    Test_Int --> Deploy_Stage
    Deploy_Stage --> Test_E2E
    Test_E2E --> Approve
    Approve --> Deploy_Prod
    Deploy_Prod --> Health
    Health --> Metrics
    Metrics --> Alerts
```

### Diagram Requirements Summary

System Architecture documents must include the following **Mermaid diagrams**:

1. **System Context Diagram**: High-level view of system relationships and external entities
2. **High-Level Architecture Diagram**: Complete system overview with all major components
3. **System Interaction Diagrams**: Sequence diagrams for key workflows
4. **Data Flow Diagrams**: How data moves through the system
5. **Entity Relationship Diagrams**: Key data relationships across systems
6. **System State Diagrams**: For systems with complex state management
7. **Deployment Architecture Diagram**: Infrastructure and environment layout
8. **CI/CD Pipeline Diagram**: Build and deployment workflow

**Diagram Standards**:
- Use consistent naming conventions across all diagrams
- Include clear titles and legends
- Use appropriate Mermaid diagram types for different purposes
- Ensure diagrams are readable and not overly complex
- Update diagrams when architecture changes
- Place diagrams in relevant sections for context

### Step 4: Architecture Decision Records (ADRs)

For each significant architectural decision, create an ADR using this template:

#### ADR Template: `adr-[system]-[decision-topic].md`

```markdown
# ADR: [System] - [Decision Title]

**Status**: Proposed/Accepted/Superseded
**Date**: [YYYY-MM-DD]
**Decision Makers**: [Who made this decision]
**Consulted**: [Who was consulted]
**Informed**: [Who was informed]

## Context and Problem Statement

[Describe the architectural decision to be made, including:]
- [What is the issue we're trying to solve?]
- [What are the driving forces behind this decision?]
- [What constraints or requirements are influencing this choice?]

## Decision Drivers

- [Driver 1: e.g., performance requirements]
- [Driver 2: e.g., team expertise]
- [Driver 3: e.g., integration constraints]
- [Driver 4: e.g., budget limitations]

## Considered Options

### Option 1: [Option Name]
**Description**: [Brief description of this option]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Cost/Effort**: [Implementation cost and effort]

### Option 2: [Option Name]
[Same structure as Option 1]

### Option 3: [Option Name]
[Same structure as Option 1]

## Decision Outcome

**Chosen Option**: [Selected option name]

**Rationale**: [Explain why this option was chosen over the alternatives]

### Consequences

**Positive**:
- [Positive consequence 1]
- [Positive consequence 2]

**Negative**:
- [Negative consequence 1 and mitigation strategy]
- [Negative consequence 2 and mitigation strategy]

**Neutral**:
- [Neutral consequence 1]

## Implementation Notes

- [Implementation consideration 1]
- [Implementation consideration 2]
- [Timeline and milestones]

## Related Decisions

- [Link to related ADR 1]
- [Link to related ADR 2]

## Review Schedule

**Next Review**: [Date when this decision should be revisited]
**Review Criteria**: [What changes would trigger a review of this decision]
```

#### Common ADR Categories

1. **Technology Choices**
   - Programming languages and frameworks
   - Database technologies
   - Infrastructure and deployment platforms
   - Third-party service selections

2. **Architectural Patterns**
   - Microservices vs. monolith decisions
   - Communication patterns (sync vs. async)
   - Data consistency approaches
   - Security patterns and implementations

3. **Integration Decisions**
   - API design approaches (REST vs. GraphQL vs. gRPC)
   - Message queue and event streaming choices
   - Data sharing and synchronization strategies
   - External service integration patterns

### Step 5: Validation and Review Process

#### Architecture Review
1. **Technical Review**
   - Validate against non-functional requirements from PRDs
   - Ensure chosen technologies can meet performance requirements
   - Review integration complexity and failure modes
   - Assess scalability and operational characteristics

2. **Business Alignment Review**
   - Confirm architecture supports all PRD user stories
   - Validate that system boundaries align with business domains
   - Ensure integration patterns support business workflows
   - Review cost and timeline implications

3. **Risk Assessment**
   - Identify technical risks and mitigation strategies
   - Assess team capability gaps and training needs
   - Review dependency risks and alternatives
   - Evaluate operational complexity and support requirements

#### Stakeholder Approval
- **Technical stakeholders**: Architecture team, senior engineers
- **Business stakeholders**: Product owners, business sponsors
- **Operations stakeholders**: DevOps, security, compliance teams
- **Development stakeholders**: Engineering managers, tech leads

### Step 6: File Management and Maintenance

#### File Organization
**Monorepo Structure**:
```
docs/
├── system-architecture.md
└── architecture-decisions/
    ├── adr-auth-service-token-strategy.md
    ├── adr-data-service-database-choice.md
    └── adr-api-gateway-selection.md
```

**Polyrepo Structure**:
```
[project-name]-specs/
├── system-architecture.md
└── architecture-decisions/
    ├── adr-auth-service-token-strategy.md
    ├── adr-data-service-database-choice.md
    └── adr-api-gateway-selection.md
```

#### Version Control and Change Management
- All architecture documents under version control
- Link architecture versions to PRD versions
- Establish change approval process for architectural modifications
- Maintain ADR status (proposed → accepted → superseded)

## Quality Assurance

### Architecture Validation Checklist

- [ ] **Completeness**: All PRD requirements addressed by architecture
- [ ] **Consistency**: ADRs align with overall architectural principles
- [ ] **Feasibility**: Chosen technologies can meet requirements
- [ ] **Scalability**: Architecture can handle expected growth
- [ ] **Maintainability**: System boundaries enable independent development
- [ ] **Testability**: Architecture supports comprehensive testing strategies

### Common Architecture Anti-Patterns to Avoid

- **Distributed Monolith**: Systems too tightly coupled despite being separate
- **Chatty Interfaces**: Too many fine-grained service calls
- **Shared Database**: Multiple systems directly accessing same database
- **Technology Sprawl**: Too many different technologies without justification
- **Single Point of Failure**: Critical systems without redundancy

## Output to Next Phase

The completed system architecture and ADRs enable creation of:
- **System Requirements Documents (SRDs)**: Detailed requirements for each system
- **Implementation Planning**: Task breakdown and development sequencing
- **Team Formation**: System ownership and development responsibilities
- **Infrastructure Planning**: Environment setup and deployment strategies

This systematic approach ensures that the overall architecture is well-thought-out, documented, and ready to guide detailed system design and implementation.
