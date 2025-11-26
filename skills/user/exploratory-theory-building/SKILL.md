# Exploratory Theory Building in Strategic Organization Research

**Version**: 1.0.0 (Phase 1 Implementation)  
**Created**: 2025-11-08  
**Domain**: Strategic Management & Organization Theory  
**Philosophical Foundation**: Dialectical integration of external resources and internal cognitive capabilities for dynamic knowledge creation  
**Implementation Status**: Phase 1 (Foundation Building) — 1-2 months, ~76 hours

---

## Executive Summary: The Essence of Integrated Theory Building

Excellence in theory construction emerges from the dialectical synthesis of two essential dimensions: the strategic utilization of existing intellectual capital (external tools and methodologies) and the systematic cultivation of unique cognitive capabilities (internal skills). This skill system crystallizes this epistemological duality into practical workflows that accelerate the cyclical process of exploration and verification.

**Three Pillars of Integration**:

1. **Strategic Utilization of External Intellectual Ecosystem**  
   Selective introduction and optimization of causal inference libraries (DoWhy, EconML), qualitative analysis tools (ATLAS.ti, NVivo), statistical environments (R/Python), and classical methodological literature (Eisenhardt, Gioia, Glaser-Strauss)

2. **Systematic Construction of Internal Cognitive Capabilities**  
   Internalization of multiple competing hypotheses generation framework, systematic literature synthesis methodology, dialogical theory development process, and methodological rigor assessment mechanisms

3. **Mutually Reinforcing Integrated Workflow**  
   Construction of practical systems where external tools and internal skills interact to simultaneously enhance theoretical creativity and methodological rigor

---

## I. Epistemological Foundation: Understanding the Essential Duality

### A. The Inherent Duality in Theory Building

Theory construction demands a dialectical synthesis of seemingly contradictory intellectual endeavors: objective methodological rigor and creative theoretical imagination. This epistemological tension is not merely a technical challenge but the very essence of the dynamic process of knowledge creation in exploratory research.

**Role of External Resources**:  
Existing theoretical knowledge, methodological accumulation, and analytical tools provide the intellectual infrastructure for researchers to "stand on the shoulders of giants." Eisenhardt's (1989) 8-step process, Gioia et al.'s (2013) data structure diagrams, and DoWhy's causal inference framework are all crystallizations of intellectual labor by prior researchers, enabling significant advancement of the starting point for theory construction.

**Role of Internal Skills**:  
However, mere application of external resources does not yield genuine theoretical innovation. The researcher's own cognitive capabilities—the ability to interpret phenomena from multiple perspectives, to generate and critically evaluate multiple theoretical explanations, to read the theoretical assumptions behind literature—are the sources that produce new theoretical insights beyond existing knowledge.

**Necessity of Dialectical Integration**:  
External resources and internal skills manifest their potential only through mutual interaction. Excellent tools without the cognitive ability to master them become useless treasures, while advanced cognitive capabilities without appropriate tool support end in inefficient trial and error. This skill system explicitly recognizes this interdependence and provides a systematic approach to promote co-evolution of both dimensions.

---

## II. Phase 1 Implementation: Foundation Building (1-2 Months)

### A. Week 1-2: Mastering Theoretical Foundations

**Objective**: Acquire foundational understanding of three major methodological approaches and select the optimal approach for your research question

#### External Resources (18 hours)

**Core Methodological Literature**:

1. **Eisenhardt, K. M. (1989). Building theories from case study research** (8 hours)
   - *Academy of Management Review*, 14(4), 532-550
   - *Citations*: 40,000+
   - *Epistemological Stance*: Positivist approach
   - *Core Process*: 8-step systematic theory building (theoretical sampling → multiple case comparison → pattern discovery → testable theory generation)
   - *Application*: Strategic comparisons across multiple firms, industry structure analysis, research aiming to derive verifiable propositions

2. **Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive research** (6 hours)
   - *Academy of Management Journal*, 56(1), 15-31
   - *Citations*: 15,000+
   - *Epistemological Stance*: Interpretivist approach
   - *Core Process*: Gradual abstraction from 1st order concepts → 2nd order themes → aggregate dimensions; creation of data structure diagrams
   - *Application*: New concept development from interview data, sensemaking research, research emphasizing participants' perspectives

3. **Gehman, J., Glaser, V. L., Eisenhardt, K. M., Gioia, D., Langley, A., & Corley, K. G. (2018). Finding theory-method fit** (4 hours)
   - *Academy of Management Review*, 43(2), 284-303
   - *Contribution*: Compares three major approaches (Eisenhardt, Gioia, Langley) from philosophical foundations, providing criteria for theory-method fit judgment
   - *Practical Value*: Decision framework for selecting optimal methodology for your research

#### Internal Skills Development (12 hours)

**Skill 1: Comparative Understanding of Philosophical Assumptions**

Create a comparison matrix analyzing:

