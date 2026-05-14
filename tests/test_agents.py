"""
SwarmSight — Agent Test Suite
Run with: python -m pytest tests/ -v
       or: python tests/test_agents.py
"""
import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd


# ─────────────────────────────────────────────────────────────
# 1. test_schemas — verify all Pydantic schemas instantiate
# ─────────────────────────────────────────────────────────────
class TestSchemas(unittest.TestCase):

    def test_import_schemas(self):
        """All schema classes must be importable from utils.schemas."""
        from utils import schemas
        required = ["PlannerOutput", "CleanerOutput", "AnalystOutput",
                    "ValidatorOutput", "ReporterOutput"]
        for name in required:
            self.assertTrue(hasattr(schemas, name),
                            f"utils.schemas is missing class: {name}")

    def test_planner_output(self):
        from utils.schemas import PlannerOutput
        obj = PlannerOutput(
            analysis_goals=["Find trends", "Detect anomalies"],
            columns_of_interest=["region", "total_price"],
            cleaning_instructions="Drop duplicates, fill nulls with median",
            analysis_strategy="Correlate region vs revenue",
        )
        self.assertIsInstance(obj.analysis_goals, list)
        self.assertGreater(len(obj.analysis_goals), 0)

    def test_cleaner_output(self):
        from utils.schemas import CleanerOutput
        obj = CleanerOutput(
            rows_before=205,
            rows_after=200,
            duplicates_removed=5,
            nulls_fixed=12,
            type_fixes=["order_date → datetime", "unit_price → float"],
            cleaning_summary="Removed 5 dupes, filled 12 nulls with median.",
        )
        self.assertEqual(obj.rows_before - obj.duplicates_removed, obj.rows_after)

    def test_analyst_output(self):
        from utils.schemas import AnalystOutput
        obj = AnalystOutput(
            key_findings=["North region leads revenue by 23%"],
            anomalies=["Order ORD-0042 has unit_price = 0"],
            correlations=[{"columns": ["quantity", "total_price"], "strength": 0.91}],
            summary="Revenue concentrated in North; one pricing anomaly detected.",
        )
        self.assertIsInstance(obj.anomalies, list)

    def test_validator_output(self):
        from utils.schemas import ValidatorOutput
        obj = ValidatorOutput(
            confidence_score=0.88,
            issues_found=[],
            retry_needed=False,
            retry_agent="None",
            validation_notes="All outputs look consistent and complete.",
        )
        self.assertFalse(obj.retry_needed)
        self.assertGreaterEqual(obj.confidence_score, 0.0)
        self.assertLessEqual(obj.confidence_score, 1.0)

    def test_reporter_output(self):
        from utils.schemas import ReporterOutput
        obj = ReporterOutput(
            title="Sales Analysis Report — Q1 2024",
            executive_summary="Revenue grew 12% QoQ driven by North region.",
            key_insights=["Top product: Wireless Headphones ($42k)", "3 sales reps underperforming"],
            recommendations=["Reallocate budget to North region", "Review pricing in East"],
            confidence_score=0.91,
        )
        self.assertIsInstance(obj.key_insights, list)
        self.assertIsInstance(obj.recommendations, list)


# ─────────────────────────────────────────────────────────────
# 2. test_logger — SwarmLogger fires events and callbacks
# ─────────────────────────────────────────────────────────────
class TestLogger(unittest.TestCase):

    def test_logger_logs_events(self):
        from utils.logger import SwarmLogger
        log = SwarmLogger()
        log.log("Planner", "Starting analysis", "info")
        self.assertEqual(len(log.logs), 1)
        self.assertEqual(log.logs[0]["agent"], "Planner")

    def test_logger_callback_fires(self):
        from utils.logger import SwarmLogger
        log = SwarmLogger()
        received = []
        log.set_callback(received.append)
        log.log("Cleaner", "Fixed 5 nulls", "success")
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["status"], "success")

    def test_logger_clear(self):
        from utils.logger import SwarmLogger
        log = SwarmLogger()
        log.log("Analyst", "Running...", "info")
        log.log("Analyst", "Done", "success")
        log.clear()
        self.assertEqual(len(log.logs), 0)

    def test_logger_event_has_timestamp(self):
        from utils.logger import SwarmLogger
        log = SwarmLogger()
        log.log("Validator", "Checking outputs", "info")
        self.assertIn("timestamp", log.logs[0])


# ─────────────────────────────────────────────────────────────
# 3. test_helpers — CSV utilities
# ─────────────────────────────────────────────────────────────
class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "id":    [1, 2, 3, 4, 5],
            "name":  ["Alice", "Bob", None, "Dave", "Eve"],
            "score": [85.0, 92.0, 78.5, None, 88.0],
            "grade": ["A", "A", "B", "B", "A"],
        })

    def test_get_dataset_info_returns_dict(self):
        from utils.helpers import get_dataset_info
        info = get_dataset_info(self.df)
        self.assertIsInstance(info, dict)

    def test_get_dataset_info_contains_shape(self):
        from utils.helpers import get_dataset_info
        info = get_dataset_info(self.df)
        self.assertIn("rows", info)
        self.assertIn("columns", info)
        self.assertEqual(info["rows"], 5)
        self.assertEqual(info["columns"], 4)

    def test_get_dataset_info_reports_nulls(self):
        from utils.helpers import get_dataset_info
        info = get_dataset_info(self.df)
        self.assertIn("null_counts", info)
        self.assertEqual(info["null_counts"]["name"], 1)
        self.assertEqual(info["null_counts"]["score"], 1)

    def test_load_csv_loads_sample(self):
        from utils.helpers import load_csv
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "samples", "sales_data.csv"
        )
        if os.path.exists(sample_path):
            df = load_csv(sample_path)
            self.assertGreater(len(df), 100)
        else:
            self.skipTest("sales_data.csv not found — run Task 1 first")


