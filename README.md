# Malnutrition Research Automation

A reproducible Python-based research automation pipeline for statistical analysis of child malnutrition data.

## Project Overview

This project demonstrates how a complete statistical research workflow can be automated using Python. The pipeline starts from raw data and performs data validation, cleaning, exploratory data analysis, statistical modelling, model diagnostics, publication table generation, publication figure generation, and automated research report creation.

The project was developed as a research-oriented portfolio project to demonstrate practical skills in statistics, data analysis, machine learning, reproducible research, and Python automation.

## Research Objectives

The main objectives of this project are to:

* Build a reproducible statistical analysis workflow.
* Automate common data preparation and analysis tasks.
* Explore factors associated with child malnutrition outcomes.
* Evaluate logistic regression models for multiple binary outcomes.
* Assess multicollinearity among numerical predictors.
* Generate publication-ready tables and figures automatically.
* Produce an automated Word research report.

## Dataset

The practice dataset contains **2,000 observations and 15 variables** related to child malnutrition.

### Outcome Variables

* Stunting
* Wasting
* Underweight

### Numerical Predictors

* Age in months
* Birth weight
* Dietary diversity
* Maternal BMI

### Categorical Predictors

* Sex
* Mother’s education
* Wealth index
* Urban/rural residence
* Sanitation
* Water source
* Immunization

The dataset used in this repository is a practice dataset created for demonstrating the research automation workflow.

## Analytical Workflow

The project follows a structured analysis pipeline:

```text
Data Import
    ↓
Data Validation
    ↓
Data Cleaning
    ↓
Missing Value Assessment
    ↓
Descriptive Statistics
    ↓
Data Visualization
    ↓
Correlation Analysis
    ↓
VIF / Multicollinearity Assessment
    ↓
Logistic Regression
    ↓
Model Diagnostics
    ↓
Publication Tables
    ↓
Publication Figures
    ↓
Automated Research Report
```

## Statistical Methods

The following statistical methods were implemented:

### Descriptive Analysis

For numerical variables:

* Mean
* Standard deviation
* Minimum
* Median
* Maximum

For categorical variables:

* Frequency
* Percentage

### Correlation Analysis

Pearson correlation coefficients were calculated among numerical predictor variables.

A correlation threshold of |r| ≥ 0.70 was used to identify potentially strong correlations.

### Multicollinearity Assessment

Variance Inflation Factor (VIF) was used to assess multicollinearity among numerical predictors.

A VIF threshold of 5 was used as the primary screening criterion.

### Logistic Regression

Separate logistic regression models were fitted for:

1. Stunting
2. Wasting
3. Underweight

Both numerical and categorical predictors were included in the models.

### Model Evaluation

Model performance was assessed using:

* Accuracy
* Sensitivity
* Specificity
* ROC-AUC
* Confusion matrix
* True positives
* True negatives
* False positives
* False negatives

## Project Structure

