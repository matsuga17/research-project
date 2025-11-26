# Theory Building Support Skill

**Status:** Phase 1 Complete, Phase 2 Planned  
**Version:** 1.0  
**Created:** 2025-11-17  
**Author:** Changu (Strategic Management & Organization Theory Researcher)

---

## 📚 Overview

This skill enables Claude to support **exploratory theory building** in strategic management and organization theory research. It guides researchers through rigorous theory construction using established methodologies (Eisenhardt 1989, Gioia et al. 2013).

### What This Skill Does

**Claude becomes your theory-building partner:**
- Generates multiple competing hypotheses (prevents single-theory fixation)
- Facilitates dialectical integration of contradictory theories
- Drives deeper inquiry through Socratic questioning
- Detects and mitigates cognitive biases
- Clarifies boundary conditions and scope statements

**Grounded in:**
- Critical realism (ontology)
- Abductive reasoning (logic)
- Eisenhardt's case study methodology
- Gioia's qualitative rigor framework

---

## 📁 File Structure

```
theory-building/
├── README.md                    ← You are here
├── SKILL.md                     ← Phase 1 executable (820 lines)
├── DEVELOPMENT_PHASE1.md        ← Phase 1 design rationale
└── PHASE2_PLAN.md              ← Phase 2 future plans
```

### File Descriptions

**SKILL.md** (Phase 1 - Complete)
- The actual file Claude reads and executes
- 820 lines of actionable theory-building support
- Covers: Hypotheses generation, integration, questioning, bias detection
- **Use this file** to activate the skill

**DEVELOPMENT_PHASE1.md**
- Development documentation for Phase 1
- Explains design decisions and rationale
- For skill developers and maintainers

**PHASE2_PLAN.md**
- Planned features for Phase 2
- Focus: Qualitative data analysis, case analysis, saturation
- Implementation roadmap and open questions

---

## 🎯 Phase 1: Core Theory Building (Current)

### Capabilities

**1. Competing Hypotheses Generation**
- Automatically generates 5-7 alternative explanations
- Uses multiple theoretical lenses (RBV, TCE, Institutional Theory, etc.)
- Specifies mechanisms, variables, boundaries, predictions, falsification

**2. Dialectical Integration**
- Resolves contradictions between theories
- Three integration modes: Temporal, Conditional, Mechanistic
- Proposes synthesized frameworks

**3. Socratic Questioning**
- 5-level question hierarchy (Descriptive → Theoretical)
- Always pushes to Level 3-5 (mechanistic/contingent/theoretical)
- Never accepts surface-level explanations

**4. Bias Detection & Mitigation**
- Monitors 6 types of cognitive biases
- Flags explicitly: 🚨 [Bias Name] Alert
- Provides specific mitigation strategies

**5. Boundary Condition Specification**
- Clarifies temporal, contextual, organizational scope
- Tests where theory applies and where it fails
- Strengthens falsifiability

### What Phase 1 Does NOT Include

❌ Detailed qualitative data coding  
❌ Within-case vs cross-case analysis  
❌ Gioia data structure creation  
❌ Literature review support  
❌ Theory paper writing

→ **These features planned for Phase 2**

---

## 🚀 How to Use

### For Researchers

**Step 1: Activate the Skill**
```
In your Claude conversation, mention:
- "I'm building a new theory about..."
- "Help me understand why X causes Y"
- "I need to integrate RBV and institutional theory"
- "I'm doing exploratory research on..."
```

**Step 2: Engage in Extended Dialogue**
- Expect 15-30 exchanges for deep theory building
- Provide concrete examples from your research
- Be open to having assumptions challenged
- Don't rush to closure—saturation takes time

**Step 3: Iterate as Theory Evolves**
- Return to the skill as your thinking develops
- Test new data against emerging theory
- Refine boundary conditions
- Sharpen propositions

### Example Session Flow

```
[Exchange 1-5]
You: "I observed [phenomenon]"
Claude: Clarifies boundaries, identifies theoretical puzzle

[Exchange 6-15]
Claude: Generates 6 competing hypotheses
You: "H3 resonates most"
Claude: Challenges with confirmation bias check

[Exchange 16-25]
Claude: Probes mechanisms (Level 3-5 questions)
You: Refines causal process
Claude: Identifies boundary conditions

[Exchange 26-30]
Claude: Synthesizes refined theory
You: Tests against anomalies
Claude: Suggests next empirical steps
```

---

