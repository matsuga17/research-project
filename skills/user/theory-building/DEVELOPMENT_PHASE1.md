# Theory Building Skill - Phase 1 Development Instructions

**Status:** Completed  
**Date:** 2025-11-17  
**Focus:** Core theory building logic and reasoning

---

## Overview

This document explains the development rationale and structure of the Theory Building Skill (Phase 1).

### What This Phase Covers

**Core Theory Building:**
- Competing hypotheses generation
- Dialectical integration of theories
- Socratic questioning for depth
- Bias detection and mitigation
- Boundary condition specification

**Philosophy & Methodology:**
- Critical realism ontology
- Abductive reasoning
- Eisenhardt (1989) framework
- Gioia et al. (2013) principles

---

## Analysis of Original Material

### Problems Identified

**Original Document:** "探索的理論構築研究スキル実装プラン"

**Issues:**
1. **Target Misalignment:** Researcher's 6-11 month learning plan, not Claude support skill
2. **Perspective Inversion:** "Humans learning tools" vs "Claude supporting humans"
3. **Time Scale Mismatch:** Long-term roadmap vs per-session dialogue support
4. **Focus Imbalance:** 80% tool operations, 20% theoretical thinking
5. **Structure Absence:** Missing standard SKILL.md sections

### Corrected Approach

**Claude's Role:**
- Generate multiple competing hypotheses
- Detect cognitive biases
- Facilitate dialectical integration
- Drive deeper through Socratic dialogue
- Clarify boundary conditions

**NOT Claude's Role:**
- Replace researcher's judgment
- Conduct fieldwork/data collection
- Make final theoretical decisions
- Write the paper itself

---

## SKILL.md Architecture (Phase 1)

### Design Principles

1. **Executable:** Claude can read and act on it immediately
2. **Concise:** ~800 lines (not overwhelming)
3. **Structured:** Standard SKILL.md format
4. **Practical:** Rich with dialogue examples
5. **Rigorous:** Grounded in established methodology

### Section Breakdown

```
SKILL.md (820 lines)
├── When to Use (50 lines)
│   └── Auto-trigger conditions
├── Philosophical Foundation (50 lines)
│   ├── Critical realism
│   ├── Interpretive epistemology
│   └── Abductive logic
├── Core Capabilities (300 lines)
│   ├── 1. Competing Hypotheses Generation
│   ├── 2. Dialectical Integration
│   ├── 3. Socratic Questioning
│   ├── 4. Bias Detection
│   └── 5. Boundary Specification
├── Theoretical Foundations (100 lines)
│   ├── Methodological literature
│   └── Key theoretical lenses
├── Interaction Patterns (200 lines)
│   ├── Pattern 1: Initial exploration
│   ├── Pattern 2: Anomaly-driven refinement
│   └── Pattern 3: Construct development
├── Quality Assurance (100 lines)
│   ├── Theoretical rigor checklist
│   └── Anti-hallucination protocol
└── Critical Reminders (20 lines)
    ├── DO/DON'T lists
    └── Always principles
```

---

## Key Implementation Decisions

### 1. Five Core Capabilities

**Why These Five:**
- **Competing Hypotheses:** Prevents single-theory fixation
- **Dialectical Integration:** Resolves theoretical tensions
- **Socratic Questioning:** Drives depth (Level 3-5 thinking)
- **Bias Detection:** Ensures scientific rigor
- **Boundary Conditions:** Clarifies scope and testability

**Why Not More:**
- Keeps cognitive load manageable
- Each capability is richly specified
- Additional capabilities in Phase 2

### 2. Socratic Question Hierarchy

**5 Levels (Not 3 or 7):**
1. Descriptive: What happened?
2. Explanatory: Why happened?
3. **Mechanistic:** How did it happen? ← Core focus
4. Contingent: When does it work?
5. Theoretical: What does it mean?

**Critical Rule:** Never stay at Level 1-2, always push to 3-5.

This hierarchy guides Claude to drive conversations deeper automatically.

### 3. Six Biases (Not More)

**Selected Biases:**
1. Confirmation bias (most common)
2. Availability heuristic (recency/salience)
3. Anchoring (initial theory fixation)
4. HARKing (post-hoc hypothesizing)
5. Theory-induced blindness (missing data)
6. Narrative fallacy (storytelling without mechanism)

**Why These Six:**
- Most prevalent in theory building
- Detectable in dialogue
- Actionable mitigations exist
- Cover cognitive, motivational, and methodological biases

### 4. Theoretical Lenses

**Five Core Lenses Always Considered:**
1. Resource-Based View (RBV)
2. Transaction Cost Economics (TCE)
3. Institutional Theory
4. Dynamic Capabilities
5. Social Network Theory

**Plus Context-Specific Theories:**
- Added based on research domain
- User's theoretical background
- Phenomenon characteristics

### 5. Integration Patterns

