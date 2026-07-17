# 🤖 AI Data Analyst — Agentic AI Project
<img width="1900" height="847" alt="image" src="https://github.com/user-attachments/assets/c0324918-44c6-4279-9090-85ad38bc3b8c" />

**An autonomous AI-powered data analyst that explores, visualizes, and interprets your data using natural language.**

## 📌 Overview

**AI Data Analyst** is an agentic AI project built with Python and Streamlit. It uses the **Groq API** (LLaMA 3.3-70b) to power an autonomous **ReAct (Reason + Act)** loop that plans and executes multi-step data analysis pipelines — without you writing a single line of code.

Just upload a dataset, ask a question in plain English, and watch the agent:
- 🔍 Explore and profile your data
- 📊 Generate beautiful interactive charts
- 🧮 Run statistical and ML analyses
- 🗃️ Execute SQL queries
- 📝 Deliver a full written report with insights

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Agentic ReAct Loop** | Plan → Act → Observe → Reflect → Repeat autonomously |
| 💬 **Natural Language Q&A** | Ask anything about your data in plain English |
| 📂 **Multi-Format Upload** | Supports CSV, Excel (.xlsx), JSON |
| 📊 **Auto Visualization** | Bar, line, scatter, heatmap, histogram, box plots via Plotly |
| 🔍 **Full EDA** | Automated Exploratory Data Analysis in one click |
| 🧠 **ML Insights** | Correlation analysis, outlier detection, K-Means clustering |
| 📈 **Forecasting** | Linear regression time-series forecasting |
| 🗃️ **SQL Agent** | Run natural-language SQL queries on your dataset |
| 🔎 **Outlier Detection** | IQR + Z-score based outlier detection |
| 💾 **Conversation Memory** | Multi-turn contextual analysis sessions |
| 📝 **Report Download** | Auto-generated Markdown analysis reports |
| 🎨 **Premium Dark UI** | Glassmorphism dark theme with animated charts |

---

## 🖥️ Demo

### Main Chat Interface
> Upload a dataset → Ask questions → Get instant AI analysis with charts

