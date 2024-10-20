import pandas as pd
import algo
from importlib import reload
reload(algo)
from algo import *
from io import StringIO
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
import logging
logging.basicConfig(level=logging.INFO)

def remove_rows_above_main_data(df, threshold=0.3):
    """
    Remove rows above the main data based on a threshold of populated cells.
    """
    total_columns = len(df.columns)
    required_populated_cells = threshold * total_columns

    for idx, (index, row) in enumerate(df.iterrows()):
        populated_cells = row.count()
        if populated_cells >= required_populated_cells:
            # Main data starts here
            df = df.iloc[idx:].reset_index(drop=True)
            break
    return df

def remove_empty_left_columns(df, threshold=0.5):
    """
    Remove empty columns on the left until a column meets the populated cell threshold.
    """
    total_rows = len(df)
    required_populated_cells = threshold * total_rows

    columns = df.columns.tolist()
    for col in columns:
        populated_cells = df[col].count()
        if populated_cells >= required_populated_cells:
            # Main data column found
            break
        else:
            # Drop the column
            df = df.drop(columns=col)
    return df

def merge_insufficient_columns(df, threshold=0.7):
    """
    Merge columns with insufficient data into the next column.
    TODO: improve robustness of this function
    """
    total_rows = len(df)
    required_populated_cells = threshold * total_rows

    columns = df.columns.tolist()
    i = 0
    columns_to_drop = []

    while i < len(columns) - 1:
        col = columns[i]
        populated_cells = df[col].count()
        if populated_cells < required_populated_cells:
            next_col = columns[i + 1]
            # Combine current column into the next column
            df[next_col] = df[col].fillna('') + ' ' + df[next_col].fillna('')
            columns_to_drop.append(col)
            i += 1  # Move to next column
        else:
            break
    df = df.drop(columns=columns_to_drop)
    return df

def remove_empty_rows_and_columns(df):
    """
    Remove rows and columns that are entirely empty.
    """
    df = df.dropna(axis=0, how='all')  # Drop empty rows
    df = df.dropna(axis=1, how='all')  # Drop empty columns
    return df

def general_data_cleaning(df):
    """
    Perform general data cleaning operations.
    """
    # Apply strip only to string columns
    for col in df.columns:
        # Check if the column contains any string values
        if df[col].apply(lambda x: isinstance(x, str)).any():
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def clean_dataframe(df):
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(map(str, col)).strip() for col in df.columns.values]
    try:
        df = remove_rows_above_main_data(df)
        # logging.info("Removed rows above main data.")
    except Exception as e:
        logging.error(f"Error removing rows: {e}")

    try:
        df = remove_empty_left_columns(df)
        # logging.info("Removed empty left columns.")
    except Exception as e:
        logging.error(f"Error removing columns: {e}")

    try:
        df = merge_insufficient_columns(df)
        # logging.info("Merged insufficient columns.")
    except Exception as e:
        logging.error(f"Error merging columns: {e}")

    try:
        df = remove_empty_rows_and_columns(df)
        # logging.info("Removed empty rows and columns.")
    except Exception as e:
        logging.error(f"Error removing empty rows/columns: {e}")

    try:
        df = general_data_cleaning(df)
        # logging.info("Performed general data cleaning.")
    except Exception as e:
        logging.error(f"Error in general data cleaning: {e}")
    df.reset_index(drop=True, inplace=True)
    return df

def convert_to_float(data):
    data
    if data is None or pd.isna(data):
        return None, None
    elif isinstance(data, (float, int)):
        return float(data), None
    elif isinstance(data, str):
        data = ' '.join(data.strip().split()).replace(" ","")
        value=data
        currency_symbols = ['$', '€', '£', '¥', '₹', '₽', '₩', '₪', 'Fr', 'kr', 'R$', 'A$', 'C$', '₺', '₫', '₦']
        symbol = None
        
        if "%"  in value:
            symbol = "%"
            value = value.replace("%", "")
        elif "percent"  in value:
            symbol = "%"
            value = value.replace("%", "")
        else:
            for curr_symbol in currency_symbols:
                if curr_symbol in value:
                    symbol = curr_symbol
                    value = value.replace(curr_symbol, "")
                    break
        
        value = value.replace(",", "").replace("'", "")
        if value == "-":
            return None, None
        if "(" in value and ")" in value:
            value = "-" + value.strip("()")

        try:
            return float(value), symbol
        except ValueError:
            return data, None  # Return the original string if it can't be converted
    else:
        return None, None

def preprocess_dataframe(df):
    """
    Preprocess the DataFrame for formula calculations.
    Args:
    df (pd.DataFrame): Input DataFrame
    Returns:
    tuple: (list of bool indicating text-based columns, matrix of symbols, preprocessed DataFrame)
    """

    # Create a matrix of symbols and preprocess the DataFrame
    symbol_matrix =[]
    threshold=0.3

    # Backup original columns
    original_df = df.copy()
    is_text_based = [False] * len(df.columns)  # Initialize all columns as not text-based
    for i, col in enumerate(df.columns):
        symbol_col = []
        
        for index in range(len(df)):
            value, symbol = convert_to_float(df.at[index, col])
            symbol_col.append(symbol)
            df.at[index, col] = value
        
        # After the end of the row loop, determine if the column is text-based
        if sum(isinstance(x, str) or x is None for x in df[col].values) > threshold * len(symbol_col):
            for index in range(len(df)):
                if df.at[index, col] is None or isinstance(df.at[index, col], str):
                    if symbol_col[index]!='date':
                        df.at[index, col] = original_df.at[index, col]  # Replace with original value if None or string
                        symbol_col[index]=None
            is_text_based[i] = True  # Column remains text-based if any value is None or string
        else:
            is_text_based[i] = False  # Mark column as not text-based
        symbol_matrix.append(symbol_col)
    symbol_matrix = [list(row) for row in zip(*symbol_matrix)]
    symbol_matrix=[[None]*len(df.columns)]+symbol_matrix
    return is_text_based, symbol_matrix, df


