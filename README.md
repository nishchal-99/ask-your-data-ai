# Ask Your Data AI

Ask Your Data AI is an AI-powered data analytics assistant that allows users to upload their own datasets and query them using natural language.

Instead of writing SQL manually, users can ask questions in plain English, and the system generates, validates, explains, and executes SQL queries safely — with results visualized instantly.

## 🚀 Key Features

📊 Core Functionality

- Upload your own CSV files
- Natural Language → SQL conversion
- Schema-aware SQL generation (uses actual dataset structure)
- SQLite database integration
- Automatic result tables and chart visualization

🧠 AI Capabilities

- AI-generated SQL queries using OpenAI
- AI-powered SQL auto-correction when queries fail
- Plain-English SQL explanation
- Context-aware query generation using detected schema

⚠️ Query Safety System

- Risk classification:
  - ✅ Safe → SELECT queries
  - ⚠️ Medium → INSERT, UPDATE
  - 🚨 High → DELETE, DROP, ALTER, TRUNCATE
- Warning system for risky queries
- Mandatory confirmation before execution
- Dry-run preview for DELETE queries (shows affected row count)

🛠️ Product Features

- Query history with timestamps
- Favorite queries support
- Download results as CSV
- Download generated SQL
- Reset query without re-uploading dataset
- Interactive Streamlit UI

## 🧠 How It Works

User uploads CSV
↓
Data is loaded into SQLite
↓
Schema is automatically extracted
↓
User asks a question in English
↓
AI generates SQL using schema context
↓
Safety analyzer checks query risk
↓
Safe queries execute directly
Risky queries require confirmation + dry-run preview
↓
Query executes
↓
Results + Charts displayed
↓
If error → AI auto-fixes SQL
↓
User can view explanation, download results, or save query

## 🏗️ Architecture Overview

User
↓
Streamlit UI
↓

---

| Schema Reader |
| AI SQL Generator |
| Query Safety Analyzer |
| Dry Run Engine |
| Query Executor |
| Error Auto-Fixer (AI) |
| SQL Explainer (AI) |
| History Manager |

---

↓
SQLite Database
↓
Results + Charts + Export

## 🛠️ Tech Stack

- Python
- SQLite
- Streamlit
- OpenAI API
- Pandas
- python-dotenv

## 📊 Example Queries

After uploading a CSV, users can ask:

- Show top 5 rows
- Which category has the highest sales?
- Show total revenue by region
- Find average profit by product
- Monthly sales trends
- Most profitable category
- Delete rows where sales is empty
- Update missing region values to Unknown

## 📸 Screenshots

### Upload CSV

![Upload CSV screen](screenshots/Upload_CSV.png)

### Ask a Question

![Ask a Question screen](screenshots/Ask_A_Question.png)

### Generated SQL

![Generated SQL screen](screenshots/Results.png)

### Chart

![Results and chart screen](screenshots/Charts.png)

⚠️ SQL Safety Behavior

The system does not blindly block queries.

Instead, it intelligently analyzes risk:

Safe Queries

- Executed immediately
- Example: SELECT
  Risky Queries
- Warning displayed
- Risk keywords highlighted
- Confirmation required before execution
  High-Risk Queries (DELETE, DROP, etc.)
- Dry-run preview shows affected rows
- User must explicitly confirm execution

## ⚡ Setup

git clone https://github.com/nishchal-99/ask-your-data-ai.git
cd ask-your-data-ai
pip install -r requirements.txt