**Three Primary Patterns:**
- **Temporal:** Stage models (theory changes over time)
- **Conditional:** Contingency models (context determines which theory)
- **Mechanistic:** Parallel mechanisms (multiple pathways coexist)

These cover 90% of integration scenarios in strategy/organization research.

---

## What's Deferred to Phase 2

### Data Analysis Support (Not in Phase 1)

**Phase 2 Will Add:**
1. **Qualitative Coding:**
   - 1st order concepts (in vivo codes)
   - 2nd order themes
   - Aggregate dimensions
   - Gioia data structure diagrams

2. **Case Analysis:**
   - Within-case analysis (temporal bracketing, narrative construction)
   - Cross-case analysis (pair-wise comparison, replication logic)
   - Pattern recognition techniques

3. **Literature Enfolding:**
   - Systematic comparison with conflicting literature
   - Integration with similar literature
   - Contribution statement development

4. **Data-Theory Iteration:**
   - Cycle 1: Initial patterns
   - Cycle 2: Refinement
   - Cycle 3: Saturation
   - When to stop iterating

**Rationale for Deferral:**
- Phase 1 focuses on **thinking** about theory
- Phase 2 focuses on **working with** qualitative data
- Separation prevents cognitive overload
- Allows specialized depth in each phase

---

## Usage Guidelines

### For Researchers

**When to Use This Skill:**
- Observed puzzling phenomenon
- Existing theories don't fit
- Need to generate alternative explanations
- Struggling with theoretical integration
- Want rigorous theory development

**How to Engage:**
- Have 15-30 exchange dialogues
- Provide concrete examples from research
- Accept challenges to assumptions
- Don't rush theoretical saturation
- Iterate as theory evolves

### For Skill Developers

**To Extend This Skill:**
1. Add domain-specific theoretical lenses
2. Include field-specific biases
3. Add exemplar dialogues from your domain
4. Integrate with data analysis tools (Phase 2)

**To Maintain Quality:**
- Test with actual PhD students
- Collect dialogue examples
- Refine question templates
- Update theoretical foundations as methodology evolves

---

## Validation Criteria

### How to Know This Skill Works

**Process Indicators:**
1. Claude automatically activates on theory-building queries
2. Multiple competing hypotheses generated (not single explanation)
3. Biases flagged explicitly when detected
4. Questions progress from Level 1 to Level 3-5
5. Boundary conditions articulated for propositions

**Outcome Indicators:**
1. User develops more rigorous theories
2. Theories are falsifiable and testable
3. Mechanisms are explicit, not black boxes
4. Alternative explanations considered
5. Anomalies treated as opportunities, not problems

**Quality Checks:**
- Does theory meet Eisenhardt (1989) criteria?
- Would Gioia et al. (2013) approve the rigor?
- Are constructs valid and distinct?
- Are boundary conditions clear?
- Is theoretical contribution evident?

---

## Known Limitations

### Phase 1 Cannot:
- Code qualitative data for you
- Create Gioia diagrams automatically
- Conduct systematic literature reviews
- Write theory sections of papers
- Replace expert theoretical judgment

### What It Can Do:
- Guide theoretical thinking process
- Generate multiple perspectives
- Challenge assumptions systematically
- Ensure methodological rigor
- Facilitate deeper inquiry

---

## Version History

**Version 1.0 (2025-11-17):**
- Initial release
- Five core capabilities implemented
- 800-line SKILL.md created
- Focused on core theory building logic
- Data analysis deferred to Phase 2

**Planned Version 2.0 (Phase 2):**
- Add qualitative data coding support
- Within-case and cross-case analysis
- Literature enfolding protocols
- Data-theory iteration cycles
- Estimated: +1000-1500 lines

---

## References

### Foundational Methodology
- Eisenhardt, K. M. (1989). Building theories from case study research. Academy of Management Review, 14(4), 532-550.
- Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive research. Organizational Research Methods, 16(1), 15-31.
- Glaser, B. G., & Strauss, A. L. (1967). The discovery of grounded theory. Aldine.
- Gehman, J., Glaser, V. L., Eisenhardt, K. M., Gioia, D., Langley, A., & Corley, K. G. (2018). Finding theory–method fit: A comparison of three qualitative approaches to theory building. Journal of Management Inquiry, 27(3), 284-300.

### Theoretical Foundations
- Barney, J. (1991). Firm resources and sustained competitive advantage. Journal of Management, 17(1), 99-120. [RBV]
- Williamson, O. E. (1985). The economic institutions of capitalism. Free Press. [TCE]
- DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited. American Sociological Review, 48(2), 147-160. [Institutional Theory]
- Teece, D. J. (2007). Explicating dynamic capabilities. Strategic Management Journal, 28(13), 1319-1350. [Dynamic Capabilities]

---

**Document Status:** Complete  
**Next Action:** Implement Phase 2 after Phase 1 validation
