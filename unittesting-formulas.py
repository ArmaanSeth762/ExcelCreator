import unittest
from algo import get_all_formulas
from script import *
import pandas as pd
import random

class TestExcelTableCreator(unittest.TestCase):

    def test_all_none_values(self):
        data = [[None, None, None, None]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], []])

    def test_no_solution_exists(self):
        data = [[2, 4, 8, 16, 31]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [], []])

    def test_negative_numbers(self):
        data = [[5, -3, 1, None, 9]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [], [1, -2, 3]])

    def test_zero_values(self):
        data = [[0, 0, 0, 0]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], []])

    # TODO: decide
    def test_duplicate_values(self):
        data = [[1, 2, 2, 4], [1,3, 2, 5]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [2, 3]])

    def test_exceeding_recursion_depth(self):
        data = [[1] * 1000]
        try:
            result = get_all_formulas(data)
            self.assertTrue(True)  # If it reaches here, no RecursionError was raised
        except RecursionError:
            self.fail("RecursionError was raised")

    def test_non_numeric_data_types(self):
        data = [[1, 'A', 3, 4]]
        with self.assertRaises(TypeError):
            get_all_formulas(data)

    def test_mixed_integers_and_floats(self):
        data = [[1.0, 2, 3.5, 6.5]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [1, 2, 3]])

    def test_floating_point_precision_errors(self):
        data = [[0.1, 0.2, 0.3]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [1, 2]])

    def test_large_numbers(self):
        data = [[1e12, 2e12, 3e12]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [1, 2]])

    # TODO: FInd solution
    def test_ambiguous_formulas(self):
        data = [[1, 2, 3, 6], [1, 2, 4, 7]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [1, 2, 3]])

    def test_zero_tolerance_for_integers(self):
        data = [[1, 2, 4]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], []])

    def test_non_linear_relationships(self):
        data = [[2, 3, 6]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], []])

    def test_empty_sign_list(self):
        data = [[5]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[]])

    def test_multiple_none_in_a_row(self):
        data = [[1, None, None, 4]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], []])

    def test_inconsistent_column_lengths(self):
        data = [
            [1, 3, 4, None],
            [2, 4, 6]
        ]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [1, 2], []])

    #TODO: Decide number of fowrard lookahead to check
    # def test_nested_formulas_across_columns(self):
    #     data = [
    #         [2, 4, 6, 8],
    #         [1, 1, 1, 1]
    #     ]
    #     result = get_all_formulas(data)
    #     self.assertEqual(result, [[], [], [], []])


    def test_multi_column_synchronization_requirement(self):
        data = [
            [1, None, 3, None],
            [2, None, 4, None]
        ]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], []])

    def test_non_numeric_data_in_adjacent_columns(self):     
        data = pd.DataFrame({
            'Numeric': [5, 10, 15, 20],
            'Letters': ['A', 'B', 'C', 'D']
        })
        _, _, all_columns=prepare(data)
        result=get_all_formulas(all_columns)
        self.assertEqual(result, [[], [], [], []])

    def test_large_multi_column_dataset(self):
        data = [
            list(range(1, 101)),
            [x * 2 for x in range(1, 101)],
            [x ** 2 for x in range(1, 101)]
        ]
        result = get_all_formulas(data)
        self.assertTrue(len(result) == 100)  # Ensure we get a result for each row

    def test_dataset_with_random_missing_values(self):
        random.seed(42)  # For reproducibility
        data = [
            [random.randint(1, 100) if random.random() > 0.1 else None for _ in range(100)]
        ]
        result = get_all_formulas(data)
        self.assertEqual(len(result), 100)

    def test_high_precision_floating_point_numbers(self):
        data = [[0.3333333333, 0.6666666667, 1.0]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [1, 2]])

    def test_formulas_requiring_reuse_of_values(self):
        data = [[2, None, None, 8]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], []])

    #TODO: decide
    def test_negative_results_and_subtraction(self):
        data = [[10, 5, None, -5]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [-1, 2]])

    def test_accumulating_errors_with_floating_point_arithmetic(self):
        data = [[0.1, 0.2, 0.5, 0.9, 1.7]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [], [1, 2, 3, 4]])

    def test_extremely_large_values(self):
       data = pd.DataFrame({"Large_values": [1e100, 2e100, 3e100]})
       row_skip, col_skip, all_columns=prepare(data)
       result = get_all_formulas(all_columns)
       self.assertEqual(result, [[], [], [1, 2]])

    def test_extremely_small_values(self):
       data = [[1e-100, 2e-100, 3e-100]]
       result = get_all_formulas(data)
       self.assertEqual(result, [[], [], [1, 2]])

    def test_mixed_positive_and_negative_zeros(self):
       data = [[0, -0, 0.0, -0.0, 0]]
       result = get_all_formulas(data)
       self.assertEqual(result, [[], [], [], [], []])

    def test_exponential_growth_sequence(self):
        data = [[1, 2, 4, 8, 16, 32, 64]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [], [], [], [], []])  # Assuming it can't find multiplicative formulas

    def test_decimal_precision_edge_cases(self):
        from decimal import Decimal
        data = [[Decimal('0.1'), Decimal('0.2'), Decimal('0.3')]]
        result = get_all_formulas(data)
        self.assertEqual(result, [[], [], [1, 2]])

if __name__ == '__main__':
    unittest.main()