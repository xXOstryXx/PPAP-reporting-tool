# Automated PPAP Dimensional Inspection Reporting Tool
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-black)

## The Problem
In metrology and quality control, preparing documentation for PPAP requires processing vast ammounts of measurements. Creating reports and hunting for data anomalies using Excel is time consuming and susceptible to human error.

## The Solution
This project is a fully automated Python pipeline designed to take raw dimensional data (CSV), perform statistical quality analysis and create ready to use reports, being a bridge between metrology and quality documents

## Key Features
* **Automated Data Pipeline:** Cleans and aggregates nested measurement nomenclature across multiple part references.
* **Statistical Anomaly Detection:** Implements outlier detection using Interquartile Range (IQR) and Median Absolute Deviation (MAD), depending on the sample size, to filter natural process variations from critical out-of-tolerance errors.
* **Dynamic PDF Generation:** Automatically compiles PDF reports featuring:
  * Histograms with normal distribution curves.
  * Scatter plots with localized annotations strictly for out-of-bounds measurements.
  * Summary table mapping all outliers to their part IDs and data.
* **Self-Contained Testing Environment:** Includes companion scripts to generate synthetic CMM measurement datasets and mock technical drawings, allowing the tool to be tested without exposing sensitive manufacturing data.

## 📂 Project Structure

```text
Reports generator/
├── Characteristics/                # Folder for mock technical drawings
│   ├── DETAL-A.png                 # Drawing for part A
│   ├── DETAL-B.png                 # Drawing for part B
│   ├── DETAL-C.png                 # Drawing for part C
│   └── DETAL-D.png                # Drawing for part D
├── characteristics_generator.py    # Script generating mock drawings
├── dane_testowe.csv                # Sample dataset(synthetic CMM data)
├── data_generator.py               # Script generating synthetic CSV datasets
├── End_page.jpg                    # Rendered back cover for the report
├── pages_generator.py              # Script rendering cover & end pages
├── main.py            # Main pipeline and PDF compiler
├── raport_statystyczny_2026-09-14.pdf # Output: Final compiled PPAP report
├── README.md                       # Project documentation
└── Title_page.jpg                  # Rendered front cover for the report
