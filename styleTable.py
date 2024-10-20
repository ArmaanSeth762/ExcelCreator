import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import pyperclip
import io
import json

def load_config(config_file='table_export_config.json'):
    with open(config_file, 'r') as f:
        return json.load(f)

def rgb_to_hex(rgb):
    if rgb is None:
        return None
    if isinstance(rgb, str):
        return rgb.replace('00', '')  # Remove leading '00' if present
    if hasattr(rgb, 'rgb'):
        return rgb.rgb.replace('00', '')  # Remove leading '00' if present
    if isinstance(rgb, tuple) and len(rgb) == 3:
        return '{:02x}{:02x}{:02x}'.format(*rgb)
    return None

def dataframe_to_html_with_style(df, config, wb=None, ws=None):
    if wb is None:
        wb = openpyxl.Workbook()
    if ws is None:
        ws = wb.active

    # Apply styles based on configuration
    header_fill = PatternFill(
        start_color=config['header']['backgroundColor'],
        end_color=config['header']['backgroundColor'],
        fill_type='solid'
    )
    header_font = Font(
        color=config['header']['fontColor'],
        bold=config['header'].get('bold', False),  # Use the config to determine if header font should be bold
        size=config['header']['fontSize'],
        name=config['font']['family']
    )
    body_font = Font(
        color=config['body']['fontColor'],
        size=config['body']['fontSize'],
        name=config['font']['family']
    )
    alignment = Alignment(
        horizontal=config['alignment']['horizontal'],
        vertical=config['alignment']['vertical'],
        wrap_text=config['alignment'].get('wrapText', True)  # Use the new config option, default to False
    )

    headeralignment = Alignment(
        horizontal=config['headeralignment']['horizontal'],
        vertical=config['headeralignment']['vertical'],
        wrap_text=config['headeralignment'].get('wrapText', True)  # Use the new config option, default to False
    )
    
    # Handle borders based on configuration
    if config['cell'].get('borders', True):
        border = Border(
            left=Side(style=config['cell']['borderStyle'], color=config['cell']['borderColor']),
            right=Side(style=config['cell']['borderStyle'], color=config['cell']['borderColor']),
            top=Side(style=config['cell']['borderStyle'], color=config['cell']['borderColor']),
            bottom=Side(style=config['cell']['borderStyle'], color=config['cell']['borderColor'])
        )
    else:
        border = Border()

    # Calculate column widths based on the maximum length of content in each column
    column_widths = {}
    for c, column in enumerate(df.columns, start=1):
        max_length = max(
            df[column].astype(str).map(len).max(),
            len(str(column))
        )
        adjusted_width = max_length
        column_widths[c] = adjusted_width
        ws.column_dimensions[get_column_letter(c)].width = adjusted_width  # Set column width in Excel

    # Calculate row heights based on font size (optional, can be adjusted as needed)
    row_heights = {}
    for idx, font_size in enumerate([config['header']['fontSize']] + [config['body']['fontSize']] * (len(df) + 1), start=1):
        row_height = font_size * 1.2  # Example multiplier, adjust as needed
        row_heights[idx] = row_height
        ws.row_dimensions[idx].height = row_height  # Set row height in Excel

    # Add header row
    for c, column in enumerate(df.columns, start=1):
        cell = ws.cell(row=1, column=c, value=column)
        cell.alignment = headeralignment
        cell.border = border
        cell.fill = header_fill
        cell.font = header_font
    ws.row_dimensions[1].height = None
    print(config['cell']['wrapThreshold'])
    # Add body rows
    for r, row in enumerate(df.values, start=2):
        for c, value in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=value)
            cell.alignment = alignment
            cell.border = border
            cell.font = body_font

            if len(str(value)) > config['cell']['wrapThreshold']:
                cell.alignment = Alignment(
                    horizontal=config['alignment']['horizontal'],
                    vertical=config['alignment']['vertical'],
                    wrap_text=True  # Enable text wrapping
                )
            
            if r % 2 == 0:
                cell.fill = PatternFill(
                    start_color=config['body']['evenRowBackgroundColor'],
                    end_color=config['body']['evenRowBackgroundColor'],
                    fill_type='solid'
                )
            else:
                cell.fill = PatternFill(
                    start_color=config['body']['oddRowBackgroundColor'],
                    end_color=config['body']['oddRowBackgroundColor'],
                    fill_type='solid'
                )
        ws.row_dimensions[r].height = None
    # Convert the worksheet to HTML
    output = io.StringIO()
    output.write('<table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">')
    for r in range(1, ws.max_row + 1):
        output.write(f'<tr style="height: {row_heights[r]}px;">')
        for c in range(1, ws.max_column + 1):
            cell = ws.cell(row=r, column=c)
            col_width = column_widths[c] * 7 # Convert Excel units to approximate pixels
            style = (
                f'style="padding: {config["cell"]["padding"]}px; '
                f'font-family: {config["font"]["family"]}; '
                f'width: {col_width}px; '
            )

            # Add text wrapping style based on config
            if config['alignment'].get('wrapText', False):
                style += 'white-space: normal; '
            else:
                style += 'white-space: nowrap; overflow: hidden; text-overflow: ellipsis; '

            if r == 1:  # Header row
                style += (
                    f'background-color: #{config["header"]["backgroundColor"]}; '
                    f'color: #{config["header"]["fontColor"]}; '
                    f'font-weight: bold; '
                    f'font-size: {config["header"]["fontSize"]}pt; '
                )
            else:  # Body rows
                bg_color = (
                    config["body"]["evenRowBackgroundColor"]
                    if r % 2 == 0
                    else config["body"]["oddRowBackgroundColor"]
                )
                style += (
                    f'background-color: #{bg_color}; '
                    f'color: #{config["body"]["fontColor"]}; '
                    f'font-size: {config["body"]["fontSize"]}pt; '
                )

            if config['cell'].get('borders', True):
                style += (
                    f'border: {config["cell"]["borderStyle"]} 1px #{config["cell"]["borderColor"]}; '
                )
            else:
                style += 'border: none; '

            style += (
                f'text-align: {config["alignment"]["horizontal"]}; '
                f'vertical-align: {config["alignment"]["vertical"]}; '
                '"'
            )

            output.write(f'<td {style}>{cell.value if cell.value is not None else ""}</td>')
        output.write('</tr>')
    output.write('</table>')
    return output.getvalue(), wb

def copy_table_to_clipboard(df, config_file='table_export_config.json', output_excel_file="output.xlsx"):
    config = load_config(config_file)
    html, wb = dataframe_to_html_with_style(df, config)
    pyperclip.copy(html)
    print("Table copied to clipboard with styling. You can now paste it into Excel.")

    # Save the workbook with all the applied styles
    wb.save(output_excel_file)
    print(f"Excel file saved as {output_excel_file}.")

import table
df = table.df

copy_table_to_clipboard(df)
