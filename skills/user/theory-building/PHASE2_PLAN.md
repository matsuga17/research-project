# Theory Building Skill - Phase 2 Plan

**Status:** Planned (Not Yet Implemented)  
**Estimated Completion:** TBD  
**Focus:** Qualitative data analysis and theory-data iteration

---

## Phase 2 Scope: Data Analysis Support

### What Phase 2 Will Add

Phase 1 covered **thinking about theory**.  
Phase 2 will cover **working with qualitative data**.

**Core Additions:**
1. Qualitative Data Coding Support
2. Within-Case & Cross-Case Analysis
3. Data-Theory Iteration Cycles
4. Literature Enfolding Protocols
5. Theoretical Saturation Detection

---

## Module 1: Qualitative Data Coding

### 1.1 First-Order Coding (In Vivo Codes)

**What Claude Will Support:**
```
User uploads: Interview transcript, field notes, archival data

Claude assists with:
├─ Open coding guidance
│  ├─ "What are the participant's own words?"
│  ├─ "What recurring phrases appear?"
│  └─ "What surprised you in this data?"
│
├─ In vivo code extraction
│  ├─ Highlight verbatim terms
│  ├─ Preserve informant voice
│  └─ Avoid premature theorizing
│
└─ Initial pattern spotting
   ├─ "These 5 codes seem related"
   ├─ "This code appears in 8/15 interviews"
   └─ "Contradictions between codes X and Y"
```

**Example Interaction:**
```
User: [Uploads 50-page transcript]
      "Help me start coding this interview with CEO about AI adoption."

Claude: "Let's begin with open coding. I'll read through and suggest 
initial codes based on the CEO's own language.

📋 SUGGESTED IN VIVO CODES (First 10 pages):

1. 'fear of being left behind' (p.2, p.5, p.7)
   → Appears 3x, seems central to motivation
   
2. 'lack of clear ROI' (p.3, p.8)
   → Barrier to adoption
   
3. 'champions in the middle' (p.4, p.6, p.9)
   → Refers to mid-level managers driving change

[continues...]

PATTERNS EMERGING:
- Strong emotional language around competitive pressure
- Technical concerns secondary to organizational dynamics
- Middle management more important than expected

What stands out to YOU as most surprising or important?"
```

### 1.2 Second-Order Theming

**What Claude Will Support:**
```
Input: First-order codes from multiple sources

Claude facilitates:
├─ Grouping codes into themes
│  ├─ "Codes 1, 3, 7 share what common concept?"
│  ├─ "What theoretical construct explains these?"
│  └─ "Is this theme distinct from existing constructs?"
│
├─ Moving from descriptive to conceptual
│  ├─ In vivo: "champions in the middle"
│  └─ Theme: "Distributed change agency"
│
└─ Ensuring theoretical grounding
   ├─ "This theme aligns with [existing theory]"
   ├─ "This theme extends [existing theory]"
   └─ "This theme contradicts [existing theory]"
```

### 1.3 Aggregate Dimensions

**What Claude Will Support:**
```
Input: Second-order themes

Claude helps create:
├─ Overarching theoretical dimensions
├─ Relationship mapping between dimensions
└─ Connection to research questions
```

### 1.4 Gioia Data Structure

**What Claude Will Support:**
```
Generate Gioia-style diagram:

1st Order Concepts    2nd Order Themes    Aggregate Dimensions
(Informant terms)     (Researcher terms)  (Theoretical)

"fear of rivals"  ┐
"need to keep up"  ├─→ Competitive   ┐
"pressure from    ┘    Anxiety       │
 board"                              ├─→ Extrinsic
                                     │   Motivation
"unclear benefits"┐                  │
"no proven ROI"   ├─→ Uncertainty   ┘
"risky investment"┘    about Value

[Claude generates text-based or suggests visualization tools]
```

---

## Module 2: Case Analysis Techniques

### 2.1 Within-Case Analysis

**What Claude Will Support:**

**A. Temporal Bracketing**
```
Claude helps:
├─ Identify critical phases
├─ Mark phase transitions
├─ Analyze phase-specific mechanisms
└─ Compare across phases

Example:
"Your company's AI adoption has 3 phases:
Phase 1 (Jan-Mar): Pilot with IT team
Phase 2 (Apr-Jun): Expansion to marketing
Phase 3 (Jul-Sep): Enterprise-wide rollout

Let's analyze what differed between phases..."
```

