# 🏎️ F1 Virtual Pit Wall: Dynamic Race Strategy Optimizer

A **real-time Formula 1 strategy optimization engine** that predicts tire degradation and computes the optimal pit stop window using **Machine Learning + Dynamic Programming**.

Includes an **AI Race Engineer (Google Gemini-powered)** that explains strategy choices in plain English — like you're talking to your real race engineer on the pit wall.

---

## 🚀 Features

- **📊 Real-Time Strategy Optimization**  
  Dynamic Programming algorithm that evaluates 1-stop vs 2-stop strategies instantly.

- **🧠 ML Tire Degradation Models**  
  Linear Regression models trained on fastf1 telemetry data to forecast tire wear.

- **🎧 AI Race Engineer**  
  Uses Google Gemini LLM to provide context-aware insights (E.g. _"Why is the 2-stop faster?"_).

- **🏎️ Interactive Dashboard**  
  React-based visualization of sawtooth race pace patterns and stint deltas.

---

## 🛠️ Tech Stack

| Component   | Technologies Used |
|------------|-------------------|
| **Frontend** | React.js, Chart.js, Axios |
| **Backend** | FastAPI, Uvicorn, Python |
| **Data Science** | Pandas, Scikit-Learn, NumPy, FastF1 |
| **AI / LLM** | Google Generative AI — Gemini 1.5 Flash |

---

## 📂 Project Structure

F1-Virtual-Pit-Wall/
├── backend/ # FastAPI Server & Strategy Logic
│ ├── app/services/ # AI & Optimization Algorithms
│ └── ml_models/ # Trained .pkl machine learning models
├── frontend/ # React Dashboard
└── notebooks/ # Notebooks for data extraction + training


---

## ⚡ Quick Start

### 1. Backend Setup — Python

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```
Create .env inside /backend:

```bash
GEMINI_API_KEY=your_api_key_here
```
Run server:
```bash
uvicorn main:app --reload
```

### 2. Frontend Setup — React

```bash
cd frontend
npm install
npm start
```

---

## 🧪 How It Works

### 1. Data Ingestion: 
We fetch historical race data (lap times, tire compounds) using the fastf1 library.

### 2. Training: 
We train a regression model to learn the "Degradation Coefficient" (how much time a tire loses per lap).

### 3. Simulation: 
The backend runs a simulation of the remaining race laps for every possible strategy combination.

### 4. Optimization: 
The system minimizes the Total Race Time function:
```math
T_{total} = \sum_{l=1}^{L} T_{lap}(age) + N_{stops} \times T_{loss}
```

### 5. Explanation: 
The optimal result is sent to Google Gemini, which translates the math into a "Team Radio" message.

---

## 🔮 Future Scope

- Live timing integration for real Grand Prix weekends
- Telemetry support for Sim Racing (F1 24 / iRacing)
- Safety Car probability modeling (stochastic optimization)

