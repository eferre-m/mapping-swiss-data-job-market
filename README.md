# Mapping the Swiss Data Job Market

> **A data-driven exploration of the Swiss labour market for Data, Research and Customer Insights careers.**

---

# Abstract

The Swiss labour market is often described as highly competitive, particularly for junior candidates entering Data and Research careers.

Rather than relying on assumptions or general advice, this project approaches the job search as a data analysis problem.

By collecting, structuring and analysing Swiss job offers, the objective is to better understand market expectations, compare them with my own profile and document the recruitment process over time.

This repository combines research methodology, data analysis and visual communication to transform a personal career transition into a reproducible analytical project.

---

# Research Question

> **How can I become a competitive candidate for Data & Research roles in Switzerland?**

This project is organised around three complementary research questions.

---

## 1. Understanding the Market

**What does the Swiss Data & Research job market actually demand?**

The first objective is to build a structured database of Swiss job offers in order to identify market expectations.

The analysis focuses on:

- Technical skills
- Soft skills
- Languages
- Experience requirements
- Sectors
- Geographic distribution
- Salary information (when available)

---

## 2. Understanding My Position

**How does my current profile compare with market expectations?**

Every collected job offer is compared with my own profile in order to estimate my current level of correspondence.

The objective is not simply to obtain a percentage, but to identify:

- my strongest competencies
- the skills most frequently missing
- the competencies with the greatest impact on future employability

---

## 3. Understanding the Recruitment Process

**What factors appear to influence recruitment outcomes?**

Every application is documented throughout the recruitment process.

The objective is to analyse questions such as:

- Which offers generate interviews?
- At which recruitment stage do applications stop?
- Does profile matching correlate with interview invitations?
- Which competencies appear to influence recruitment outcomes?

---

# Why this project?

My academic background is in Sociology, where I learned to formulate research questions, collect information and analyse complex social phenomena.

Later, Documentary Photography taught me another way of observing reality: selecting meaningful information and communicating it visually.

Today, as I transition towards Data & Research roles, I wanted to combine these experiences into a single project.

Rather than creating a portfolio based on fictional datasets, I chose to work on a real problem that directly concerns me.

Every new job offer becomes a new observation.

Every application enriches the dataset.

Every recruitment process contributes to a better understanding of the Swiss labour market.

This repository is therefore both a personal research project and a practical learning journey in Data Analytics.

---

# Methodology

The project follows a simple analytical workflow.

```text
Swiss Job Offers
        │
        ▼
Information Extraction
        │
        ▼
Standardised Database
        │
        ├──────────────┐
        ▼              ▼
Market Analysis   Profile Matching
        │              │
        └──────┬───────┘
               ▼
Recruitment Analysis
```

---

## Data Collection

Job offers are collected from public recruitment platforms and official company websites.

Each offer is archived before being analysed.

---

## Information Extraction

The information contained in each job description is converted into a standardised structure.

This process extracts relevant variables such as:

- required technical skills
- languages
- experience level
- education
- responsibilities
- location
- contract type

The extracted information is manually verified before integration into the database.

---

## Database Construction

Every job offer is stored using the same structure in order to facilitate comparisons and future analyses.

The database continuously grows as new opportunities are identified.

---

## Data Analysis

The database is analysed to identify trends within the Swiss labour market.

Examples include:

- frequency of technical skills
- language requirements
- experience expectations
- regional differences
- sector comparisons

---

## Profile Matching

Each job offer is compared with my own profile.

The objective is to estimate my correspondence with the market while identifying the competencies that would provide the greatest improvement.

---

## Recruitment Tracking

Applications are monitored throughout the recruitment process.

The collected information will allow future analyses of recruitment outcomes and possible relationships between profile matching and interview success.

---

# Dataset

The database currently includes information organised into several categories.

### Company Information

- Company
- Industry
- Location
- Canton
- Contract type

### Technical Skills

- Python
- SQL
- Excel
- Power BI
- Tableau
- Databricks
- AI tools

### Languages

- French
- German
- Italian
- English

### Candidate Requirements

- Education
- Experience
- Soft skills

### Recruitment

- Date of application
- Recruitment stage
- Outcome

---

# Repository Structure

```
mapping-swiss-data-job-market/

│

├── data/
│   ├── raw/
│   ├── processed/
│   └── catalogs/
│
├── prompts/
│
├── scripts/
│
├── notebooks/
│
├── dashboard/
│
├── visualisations/
│
├── images/
│
└── README.md
```

---

# Automation

To improve consistency and reduce manual work, job descriptions are processed using a structured extraction workflow.

Current workflow:

```
Job Offer

↓

Structured Prompt

↓

LLM-assisted Extraction

↓

Manual Verification

↓

Database
```

Future versions will progressively automate this workflow using Python scripts.

---

# Visualisations

The project will progressively include visual analyses created with:

- Excel
- Tableau
- Python (Matplotlib / Plotly)

Examples:

- Skills frequency
- Language distribution
- Market trends
- Profile matching
- Recruitment statistics

*(Visualisations will be added as the project progresses.)*
