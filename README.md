### Dummy Network Security Phishing Data Model.

#### Requirements
- The `-e .` in the requirements file is intended to be used by pip instead of `pip install -r requirements.txt`. This will allow anyone who sets up the project to install all the packages and requirements.
- Also, it will make the code modular without relative import headaches! You can import anything from anywhere and it will work.

---

### 💾 Data Ingestion
- The data is pulled from MongoDB Atlas into the pipeline using the `DataIngestion` component.
- The data is saved in two forms:
  - `feature_store`: the raw form saved as a CSV.
  - `ingested`: split into train/test files using the configured `train_test_split_ratio`.
- Each ingestion run creates a timestamped folder under `Artifacts/`.

---

### ✅ Data Validation
- Schema is defined in `data_schema/schema.yaml`.
- We check:
  - Column count.
  - Presence of all required numerical columns.
- Drift detection is done using `ks_2samp` to compare training vs test distributions.
- Drift report is written to a YAML file inside `data_validation/drift_report/report.yaml`.

---

### 🔄 Data Transformation
- Handles preprocessing, including:
  - Cleaning target labels (converting `-1` to `0` for binary classification).
  - Applying transformers (e.g., scalers, imputers, encoders) to features using a pipeline.
- The transformed data is saved as `.npy` files for both train/test.
- The transformation object (preprocessor) is saved as `preprocessing.pkl`.

---

### 🤖 Model Training
- Multiple models are evaluated:
  - LogisticRegression, KNN, DecisionTree, RandomForest, GradientBoosting, AdaBoost.
- We use `RandomizedSearchCV` to tune hyperparameters.
- The best model is selected based on **test accuracy**.
- A custom class `NetworkModel` wraps the final model and the preprocessor.
- The final model is saved as `model.pkl` under `model_trainer/trained_model`.

---

### 🧪 Metrics & Evaluation
- We compute classification metrics: `accuracy`, `precision`, `recall`, `f1_score`.
- Metrics are encapsulated in a `ClassificationMetricArtifact` and saved along with the trained model artifact.
- Overfitting check is available via config threshold (difference between train/test accuracy).

---

### 🪵 Logging
- Logs are managed using a custom `setup_logging()` function.
- Each component logs to a timestamped `.log` file automatically under `logs/`.
- Every method includes detailed try-except blocks that log and raise custom exceptions.

---

### ⚠️ Exception Handling
- Every exception across the entire pipeline is handled using a custom class `NetworkSecurityException`.
- It provides full traceback, custom error codes, and logs with context: file, line number, function.

---

### ☁️ Cloud Integration (MongoDB Atlas)
- Uses `push_data.py` to populate MongoDB Atlas with initial data.
- Connection string and secrets are managed via `.env` and loaded using `dotenv`.

---

### 🔬 Modularity
- The entire project follows a clean architecture:
  - `entity/`: all input and output dataclasses.
  - `components/`: step-by-step logic (ingestion, validation, transformation, trainer).
  - `utils/`: reusable utilities like logging, exception handling, metrics, serialization.
  - `constants/`: centralized config.

---

### 🚀 Pipeline Execution
- The pipeline is triggered via `main.py`, which:
  1. Ingests data.
  2. Validates it.
  3. Transforms it.
  4. Trains the best model.
  5. Logs all artifacts.
- Output artifacts are saved under `Artifacts/{timestamp}/...`.

---

### 📦 Installation & Setup
```bash
git clone https://github.com/EsmaelAwad/End-To-End-ML-Project.git
cd End-To-End-ML-Project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---