**Example questions you can ask:**
```
"Give me a full EDA of this dataset"
"What are the top correlations?"
"Show distribution of all numeric columns"
"Find outliers in the data"
"Cluster the data into 3 groups"
"What are the key trends over time?"
"Run SQL: SELECT department, AVG(salary) FROM df GROUP BY department"
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit + Custom CSS (Dark Glassmorphism) |
| **LLM / Agent** | Groq API — `llama-3.3-70b-versatile` |
| **Agentic Framework** | Custom ReAct Loop (no LangChain) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly Express + Plotly Graph Objects |
| **ML / Stats** | Scikit-learn, SciPy |
| **SQL** | PandasSQL (SQLite on DataFrames) |
| **Reporting** | Markdown2 |

---

## 📁 Project Structure

```
ai-data-analyst/
├── app.py                      # Main Streamlit app & UI
├── agent/
│   ├── __init__.py
│   └── controller.py           # ReAct loop controller (Groq + tool calls)
├── tools/
│   ├── __init__.py
│   ├── registry.py             # 19 tool schemas + central dispatcher
│   ├── data_tools.py           # Data loading, profiling, filtering, grouping
│   ├── chart_tools.py          # Plotly chart generation (6 chart types)
│   ├── stats_tools.py          # Correlation, statistics, missing value analysis
│   ├── ml_tools.py             # Outlier detection, clustering, forecasting
│   └── sql_tools.py            # Natural language SQL on DataFrames
├── utils/
│   ├── __init__.py
│   ├── prompts.py              # System prompt & agent instructions
│   └── report.py               # Markdown report generator
├── requirements.txt
├── .env                        # API keys (not committed to Git)
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- A free [Groq API Key](https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/ai-data-analyst.git
cd ai-data-analyst
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up your API key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

> Get your **free** Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

### Step 5 — Run the app
```bash
# Windows (recommended — avoids encoding issues)
set PYTHONUTF8=1 && streamlit run app.py

# macOS / Linux
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 📖 Usage

### 1. Add your Groq API Key
Paste your key in the **sidebar** under "Configuration", or add it to the `.env` file.

### 2. Load a Dataset
- **Upload your own**: CSV, Excel (.xlsx / .xls), or JSON
- **Use a sample**: Click any sample dataset in the sidebar (Titanic, Iris, Tips, Housing)

### 3. Ask Questions
Type any question in the chat box and hit **Analyze**:

| Question Type | Example |
|---|---|
| EDA | "Give me a complete EDA of this dataset" |
| Comparison | "Compare average salary by department" |
| Distribution | "Show the distribution of Age column" |
| Correlation | "What are the strongest correlations?" |
| Outliers | "Find outliers in the Fare column" |
| Clustering | "Cluster passengers by age and fare into 3 groups" |
| SQL | "Show top 10 rows where salary > 50000" |
| Forecast | "Forecast sales for the next 10 periods" |

### 4. View Agent Trace
Expand **"Agent Trace"** under any response to see exactly how the agent reasoned and which tools it called.

### 5. Download Report
Click **"📥 Report"** in the sidebar to download a Markdown analysis report of the entire session.

---

## 🔧 Tool Registry (19 Tools)

The agent autonomously selects from these tools:

### Data Tools
| Tool | Description |
|---|---|
| `describe_data` | Statistical summary (mean, std, min, max, nulls) |
| `get_column_info` | Column names, dtypes, unique counts |
| `get_sample_data` | Preview first N rows |
| `get_value_counts` | Frequency counts for categorical columns |
| `filter_data` | Filter rows using pandas query syntax |
| `group_aggregate` | GroupBy + aggregation (mean/sum/count/min/max) |

### Chart Tools
| Tool | Description |
|---|---|
| `plot_bar` | Bar chart with optional color grouping |
| `plot_line` | Line / time-series chart |
| `plot_scatter` | Scatter plot with optional trendline |
| `plot_heatmap` | Correlation heatmap |
| `plot_histogram` | Distribution histogram with box marginal |
| `plot_box` | Box plot for outlier visualization |

### Statistics & ML Tools
| Tool | Description |
|---|---|
| `find_correlations` | Pearson correlation matrix + top pairs |
| `run_statistical_summary` | Skewness, kurtosis, percentiles |
| `detect_missing` | Missing value analysis across all columns |
| `detect_outliers` | IQR + Z-score outlier detection |
| `cluster_data` | K-Means clustering |
| `forecast_series` | Linear regression time-series forecast |

### SQL Tool
| Tool | Description |
|---|---|
| `run_sql` | Execute SQL SELECT queries (table name: `df`) |

---

## 🏗️ Architecture

```
User Question (Natural Language)
         ↓
   Streamlit UI
         ↓
┌─────────────────────────────────────────┐
│       AgentController (Groq API)        │
│                                         │
│  1. Build system prompt + df context   │
│  2. Call llama-3.3-70b with tools      │
│  3. Parse tool_calls from response     │
│  4. Dispatch to tool registry           │
│  5. Feed observation back to LLM       │
│  6. Repeat until final answer           │
│     (max 12 iterations)                │
└─────────────────────────────────────────┘
         ↓
  Tool Registry (19 tools)
    ├── data_tools.py
    ├── chart_tools.py
    ├── stats_tools.py
    ├── ml_tools.py
    └── sql_tools.py
         ↓
  Final Answer + Charts + Insights
```

## ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `PYTHONUTF8` | Force UTF-8 on Windows | `1` |
| `PYTHONIOENCODING` | Python IO encoding | `utf-8` |

---

## 📦 Requirements

```
streamlit>=1.35.0
groq>=0.9.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
scipy>=1.11.0
pandasql>=0.7.3
python-dotenv>=1.0.0
openpyxl>=3.1.0
markdown2>=2.4.0
```

---