| Dimension | Eisenhardt | Gioia | Glaser-Strauss |
|-----------|-----------|-------|----------------|
| Nature of Theory | Testable propositions | Conceptual framework | Process theory |
| Data Analysis | Structured comparison | Gradual abstraction | Constant comparison |
| Researcher's Role | Objective observer | Interpretive mediator | Theoretical sensitivity |
| Output | Propositions | Data structure | Core category |
| Generalizability | Analytical generalization | Conceptual transferability | Theoretical saturation |

**Skill 2: Research Question-Method Fit Judgment**

Develop ability to select appropriate approach based on:
- **What-type questions**: Gioia (discovery of new phenomena)
- **How-type questions**: Glaser-Strauss (process theory)
- **Why-type questions**: Eisenhardt (causal mechanisms)

**Skill 3: Cultivating Theoretical Sensitivity**

Practice identifying:
- Implicit theoretical assumptions in your field
- Conceptual relationships within phenomena
- Patterns across multiple cases or contexts

#### Integrated Practice

While reading each paper:
1. Apply the approach to your research theme
2. Identify which aspects resonate with your research style
3. Note specific techniques you want to implement
4. Create concrete examples demonstrating differences among the three approaches

**Week 1-2 Deliverables**:
- [ ] Methodological comparison report (1-2 pages)
- [ ] Selected primary approach with justification
- [ ] Research question-method fit analysis
- [ ] Personal notes on theoretical sensitivity development

---

### B. Week 3-4: Basic Tool Setup and Initial Utilization

**Objective**: Establish reproducible research environment and acquire basic causal inference thinking

#### External Resources (18 hours)

**Tool 1: Git/GitHub Fundamentals** (4 hours)

*Installation*:
```bash
# macOS (Homebrew)
brew install git

# Verify installation
git --version
```

*Basic Workflow*:
```bash
# Initialize repository
cd /path/to/your/research/project
git init

# Configure identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Basic operations
git add .
git commit -m "Initial commit: Project structure"

# Connect to GitHub
git remote add origin https://github.com/yourusername/repository.git
git push -u origin main
```

*Learning Resources*:
- GitHub's "Getting Started" guide: https://docs.github.com/en/get-started
- Grant McDermott's slides for economists: https://github.com/uo-ec607/lectures

**Tool 2: Python/R Environment Construction** (6 hours)

*Python Setup (conda)*:
```bash
# Install Miniconda
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create environment for theory building
conda create -n theory_building python=3.10
conda activate theory_building

# Install core packages
conda install pandas numpy matplotlib seaborn jupyter
pip install dowhy econml --break-system-packages
```

*R Setup (renv)*:
```r
# Install renv
install.packages("renv")

# Initialize project
renv::init()

# Install core packages
install.packages(c("tidyverse", "lavaan", "semPlot"))

# Take snapshot
renv::snapshot()
```

**Tool 3: DoWhy - Causal Inference Foundations** (8 hours)

*Installation*:
```bash
pip install dowhy --break-system-packages
```

*Tutorial Completion*:
1. Work through official tutorials: https://www.pywhy.org/dowhy/
2. Practice with lalonde dataset (labor economics data)
3. Create your first causal graph
4. Execute basic causal effect estimation
5. Run refutation tests

*Core Concepts to Master*:
- Causal graphs (DAGs - Directed Acyclic Graphs)
- Backdoor criterion (identifying confounders)
- Treatment effect estimation
- Refutation tests (placebo treatment, subset validation)

#### Internal Skills Development (10 hours)

**Skill 1: Version Control Habit Formation**

- Commit daily with meaningful messages
- Document significant decisions in commit messages
- Use branches for experimental analyses

**Skill 2: Causal Graph Thinking**

Practice translating theoretical claims into causal graphs:
- "A influences B" → Draw arrow A → B
- Identify potential confounders (common causes)
- Distinguish correlation from causation

**Example Exercise**:
```
Theoretical Claim: "Organizational learning capability enhances innovation performance"

Causal Graph Elements:
- Treatment: Learning capability (L)
- Outcome: Innovation performance (I)
- Potential confounders: Firm size (S), Industry (Ind), R&D investment (R)

Question: How would you draw this as a causal graph?
Answer: S → L, S → I, Ind → L, Ind → I, R → L, R → I, L → I
```

**Skill 3: Reflexive Analysis of Causal Assumptions**

Constantly ask:
- "Why does this causal relationship exist?"
- "What alternative explanations are possible?"
- "What confounders might I be missing?"

#### Integrated Practice

1. Create Git repository for your research project
2. Execute simple causal analysis with DoWhy while theoretically considering:
   - "Why am I controlling for this variable?"
   - "What other confounders might exist?"
3. Manage code and theoretical memos in the same Git repository

**Week 3-4 Deliverables**:
- [ ] Git-managed research repository
- [ ] Configured Python/R environment (with environment.yml or renv.lock)
- [ ] Completed DoWhy tutorial with notes
- [ ] One executed causal analysis example
- [ ] Theoretical memo documenting causal assumptions

---

### C. Week 5-6: Practicing Multiple Competing Hypotheses Generation

**Objective**: Master the intellectual core of exploratory theory building—generating and comparing multiple theoretical explanations

#### External Resources (22 hours)

**Activity 1: Systematic Literature Review** (20 hours)

