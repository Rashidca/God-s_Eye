import csv
import datetime

class CSVLogger:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self._create_csv_if_not_exists()

    def _create_csv_if_not_exists(self):
        try:
            with open(self.csv_file, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "cam1", "cam2", "cam3", "cam4"])  # Write header
        except FileExistsError:
            pass  # If file exists, continue without writing the header again

    def log_data(self, timestamp, cam1, cam2=1, cam3=2, cam4=3):
        data = [timestamp, cam1, cam2, cam3, cam4]
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)