---
name: project-planner
description: Comprehensive project planning and documentation generator for software projects. Creates structured requirements documents, system design documents, and task breakdown plans with implementation tracking. Use when starting a new project, defining specifications, creating technical designs, or breaking down complex systems into implementable tasks. Supports user story format, acceptance criteria, component design, API specifications, and hierarchical task decomposition with requirement traceability.
---

# Project Planner Skill

This skill provides templates and guidance for generating comprehensive project planning documents that serve as blueprints for AI-assisted implementation.

## Quick Start

When a user wants to start a new project, generate three core documents:
1. **Requirements Document** - User stories with acceptance criteria
2. **Design Document** - Technical architecture and component specifications  
3. **Implementation Plan** - Hierarchical task breakdown with requirement tracing

## Why Explicit Architectural Planning Works

Setting clear roles, responsibilities, and deliverables upfront dramatically improves project outcomes:

### Benefits of Upfront Definition

1. **Component Clarity** - Defining all system components first prevents scope creep and ensures complete coverage
2. **Data Flow Visibility** - Mapping data movement early reveals integration complexities and performance bottlenecks
3. **Integration Planning** - Identifying all touchpoints upfront prevents surprise dependencies during implementation
4. **Clear Boundaries** - Explicitly stating what's in/out of scope focuses effort and prevents feature drift
5. **Measurable Success** - Specific goals and constraints enable objective progress tracking

### The Architect Mindset

When acting as a **Project Architect**, approach planning with:
- **Systems Thinking** - See the whole before diving into parts
- **Interface-First Design** - Define contracts between components before internals
- **Traceability Focus** - Every requirement maps to design elements and tasks
- **Constraint Awareness** - Acknowledge limitations upfront to guide decisions
- **Deliverable Orientation** - Know exactly what artifacts you're producing

## Document Generation Workflow

### 1. Project Architect Role Definition

When starting a project, explicitly establish Claude as the **Project Architect** with clear responsibilities:

**Role:** System Architect and Planning Specialist
**Responsibilities:**
- Define complete system architecture with all components
- Map data flow between system elements
- Identify all integration points and interfaces
- Establish clear project boundaries and constraints
- Create traceable requirements to implementation tasks

### 2. Initial Project Understanding

Before generating documents, gather key information and architectural elements:

```
Required Project Information:
- Project name and purpose
- Target users (single-user local, multi-tenant SaaS, etc.)
- Core functionality (3-5 main features)
- Technical preferences (languages, frameworks, deployment)
- Non-functional requirements (performance, security, scalability)

Required Architectural Elements (define upfront):
- System Components: All major modules/services and their purposes
- Data Flow: How data moves through the entire system
- Integration Points: All external APIs, services, databases
- System Boundaries: What's in scope vs out of scope
- Constraints: Technical, business, and resource limitations
- Success Metrics: Clear, measurable goals for the system
```

## Requirements Document Template

```markdown
# Requirements Document

## Introduction
[System description in 2-3 sentences. Target user and deployment model.]

## Glossary
- **Term**: Definition specific to this system

## Requirements

### Requirement [NUMBER]
**User Story:** As a [user type], I want [capability], so that [benefit]

#### Acceptance Criteria
1. WHEN [trigger/condition], THE [component] SHALL [action/behavior]
2. WHERE [mode/context], THE [component] SHALL [action/behavior]  
3. IF [condition], THEN THE [component] SHALL [action/behavior]
```

## Design Document Template

```markdown
# Design Document

## Overview
[System architecture summary in 3-4 sentences.]

## System Architecture

### Component Map
| Component ID | Name | Type | Responsibility |
|-------------|------|------|----------------|
| COMP-1 | Web Frontend | UI | User interface |

## Data Flow Specifications
[Data movement between components]

## Integration Points
[External and internal integration specifications]
```

## Implementation Plan Template

```markdown
# Implementation Plan

- [x] 1. [Phase Name]
  - [x] 1.1 [Task name]
    - [Subtask description]
    - _Requirements: [REQ-X.Y]_
    
  - [ ] 1.2 [Task name]
    - [Subtask description]
    - _Dependencies: Task 1.1_
```

## Quality Checklist

### Requirements Document
- [ ] Every requirement has a clear user story
- [ ] All acceptance criteria are testable
- [ ] Requirements are numbered for tracing

### Design Document
- [ ] Architecture diagram included
- [ ] All components have clear responsibilities
- [ ] Performance targets specified

### Implementation Plan
- [ ] Tasks grouped into logical phases
- [ ] Dependencies identified between tasks
- [ ] Requirements traced to tasks

## Output Format

Generate documents in Markdown format:
- `requirements.md` - Requirements document
- `design.md` - Design document
- `tasks.md` - Implementation plan