*Target*: 10-15 papers directly relevant to your research theme

*Search Strategy*:
1. **Backward search**: Trace citations from seminal papers
2. **Forward search**: Use Google Scholar's "Cited by" feature
3. **Database search**: ABI/INFORM, JSTOR, Web of Science, Scopus

*Literature Review Matrix Template*:

| Paper | Theoretical Lens | Main Propositions | Empirical Context | Key Findings | Limitations |
|-------|-----------------|-------------------|-------------------|--------------|-------------|
| Author (YYYY) | RBV | Resources → Competitive Advantage | Manufacturing firms | Positive relationship | Small sample |
| ... | ... | ... | ... | ... | ... |

**Activity 2: Literature Management with Zotero** (2 hours)

*Setup*:
1. Install Zotero: https://www.zotero.org/
2. Install browser connector
3. Create collections by research theme
4. Export to BibTeX format for LaTeX/Markdown integration

#### Internal Skills Development (14 hours)

**Skill 1: Extracting Theoretical Perspectives from Literature**

For each paper, identify:
- Core theoretical lens (RBV, TCE, Institutional Theory, etc.)
- Implicit assumptions (about human rationality, organizational goals, etc.)
- Boundary conditions (when does this theory apply?)

**Skill 2: Comparative Analysis of Competing Explanations**

Create a "Theoretical Explanation Comparison Table":

| Theoretical Lens | Causal Mechanism | Key Concepts | Predictions | Strengths | Weaknesses |
|-----------------|------------------|--------------|-------------|-----------|------------|
| Resource-Based View | Unique resources → Competitive advantage | VRIN resources, Capabilities | Heterogeneous performance | Explains sustained advantage | Static view |
| Transaction Cost Economics | Transaction cost minimization → Governance choice | Asset specificity, Opportunism | Make vs. buy decisions | Explains boundaries | Limited to efficiency |
| Institutional Theory | Institutional pressures → Isomorphism | Legitimacy, Coercive/Mimetic/Normative | Organizational homogeneity | Explains conformity | Underemphasizes agency |
| Dynamic Capabilities | Sensing/Seizing/Transforming → Adaptation | Routines, Learning | Capability reconfiguration | Explains change | Ambiguous construct |

**Skill 3: Generating 3-5 Competing Hypotheses**

**Framework**:

**Phase 1: Multi-perspectival Observation**  
Observe the same phenomenon through multiple theoretical lenses

**Phase 2: Independent Causal Mechanism Generation**  
Propose distinct causal mechanisms from each perspective

**Phase 3: Quality Evaluation**  
Assess each explanation on:
- **Testability**: Can it be empirically verified?
- **Explanatory Power**: How much of observed variation does it explain?
- **Parsimony**: Does it explain maximum with minimum assumptions?
- **Consistency**: Is it consistent with existing theory? If not, is the contradiction justified?
- **Novelty**: Does it add new insights to existing knowledge?

**Phase 4: Integrative Framework Construction**  
Rather than forcing unification, specify boundary conditions for each explanation:

*Example*: "In early internationalization stages, Institutional Theory has high explanatory power; in mature stages, RBV becomes more important. However, in industries with high environmental volatility, Dynamic Capabilities are influential across all stages."

#### Integrated Practice

**Exercise: Generate Competing Hypotheses for Your Research Theme**

1. Select a central phenomenon in your research
2. Examine it through 3-4 different theoretical lenses
3. For each lens, write:
   - Core causal mechanism (2-3 sentences)
   - Key concepts (3-5 terms)
   - Testable predictions (2-3 propositions)
   - Boundary conditions (when does this apply?)
4. Create a visual comparison (table or diagram)
5. Draft an integrative framework specifying when each explanation applies

**Week 5-6 Deliverables**:
- [ ] Literature review matrix (10-15 papers)
- [ ] Zotero library with organized collections
- [ ] Theoretical explanation comparison table
- [ ] 3-5 competing hypotheses for your research theme
- [ ] Visual representation of competing explanations
- [ ] Initial integrative framework (1-2 pages)

---

### D. Week 7-8: Constructing Initial Theoretical Framework

**Objective**: Synthesize competing hypotheses into a coherent theoretical framework through dialogical theory development

#### External Resources (2 hours)

**Activity: Theoretical Model Visualization**

*Tools*:
- PowerPoint/Keynote (accessible, good for presentations)
- draw.io (free, web-based, professional diagrams)
- Mermaid (code-based, version-controllable)

*Model Components*:
1. Constructs (boxes/circles)
2. Relationships (arrows)
3. Mediators/Moderators (if applicable)
4. Feedback loops (if process theory)

#### Internal Skills Development (14 hours)

**Skill 1: Dialogical Theory Development with Claude**

**4-Stage Process**:

**Stage 1: Understanding (Context Exploration)**

*Prompt Template*:
```
I am developing a theory about [phenomenon]. Currently, I have these competing explanations:

1. [Theoretical Lens A]: [Brief mechanism]
2. [Theoretical Lens B]: [Brief mechanism]
3. [Theoretical Lens C]: [Brief mechanism]

Which perspective seems most compelling for explaining [specific aspect]? Why?
What are the limitations of each perspective that I should consider?
```

