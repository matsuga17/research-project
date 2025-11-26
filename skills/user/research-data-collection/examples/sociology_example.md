# Sociology Research Example: Social Media and Political Polarization

**Research Topic**: Impact of Social Media Usage on Political Polarization Among Young Adults  
**Field**: Sociology, Political Science, Communication Studies  
**Researcher**: [Sample Project]  
**Date**: 2025-10-31  
**IRB Status**: Approved (IRB #2025-002, Approval Date: 2025-02-10)

---

## Project Overview

### Research Question
How does social media usage intensity and platform diversity relate to political attitude polarization among young adults (ages 18-30) in the United States?

### Theoretical Framework
- **Echo Chamber Theory**: Selective exposure to like-minded content reinforces existing beliefs
- **Filter Bubble Hypothesis**: Algorithmic curation limits exposure to diverse viewpoints
- **Social Identity Theory**: Group membership strengthens in-group/out-group distinctions

### Study Design
- **Type**: Mixed-methods (Primary: Survey, Secondary: Social Media Data Analytics)
- **Population**: US adults aged 18-30
- **Sample Strategy**: Stratified random sampling by age, gender, region, and political affiliation
- **Target Sample Size**: 1,500 respondents
- **Timeline**: 6-month data collection period (March-August 2025)

### Hypotheses
- **H1**: Higher social media usage intensity correlates with greater political polarization
- **H2**: Lower platform diversity (single-platform users) shows stronger polarization than multi-platform users
- **H3**: Political polarization is mediated by echo chamber exposure (measured by network homophily)

---

## Phase 1: Research Requirements Analysis

### Data Requirements

**Survey Data** (Primary):
1. **Demographics**:
   - Age, gender, race/ethnicity
   - Education level, employment status
   - Geographic region (urban/suburban/rural)
   - Household income bracket

2. **Political Attitudes**:
   - Political ideology (7-point scale: Very Liberal to Very Conservative)
   - Party affiliation (Democrat, Republican, Independent, Other)
   - Issue positions (20 items on key political issues)
   - Political tolerance scale (willingness to engage with opposing views)
   - Affective polarization (feeling thermometer toward own party vs. opposing party)

3. **Social Media Behavior**:
   - Platforms used (Facebook, Twitter/X, Instagram, TikTok, Reddit, YouTube)
   - Daily usage hours per platform
   - Primary activities (posting, reading, commenting, sharing)
   - News consumption sources (social media vs. traditional media)
   - Network characteristics (estimated % of same-political-view friends)

4. **Psychological Measures**:
   - Confirmation bias tendency
   - Open-mindedness scale
   - Need for cognitive closure

**Secondary Data Sources**:
1. **Pew Research Center**: 
   - National surveys on social media usage trends
   - Political polarization tracking data
   - Demographic benchmarks

2. **General Social Survey (GSS)**:
   - Long-term trends in political attitudes
   - Validation of polarization measures

3. **Public APIs** (if participant consent obtained):
   - Twitter/X API: Network analysis (following patterns)
   - Reddit API: Subreddit participation analysis

**Sample Size Calculation**:
- Effect size: medium (r = 0.25)
- Power: 0.80
- Alpha: 0.05
- Required n: 1,500 (accounting for 20% non-response)

---

## Phase 2: Data Source Discovery

### Primary Data Collection: Survey

#### 1. Survey Platform: Qualtrics
- **Institution License**: Yes (University site license)
- **Features**:
  - Advanced skip logic and branching
  - Multi-language support (English, Spanish)
  - Mobile-responsive design
  - Real-time data monitoring
  - GDPR/CCPA compliance tools
- **Cost**: Covered by institutional license
- **Quality**: ★★★★★ (5/5)

#### 2. Survey Panel Provider: Prolific Academic
- **URL**: https://www.prolific.co/
- **Purpose**: Recruit diverse US sample with demographic quotas
- **Features**:
  - Pre-screened participants with verified demographics
  - High data quality (attention check failures < 5%)
  - Fair compensation ($8-12/hour equivalent)
  - Built-in demographic filters
- **Cost**: ~$6.50 per complete response (participant payment + platform fee)
- **Total Budget**: $9,750 for 1,500 responses
- **Quality**: ★★★★☆ (4/5) - Better than MTurk for academic research
- **Alternative**: CloudResearch (Prime Panels) - more expensive but higher quality

#### 3. Survey Design Best Practices
- **Pre-testing**: Pilot with 50 respondents, revise based on feedback
- **Attention Checks**: 3 embedded validity checks
- **Survey Length**: ~15 minutes (balance completeness vs. fatigue)
- **Incentive**: $2.00 base + $0.50 completion bonus
- **Data Quality Screening**:
  - Speeding (< 5 min completion → exclude)
  - Straight-lining (same response to all items)
  - Failed attention checks (2+ failures → exclude)

### Secondary Data Sources

#### 4. Pew Research Center - Social Media Trends
- **URL**: https://www.pewresearch.org/internet/
- **Data Available**:
  - Social media usage by demographics (2019-2024)
  - Political polarization trends
  - News consumption patterns
- **Access**: Free download (CSV, SPSS)
- **Use**: Validate sample representativeness, contextualize findings

#### 5. General Social Survey (GSS)
- **URL**: https://gss.norc.org/
- **Data Available**:
  - Political views (1972-2022)
  - Social trust measures
  - Demographic trends
- **Access**: Free download via NORC or ICPSR
- **Use**: Historical comparison, measure replication

#### 6. American National Election Studies (ANES)
- **URL**: https://electionstudies.org/
- **Data Available**:
  - Political ideology time-series
  - Affective polarization measures
  - Party identification trends
- **Access**: Free registration required
- **Use**: Validate polarization scales

#### 7. Twitter/X API v2 (Optional, with consent)
- **URL**: https://developer.twitter.com/en/docs/twitter-api
- **Purpose**: Analyze network structure for subsample willing to share username
- **Variables**:
  - Following list (political accounts followed)
  - Tweet sentiment analysis
  - Retweet network (echo chamber indicator)
- **Access**: Free tier (500k tweets/month) or Academic Research tier
- **Privacy**: Requires explicit participant consent + data use agreement
- **Limitation**: Not all participants will consent; small subsample (~300 expected)

---

## Phase 3: Collection Strategy and Plan

### IRB Approval Process

**Protocol Type**: Survey research with minimal risk  
**IRB Number**: 2025-002  
**Review Type**: Expedited (Category 7: Research on individual or group characteristics or behavior)  
**Approval Date**: February 10, 2025  
**Informed Consent**: Electronic consent via Qualtrics (first page of survey)  
**Data Security**: De-identified data stored on encrypted university server

**Key IRB Considerations**:
- Political attitudes can be sensitive → Strong confidentiality protections
- Social media data (if collected) → Separate opt-in consent
- Minimal psychological risk → No deception, full disclosure of study purpose
- Participant compensation adequate → $2.00 for ~15 min = $8/hour

### Survey Implementation Timeline

**Week 1-2: Survey Development**
- Draft survey instrument (Day 1-3)
- Expert review by faculty advisors (Day 4-6)
- Program in Qualtrics (Day 7-9)
- Pre-test with 10 colleagues (Day 10-12)
- Revise based on feedback (Day 13-14)

**Week 3: Pilot Study**
- Launch pilot on Prolific (n=50)
- Monitor completion rates and time
- Analyze data quality (attention checks, missing data)
- Final revisions to survey

**Week 4: Recruitment Setup**
- Configure Prolific study parameters:
  - Location: United States
  - Age: 18-30
  - Approval rate: ≥ 95%
  - Stratification quotas: Age×Gender×Region (12 strata)
- Calculate sample size per stratum
- Prepare consent form and study description

**Week 5-10: Main Data Collection**
- Release survey in batches (300/week to manage quality)
- Daily monitoring of:
  - Completion rate
  - Data quality metrics
  - Participant questions/issues
- Weekly data export and preliminary checks
- Adjust recruitment if needed (e.g., undersampled strata)

**Week 11-12: Quality Assurance and Cleaning**
- Screen out low-quality responses
- Check for duplicate IP addresses
- Verify quota fulfillment
- Final dataset preparation

### Survey Structure

**Section 1: Consent and Screening (2 min)**
- Informed consent
- Age verification (18-30?)
- US residency confirmation

**Section 2: Demographics (2 min)**
- Age, gender, race/ethnicity
- Education, employment, income
- Geographic region, urbanicity

**Section 3: Political Attitudes (5 min)**
- Ideology self-placement (7-point scale)
- Party identification (with strength)
- 20 issue positions (5-point Likert scales)
  - Economy, healthcare, immigration, climate, gun control, etc.
- Feeling thermometers (own party, opposing party, specific politicians)

**Section 4: Social Media Use (4 min)**
- Platforms used (check all that apply)
- Hours per day per platform
- Primary activities (posting, reading, commenting)
- News sources (social media vs. traditional media %)
- Network homophily ("What % of your social media friends share your political views?")

**Section 5: Psychological Scales (3 min)**
- Confirmation bias scale (4 items)
- Open-mindedness scale (5 items)
- Need for cognitive closure (6 items)

**Section 6: Optional Social Media Data Sharing (1 min)**
- Opt-in for Twitter/X username sharing (for network analysis)
- Separate consent form
- Clear explanation of data use

**Total Time**: ~17 minutes (target: 15 min, pilot avg: 16.8 min)

### Data Quality Control Measures

**During Collection**:
1. **Attention Checks** (3 embedded):
   - "Please select 'Strongly Agree' for this item"
   - "What is 2 + 2?" (open-ended, must answer 4)
   - "On what device are you taking this survey?" (check consistency with meta-data)

2. **Speeding Detection**:
   - Flag responses < 8 minutes (< 50% of median time)
   - Manual review of flagged cases

3. **Straight-Lining**:
   - Calculate standard deviation of Likert responses
   - Flag if SD < 0.5 on scales with 10+ items

4. **Open-Ended Validation**:
   - "Please briefly explain your political views" (optional)
   - Check for nonsensical or copy-pasted text

**Post-Collection**:
1. **Duplicate Detection**: Check for duplicate IP addresses (allow max 2 from same IP, e.g., roommates)
2. **Geolocation Verification**: Prolific provides country-level geolocation
3. **Demographic Consistency**: Check for implausible combinations (e.g., age 18 + PhD degree)

**Exclusion Criteria**:
- Failed 2+ attention checks
- Completion time < 8 minutes
- Straight-lining on 50%+ of scales
- Duplicate submission
- Non-US IP address

**Expected Exclusion Rate**: 5-8% (based on Prolific averages)  
**Over-recruitment**: Collect 1,620 to ensure 1,500 high-quality responses

---

## Phase 4: Quality Assurance

### Pilot Study Results (n=50)

**Completion Rate**: 96% (48/50 started completed)  
**Average Time**: 16.8 minutes (SD = 4.2)  
**Attention Check Pass Rate**: 94% (47/50)  

**Issues Identified**:
1. Item #12 (immigration policy) confusing wording → Revised
2. One attention check too obvious (100% passed) → Made more subtle
3. Qualtrics mobile display issue on iPhone → Fixed CSS

**Participant Feedback** (n=12 comments):
- "Survey was engaging and well-organized" (positive)
- "Would like option to explain nuanced views" (added optional comment boxes)
- "Some questions felt repetitive" (expected for reliability; kept as is)

### Main Study Quality Metrics (Final Dataset)

**Total Responses Collected**: 1,623  
**Excluded**: 123 (7.6%)  
- Failed attention checks: 58 (3.6%)
- Speeders (< 8 min): 41 (2.5%)
- Straight-lining: 19 (1.2%)
- Duplicate IPs: 5 (0.3%)

**Final Sample Size**: 1,500 ✓

### Data Quality Report

#### 1. Completeness

| Variable Category | Mean Missing % | Max Missing % |
|-------------------|----------------|---------------|
| Demographics | 0.3% | 1.2% (income) |
| Political attitudes | 1.1% | 3.8% (one issue item) |
| Social media use | 0.9% | 2.1% (hours on platform) |
| Psychological scales | 1.4% | 2.9% (cognitive closure) |

**Approach to Missing Data**:
- Missing Completely at Random (MCAR) test: Little's MCAR test, χ² = 124.3, p = 0.18 (fail to reject MCAR)
- Imputation: Multiple imputation by chained equations (MICE) with 20 imputations
- Sensitivity analysis: Complete case analysis vs. imputed data

#### 2. Sample Representativeness

Comparison with US Census (ages 18-30):

| Demographic | Sample | US Census | Difference |
|-------------|--------|-----------|------------|
| Female | 51.2% | 49.4% | +1.8% |
| White | 58.3% | 54.8% | +3.5% |
| Hispanic | 24.1% | 26.7% | -2.6% |
| College degree | 38.4% | 41.2% | -2.8% |
| Urban | 42.8% | 43.1% | -0.3% |

**Assessment**: Sample closely matches Census demographics (all differences < 5%). Slight overrepresentation of White respondents; will use survey weights in analysis.

Comparison with Pew Social Media Usage:

| Platform | Sample | Pew (2024) | Difference |
|----------|--------|------------|------------|
| Facebook | 68.2% | 71.0% | -2.8% |
| Instagram | 82.4% | 84.3% | -1.9% |
| TikTok | 59.7% | 62.1% | -2.4% |
| Twitter/X | 38.1% | 36.4% | +1.7% |

**Assessment**: Social media usage patterns closely match national trends ✓

#### 3. Scale Reliability

| Scale | # Items | Cronbach's α | Interpretation |
|-------|---------|--------------|----------------|
| Political ideology | 1 | N/A (single item) | -- |
| Issue positions | 20 | 0.89 | Excellent |
| Affective polarization | 2 | 0.76 | Acceptable |
| Confirmation bias | 4 | 0.81 | Good |
| Open-mindedness | 5 | 0.84 | Good |
| Need for closure | 6 | 0.79 | Acceptable |

**Overall**: All multi-item scales demonstrate adequate to excellent reliability (α > 0.75)

#### 4. Construct Validity

**Known-Groups Validity**:
- Republicans more conservative than Democrats: t(1,498) = 42.3, p < 0.001, d = 2.89 ✓
- Heavy social media users (>4 hrs/day) show higher polarization: t(1,498) = 3.8, p < 0.001, d = 0.31 ✓

**Convergent Validity**:
- Issue positions correlated with ideology: r = 0.78, p < 0.001 ✓
- Affective polarization correlated with ideological extremity: r = 0.45, p < 0.001 ✓

---

## Phase 5: Data Integration and Preparation

### Data Processing Pipeline

**Step 1: Raw Data Import**
```python
import pandas as pd
import numpy as np

# Load Qualtrics export
df_raw = pd.read_csv('data/raw/qualtrics_export_2025-08-15.csv')

# Remove first 2 rows (Qualtrics metadata)
df = df_raw.iloc[2:].reset_index(drop=True)

# Convert data types
df['Age'] = pd.to_numeric(df['Age'])
df['Duration_seconds'] = pd.to_numeric(df['Duration (in seconds)'])
```

**Step 2: Quality Filtering**
```python
# Flag low-quality responses
df['fail_attention_checks'] = (df[['attn1', 'attn2', 'attn3']] != 'correct').sum(axis=1)
df['speeder'] = df['Duration_seconds'] < 480  # < 8 minutes
df['straight_liner'] = df[issue_items].std(axis=1) < 0.5

# Exclude low-quality
df_clean = df[
    (df['fail_attention_checks'] < 2) &
    (~df['speeder']) &
    (~df['straight_liner'])
]

print(f"Excluded: {len(df) - len(df_clean)} ({100*(len(df)-len(df_clean))/len(df):.1f}%)")
```

**Step 3: Variable Construction**

```python
# Political polarization index (absolute distance from center)
df_clean['ideology_extremity'] = abs(df_clean['ideology'] - 4)  # 4 = center of 7-pt scale

# Affective polarization (in-party rating - out-party rating)
df_clean['affective_polarization'] = (
    df_clean['own_party_thermometer'] - df_clean['opposing_party_thermometer']
)

# Issue position polarization (SD across 20 issue items)
issue_cols = [f'issue_{i}' for i in range(1, 21)]
df_clean['issue_consistency'] = df_clean[issue_cols].std(axis=1)

# Social media intensity (total hours per day)
sm_platforms = ['facebook_hours', 'instagram_hours', 'tiktok_hours', 
                'twitter_hours', 'reddit_hours', 'youtube_hours']
df_clean['sm_total_hours'] = df_clean[sm_platforms].fillna(0).sum(axis=1)

# Platform diversity (number of platforms used)
df_clean['platform_count'] = (df_clean[sm_platforms] > 0).sum(axis=1)

# Echo chamber index (network homophily)
df_clean['echo_chamber'] = df_clean['percent_same_views'] / 100  # Convert % to proportion
```

**Step 4: Merge with Secondary Data**

```python
# Load Pew benchmark data
pew_data = pd.read_csv('data/external/pew_social_media_2024.csv')

# Calculate deviation from national average
national_avg_hours = pew_data['avg_sm_hours_18_30'].iloc[0]
df_clean['sm_hours_deviation'] = df_clean['sm_total_hours'] - national_avg_hours

# Load GSS polarization trends
gss_data = pd.read_csv('data/external/gss_cumulative_1972_2022.csv')
# [Further processing to compare with historical trends]
```

**Step 5: Create Analysis-Ready Dataset**

```python
# Select final variables
analysis_vars = [
    # Demographics
    'age', 'gender', 'race_ethnicity', 'education', 'income', 'region', 'urban',
    # Political attitudes
    'ideology', 'party_id', 'ideology_extremity', 'affective_polarization', 'issue_consistency',
    # Social media
    'sm_total_hours', 'platform_count', 'echo_chamber', 'sm_news_pct',
    # Psychological
    'confirmation_bias', 'openness', 'need_closure',
    # Control variables
    'political_interest', 'news_consumption', 'education_years'
]

df_final = df_clean[analysis_vars].copy()

# Save final dataset
df_final.to_csv('data/processed/political_polarization_analysis_2025.csv', index=False)
```

### Descriptive Statistics

| Variable | Mean | SD | Min | Max | N |
|----------|------|----|----|-----|---|
| Age | 24.3 | 3.6 | 18 | 30 | 1,500 |
| Ideology (1-7) | 3.8 | 1.9 | 1 | 7 | 1,500 |
| Ideology extremity | 1.2 | 1.1 | 0 | 3 | 1,500 |
| Affective polarization | 28.4 | 22.1 | -40 | 90 | 1,500 |
| SM total hours/day | 4.2 | 2.8 | 0.5 | 14 | 1,500 |
| Platform count | 3.8 | 1.6 | 1 | 6 | 1,500 |
| Echo chamber (0-1) | 0.64 | 0.23 | 0 | 1 | 1,500 |

---

## Phase 6: Documentation

### Codebook (Excerpt)

```
Variable: ideology
Label: Political Ideology Self-Placement
Type: Ordinal
Values: 1 = Very Liberal, 2 = Liberal, 3 = Slightly Liberal, 
        4 = Moderate, 5 = Slightly Conservative, 
        6 = Conservative, 7 = Very Conservative
Missing: 0.2% (n=3)
Source: Survey Q3.1

Variable: affective_polarization
Label: Affective Polarization Score
Type: Continuous
Range: -100 to 100 (own party rating - opposing party rating)
Interpretation: Higher values = greater in-group favoritism
Missing: 1.8% (n=27)
Source: Calculated from Survey Q3.8-Q3.9
Notes: Feeling thermometers ranged from 0 (very cold) to 100 (very warm)

Variable: sm_total_hours
Label: Total Daily Social Media Usage
Type: Continuous
Range: 0.5 to 14 hours
Measurement: Sum of hours across all platforms
Missing: 0.9% (n=14)
Source: Calculated from Survey Q4.2-Q4.7
```

### Methods Section for Manuscript

```
Data Collection and Sample

We conducted an online survey of US adults aged 18-30 (N=1,500) recruited through
Prolific Academic between March and August 2025. Participants were compensated $2.00
for completing the 15-minute survey. We employed stratified sampling quotas to ensure
representativeness across age, gender, and geographic region.

Data quality was ensured through multiple attention checks, speeding detection, and
straight-lining identification. Responses failing two or more quality checks (7.6%)
were excluded from analysis. The final sample closely matched US Census demographics
(all differences < 5%; see Appendix Table A1).

Measures

Political polarization was measured using three indicators: (1) ideological extremity
(absolute distance from the scale midpoint on a 7-point liberal-conservative scale),
(2) affective polarization (difference between in-party and out-party feeling
thermometer ratings), and (3) issue position consistency (standard deviation across
20 issue items; α = 0.89).

Social media usage was assessed via self-reported daily hours on six major platforms
(Facebook, Instagram, TikTok, Twitter/X, Reddit, YouTube). We calculated total usage
intensity (summed hours) and platform diversity (count of platforms used). Echo
chamber exposure was measured by asking participants to estimate the percentage of
their social media network sharing their political views (network homophily).

Control variables included demographics, education, political interest, and
psychological traits (confirmation bias, open-mindedness, need for cognitive closure).
All scales demonstrated acceptable to excellent reliability (α > 0.75).

Statistical Analysis

We employed ordinary least squares (OLS) regression with robust standard errors to
test associations between social media usage and political polarization. Mediation
analysis (using the PROCESS macro for SPSS) examined whether echo chamber exposure
mediated the relationship between social media intensity and polarization. All analyses
were conducted using R 4.3.1 and controlled for demographic characteristics.

To address potential selection bias, we applied entropy balancing weights to match
heavy social media users (>6 hours/day) with moderate users (2-4 hours/day) on
observable demographics. Sensitivity analyses using alternative polarization measures
and subgroup analyses by party affiliation ensured robustness of findings.

Data Availability

Survey data and analysis code are available at [OSF repository: DOI]. Due to
participant privacy protections, we do not share individual-level social media
network data (collected from the opt-in subsample). Aggregated descriptive statistics
for this subsample are provided in Appendix B.
```

---

## Preliminary Findings

### H1: Social Media Usage and Polarization

| Outcome | β (Usage Hours) | 95% CI | P-value | R² |
|---------|-----------------|--------|---------|-----|
| Ideological extremity | 0.08 | [0.04, 0.12] | <0.001 | 0.23 |
| Affective polarization | 1.52 | [0.88, 2.16] | <0.001 | 0.31 |
| Issue consistency | 0.03 | [0.01, 0.05] | 0.004 | 0.18 |

**Finding**: Higher social media usage significantly associated with all three polarization indicators (H1 supported).

### H2: Platform Diversity

| Comparison | Mean Polarization | Difference | P-value |
|------------|-------------------|------------|---------|
| Single platform users (n=142) | 32.8 | -- | -- |
| Multi-platform users (n=1,358) | 27.6 | -5.2 | 0.02 |

**Finding**: Single-platform users show significantly higher affective polarization than multi-platform users (H2 supported).

### H3: Mediation by Echo Chamber

```
Total effect: SM hours → Polarization (β = 1.52, p < 0.001)
Direct effect: SM hours → Polarization (β = 0.89, p = 0.002)
Indirect effect (via echo chamber): β = 0.63, 95% CI [0.38, 0.91]

Proportion mediated: 41.4%
```

**Finding**: Echo chamber exposure partially mediates the social media-polarization relationship (H3 supported).

---

## Implications and Next Steps

### Key Contributions
1. **Causal Mechanisms**: Identifies echo chamber as key mediator
2. **Platform Diversity**: Novel finding on protective effect of multi-platform use
3. **Methodological**: Demonstrates feasibility of large-scale survey research via Prolific

### Limitations
1. **Cross-sectional design**: Cannot establish causality (longitudinal follow-up planned)
2. **Self-report bias**: Social media usage may be overestimated (objective tracking needed)
3. **Young adult sample**: Findings may not generalize to older adults

### Future Directions
1. **Longitudinal Study**: Track same participants over 12 months to establish temporal ordering
2. **Experimental Intervention**: Randomize participants to increase platform diversity
3. **Digital Trace Data**: Collect actual social media API data (with consent) for validation
4. **Comparative Study**: Replicate in other countries (European democracies, Asia)

---

## Lessons Learned

### What Worked Well
1. **Prolific Recruitment**: High-quality data, excellent demographic controls
2. **Stratified Sampling**: Achieved representativeness without post-hoc weighting
3. **Pilot Study**: Caught survey issues early, minimal revisions needed during main study
4. **Quality Controls**: Only 7.6% excluded (industry standard: 10-15%)

### Challenges
1. **Survey Length**: Some feedback about length despite being within 15-20 min range
2. **Social Desirability Bias**: Some politically extreme respondents may have moderated answers
3. **Twitter API**: Only 22% of sample consented to share username (lower than expected 40%)

### Recommendations for Similar Studies
1. **Over-recruit by 10%**: Account for exclusions even with high-quality platforms
2. **Multiple Attention Checks**: 3 is optimal (2 is too few, 5 causes fatigue)
3. **Pilot with Target Population**: Not just convenience sample (colleagues, students)
4. **Budget for Quality**: Prolific costs more than MTurk but worth it for academic rigor
5. **IRB Timeline**: Allow 4-6 weeks for approval, even for minimal-risk surveys

---

**Project Status**: ✅ Data Collection Complete, Analysis In Progress  
**Sample Size**: 1,500 (target achieved)  
**Quality Score**: 94/100 (Excellent)  
**Time Investment**: 14 weeks (survey development + recruitment + QA + analysis)  
**Next Milestone**: Manuscript submission to *Social Forces* by [DATE]

---

## References

Bail, C. A., et al. (2018). *Exposure to opposing views on social media can increase political polarization*. *Proceedings of the National Academy of Sciences*, 115(37), 9216-9221.

Pariser, E. (2011). *The Filter Bubble: What the Internet Is Hiding from You*. Penguin Press.

Pew Research Center. (2024). *Social Media Use in 2024*. Retrieved from https://www.pewresearch.org/internet/2024/04/10/social-media-use-in-2024/

Sunstein, C. R. (2017). *#Republic: Divided Democracy in the Age of Social Media*. Princeton University Press.

Tucker, J. A., et al. (2018). *Social media, political polarization, and political disinformation: A review of the scientific literature*. William and Flora Hewlett Foundation.

---

**Example Version**: 1.0  
**Last Updated**: 2025-10-31  
**Field**: Sociology, Political Science, Communication Studies  
**Skill**: Research Data Collection v1.0  
**IRB Approved**: Yes (IRB #2025-002)  
**Data Sharing**: Public (OSF)