## 🔮 Phase 2: Data Analysis (Planned)

### Future Capabilities

**Module 1: Qualitative Coding**
- 1st order coding (in vivo)
- 2nd order theming
- Aggregate dimensions
- Gioia data structure generation

**Module 2: Case Analysis**
- Within-case: Temporal bracketing, narratives
- Cross-case: Pair-wise comparison, pattern search
- Replication logic

**Module 3: Theory-Data Iteration**
- Cycle 1: Initial patterns
- Cycle 2: Refinement
- Cycle 3: Saturation detection

**Module 4: Literature Enfolding**
- Conflicting literature analysis
- Similar literature integration
- Contribution statement development

**Estimated:** +1400 lines, 4-6 weeks development after Phase 1 validation

---

## 📊 Validation & Quality

### How to Know It's Working

**Process Indicators:**
✓ Claude auto-activates on theory-building queries  
✓ Multiple (not single) hypotheses generated  
✓ Biases flagged explicitly  
✓ Questions progress to Level 3-5  
✓ Boundary conditions articulated

**Outcome Indicators:**
✓ More rigorous theories developed  
✓ Falsifiable and testable propositions  
✓ Explicit mechanisms (no black boxes)  
✓ Alternative explanations considered  
✓ Anomalies seen as opportunities

### Quality Standards

Theories developed with this skill should meet:
- **Eisenhardt (1989)** criteria for case-based theory
- **Gioia et al. (2013)** standards for qualitative rigor
- **Construct validity:** Clear, distinct definitions
- **Causal clarity:** Step-by-step mechanisms
- **Boundary specification:** Scope explicitly stated
- **Falsifiability:** Conditions for disconfirmation

---

## 🎓 Theoretical Foundations

### Key Methodologies

**Eisenhardt (1989)**
- Building theories from case study research
- 8-step process from question to closure
- Theoretical sampling, cross-case patterns, literature enfolding

**Gioia et al. (2013)**
- Seeking qualitative rigor in inductive research
- 1st order → 2nd order → aggregate dimensions
- Data structure diagrams

**Glaser & Strauss (1967)**
- Discovery of grounded theory
- Constant comparison, theoretical sampling, saturation

**Gehman et al. (2018)**
- Finding theory-method fit
- Abductive reasoning, iterative theory building

### Theoretical Lenses

**Always Considered:**
1. Resource-Based View (RBV)
2. Transaction Cost Economics (TCE)
3. Institutional Theory
4. Dynamic Capabilities View
5. Social Network Theory

**Context-Specific:** Added based on research domain

---

## ⚙️ Technical Details

### SKILL.md Specifications

- **File Size:** 820 lines
- **Format:** Markdown with embedded protocols
- **Encoding:** UTF-8
- **Structure:** Standard MCP SKILL.md format
- **Compatibility:** Claude Sonnet 4+ recommended

### Integration

**With Other Skills:**
- Can work alongside empirical research skills
- Complements data collection skills
- Independent of statistical analysis skills

**Limitations:**
- Not a replacement for researcher judgment
- Does not conduct fieldwork
- Does not write papers automatically
- Requires iterative human-AI collaboration

---

## 🔄 Version History

### Version 1.0 (2025-11-17) - Phase 1 Complete

**Implemented:**
✅ Five core capabilities  
✅ Philosophical foundations  
✅ Interaction patterns  
✅ Quality assurance protocols  
✅ Anti-hallucination safeguards

**File Structure:**
- SKILL.md (820 lines) - Executable
- DEVELOPMENT_PHASE1.md - Design docs
- PHASE2_PLAN.md - Future roadmap
- README.md - This file

### Version 2.0 (Future) - Phase 2 Planned

**Will Add:**
- Qualitative data coding support
- Case analysis techniques
- Theory-data iteration cycles
- Literature enfolding protocols
- Estimated +1400 lines

---

## 📖 Usage Examples

### Example 1: Initial Theory Building

```
User: "I interviewed 15 firms about AI adoption. 
      Some succeeded, some failed. Not sure why."

Claude: [Activates skill automatically]

"Perfect timing to build theory. Let's clarify:

1️⃣ PHENOMENON BOUNDARIES
- 'AI adoption' = which technologies?
- 'Success' = what metric?
- Which industries/sizes?
- What time frame?

Answer these and we'll identify your puzzle."
```

### Example 2: Bias Detection