def save_excel(file_path, output_path, row_skip, col_skip, formula_sign, is_text_based, symbol_matrix):
    # Load the workbook and get the active sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    max_row = sheet.max_row
    max_col = sheet.max_column

    # Define a bold font style
    bold_font = Font(bold=True)
    
    # Define wrap text alignment for both rows and columns
    wrap_alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
    
    # Iterate over all cells in the sheet
    for row_sheet in range(1, max_row + 1):
        for col_sheet in range(1, max_col + 1):
            cell = sheet.cell(row=row_sheet, column=col_sheet)
            cell.alignment = wrap_alignment

    # Track rows that have formulas
    rows_with_formulas = []
    
    # Iterate over the columns starting from the column after the skipped columns
    for col_sheet in range(col_skip, max_col + 1):
        col = get_column_letter(col_sheet)
        col_index = col_sheet - col_skip

        # Check if the column is text-based
        if not is_text_based[col_index]:
            # If not text-based, apply formulas and symbols
            # Check if the first cell in the column is empty
            first_cell_empty = sheet[col + str(row_skip + 1)].value is None or sheet[col + str(row_skip + 1)].value == ""


            # Iterate over the rows starting from the row after the skipped rows
            for row_sheet in range(row_skip + 1, max_row + 1):
                row = row_sheet - (row_skip + 1)
                cell = sheet[col + str(row_sheet)]

                if len(formula_sign[row]) > 0:
                    generated_formula = "="  # Initialize the formula string
                    for i in formula_sign[row]:
                        # Check if the referred cell value is 0 and the first cell is empty
                        referred_cell = sheet[col + str(abs(i) + row_skip)]
                        if referred_cell.value == 0 and first_cell_empty:
                            continue  # Skip this cell reference in the formula
                        
                        if generated_formula != "=":
                            generated_formula += " + " if i > 0 else " - "
                        elif i < 0:
                            generated_formula += "-"
                        generated_formula += col
                        generated_formula += str(abs(i) + row_skip)
                    
                    if generated_formula != "=":
                        cell.value = generated_formula  # Set the cell value to the generated formula
                        rows_with_formulas.append(row_sheet)  # Track the row with a formula
                    else:
                        cell.value = 0  # Set to 0 if all references were removed
                else:
                    # If no formula is present, ensure the value is a float
                    cell.value = convert_to_float(cell.value)[0]

                # Apply symbol if present in symbol_matrix
                if symbol_matrix[row-1][col_index]:
                    cell.number_format = f'0.00{symbol_matrix[row-1][col_index]}'

        # Set a reasonable default column width
        sheet.column_dimensions[col].width = 15

    # Apply bold formatting to the entire rows that have formulas
    for row in rows_with_formulas:
        for col_row in range(1, max_col + 1):
            sheet.cell(row=row, column=col_row).font = bold_font

    # Force recalculation of all cell formulas
    for sheet in workbook.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.data_type == 'f':
                    cell.value = cell.value

    print("File successfully saved!")
    workbook.save(output_path)  # Save the workbook to the specified output path
    workbook.close()  # Close the workbook

def html_to_dataframe(html):
    df_list = pd.read_html(StringIO(html), header=[0, 1])  
    if df_list:
        return df_list[0]
    else:
        raise ValueError("No tables found in the provided HTML string.")
    
def run(html):
    df = html_to_dataframe(html)
    row_skip = max([len(col) for col in df.columns]) if isinstance(df.columns, pd.MultiIndex) else 1
    df=clean_dataframe(df)
    is_text_based, symbol_matrix, df = preprocess_dataframe(df)
    col_skip=0
    while(col_skip<len(is_text_based) and is_text_based[col_skip]): col_skip+=1
    all_columns = []
    for column in df.columns:
        ls = df[column].values.tolist()
        for i in range(len(ls)):
            if isinstance(ls[i], str):
                try:
                    ls[i] = float(ls[i].replace(',', '').replace(" ","").strip())  # Remove commas and convert to float
                except ValueError:
                    ls[i] = 0.0  # If conversion fails, set to 0.0
            elif pd.isna(ls[i]):
                ls[i] = 0.0
        all_columns.append(ls)
    all_columns=all_columns[col_skip:]
    formulas=get_all_formulas(all_columns)
    df.to_excel("tmp.xlsx", index=False)
    save_excel('tmp.xlsx', 'tmp.xlsx', row_skip, col_skip, formulas, is_text_based, symbol_matrix)
    return row_skip, col_skip, is_text_based, symbol_matrix, all_columns, formulas
