---
description: Workflow for creating comprehensive Business Requirements Documents (BRDs) as the foundation of spec-driven development
applyTo: "**/docs/**/business-requirements.md,**/brd*.md"
---

# Business Requirements Document (BRD) Creation Workflow

## Overview

The Business Requirements Document (BRD) is the **foundational document** in spec-driven development that captures business objectives, stakeholder needs, and high-level requirements. It serves as the root from which all other specification documents flow.

**Position in Spec-Driven Flow**: **BRD** → PRDs with User Stories → System Architecture (with ADRs) → SRDs → Implementation Tasks

## Prerequisites

Before creating a BRD, gather:
- ✅ **Business stakeholder input** and executive sponsor alignment
- ✅ **Market research** and competitive analysis (if applicable)
- ✅ **User research** and persona definitions (if user-facing)
- ✅ **Technical constraints** and existing system inventory
- ✅ **Budget and timeline** parameters

## Process

### Step 1: Business Context and Problem Analysis

1. **Define the Business Problem**
   - What specific business challenge are we addressing?
   - What is the current state that needs improvement?
   - What are the consequences of not solving this problem?
   - How does this align with overall business strategy?

2. **Identify Stakeholders**
   - **Primary stakeholders**: Those directly impacted by the solution
   - **Secondary stakeholders**: Those indirectly affected or with influence
   - **Decision makers**: Those with approval authority
   - **Users**: Those who will interact with the solution

3. **Establish Business Context**
   - Market conditions and competitive landscape
   - Regulatory requirements and compliance needs
   - Organizational goals and strategic initiatives
   - Budget constraints and resource availability

### Step 2: Business Requirements Gathering

Conduct structured interviews and workshops to understand:

- **Business Objectives**: What business outcomes are expected?
- **Success Criteria**: How will success be measured?
- **Functional Needs**: What capabilities must the solution provide?
- **Business Rules**: What constraints and policies must be enforced?
- **Performance Expectations**: What are the scalability and reliability needs?
- **Integration Requirements**: How does this connect to existing systems?
- **Timeline Constraints**: What are the critical delivery milestones?

### Step 3: BRD Structure (Standardized Template)

Create a comprehensive BRD with these **required sections**:

#### 1. Executive Summary
- **Project Name**: Clear, descriptive project identifier
- **Business Sponsor**: Executive sponsor and primary stakeholder
- **Project Vision**: High-level description of desired future state
- **Business Value**: Expected return on investment and key benefits
- **Timeline**: High-level milestones and delivery expectations

#### 2. Business Context
- **Background**: Current situation and history leading to this need
- **Market Context**: Competitive landscape and market drivers
- **Strategic Alignment**: How this supports broader business strategy
- **Risk Factors**: Key business risks if project is not completed

#### 3. Business Objectives
- **Primary Goals**: Core business outcomes expected
- **Secondary Goals**: Additional benefits anticipated
- **Success Metrics**: Quantifiable measures of success
- **Assumptions**: Critical assumptions about market, users, or technology

#### 4. Stakeholder Analysis
```markdown
| Stakeholder Type | Names/Roles | Interests | Influence Level | Engagement Strategy |
|------------------|-------------|-----------|-----------------|-------------------|
| Executive Sponsor | [Name, Title] | [Key interests] | High | [How to engage] |
| Business Users | [User groups] | [User needs] | Medium | [Engagement plan] |
| IT Operations | [Teams] | [Operational concerns] | Medium | [Collaboration approach] |
```

#### 5. Business Requirements

##### Functional Requirements
- **Core Capabilities**: What the solution must be able to do
- **Business Processes**: Workflows that must be supported
- **Data Requirements**: Information that must be captured, processed, or reported
- **User Interactions**: High-level user experience expectations
- **Integration Points**: External systems that must connect

##### Non-Functional Requirements
- **Performance**: Expected response times, throughput, concurrent users
- **Availability**: Uptime requirements and acceptable downtime windows
- **Security**: Data protection, access control, and compliance requirements
- **Scalability**: Expected growth in users, data, or transaction volume
- **Usability**: User experience standards and accessibility requirements