**Stage 2: Divergence (Creative Exploration)**

*Prompt Template*:
```
Let's explore alternative explanations. Can you:
1. Suggest an interdisciplinary analogy for this phenomenon (e.g., from biology, physics, sociology)
2. What would change if I reversed my core assumption [specify assumption]?
3. Can this individual-level phenomenon be scaled to the organizational level?
4. What would happen if I integrated [Theory X] with [Theory Y]?
```

**Stage 3: Integration (Connection Making)**

*Prompt Template*:
```
I've generated these diverse perspectives:
[List perspectives]

Help me identify:
1. Common themes across these perspectives
2. How do they complement each other?
3. What contradictions exist, and are they productive tensions or fundamental incompatibilities?
4. Can you suggest a higher-order framework that encompasses these perspectives?
```

**Stage 4: Critical Evaluation (Rigorous Assessment)**

*Prompt Template*:
```
Critically evaluate my theoretical framework:

[Present framework]

Assess:
1. Logical consistency: Are there any contradictions?
2. Testability: Can each proposition be empirically tested?
3. Novelty: What new insights does this offer beyond existing theories?
4. Boundary conditions: When does this theory NOT apply?
5. Alternative explanations: What have I potentially overlooked?
```

**Skill 2: Visual Model Construction**

**Model Types**:

1. **Variance Model** (Eisenhardt approach)
   - Boxes for constructs
   - Arrows for hypothesized relationships
   - +/- signs for direction

2. **Process Model** (Glaser-Strauss approach)
   - Stages or phases
   - Transitions and conditions
   - Feedback loops

3. **Data Structure Diagram** (Gioia approach)
   - 1st order concepts (left)
   - 2nd order themes (middle)
   - Aggregate dimensions (right)
   - Arrows showing abstraction

**Skill 3: Articulating Theoretical Contributions**

**Three Types of Contributions**:

1. **Construct Development**  
   "I introduce a new construct, [X], defined as [definition], which differs from existing constructs [A] and [B] because [distinction]"

2. **Relationship Discovery**  
   "I propose a novel relationship between [X] and [Y], mediated by [M], which previous research has not examined"

3. **Boundary Specification**  
   "I refine existing theory by specifying that [existing relationship] holds under conditions [C1] but not [C2], resolving prior contradictions"

#### Integrated Practice

**Activity: Complete Theory Development Cycle**

1. **Prepare**: Consolidate competing hypotheses from Week 5-6
2. **Dialogue Session 1** (2 hours): Understanding and Divergence
   - Present current thinking to Claude
   - Explore creative alternatives
   - Document all generated ideas
3. **Integration Work** (4 hours): Solo synthesis
   - Identify patterns across perspectives
   - Draft integrative framework
   - Create visual model
4. **Dialogue Session 2** (2 hours): Critical Evaluation
   - Present draft framework to Claude
   - Receive critical feedback
   - Identify weaknesses and gaps
5. **Refinement** (4 hours): Revision
   - Address identified issues
   - Strengthen logical consistency
   - Clarify boundary conditions
6. **Documentation** (2 hours): Write theoretical framework section

**Week 7-8 Deliverables**:
- [ ] Dialogue session transcripts (2 sessions)
- [ ] Visual theoretical model (PowerPoint/draw.io/Mermaid)
- [ ] Theoretical framework draft (3-5 pages) including:
  - Core constructs and definitions
  - Propositions or hypotheses
  - Theoretical mechanisms
  - Boundary conditions
  - Expected contributions
- [ ] Self-assessment against quality criteria

---

## III. Phase 1 Success Metrics and Evaluation

### A. Knowledge & Understanding Checklist

By the end of Phase 1, you should be able to:

- [ ] **Explain** the three major approaches (Eisenhardt, Gioia, Glaser-Strauss) and their philosophical differences
- [ ] **Select** the appropriate approach for your research with justification
- [ ] **Read and draw** basic causal graphs (DAGs)
- [ ] **Distinguish** correlation from causation in theoretical claims
- [ ] **Identify** theoretical lenses and assumptions in published papers
- [ ] **Recognize** theoretical gaps in literature

### B. Skills & Practices Checklist

- [ ] **Generate** 3-5 competing hypotheses independently
- [ ] **Identify** theoretical gaps from literature review matrix
- [ ] **Execute** simple causal analysis with DoWhy
- [ ] **Conduct** productive dialogical theory sessions with Claude
- [ ] **Create** visual theoretical models
- [ ] **Use** Git for daily version control

### C. Deliverables Checklist

- [ ] Git-managed research repository exists and is regularly updated
- [ ] Literature review matrix (10-15 papers) completed
- [ ] Competing hypotheses document (3-5 hypotheses) created
- [ ] Provisional theoretical model diagram created
- [ ] Theoretical framework draft (3-5 pages) written
- [ ] DoWhy causal analysis example executed

### D. Overall Assessment

**Phase 1 Completion Criterion**:  
"I understand the complete theory building process and can use basic tools to execute each stage"

