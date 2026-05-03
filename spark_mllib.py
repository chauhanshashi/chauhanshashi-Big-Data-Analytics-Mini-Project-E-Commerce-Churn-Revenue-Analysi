from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
import sys

def main(input_file):
    print("Initializing Spark Session for MLlib...")
    spark = SparkSession.builder \
        .appName("EcommerceChurnPrediction") \
        .master("local[*]") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("ERROR")
    
    print(f"Reading data from {input_file}...")
    df = spark.read.csv(input_file, header=True, inferSchema=True)
    
    # We want to predict 'churn' based on 'category', 'quantity', and 'price'
    
    # 1. Index the categorical column 'category'
    indexer = StringIndexer(inputCol="category", outputCol="category_index")
    
    # 2. Assemble features into a vector
    assembler = VectorAssembler(
        inputCols=["category_index", "quantity", "price"],
        outputCol="features"
    )
    
    # 3. Scale the features (Optional but good practice)
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
    
    # 4. Define the classifier
    rf = RandomForestClassifier(labelCol="churn", featuresCol="scaledFeatures", numTrees=10)
    
    # 5. Create a Pipeline
    pipeline = Pipeline(stages=[indexer, assembler, scaler, rf])
    
    # Split data into training and test sets (80% / 20%)
    train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
    
    print("Training Random Forest model...")
    # Train the model
    model = pipeline.fit(train_data)
    
    print("Making predictions on test data...")
    # Make predictions
    predictions = model.transform(test_data)
    
    # Evaluate the model
    evaluator_acc = MulticlassClassificationEvaluator(
        labelCol="churn", predictionCol="prediction", metricName="accuracy"
    )
    accuracy = evaluator_acc.evaluate(predictions)
    
    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="churn", predictionCol="prediction", metricName="f1"
    )
    f1_score = evaluator_f1.evaluate(predictions)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    print(f"Model F1 Score: {f1_score:.4f}")
    
    # Extract Feature Importances
    rf_model = model.stages[-1]
    importances = rf_model.featureImportances
    
    print("\nFeature Importances:")
    print(f"Category: {importances[0]:.4f}")
    print(f"Quantity: {importances[1]:.4f}")
    print(f"Price: {importances[2]:.4f}")
    
    # Save the metrics to a file for visualization
    with open("ml_metrics.txt", "w") as f:
        f.write(f"{accuracy},{f1_score},{importances[0]},{importances[1]},{importances[2]}")
        
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: spark_mllib.py <input_csv_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    main(input_file)