# ─────────────────────────────────────────────────────────────
# 4. test_cleaner_cleaning — dirty DataFrame gets cleaned
# ─────────────────────────────────────────────────────────────
class TestCleanerCleaning(unittest.TestCase):

    def _make_dirty_df(self):
        """Create a DataFrame with nulls and duplicate rows."""
        rows = [
            {"id": i, "value": float(i * 10), "category": "A"} for i in range(1, 21)
        ]
        # Add nulls
        rows[3]["value"] = None
        rows[7]["value"] = None
        rows[12]["category"] = None
        # Add duplicates
        rows.append(rows[5].copy())
        rows.append(rows[9].copy())
        return pd.DataFrame(rows)

    @patch("agents.base.call_claude")
    def test_cleaner_reduces_nulls(self, mock_call):
        """Cleaner should return a DataFrame with fewer or equal nulls."""
        mock_call.return_value = {
            "rows_before": 22,
            "rows_after": 20,
            "duplicates_removed": 2,
            "nulls_fixed": 3,
            "type_fixes": [],
            "cleaning_summary": "Removed 2 dupes, filled 3 nulls with mode/median.",
        }
        from agents import cleaner
        from utils.schemas import PlannerOutput
        dummy_plan = PlannerOutput(
            analysis_goals=["Test cleaning"],
            columns_of_interest=["value", "category"],
            cleaning_instructions="Fill nulls, drop dupes",
            analysis_strategy="Basic stats",
        )
        dirty_df = self._make_dirty_df()
        null_count_before = dirty_df.isnull().sum().sum()

        df_clean, clean_out = cleaner.run(dirty_df, dummy_plan)

        null_count_after = df_clean.isnull().sum().sum()
        self.assertLessEqual(null_count_after, null_count_before)
        self.assertEqual(clean_out.duplicates_removed, 2)


# ─────────────────────────────────────────────────────────────
# 5. test_full_pipeline — mock Claude, run complete swarm
# ─────────────────────────────────────────────────────────────
class TestFullPipeline(unittest.TestCase):

    def _make_sample_df(self):
        return pd.DataFrame({
            "order_id":    [f"ORD-{i:04d}" for i in range(1, 11)],
            "region":      ["North","South","East","West","North","South","East","West","North","East"],
            "total_price": [100.0, 200.0, 150.0, 300.0, 250.0, 175.0, 225.0, 400.0, 125.0, 275.0],
            "quantity":    [1, 2, 1, 3, 2, 1, 2, 4, 1, 2],
        })

    def _mock_planner(self):
        return {
            "analysis_goals": ["Find top regions"],
            "columns_of_interest": ["region", "total_price"],
            "cleaning_instructions": "No cleaning needed",
            "analysis_strategy": "Group by region",
        }

    def _mock_cleaner(self):
        return {
            "rows_before": 10, "rows_after": 10,
            "duplicates_removed": 0, "nulls_fixed": 0,
            "type_fixes": [], "cleaning_summary": "Data was clean.",
        }

    def _mock_analyst(self):
        return {
            "key_findings": ["North has highest revenue"],
            "anomalies": [],
            "correlations": [{"columns": ["quantity","total_price"], "strength": 0.85}],
            "summary": "North region leads. Quantity strongly correlates with price.",
        }

    def _mock_validator(self):
        return {
            "confidence_score": 0.92,
            "issues_found": [],
            "retry_needed": False,
            "retry_agent": "None",
            "validation_notes": "All outputs verified.",
        }

    def _mock_reporter(self):
        return {
            "title": "Test Report",
            "executive_summary": "North leads revenue.",
            "key_insights": ["North = 37% of total revenue"],
            "recommendations": ["Invest more in North region"],
            "confidence_score": 0.92,
        }

    @patch("agents.base.call_claude")
    def test_full_pipeline_returns_all_keys(self, mock_call):
        """run_swarm() must return all 5 result keys."""
        responses = [
            self._mock_planner(),
            self._mock_cleaner(),
            self._mock_analyst(),
            self._mock_validator(),
            self._mock_reporter(),
        ]
        mock_call.side_effect = responses

        from main import run_swarm
        df = self._make_sample_df()
        results = run_swarm(df, "Find top-performing regions")

        for key in ["plan", "cleaner", "analyst", "validator", "reporter"]:
            self.assertIn(key, results, f"Missing key in results: {key}")

    @patch("agents.base.call_claude")
    def test_pipeline_cleaned_df_in_results(self, mock_call):
        """run_swarm() must include cleaned_df in results."""
        mock_call.side_effect = [
            self._mock_planner(), self._mock_cleaner(), self._mock_analyst(),
            self._mock_validator(), self._mock_reporter(),
        ]
        from main import run_swarm
        results = run_swarm(self._make_sample_df(), "Test goal")
        self.assertIn("cleaned_df", results)
        self.assertIsInstance(results["cleaned_df"], pd.DataFrame)


if __name__ == "__main__":
    unittest.main(verbosity=2)