**Signs of Successful Completion**:
- You can explain your theoretical framework to a colleague in 10 minutes
- You can defend why you chose your methodological approach
- You feel confident starting data collection/analysis
- You have a clear roadmap for Phase 2

**If Not Yet Complete**:
- Extend Phase 1 by 1-2 weeks
- Focus on the weakest area (tools vs. conceptual understanding)
- Schedule additional Claude dialogue sessions
- Consult Phase 1 implementation guidelines again

---

## IV. Integration with Existing Skills

### A. Relationship with strategic-organizational-empirical Skill

**This skill (exploratory-theory-building)** focuses on:
- Theory generation phase (exploratory)
- Conceptual development
- Hypothesis formation
- Qualitative foundations

**strategic-organizational-empirical skill** focuses on:
- Theory verification phase (confirmatory)
- Quantitative analysis
- Hypothesis testing
- Statistical rigor

**Integration Points**:
1. Use **exploratory-theory-building** in early project stages to develop constructs and propositions
2. Transition to **strategic-organizational-empirical** for empirical testing with large-scale data
3. Iterate between both: empirical findings may reveal need for theoretical refinement

**Workflow Example**:
```
[Phase 1-2: Theory Development]
Use exploratory-theory-building skill
↓ Generate constructs, propositions, mechanisms
↓
[Phase 3: Empirical Testing]
Use strategic-organizational-empirical skill
↓ Test with quantitative data, SEM, causal inference
↓
[Phase 4: Theory Refinement]
Return to exploratory-theory-building
↓ Refine based on empirical results
```

### B. Avoiding Confusion and Overlap

**Clear Boundaries**:

| Aspect | Exploratory Theory Building | Strategic Organizational Empirical |
|--------|----------------------------|-----------------------------------|
| Primary Goal | Develop new theory | Test existing theory |
| Data Type | Primarily qualitative | Primarily quantitative |
| Key Activities | Concept development, hypothesis generation | Hypothesis testing, effect estimation |
| Main Tools | ATLAS.ti, NVivo, causal graphs | R/Python, SEM, econometric models |
| Output | Theoretical framework, propositions | Empirical evidence, effect sizes |
| Publication Target | Theory sections, conceptual papers | Empirical sections, data-driven papers |

**When to Use Which**:
- **Start with exploratory** when: Phenomenon is new, existing theories inadequate, need new constructs
- **Start with empirical** when: Clear hypotheses exist, testing relationships, large dataset available
- **Use both** when: Mixed-methods design, grounded theory with quantitative validation

---

## V. Claude Integration Protocols

### A. Activating the Theory Building Skill

**Trigger Phrases for Automatic Activation**:

When you use these phrases, Claude will activate exploratory-theory-building protocols:

- "Help me develop a theory about [phenomenon]"
- "I need to generate competing hypotheses for [topic]"
- "Let's do dialogical theory development for [research question]"
- "Critically evaluate my theoretical framework"
- "What theoretical lenses could explain [observation]?"
- "Help me identify theoretical gaps in [literature area]"

**Explicit Activation**:
```
Claude, please activate the exploratory-theory-building skill to help me [specific task]
```

### B. Theory Development Dialogue Protocols

**Protocol 1: Understanding Phase**

Claude will:
- Ask clarifying questions about the phenomenon
- Help identify implicit assumptions
- Surface theoretical perspectives already in play
- Assess current theoretical sensitivity level

**Protocol 2: Divergent Exploration Phase**

Claude will:
- Suggest interdisciplinary analogies
- Propose assumption reversals
- Offer scale shifts (micro→macro, individual→organizational)
- Suggest theoretical integrations

**Protocol 3: Integration Phase**

Claude will:
- Identify common themes across perspectives
- Map complementarities and contradictions
- Propose higher-order frameworks
- Assess theoretical coherence

**Protocol 4: Critical Evaluation Phase**

Claude will:
- Check logical consistency
- Assess testability of propositions
- Evaluate novelty and contribution
- Identify boundary conditions
- Suggest alternative explanations

### C. Quality Assurance Mechanisms

**Forbidden Patterns in Theory Building Assistance**:

Claude will NOT:
- Provide generic theoretical frameworks without context
- Generate hypotheses without grounding in literature
- Offer methodological advice without considering epistemology
- Present tools as solutions without theoretical justification
- Encourage theoretical eclecticism without integration logic

**Required Patterns**:

Claude WILL:
- Always ask about your research question and context first
- Ground suggestions in methodological literature
- Provide specific, actionable guidance
- Explain WHY a theoretical approach is appropriate
- Identify tradeoffs and limitations of suggestions
- Connect tools to theoretical purposes

---

## VI. Tools and Resources

### A. Essential Phase 1 Tools (All Free/Open Source)

**Version Control**:
- Git: https://git-scm.com/
- GitHub: https://github.com/
- Installation: `brew install git` (macOS)

**Literature Management**:
- Zotero: https://www.zotero.org/ (Free, open-source)
- Browser connector for automatic citation capture
- Export to BibTeX for LaTeX/Markdown