**B. Narrative Construction**
```
Claude facilitates:
├─ Chronological story assembly
├─ Critical event identification
├─ Causal linkage between events
└─ Alternative narrative testing

"You've described 8 events. Let me test 3 causal narratives:

Narrative 1: Top-down diffusion
Event 1 (CEO mandate) → Event 3 (dept. adoption) → Event 7 (success)

Narrative 2: Bottom-up emergence  
Event 2 (developer experiment) → Event 5 (viral spread) → Event 7

Narrative 3: Middle-out
Event 4 (mid-manager advocacy) → Event 6 (cross-dept) → Event 7

Which narrative best fits your full data?"
```

**C. Visual Mapping**
```
Claude suggests:
├─ Process diagrams
├─ Event sequence charts
├─ Actor-network maps
└─ Timeline visualizations
```

### 2.2 Cross-Case Analysis

**What Claude Will Support:**

**A. Pair-Wise Comparison**
```
Claude structures:

Case A vs Case B
├─ Similarities
│  ├─ Both had CEO support
│  ├─ Both in tech industry
│  └─ Both used ChatGPT
│
├─ Differences
│  ├─ A had training, B did not
│  ├─ A succeeded, B failed
│  └─ A had 200 employees, B had 5000
│
└─ Inference
   "Training may matter, but size also differs.
    Need Case C (small, no training) to isolate effect."
```

**B. Dimension Listing**
```
Claude creates comparison matrix:

|        | Training | Size | Success | Culture | Leadership |
|--------|----------|------|---------|---------|------------|
| Case A | Yes      | Small| Yes     | Open    | Transf.    |
| Case B | No       | Large| No      | Hier.   | Transact.  |
| Case C | No       | Small| Yes     | Open    | Transf.    |
| Case D | Yes      | Large| No      | Hier.   | Transf.    |

"Pattern: Success correlates with 'Open culture' (4/4 matches),
not with 'Training' (2 Yes succeed, 2 No succeed).
Culture may be the key variable."
```

**C. Replication Logic**
```
Claude applies:
├─ Literal replication: Similar cases, similar outcomes?
├─ Theoretical replication: Different conditions, different outcomes?
└─ Disconfirming cases: Where does theory fail?
```

---

## Module 3: Data-Theory Iteration

### 3.1 Iterative Cycle Framework

**What Claude Will Facilitate:**

**Cycle 1: Initial Pattern Recognition**
```
Input: Raw data (first 3-5 cases)

Claude guides:
1. "What patterns jump out?"
2. "Generate 3-5 preliminary propositions"
3. "What would disconfirm each proposition?"
4. "Which cases should you analyze next?" (theoretical sampling)
```

**Cycle 2: Pattern Refinement**
```
Input: Additional cases (next 5-7)

Claude probes:
1. "Do propositions still hold?"
2. "What exceptions appeared?"
3. "Revise propositions or add contingencies?"
4. "What new patterns emerged?"
```

**Cycle 3: Theoretical Saturation**
```
Input: Final cases (last 3-5)

Claude checks:
1. "Are new patterns still emerging?" 
   - If yes: Continue sampling
   - If no: Approaching saturation
   
2. "Do you understand all major variations?"
3. "Are boundary conditions clear?"
4. "Can you explain all anomalies?"

When 3-4 consecutive cases add no new insights → Saturation
```

### 3.2 When to Stop Iterating

**Claude Will Assess:**
```
Theoretical Saturation Indicators:
├─ No new codes emerging from new data
├─ All relationships between categories understood
├─ All variations of main categories explained
├─ Core categories well-developed and validated
└─ Researcher confident in understanding

Claude asks:
"Saturation check:
- Last 3 cases added how many new codes? [If <3, likely saturated]
- Can you explain Case X's deviation from pattern? [If yes, good]
- If I gave you one more case, what could it change? [If 'nothing major', saturated]"
```

---

## Module 4: Literature Enfolding

### 4.1 Conflicting Literature Analysis

**What Claude Will Support:**
```
Your Finding: X causes Y

Conflicting Literature: Smith (2020) found Y causes X

Claude facilitates:
├─ Mechanism-level comparison
│  ├─ "What mechanism did Smith propose?"
│  ├─ "How does it differ from yours?"
│  └─ "Are they testing same construct?"
│
├─ Boundary condition comparison
│  ├─ "Smith studied large firms, you studied small"
│  ├─ "Could this explain contradiction?"
│  └─ "Contingency model: X→Y in small firms, Y→X in large?"
│
└─ Measurement differences
   ├─ "How did Smith operationalize X?"
   ├─ "How did you operationalize X?"
   └─ "Are you measuring same thing?"
```

