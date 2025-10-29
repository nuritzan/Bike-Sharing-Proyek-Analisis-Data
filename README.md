# 🚲 Bike Sharing Data Analysis

An end-to-end exploratory data analysis project using the **Bike Sharing Dataset** from Kaggle.  
This project aims to understand **user behavior** and identify **key factors influencing bike rental demand** based on season, weather, and working days.  
It also demonstrates data cleaning, transformation, visualization, and dashboard development using Python.

---

## 🧩 1. Problem Statement
Urban bike-sharing systems experience fluctuating demand influenced by weather, season, and commuting patterns.  
Understanding these factors is essential for improving **bike availability**, **resource allocation**, and **urban mobility planning**.

---

## 🎯 2. Objectives
- Explore patterns and correlations that affect bike rental usage.  
- Perform data cleaning, transformation, and exploratory data analysis (EDA).  
- Visualize insights through interactive charts and dashboards.  
- Provide data-driven insights that can support better decision-making for transportation planning.

---

## 🧠 3. Dataset & Scope
- **Source:** [Kaggle - Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)  
- **Size:** 17,379 records  
- **Features:** Temperature, humidity, wind speed, season, weather, holiday, working day, and rental counts  
- **Preprocessing:** Handled missing values, normalized numeric features, and converted date/time columns.

---

## ⚙️ 4. Methodology
1. **Data Import & Cleaning:** Loaded dataset, removed duplicates, handled missing values.  
2. **Feature Engineering:** Created new features for seasonal and hourly patterns.  
3. **EDA (Exploratory Data Analysis):** Analyzed trends using Matplotlib and Seaborn.  
4. **Visualization & Dashboard:** Built an interactive dashboard using Streamlit for dynamic exploration.  

---

## 📊 5. Key Findings
- **Peak Seasons:** Highest bike rental demand occurs in **summer**, lowest in **winter**.  
- **Weather Impact:** **Clear weather** drives the most rentals, while rain and snow reduce demand significantly.  
- **User Behavior:** **Registered users** dominate weekdays; **casual users** are more active during weekends.  
- **Time Patterns:** Peak hours occur during **7–9 AM** and **5–7 PM**, matching commuter periods.  

---

## 🚀 6. Results / Output
- Processed **17,000+ records** and ensured 100% data integrity after cleaning.  
- Created **5 visualizations** illustrating seasonal and hourly demand trends.  
- Developed an **interactive Streamlit dashboard** for real-time exploration of usage patterns.  
- Presented findings applicable for **urban transportation planning** and **bike availability optimization**.

---

## Setup Environment - Shell/Terminal
mkdir Proyek_Analisis_Data<br>
cd Proyek_Analisis_Data<br>
pipenv install<br>
pipenv shell<br>
pip install -r requirements.txt

## Run steamlit app
streamlit run Dashboard-Streamlit.py