```text
malnutrition-research-automation/
│
├── config/
│   └── config.yaml
│
├── src/
│   ├── 00_test_config.py
│   ├── 01_import.py
│   ├── 02_validation.py
│   ├── 03_cleaning.py
│   ├── 04_missing.py
│   ├── 05_descriptive.py
│   ├── 06_visualization.py
│   ├── 07_correlation.py
│   ├── 08_vif.py
│   ├── 09_regression.py
│   ├── 10_diagnostics.py
│   ├── 11_tables.py
│   ├── 12_figures.py
│   └── 13_report.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Script Description

| Script                | Purpose                                   |
| --------------------- | ----------------------------------------- |
| `00_test_config.py`   | Tests project configuration               |
| `01_import.py`        | Imports and inspects the dataset          |
| `02_validation.py`    | Performs variable and data validation     |
| `03_cleaning.py`      | Cleans the dataset and removes duplicates |
| `04_missing.py`       | Assesses and handles missing values       |
| `05_descriptive.py`   | Generates descriptive statistics          |
| `06_visualization.py` | Creates exploratory visualizations        |
| `07_correlation.py`   | Performs correlation analysis             |
| `08_vif.py`           | Assesses multicollinearity using VIF      |
| `09_regression.py`    | Fits logistic regression models           |
| `10_diagnostics.py`   | Evaluates model performance               |
| `11_tables.py`        | Generates publication tables              |
| `12_figures.py`       | Generates publication figures             |
| `13_report.py`        | Generates an automated Word report        |

## Key Results

The automated analysis produced the following outcome prevalence estimates in the practice dataset:

| Outcome     | Prevalence |
| ----------- | ---------: |
| Stunting    |     38.85% |
| Wasting     |     25.05% |
| Underweight |     31.75% |

The numerical descriptive analysis showed:

| Variable          |         Mean |    SD |
| ----------------- | -----------: | ----: |
| Age               | 30.06 months | 17.28 |
| Birth weight      |      2.98 kg |  0.45 |
| Dietary diversity |         3.83 |  1.99 |
| Maternal BMI      |        21.99 |  2.93 |

### Multicollinearity

The VIF analysis identified high VIF values for:

* Birth weight: VIF = 30.001
* Maternal BMI: VIF = 31.920

Age and dietary diversity had comparatively acceptable VIF values.

### Logistic Regression Performance

The models achieved the following ROC-AUC values on the test data:

| Outcome     | ROC-AUC |
| ----------- | ------: |
| Stunting    |  0.7047 |
| Wasting     |  0.6438 |
| Underweight |  0.6857 |

Among the three models, the stunting model showed the highest ROC-AUC.

These results are based on a practice dataset and should not be interpreted as estimates of the actual population prevalence or determinants of malnutrition.

## Technologies Used

* Python
* Pandas
* NumPy
* SciPy
* Matplotlib
* Seaborn
* Scikit-learn
* Statsmodels
* OpenPyXL
* Python-docx
* PyYAML
* Git
* GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/dhrony66-dev/malnutrition-research-automation.git
```

Move into the project directory:

```bash
cd malnutrition-research-automation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Pipeline

The individual analysis scripts can be executed sequentially:

```bash
python src/00_test_config.py
python src/01_import.py
python src/02_validation.py
python src/03_cleaning.py
python src/04_missing.py
python src/05_descriptive.py
python src/06_visualization.py
python src/07_correlation.py
python src/08_vif.py
python src/09_regression.py
python src/10_diagnostics.py
python src/11_tables.py
python src/12_figures.py
python src/13_report.py
```

The generated tables, figures, and reports are saved locally in the project's results and reports directories.

## Reproducibility

The project is designed around a reproducible workflow. Configuration settings are stored separately in `config/config.yaml`, while individual analysis stages are organized into independent Python scripts.

This structure makes it easier to adapt the pipeline to appropriately structured research datasets.

## Limitations

This repository uses a practice dataset for demonstration purposes. Therefore:

* The results are not intended to represent a real population.
* Causal relationships cannot be inferred from the analysis.
* The current workflow focuses primarily on logistic regression.
* External validation has not been performed.
* More advanced statistical and machine learning models can be incorporated in future versions.

## Future Improvements

Planned improvements include:

* Automated feature selection
* LASSO regression
* Random Forest
* XGBoost
* SHAP-based model interpretation
* Hyperparameter tuning
* Cross-validation
* Automated statistical reporting
* Automated model comparison
* Support for additional research datasets
* Reproducible publication-ready outputs

## Skills Demonstrated

This project demonstrates practical experience in:

**Statistical Analysis**

* Descriptive statistics
* Correlation analysis
* Multicollinearity assessment
* Logistic regression
* Model diagnostics

**Data Science**

* Data cleaning
* Exploratory data analysis
* Data visualization
* Predictive modelling
* Model evaluation

**Research Automation**

* Reproducible workflows
* Automated tables
* Automated figures
* Automated report generation
* Configuration-based analysis

**Programming and Tools**

* Python
* Git
* GitHub
* VS Code
* Virtual environments

## Author

**Delwar Hossan Rony**

BSc (Honours) in Statistics

Bangladesh

## License

This project is intended for educational, research, and portfolio purposes.