### 4.2 Similar Literature Integration

**What Claude Will Support:**
```
Your Finding: [Your theory]

Similar Literature: Jones (2019) found related pattern

Claude probes:
├─ "Is your finding extension or replication?"
├─ "What does your study add?"
├─ "New context? New mechanism? New moderator?"
└─ "How do theories integrate?"
```

### 4.3 Contribution Statement

**What Claude Will Help Formulate:**
```
1. CHALLENGE: What assumption is questioned?
   "Previous research assumed [X]. We show [Y]."

2. EXTEND: What boundary is pushed?
   "Theory A works in context B. We extend to context C."

3. SYNTHESIZE: What is integrated?
   "We integrate theories A and B through mechanism C."

4. CONSTRUCT: What is newly conceptualized?
   "We introduce construct X, distinct from Y and Z."

5. MECHANISM: What process is revealed?
   "We open black box of X→Y by showing [steps]."
```

---

## Module 5: Writing Support (Future Extension)

**Potential Phase 2.5 or 3:**
- Theory section drafting
- Proposition formulation
- Data structure table generation
- Figure/diagram creation
- Quotation selection and presentation

---

## Implementation Roadmap

### Development Stages

**Stage 1: Core Coding Support (Est. 400 lines)**
- 1st order coding
- 2nd order theming
- Aggregate dimensions

**Stage 2: Case Analysis (Est. 400 lines)**
- Within-case techniques
- Cross-case comparison
- Pattern recognition

**Stage 3: Iteration Support (Est. 300 lines)**
- Theory-data cycling
- Saturation detection
- Theoretical sampling guidance

**Stage 4: Literature Enfolding (Est. 300 lines)**
- Conflicting literature analysis
- Similar literature integration
- Contribution statement

**Total Estimated:** ~1400 additional lines for Phase 2

### Dependencies

**Before Starting Phase 2:**
1. Validate Phase 1 with actual users
2. Collect example dialogues for coding support
3. Gather sample Gioia diagrams
4. Test saturation detection logic

### Success Metrics

**Phase 2 Will Be Successful If:**
- Users can code data with Claude's support
- Cross-case patterns are systematically identified
- Theoretical saturation is reached efficiently
- Literature is enfolded rigorously
- Users produce publication-quality theory sections

---

## Questions for Future Design

### Open Decisions

1. **Automation Level:**
   - Should Claude auto-generate codes or only suggest?
   - Should Claude create Gioia diagrams or guide users?

2. **Data Input:**
   - How much transcript can Claude handle at once?
   - Should coding be iterative (chunk by chunk)?

3. **Integration:**
   - Should Phase 2 be separate SKILL or extend Phase 1?
   - How to maintain coherence across phases?

4. **Tool Support:**
   - Recommend ATLAS.ti, NVivo, or manual coding?
   - Generate exportable formats?

---

## Preliminary Structure

### SKILL.md (Phase 2) - Proposed Sections

```markdown
# Theory Building: Data Analysis Support (Phase 2)

## When to Use This Skill
[Triggers: Data coding, case analysis, saturation questions]

## Qualitative Coding Support
### 1st Order Coding Protocol
### 2nd Order Theming Protocol
### Aggregate Dimension Development
### Gioia Data Structure Generation

## Case Analysis Techniques
### Within-Case Analysis
├─ Temporal bracketing
├─ Narrative construction
└─ Visual mapping

### Cross-Case Analysis
├─ Pair-wise comparison
├─ Dimension listing
└─ Replication logic

## Data-Theory Iteration
### Cycle 1: Initial Patterns
### Cycle 2: Refinement
### Cycle 3: Saturation
### Stopping Rules

## Literature Enfolding
### Conflicting Literature Protocol
### Similar Literature Integration
### Contribution Statement Development

## Quality Assurance
### Coding Rigor Checks
### Saturation Validation
### Triangulation Assessment

## Examples
[10-15 detailed dialogue examples]
```

---

## Next Steps

1. **Validate Phase 1** with users
2. **Collect feedback** on most-needed Phase 2 features
3. **Prioritize modules** based on user needs
4. **Develop prototype** of highest-priority module
5. **Test iteratively** with real data
6. **Refine and expand** based on usage

---

**Document Status:** Planning  
**Estimated Start:** After Phase 1 validation  
**Estimated Completion:** 4-6 weeks after start
