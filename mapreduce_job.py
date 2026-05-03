from mrjob.job import MRJob
from mrjob.step import MRStep
import csv
import time

class MRRevenueByCategory(MRJob):
    
    def configure_args(self):
        super(MRRevenueByCategory, self).configure_args()
        self.add_passthru_arg('--time', action='store_true', default=False, help='Print execution time')

    def mapper_init(self):
        self.start_time = time.time()
        
    def mapper(self, _, line):
        # Skip the header row
        if line.startswith('transaction_id'):
            return
            
        # Parse the CSV line
        # Columns: transaction_id,date,customer_id,product_id,category,quantity,price,total_amount,churn
        row = next(csv.reader([line]))
        
        try:
            category = row[4]
            total_amount = float(row[7])
            yield category, total_amount
        except (IndexError, ValueError):
            pass

    def combiner(self, category, amounts):
        # Optimization: Combine amounts locally before sending to reducer
        yield category, sum(amounts)

    def reducer(self, category, amounts):
        yield category, round(sum(amounts), 2)
        
    def reducer_final(self):
        if self.options.time:
            end_time = time.time()
            # Note: In a real distributed cluster, this time is only for this node.
            # For local execution, it gives a rough estimate.
            # print(f"Execution time: {end_time - self.start_time} seconds")
            pass

    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]

if __name__ == '__main__':
    MRRevenueByCategory.run()
