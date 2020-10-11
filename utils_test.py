"""Utils test"""
import unittest
import utils
import pandas as pd
from pandas.testing import assert_frame_equal


class TestUtils(unittest.TestCase):
    """Tests Utils module"""

    def test_convert_date(self):
        """Tests converting date"""
        df = pd.DataFrame({"date":'2020-01-01',"cases": [1],"deaths": [2], "recovered": [3]})
        df = utils.convert_date(df, date_column="date")
        self.assertEqual(df['date'].dtypes, "datetime64[ns]")

    def test_filter_criteria(self):
        """Tests filtering based on a criteria"""
        df = pd.DataFrame(
            {
                "date": ["2020-01-01","2020-01-02", "2020-01-03"],
                "cases": [1,2,3],
                "deaths": [2,4,6],
                "recovered": [3,6,9]
            }
        )
        compare_df = pd.DataFrame({"date":'2020-01-01',"cases": [1],"deaths": [2], "recovered": [3]})
        df = utils.filter_criteria(df, "date", "2020-01-01")
        assert_frame_equal(df, compare_df)

    def test_find_new(self):
        """ Tests finding new entries (by using a diff mechanism)"""
        old_df = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-02", "2020-01-03"],
                "cases": [1, 2, 3],
                "deaths": [2, 4, 6],
                "recovered": [3, 6, 9],
            }
        )

        new_df = pd.DataFrame(
            {
                "date": ["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"],
                "cases": [1, 2, 3, 6],
                "deaths": [2, 4, 6, 8],
                "recovered": [3, 6, 9, 12],
            }
        )
        df = utils.find_new(old_df, new_df)
        diff_df = pd.DataFrame({"date":'2020-01-04',"cases": [6],"deaths": [8], "recovered": [12]})
        assert_frame_equal(df.reset_index(drop=True), diff_df.reset_index(drop=True))


if __name__ == "__main__":
    unittest.main()