#### 6. Business Rules and Constraints
- **Business Logic**: Rules that govern how the solution should behave
- **Regulatory Requirements**: Compliance obligations and industry standards
- **Technical Constraints**: Existing technology limitations or requirements
- **Budget Constraints**: Financial limitations and spending guidelines
- **Timeline Constraints**: Critical dates and delivery requirements

#### 7. Success Criteria and Metrics
- **Key Performance Indicators (KPIs)**: Measurable business outcomes
- **Return on Investment (ROI)**: Expected financial benefits
- **Quality Metrics**: Standards for solution quality and user satisfaction
- **Acceptance Criteria**: Conditions that must be met for project acceptance

#### 8. Risks and Assumptions
- **Business Risks**: Potential threats to project success
- **Technical Risks**: Technology-related challenges and uncertainties
- **Market Risks**: External factors that could impact the solution
- **Assumptions**: What we're assuming to be true (and risks if wrong)
- **Mitigation Strategies**: Plans for addressing identified risks

#### 9. Project Scope and Boundaries
- **In Scope**: What is explicitly included in this project
- **Out of Scope**: What is explicitly excluded
- **Future Considerations**: Potential enhancements for later phases
- **Dependencies**: External projects or initiatives that impact this work

#### 10. Approval and Sign-off
- **Approval Authority**: Who must approve this BRD
- **Review Process**: How stakeholder feedback will be incorporated
- **Change Management**: How requirement changes will be handled
- **Documentation Control**: Version control and distribution strategy

### Step 4: Validation and Approval Process

1. **Internal Review**
   - Technical feasibility assessment
   - Budget and resource validation
   - Timeline reality check
   - Risk assessment review

2. **Stakeholder Validation**
   - Business stakeholder review sessions
   - User representative feedback
   - IT team technical review
   - Executive sponsor approval

3. **Final Approval**
   - Formal sign-off from decision makers
   - Baseline document establishment
   - Change control process activation

### Step 5: File Management and Distribution

#### File Naming and Location
- **File name**: `business-requirements.md`
- **Monorepo location**: `/docs/business-requirements.md`
- **Polyrepo location**: `[project-name]-specs/business-requirements.md`

#### Version Control and Distribution
- All BRDs must be under version control
- Establish change approval process
- Maintain stakeholder distribution list
- Regular review and update schedule

## Quality Assurance

### BRD Validation Checklist

- [ ] **Completeness**: All required sections are thoroughly documented
- [ ] **Clarity**: Requirements are unambiguous and testable
- [ ] **Alignment**: Business objectives align with organizational strategy
- [ ] **Feasibility**: Requirements are achievable within stated constraints
- [ ] **Traceability**: Success criteria are measurable and specific
- [ ] **Stakeholder Buy-in**: All key stakeholders have reviewed and approved

### Common Issues to Avoid

- **Scope creep**: Clearly define boundaries and stick to them
- **Unrealistic expectations**: Ensure timeline and budget are achievable
- **Vague requirements**: Be specific about what success looks like
- **Missing stakeholders**: Include all affected parties in the process
- **Insufficient detail**: Provide enough detail for architectural decisions

## Integration with Spec-Driven Development

### Output Artifacts
The approved BRD enables creation of:
- **Product Requirements Documents (PRDs)**: Feature-specific requirements
- **System Architecture**: High-level system design decisions
- **Architecture Decision Records (ADRs)**: Specific architectural choices
- **System Requirements Documents (SRDs)**: Detailed technical requirements

### Ongoing Role
Throughout the project lifecycle:
- **Reference point**: All downstream decisions should trace back to BRD
- **Change authority**: Changes to BRD trigger review of all dependent documents
- **Success validation**: Final solution must meet BRD success criteria
- **Stakeholder communication**: BRD serves as primary stakeholder communication tool

This systematic approach to BRD creation ensures that all subsequent specification documents are grounded in clear business value and stakeholder alignment.
