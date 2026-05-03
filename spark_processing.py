from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, round
import time
import sys

def main(input_file):
    print("Initializing Spark Session...")
    spark = SparkSession.builder \
        .appName("EcommerceRevenueByCategory") \
        .master("local[*]") \
        .getOrCreate()
        
    # Suppress verbose logging
    spark.sparkContext.setLogLevel("ERROR")
    
    start_time = time.time()
    
    print(f"Reading data from {input_file}...")
    # Read the CSV file into a DataFrame
    df = spark.read.csv(input_file, header=True, inferSchema=True)
    
    print("Processing data...")
    # Perform the aggregation: Revenue by Category
    result = df.groupBy("category") \
               .agg(round(sum("total_amount"), 2).alias("total_revenue"))
               
    # Action to trigger computation and print results
    result.show()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Spark Execution Time: {execution_time:.2f} seconds")
    
    # Save the execution time to a file for later comparison
    with open("spark_time.txt", "w") as f:
        f.write(str(execution_time))
        
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: spark_processing.py <input_csv_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    main(input_file)
