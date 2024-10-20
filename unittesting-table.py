import unittest
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import io
from datetime import datetime
from algo import get_all_formulas

# Import your main script functions here
from script import *

class TestExcelProcessor(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_files'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def create_test_excel(self, data, filename):
        df = pd.DataFrame(data)
        path = os.path.join(self.test_dir, filename)
        df.to_excel(path, index=False)
        return path

    # def test_mixed_data_types(self):
    #     data = {
    #         'Mixed': [1, 'N/A', 3, 'Unknown', 5],
    #         'Dates': ['2023-01-01', 2, '2023-03-03', 4, '2023-05-05']
    #     }
    #     input_path = self.create_test_excel(data, 'mixed_data_types.xlsx')
        
    #     df = pd.read_excel(input_path)
    #     cleaned_df = clean_dataframe(df)
    #     # print(df)
    #     is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
    #     self.assertTrue(is_text_based[0])  # 'Mixed' column should be text-based
    #     self.assertTrue(is_text_based[1])  # 'Dates' column should be text-based
    #     self.assertEqual(processed_df['Mixed'].tolist(), [1, 'N/A', 3, 'Unknown', 5])
    #     self.assertTrue(all(isinstance(x, (datetime, pd.Timestamp)) for x in processed_df['Dates']))

    def test_unexpected_currency_symbols(self):
        data = {
            'Amount': ['₺100', '₫200', '₦300', '100$', '£400', '500€']
        }
        input_path = self.create_test_excel(data, 'unexpected_currency.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        self.assertFalse(is_text_based[0])  # Should be recognized as numeric
        self.assertEqual(processed_df['Amount'].tolist(), [100.0, 200.0, 300.0, 100.0, 400.0, 500.0])
        self.assertEqual([symbol_matrix[i][0] for i in range(1, len(data['Amount'])+1)], ['₺', '₫', '₦', '$', '£', '€'])

    def test_negative_numbers(self):
        data = {
            'Values': ['-$100', '$-100', '(100)', '-100', '$(100)']
        }
        input_path = self.create_test_excel(data, 'negative_numbers.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        expected = [-100.0] * 5
        self.assertEqual(processed_df['Values'].tolist(), expected)

    def test_percentage_values(self):
        data = {
            'Percentages': ['50%', '50 %', '0.5%', '50 percent', '50', '0.5']
        }
        input_path = self.create_test_excel(data, 'percentages.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        # expected = [0.5, 0.5, 0.005, 0.5, 50.0, 0.5]
        # self.assertEqual(processed_df['Percentages'].tolist(), expected)
        self.assertEqual([symbol_matrix[i][0] for i in range(1, len(data['Percentages'])+1)], ['%', '%', '%', '%', None, None])

    # Implemented with html string
    # def test_merged_cells(self):
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.append(['Header1', 'Header2', 'Header3'])
    #     ws.append(['Merged', '', 'Value1'])
    #     ws.append(['', '', 'Value2'])
    #     ws.merge_cells('A2:B3')
        
    #     path = os.path.join(self.test_dir, 'merged_cells.xlsx')
    #     wb.save(path)
        
    #     df = pd.read_excel(path)
    #     cleaned_df = clean_dataframe(df)
        
    #     self.assertEqual(cleaned_df.iloc[0, 0], 'Merged')
    #     self.assertFalse(pd.isna(cleaned_df.iloc[0, 1]))  # Changed to assertFalse to match the expected behavior
    #     self.assertEqual(cleaned_df.iloc[1, 2], 'Value2')

    def test_insufficient_data(self):
        data = {
            'Sparse': [1, np.nan, np.nan, np.nan, 5],
            'Full': [1, 2, 3, 4, 5]
        }
        input_path = self.create_test_excel(data, 'insufficient_data.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        
        self.assertIn('Full', cleaned_df.columns)
        self.assertNotIn('Sparse', cleaned_df.columns)
        # The behavior for 'Sparse' column depends on your threshold settings

    def test_special_characters(self):
        data = {
            'Special': ['áéíóú', 'ñ', '😊', '∑']
        }
        input_path = self.create_test_excel(data, 'special_characters.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        
        self.assertEqual(cleaned_df['Special'].tolist(), ['áéíóú', 'ñ', '😊', '∑'])

    def test_empty_file(self):
        empty_df = pd.DataFrame()
        path = os.path.join(self.test_dir, 'empty.xlsx')
        empty_df.to_excel(path, index=False)
        
        with self.assertRaises(ValueError):
            df = pd.read_excel(path)
            clean_dataframe(df)

    def test_large_file(self):
        large_data = {'Col' + str(i): range(10000) for i in range(10)}
        input_path = self.create_test_excel(large_data, 'large_file.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        self.assertEqual(len(processed_df), 10000)
        self.assertEqual(len(processed_df.columns), 10)

    def test_corrupted_file(self):
        path = os.path.join(self.test_dir, 'corrupted.xlsx')
        with open(path, 'wb') as f:
            f.write(b'This is not a valid Excel file')
        
        with self.assertRaises(Exception):
            pd.read_excel(path)

    def test_whitespace_and_linebreaks(self):
        data = {
            'Values': [' 1 000 ', '2000 ', ' 3000', '4\n000']
        }
        input_path = self.create_test_excel(data, 'whitespace.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        expected = [1000.0, 2000.0, 3000.0, 4000.0]
        self.assertEqual(processed_df['Values'].tolist(), expected)

    # def test_null_values(self):
    #     data = {
    #         'Values': [1, None, np.nan, 4, 5]
    #     }
    #     input_path = self.create_test_excel(data, 'null_values.xlsx')
        
    #     df = pd.read_excel(input_path)
    #     cleaned_df = clean_dataframe(df)
    #     is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
    #     self.assertTrue(pd.isna(processed_df['Values'][1]))
    #     self.assertTrue(pd.isna(processed_df['Values'][2]))

    def test_complex_numeric_formats(self):
        data = {
            'Values': ['1,234.56', '(2,345.67)', '3.4e5', '5,00,000.00', '-6,789.01']
        }
        input_path = self.create_test_excel(data, 'complex_numeric.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        expected = [1234.56, -2345.67, 340000.0, 500000.0, -6789.01]
        self.assertAlmostEqual(processed_df['Values'].tolist(), expected, places=2)

    def test_mixed_column_types(self):
        data = {
            'Mixed': [1, '2', 3.0, '4.5', 'text', '6,000']
        }
        input_path = self.create_test_excel(data, 'mixed_column_types.xlsx')
        
        df = pd.read_excel(input_path)
        cleaned_df = clean_dataframe(df)
        is_text_based, symbol_matrix, processed_df = preprocess_dataframe(cleaned_df)
        
        expected = [1.0, 2.0, 3.0, 4.5, 'text', 6000.0]
        self.assertEqual(processed_df['Mixed'].tolist(), expected)


if __name__ == '__main__':
    unittest.main()