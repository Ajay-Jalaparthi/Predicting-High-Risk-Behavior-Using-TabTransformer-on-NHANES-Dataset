# 🧠 Predicting High-Risk Behavior Using TabTransformer on NHANES Dataset

This project uses the **NHANES (National Health and Nutrition Examination Survey)** dataset to predict an individual's likelihood of engaging in **hard drug usage** based on demographic and behavioral features.

A custom neural network based on **TabTransformer** (Transformer for tabular data) is implemented to classify individuals into high-risk and low-risk groups.

---

## 🚀 Highlights

- Cleaned and preprocessed real-world health data (NHANES)
- Encoded categorical variables using `category_encoders`
- Scaled numerical data with `StandardScaler`
- Implemented a custom **TabTransformer** with self-attention layers
- Trained a binary classifier to predict `HardDrugs` usage
- Saved and loaded the model to make real-time predictions
- Output includes a **Predicted Risk Score** with a clear risk flag

---

## 📊 Dataset

The dataset used is a version of NHANES (National Health and Nutrition Examination Survey).  
Download the CSV from the official [ProjectMOSAIC GitHub repository](https://github.com/ProjectMOSAIC/NHANES):

> 🔗 [NHANES.csv](https://github.com/ProjectMOSAIC/NHANES/blob/master/data-raw/NHANES.csv)

Place the file in the same directory as the code.

---

## 🏗️ Features Used

- Gender
- Age
- Education
- Marital Status
- Age of first sexual activity
- Number of sexual partners in life

Target:
- **HardDrugs** (Binary: Yes/No)

---

## 🧪 Model Architecture

```text
Input → Linear → Multi-Head Self Attention → ReLU → Linear → Sigmoid