**Causal Inference**:
- DoWhy: https://www.pywhy.org/dowhy/ (Python)
- Installation: `pip install dowhy --break-system-packages`
- Tutorials: Official documentation site

**Visualization**:
- draw.io: https://app.diagrams.net/ (Free, web-based)
- Mermaid: https://mermaid.js.org/ (Code-based diagrams, Git-friendly)
- PowerPoint/Keynote (familiar, good for academic presentations)

**Environment Management**:
- conda (Python): https://docs.conda.io/
- renv (R): https://rstudio.github.io/renv/

### B. Learning Resources

**Methodological Literature** (Seek through university library):
- Eisenhardt (1989): AMR, check ResearchGate if needed
- Gioia et al. (2013): AMJ, institutional access
- Gehman et al. (2018): AMR, recent and accessible

**Online Tutorials**:
- DoWhy tutorials: https://www.pywhy.org/dowhy/tutorials
- Git/GitHub: https://docs.github.com/en/get-started
- Causal inference basics: https://mixtape.scunning.com/

**Community Support**:
- Stack Overflow: Technical questions
- ResearchGate: Methodological discussions
- Academic Twitter (#AcademicTwitter, #PhDChat): Connect with scholars

### C. Templates Available in This Skill

Located in `/templates` directory:

1. `literature_review_matrix.xlsx`: Structured literature synthesis
2. `competing_hypotheses_template.md`: Multiple explanations framework
3. `theoretical_framework_template.md`: Theory section scaffold
4. `dialogue_session_template.md`: Claude theory development structure
5. `methodological_comparison_template.md`: Eisenhardt/Gioia/Glaser comparison

### D. Python Tools in This Skill

Located in `/tools` directory:

1. `hypothesis_generator.py`: Multiple competing hypotheses generation support
2. `literature_synthesizer.py`: Automated literature gap identification
3. `theory_visualizer.py`: Theoretical model diagram creation
4. `causal_graph_builder.py`: Interactive causal graph construction

*Note*: Phase 1 includes basic versions; Phase 2-3 add advanced features

---

## VII. Troubleshooting and Support

### A. Common Phase 1 Challenges

**Challenge 1: "I can't generate multiple competing hypotheses"**

*Symptoms*:
- Can only think of one explanation
- All hypotheses sound similar
- Feel stuck in one theoretical tradition

*Solutions*:
- Start with just 2 hypotheses (one conventional, one unconventional)
- Use Claude's divergent exploration prompts explicitly
- Read papers from DIFFERENT theoretical journals (e.g., if you read AMJ, read Organization Science)
- Ask: "What would [different theorist—Barney, Williamson, DiMaggio] say about this?"
- Use interdisciplinary analogies: "How is this like [phenomenon in biology/physics]?"

**Challenge 2: "DoWhy is too technical for me"**

*Symptoms*:
- Overwhelmed by Python code
- Don't understand causal graph syntax
- Can't connect causal inference to theory

*Solutions*:
- Focus on CONCEPTUAL understanding first, not code mastery
- Draw causal graphs on paper/whiteboard before coding
- Work through simplified examples (3-4 variables only)
- Remember: Phase 2 offers more time for deeper learning
- Use DoWhy primarily for causal thinking, not advanced estimation (that's Phase 2-3)

**Challenge 3: "I'm spending too much time on tools, not theory"**

*Symptoms*:
- Hours spent debugging code
- Reading tool documentation instead of theory papers
- More excited about Git than about ideas

*Solutions*:
- Set strict time limits for tool learning (2 hours max per tool session)
- Apply 80/20 rule: Learn 20% of features that give 80% value
- RULE: Tools serve theory, not vice versa
- If tool learning exceeds 25% of weekly time, refocus
- Delegate advanced tool mastery to Phase 2 if necessary

**Challenge 4: "My theoretical framework feels too simple/obvious"**

*Symptoms*:
- Framework seems to state the obvious
- Worried it's not "novel" enough
- Feels like just summarizing existing theories

*Solutions*:
- Remember: Simplicity ≠ Bad. Parsimony is valued in theory
- Apply "novel prediction" test: Does it make a prediction existing theories don't?
- Apply "boundary condition" test: When does it NOT apply?
- Apply "so what?" test: Why would someone care about this insight?
- Often, "obvious" frameworks that specify mechanisms or boundaries ARE contributions

### B. Getting Unstuck

**Scenario: No progress for 2 weeks**

*Emergency Protocol*:
1. Reduce scope to Minimum Viable Strategy (MVS)
   - Focus ONLY on: Git basics + Literature matrix + One hypothesis generation
2. Schedule Claude dialogue session to diagnose blockage
3. Identify: Is this a knowledge problem, motivation problem, or resource problem?
4. Extend Phase 1 by 1-2 weeks if necessary (this is OK!)
5. Consider: Do you need to pivot your research question?

**Scenario: Overwhelmed by literature**

*Solutions*:
1. Apply stricter inclusion criteria:
   - Only top-tier journals (FT50, ABS 4*)
   - Only papers from last 10 years
   - Only papers with >100 citations
2. Reduce initial target to 5-7 CORE papers
3. Use Zotero notes feature to extract ONLY:
   - Main theoretical lens
   - Core proposition
   - Key limitation/gap
4. Remember: Systematic ≠ Exhaustive. You're building theory, not writing a lit review paper

**Scenario: Perfectionism paralysis**

*Symptoms*:
- Can't write theory framework because it's "not ready"
- Constantly revising hypotheses
- Won't commit to a methodological approach

*Solutions*:
1. Adopt "Done is better than perfect" mantra
2. Set artificial deadlines: "Draft by Friday, no exceptions"
3. Share work with colleague/advisor for feedback (external pressure)
4. Remember: All theory papers go through multiple revisions
5. Phase 1 goal is PROVISIONAL framework, not final theory
6. Use version control to preserve old versions (reduces fear of commitment)

### C. When to Seek Human Help

**Seek advisor/mentor when**:
- Fundamental confusion about your research question
- Need help selecting methodological approach (Week 1-2)
- Ethical concerns about your research design
- Considering pivoting your research direction

**Seek peer support when**:
- Want feedback on provisional theory framework (Week 7-8)
- Stuck on literature review (Week 5-6)
- Need motivation and accountability
- Want to practice explaining your theory

**Seek technical support when**:
- Python/R installation problems persist >2 hours
- Git/GitHub authentication issues
- University library access problems

**DON'T seek help when**:
- Normal learning curve frustration (push through!)
- Temporary motivation dip (normal in Week 4-5)
- Minor coding errors (use Stack Overflow, Google)

---

## VIII. Next Steps: Looking Ahead to Phase 2

### A. Phase 2 Preview (2-3 Months, ~114 Hours)

**Phase 2 Focus**: Integration Deepening and Advanced Tool Introduction

**Month 3-4: Qualitative Data Analysis Tools (CAQDAS)**
- ATLAS.ti or NVivo introduction (20 hours)
- Gioia data structure creation (15 hours)
- Pilot interviews and coding practice (15 hours)
- Theoretical memoing habituation

**Month 4-5: Advanced Quantitative Integration**
- SEM basics with semopy/lavaan (12 hours)
- Exploratory factor analysis (EFA) (10 hours)
- Theory-driven measurement development (15 hours)
- Qual→Quant bridging thinking

**Month 5-6: Reproducible Workflow Construction**
- Snakemake pipeline building (8 hours)
- Jupyter Notebook/R Markdown documentation (ongoing)
- Paper writing begins (20 hours)
- Integration of all Phase 1-2 components

### B. Preparing for Phase 2

**Prerequisites from Phase 1**:
- Solid theoretical framework (Week 7-8 deliverable)
- Clear constructs and operational definitions
- Data collection plan (if qualitative approach)
- Survey instrument draft (if quantitative approach)

**What to Start Thinking About**:
1. **Data Strategy**:
   - Will you collect qualitative data (interviews, documents)?
   - Will you develop new measurement scales?
   - What sample size/case selection is appropriate?

2. **Tool Investment**:
   - Can you access ATLAS.ti/NVivo through university?
   - Or will you use free alternatives initially?
   - Budget for CAQDAS (student licenses ~$50-100/year)

3. **Time Management**:
   - Phase 2 is more intensive (114 vs. 76 hours)
   - Consider: Can you dedicate 10-12 hours/week?
   - May need to reduce other commitments

### C. Phase 2 Success Criteria

You'll be ready for Phase 2 when you:
- [ ] Have completed all Phase 1 deliverables
- [ ] Feel confident explaining your theoretical framework
- [ ] Understand when to use which methodological approach
- [ ] Can use Git/GitHub without referring to notes
- [ ] Have executed at least one causal inference analysis
- [ ] Know what data you need to test your theory

---

## IX. Philosophical Reflections on Theory Building

### A. The Dialectics of Knowledge Creation

Theory building in strategic management and organization studies represents more than a mere methodological exercise—it embodies the fundamental human endeavor to comprehend the complex dynamics of organized human activity. This intellectual pursuit demands what Aristotle termed *phronesis*—practical wisdom that transcends mere technical rationality.

The integration of external resources and internal capabilities proposed in this skill system reflects a deeper epistemological truth: knowledge creation is inherently dialogical. We do not discover pre-existing theories lying dormant in data; rather, we construct theoretical understanding through an iterative dialogue between our conceptual frameworks and empirical observations, between our individual cognitive capabilities and collective intellectual traditions, between abstract theoretical principles and concrete organizational realities.

### B. Theoretical Sensitivity as Intellectual Virtue

Glaser and Strauss's concept of "theoretical sensitivity" captures something profound about the researcher's intellectual disposition. It is not merely a skill to be acquired but a way of being-in-the-world as a scholar. The theoretically sensitive researcher cultivates:

**Attentiveness**: The capacity to notice subtle patterns, anomalies, and relationships that others might overlook

**Reflexivity**: The awareness of one's own theoretical biases and the humility to question one's assumptions

**Openness**: The willingness to be surprised by data, to let phenomena speak in their own voice

**Integration**: The ability to synthesize diverse perspectives into coherent yet nuanced frameworks

This intellectual virtue develops not through mechanical application of methods but through immersive engagement with both theoretical literature and empirical reality—a form of scholarly *praxis* where theory and practice interpenetrate.

### C. The Productive Tension of Multiple Paradigms

Rather than viewing the diversity of methodological approaches (Eisenhardt's positivism, Gioia's interpretivism, Glaser-Strauss's constructivism) as a problematic lack of consensus, we should recognize it as a productive pluralism that enriches organizational science. Each paradigm illuminates different facets of organizational reality:

- **Positivism** reveals causal structures and generalizable patterns
- **Interpretivism** uncovers meanings and sensemaking processes
- **Constructivism** traces the emergence of social categories and constructs

The integrated approach advocated here does not seek paradigmatic unity but rather paradigmatic dialogue—a both/and rather than either/or stance. This requires what F. Scott Fitzgerald called "first-rate intelligence": "the ability to hold two opposed ideas in mind at the same time and still retain the ability to function."

### D. Theory Building as Knowledge Architecture

Great theories are not mere collections of propositions but architectonic structures—they organize our understanding of phenomena in ways that reveal new connections, suggest novel inquiries, and reshape how we perceive organizational reality. Consider how:

- **Porter's Five Forces** restructured how we think about competitive advantage
- **Weick's Sensemaking Theory** reframed organizational cognition
- **Barney's RBV** redirected attention from external to internal sources of advantage

These theoretical frameworks endure not because they are "true" in some absolute sense, but because they are *generative*—they open up new research trajectories, practical applications, and ways of seeing.

### E. The Ethics of Theory Building

Theory building carries ethical responsibilities often overlooked in methodological discussions:

1. **Intellectual Honesty**: Acknowledging limitations, reporting contradictory findings, resisting confirmation bias

2. **Practical Wisdom**: Considering how theories might be used (or misused) in practice

3. **Epistemic Humility**: Recognizing the provisional nature of theoretical knowledge

4. **Social Responsibility**: Being mindful of how theories shape management practice and organizational life

As we construct theories about organizations, we simultaneously construct the conceptual tools that managers use to shape organizational realities. This recursive relationship between theory and practice demands that we theorize responsibly.

---

## X. Conclusion: Embarking on the Theory Building Journey

This skill system provides a structured pathway for developing excellence in exploratory theory building. Yet, as with any intellectual journey, the map is not the territory. The true learning emerges through practice—through the frustrations of conceptual confusion, the eureka moments of theoretical insight, the discipline of systematic analysis, and the creativity of imaginative synthesis.

Phase 1 establishes your foundation. You will acquire the conceptual tools, methodological literacy, and technical capabilities necessary for serious theory building. More importantly, you will begin to cultivate the intellectual virtues—theoretical sensitivity, critical reflexivity, creative imagination—that distinguish excellent from merely competent scholarship.

Remember that theory building is not a solitary endeavor but a contribution to ongoing scholarly conversations spanning decades and continents. You stand in a tradition stretching from Weber and Barnard through Cyert and March to Eisenhardt and Gioia. Honor this tradition by engaging it critically and creatively.

The journey begins with a single step: opening that first methodological paper, installing that first tool, generating that first competing hypothesis. Each small action accumulates into scholarly capability. Each theoretical insight builds upon the last. Each refinement brings you closer to a framework worthy of publication and practical impact.

**Your Phase 1 journey starts now.**

---

## References

Eisenhardt, K. M. (1989). Building theories from case study research. *Academy of Management Review*, 14(4), 532-550.

Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive research: Notes on the Gioia methodology. *Organizational Research Methods*, 16(1), 15-31.

Gehman, J., Glaser, V. L., Eisenhardt, K. M., Gioia, D., Langley, A., & Corley, K. G. (2018). Finding theory–method fit: A comparison of three qualitative approaches to theory building. *Journal of Management Inquiry*, 27(3), 284-303.

Glaser, B. G., & Strauss, A. L. (1967). *The discovery of grounded theory: Strategies for qualitative research*. Aldine.

Pearl, J. (2009). *Causality: Models, reasoning, and inference* (2nd ed.). Cambridge University Press.

Nonaka, I., & Takeuchi, H. (1995). *The knowledge-creating company: How Japanese companies create the dynamics of innovation*. Oxford University Press.

---

**Document Information**

- **Document Type**: Skill System Documentation
- **Version**: 1.0.0 (Phase 1 Implementation)
- **Created**: 2025-11-08
- **Total Length**: ~15,000 words
- **Estimated Implementation**: Phase 1 = 76 hours (1-2 months)
- **Target Audience**: Doctoral students, postdocs, early-career faculty in strategic management and organization theory
- **Update Policy**: Continuous refinement based on user feedback and methodological advances

**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

**Contact**: For questions, feedback, or implementation reports, please use GitHub Issues or Discussions.

---

#ExploratoryTheoryBuilding #StrategicManagement #OrganizationTheory #MethodologyIntegration #ExternalResources #InternalSkills #DialecticalSynthesis #KnowledgeCreation #ResearchMethods #TheoryAndPractice
