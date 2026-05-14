"""
SwarmSight — Sample Data Validation Tests
Run with: python -m pytest tests/test_data.py -v
       or: python tests/test_data.py

Verifies that each CSV in data/samples/ has the expected shape and columns.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

SAMPLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "samples"
)

EXPECTED = {
    "sales_data.csv": {
        "min_rows": 100,
        "required_columns": [
            "order_id", "customer_id", "product_name", "category",
            "quantity", "unit_price", "total_price", "order_date",
            "region", "sales_rep"
        ],
    },
    "employee_survey.csv": {
        "min_rows": 100,
        "required_columns": [
            "employee_id", "department", "tenure_years", "satisfaction_score",
            "engagement_score", "manager_rating", "would_recommend", "last_promotion_date"
        ],
    },
    "iot_sensors.csv": {
        "min_rows": 100,
        "required_columns": [
            "sensor_id", "location", "temperature", "humidity",
            "pressure", "battery_level", "timestamp", "status"
        ],
    },
}


class TestSampleData(unittest.TestCase):

    def _load(self, filename):
        path = os.path.join(SAMPLES_DIR, filename)
        if not os.path.exists(path):
            self.skipTest(f"{filename} not found in data/samples/ — run Task 1 first")
        return pd.read_csv(path)

    # ── sales_data.csv ──────────────────────────────────────
    def test_sales_data_exists(self):
        path = os.path.join(SAMPLES_DIR, "sales_data.csv")
        self.assertTrue(os.path.exists(path), "sales_data.csv not found")

    def test_sales_data_min_rows(self):
        df = self._load("sales_data.csv")
        self.assertGreaterEqual(len(df), 100,
            f"Expected ≥100 rows, got {len(df)}")

    def test_sales_data_columns(self):
        df = self._load("sales_data.csv")
        for col in EXPECTED["sales_data.csv"]["required_columns"]:
            self.assertIn(col, df.columns, f"Missing column: {col}")

    def test_sales_data_has_nulls(self):
        """sales_data.csv should have intentional nulls to test the Cleaner."""
        df = self._load("sales_data.csv")
        total_nulls = df.isnull().sum().sum()
        self.assertGreater(total_nulls, 0,
            "sales_data.csv has no nulls — Cleaner won't have anything to fix")

    def test_sales_data_numeric_prices(self):
        df = self._load("sales_data.csv")
        numeric_df = pd.to_numeric(df["unit_price"], errors="coerce")
        valid_prices = numeric_df.dropna()
        self.assertGreater(len(valid_prices), 0,
            "unit_price column has no valid numeric values")

    # ── employee_survey.csv ─────────────────────────────────
    def test_employee_survey_exists(self):
        path = os.path.join(SAMPLES_DIR, "employee_survey.csv")
        self.assertTrue(os.path.exists(path), "employee_survey.csv not found")

    def test_employee_survey_min_rows(self):
        df = self._load("employee_survey.csv")
        self.assertGreaterEqual(len(df), 100,
            f"Expected ≥100 rows, got {len(df)}")

    def test_employee_survey_columns(self):
        df = self._load("employee_survey.csv")
        for col in EXPECTED["employee_survey.csv"]["required_columns"]:
            self.assertIn(col, df.columns, f"Missing column: {col}")

    def test_employee_survey_score_range(self):
        """Most satisfaction scores should be between 1 and 10."""
        df = self._load("employee_survey.csv")
        scores = pd.to_numeric(df["satisfaction_score"], errors="coerce").dropna()
        in_range = scores[(scores >= 1) & (scores <= 10)]
        self.assertGreater(len(in_range) / len(scores), 0.8,
            "Less than 80% of satisfaction scores are in range 1-10")

    def test_employee_survey_recommend_values(self):
        """would_recommend should contain 'yes' and 'no' values."""
        df = self._load("employee_survey.csv")
        values = df["would_recommend"].str.lower().unique().tolist()
        self.assertTrue(
            any(v in ["yes", "no"] for v in values),
            f"Unexpected would_recommend values: {values}"
        )

    # ── iot_sensors.csv ─────────────────────────────────────
    def test_iot_sensors_exists(self):
        path = os.path.join(SAMPLES_DIR, "iot_sensors.csv")
        self.assertTrue(os.path.exists(path), "iot_sensors.csv not found")

    def test_iot_sensors_min_rows(self):
        df = self._load("iot_sensors.csv")
        self.assertGreaterEqual(len(df), 100,
            f"Expected ≥100 rows, got {len(df)}")

    def test_iot_sensors_columns(self):
        df = self._load("iot_sensors.csv")
        for col in EXPECTED["iot_sensors.csv"]["required_columns"]:
            self.assertIn(col, df.columns, f"Missing column: {col}")

    def test_iot_sensors_has_anomalies(self):
        """IoT data should have anomalous temperature readings."""
        df = self._load("iot_sensors.csv")
        temps = pd.to_numeric(df["temperature"], errors="coerce").dropna()
        anomalies = temps[(temps > 50) | (temps < 0)]
        self.assertGreater(len(anomalies), 0,
            "No anomalous temperature readings found — Analyst won't have anomalies to detect")

    def test_iot_sensors_status_values(self):
        """Status column should include 'active', 'inactive', or 'error'."""
        df = self._load("iot_sensors.csv")
        valid_statuses = {"active", "inactive", "error"}
        found = set(df["status"].str.lower().unique())
        overlap = valid_statuses & found
        self.assertGreater(len(overlap), 0,
            f"Status column has unexpected values: {found}")


if __name__ == "__main__":
    # Print a pass/fail summary at the end
    import unittest
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*50)
    print(f"SUMMARY: {result.testsRun} tests run")
    print(f"  ✅ Passed:  {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  ❌ Failed:  {len(result.failures)}")
    print(f"  💥 Errors:  {len(result.errors)}")
    print("="*50)
