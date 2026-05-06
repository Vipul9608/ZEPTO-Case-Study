# 🛒 Zepto Customer Analytics Dashboard

An interactive Streamlit dashboard for exploring the Zepto customer dataset (10,000 records).

## 📊 Features

- **KPI Cards** — Total customers, average age, states & cities covered  
- **Gender Distribution** — Donut chart  
- **Age Group Breakdown** — Bar chart with `pd.cut` buckets  
- **Monthly Signups Trend** — Line chart over 2023–2024  
- **Top 10 States** — Horizontal bar chart  
- **City Share** — Interactive treemap  
- **Age by Gender** — Violin + box plot  
- **State × Gender Heatmap** — Pivot heatmap  
- **Sidebar Filters** — Year, Gender, State, Age range  
- **Download** — Export filtered data as CSV  

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/zepto-dashboard.git
cd zepto-dashboard

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The dashboard opens at **http://localhost:8501**

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (make sure `Zepto_Dataset.xlsx` is included)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, and set **Main file path** to `app.py`
4. Click **Deploy** — done! 🎉

## 📁 Project Structure

```
zepto-dashboard/
├── app.py               # Main Streamlit application
├── Zepto_Dataset.xlsx   # Source data (10 000 rows × 8 cols)
├── requirements.txt     # Python dependencies
├── .gitignore
└── .streamlit/
    └── config.toml      # Theme & server settings
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Web app framework |
| Pandas | Data wrangling |
| Plotly Express | Interactive charts |
| OpenPyXL | Excel file reading |