```
User: "I found 3 cases supporting my RBV hypothesis."

Claude: 🚨 Confirmation Bias Alert

"You cite only positive evidence. Where are:
1. Cases where RBV predicted success but firm failed?
2. Cases where firm succeeded without RBV predictions?

Search systematically for disconfirming evidence."
```

### Example 3: Depth Through Questioning

```
User: "Leadership explains success."

Claude [Level 2]: "What specific behaviors differed?"

User: "Leader A visited teams, B didn't."

Claude [Level 3]: "How did visits lead to success?
Visits → [?] → [?] → Success
What happened at each step?"

User: "Visits revealed problems, informed decisions."

Claude [Level 4]: "What conditions enable this?
- Psychological safety for honesty?
- Leader's technical literacy?
- Problems solvable by visiting?"
```

---

## 🎯 Best Practices

### For Optimal Results

**DO:**
✅ Engage in extended dialogues (15-30 exchanges)  
✅ Provide concrete examples from data  
✅ Accept challenges to your assumptions  
✅ Iterate as your theory evolves  
✅ Test propositions against anomalies

**DON'T:**
❌ Expect instant complete theories  
❌ Ignore disconfirming evidence  
❌ Rush to theoretical closure  
❌ Accept "it depends" without specifics  
❌ Skip mechanistic explanations

### When to Use This Skill

**Ideal For:**
- PhD students building dissertation theories
- Junior faculty developing research streams
- Experienced researchers exploring new phenomena
- Anyone conducting exploratory/inductive research

**Less Suitable For:**
- Deductive hypothesis testing (use empirical skills)
- Literature reviews (use systematic review methods)
- Paper writing (use writing support skills)
- Statistical analysis (use quantitative skills)

---

## 🆘 Troubleshooting

### Common Issues

**Issue:** "Claude doesn't activate the skill automatically"
- **Solution:** Explicitly mention "theory building" or "exploratory research"

**Issue:** "Hypotheses are too generic"
- **Solution:** Provide more specific phenomenon details and context

**Issue:** "Too many competing hypotheses"
- **Solution:** Ask Claude to focus on top 3 most promising

**Issue:** "Need data coding support"
- **Solution:** Phase 2 not yet available, use manual coding for now

---

## 📚 References

### Foundational Works

**Methodology:**
- Eisenhardt, K. M. (1989). Building theories from case study research. *Academy of Management Review*, 14(4), 532-550.
- Gioia, D. A., et al. (2013). Seeking qualitative rigor in inductive research. *Organizational Research Methods*, 16(1), 15-31.
- Glaser, B. G., & Strauss, A. L. (1967). *The discovery of grounded theory*. Aldine.
- Gehman, J., et al. (2018). Finding theory–method fit. *Journal of Management Inquiry*, 27(3), 284-300.

**Theory:**
- Barney, J. (1991). Firm resources and sustained competitive advantage. *Journal of Management*, 17(1), 99-120.
- Williamson, O. E. (1985). *The economic institutions of capitalism*. Free Press.
- DiMaggio, P. J., & Powell, W. W. (1983). The iron cage revisited. *American Sociological Review*, 147-160.
- Teece, D. J. (2007). Explicating dynamic capabilities. *Strategic Management Journal*, 28(13), 1319-1350.

---

## 💬 Feedback & Contribution

### How to Improve This Skill

**Feedback Welcome On:**
- Dialogue quality and usefulness
- Additional capabilities needed
- Bias detection accuracy
- Question progression effectiveness
- Integration with other research tools

**To Contribute:**
1. Test with real research projects
2. Share example dialogues (anonymized)
3. Suggest theoretical lens additions
4. Propose new interaction patterns

---

## 📄 License & Attribution

**Created by:** Changu (Strategic Management & Organization Theory Researcher)  
**Purpose:** Academic research support (non-commercial)  
**Usage:** Free for academic research, with attribution  
**Based on:** Established theory-building methodologies

---

## 🔗 Quick Links

- **Main File:** [SKILL.md](./SKILL.md) ← Start here
- **Design Docs:** [DEVELOPMENT_PHASE1.md](./DEVELOPMENT_PHASE1.md)
- **Future Plans:** [PHASE2_PLAN.md](./PHASE2_PLAN.md)

---

## ✉️ Contact

For questions, suggestions, or collaboration:
- Create issues in this repository
- Share feedback with Claude directly
- Contribute example dialogues

---

**Last Updated:** 2025-11-17  
**Version:** 1.0 (Phase 1 Complete)  
**Status:** Ready for use, Phase 2 in planning
