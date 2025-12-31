##End to End Data science project in Network Security 

# End-to-End Network Security ML Project 

An **industry-grade end-to-end Machine Learning project** for Network Security (Phishing / Malicious URL detection) built with a **production-ready architecture**, covering the complete ML lifecycle from data ingestion to deployment.

---

##  Project Overview

This project detects **malicious or phishing network URLs** using machine learning techniques.  
It is designed following **real-world data science & MLOps best practices**, including experiment tracking, data versioning, logging, exception handling, and containerized deployment.

---

##  Industry-Level Architecture

✔ Modular folder structure  
✔ Config-driven pipeline  
✔ Proper logging & custom exception handling  
✔ Artifact-based pipeline outputs  
✔ Scalable & production-ready design  

network_security/
│
├── Artifacts/ # Pipeline outputs (ingestion, validation, models)
├── data_schema/ # Schema validation (schema.yaml)
├── Network_Data/ # Raw / source data
├── final_model/ # Trained & best model
├── logs/ # Centralized logging
│
├── networksecurity/ # Core source package
│ ├── components/ # Data ingestion, validation, transformation, training
│ ├── pipeline/ # Training & prediction pipelines
│ ├── utils/ # Utility functions
│ ├── exception/ # Custom exception handling
│ ├── logging/ # Logging configuration
│ └── entity/ # Config & artifact entities
│
├── app.py # Application entry point
├── main.py # Training pipeline trigger
├── Dockerfile # Docker configuration
├── requirements.txt # Dependencies
├── setup.py # Package setup
└── README.md


---

## ⚙️ Tech Stack Used

- **Python**
- **Scikit-learn**
- **MongoDB Atlas** – Cloud database
- **MLflow** – Experiment tracking & model registry
- **DagsHub** – Dataset & experiment versioning
- **Docker** – Containerization & deployment
- **Git & GitHub** – Version control

---

## 🔄 ML Pipeline Flow

1. **Data Ingestion**
   - Data fetched from MongoDB Atlas
2. **Data Validation**
   - Schema validation using YAML
3. **Data Transformation**
   - Feature engineering & preprocessing
4. **Model Training**
   - Multiple ML models trained & evaluated
5. **Experiment Tracking**
   - Metrics, parameters & artifacts logged via MLflow
6. **Best Model Selection**
7. **Model Saving**
8. **Dockerized Deployment**

---

## 📊 Experiment Tracking

- All experiments are tracked using **MLflow**
- Integrated with **DagsHub** for:
  - Code versioning
  - Experiment history
  - Artifact storage

---

## 🐳 Docker Support

Build Docker image:
```bash
docker build -t shrinathrajput04/networksecurityproject.app .

docker run -p 8000:8000 shrinathrajput04/networksecurityproject.app



