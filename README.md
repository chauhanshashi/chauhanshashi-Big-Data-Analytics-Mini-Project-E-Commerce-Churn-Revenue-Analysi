<<<<<<< HEAD
# Big Data Analytics Mini Project: E-Commerce Churn & Revenue Analysis

This mini-project demonstrates a complete end-to-end Big Data Analytics workflow. It focuses on generating/acquiring a large dataset, performing distributed data processing using both Hadoop MapReduce (via `mrjob`) and Apache Spark, and finally running predictive analytics using Spark MLlib.

## Objectives
- **Identify a Big Data Problem**: Analyzing e-commerce transactions to find total revenue per category and predicting customer churn based on purchasing behavior.
- **Data Gathering**: Generating a large-scale synthetic e-commerce dataset representing 1 million transactions.
- **Ecosystem Setup**: Installing dependencies and configuring PySpark to run on Windows (using winutils).
- **Distributed Processing (MapReduce)**: Using the MapReduce programming paradigm to calculate total revenue per category.
- **Distributed Processing (Spark)**: Using Apache Spark for faster in-memory aggregation of the same metric.
- **Comparison**: Visualizing the execution time difference between MapReduce and Spark.
- **Predictive Analytics**: Using Spark MLlib (Random Forest) to predict customer churn based on transaction features.
- **Visualization**: Generating graphs to present insights.

---

## 1. Prerequisites & Setup

### Environment Setup
You need Python 3.8+ installed on your system.
1. Open a terminal in this project directory.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Windows Specific Setup (For Spark)
Spark requires `winutils.exe` to run natively on Windows without throwing errors. 
Run the provided PowerShell script to automatically download it and set `HADOOP_HOME`.
1. Open PowerShell as Administrator (or in a normal window if you just want it for the session).
2. Run the script:
   ```powershell
   .\setup_env.ps1
   ```
*(Note: If you run it as a normal user, the environment variables are only set for that session. You may need to manually add `HADOOP_HOME` to your system environment variables pointing to the created `hadoop` folder).*

---

## 2. Generating the Dataset

Instead of downloading a massive file, we provide a script to generate a synthetic dataset of 1,000,000 rows. This ensures the data is clean, structured, and ready for processing.

```bash
python generate_data.py
```
*This will create `ecommerce_data.csv` (approx 60-70 MB).*

---

## 3. Data Processing

### Phase A: Hadoop MapReduce
We use the `mrjob` library to write a Python script that simulates the MapReduce paradigm. It groups the data by category and sums up the total amount.

```bash
python mapreduce_job.py ecommerce_data.csv > mapreduce_output.txt
```
*(You can also run this on a real Hadoop cluster by appending `-r hadoop` to the command).*

### Phase B: Apache Spark
We use `PySpark` to perform the exact same operation in memory. 

```bash
python spark_processing.py ecommerce_data.csv
```
*This script will save its execution time to `spark_time.txt`.*

---

## 4. Predictive Analytics (Spark MLlib)

We want to predict if a customer will churn based on the `category` they bought from, the `quantity`, and the `price`. We use a Random Forest Classifier.

```bash
python spark_mllib.py ecommerce_data.csv
```
*This script will evaluate the model's Accuracy and F1 Score, extract feature importances, and save these metrics to `ml_metrics.txt`.*

---

## 5. Visualizing Insights

Finally, we visualize the results of our Big Data pipeline.

```bash
python visualize_results.py
```

This will generate three PNG images:
1. `performance_comparison.png`: A bar chart comparing the execution time of MapReduce vs. Spark.
2. `model_performance.png`: The Accuracy and F1 Score of our predictive model.
3. `feature_importance.png`: Shows which features (Category, Quantity, or Price) were most predictive of customer churn.

---

## Conclusion
This project successfully demonstrates the transition from traditional disk-based MapReduce processing to fast, in-memory Spark analytics, as well as the ease of applying Machine Learning models at scale using Spark MLlib.
=======
Big Data Analytics Mini-Project: E-Commerce Churn Revenue Analysis
>>>>>>> a0dc85312bb6f16cacf7e813f53d320a26e2abf1
