"""
Excel Converter
Converts PDF and other data formats to Excel files for analysis
"""

import pandas as pd
import os
from config import Config
import logging
import tabula

logger = logging.getLogger(__name__)


class ExcelConverterService:
    """Service to convert data to Excel format"""
    
    @staticmethod
    def dataframe_to_excel(dataframe, output_filename=None, sheet_name='Data'):
        """
        Convert DataFrame to Excel file
        
        Args:
            dataframe (DataFrame): Data to convert
            output_filename (str): Output filename
            sheet_name (str): Name of the sheet
            
        Returns:
            dict: Status and filepath
        """
        try:
            if dataframe is None or dataframe.empty:
                return {'success': False, 'message': 'No data to export'}
            
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f'MF_Data_{timestamp}.xlsx'
            
            filepath = os.path.join(Config.EXCEL_FOLDER, output_filename)
            
            # Reorder columns: Fund Code, Fund Name, Date, NAV (and any others)
            df = dataframe.copy()
            desired_order = ['Fund Code', 'Fund Name', 'Date', 'NAV']
            existing_cols = [col for col in desired_order if col in df.columns]
            other_cols = [col for col in df.columns if col not in existing_cols]
            df = df[existing_cols + other_cols]
            
            # Create Excel writer
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Style the header using openpyxl
                from openpyxl.styles import Font, PatternFill
                worksheet = writer.sheets[sheet_name]
                
                # Format header row
                header_fill = PatternFill(start_color='3498DB', end_color='3498DB', fill_type='solid')
                header_font = Font(bold=True, color='FFFFFF')
                
                for cell in worksheet[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Excel file created successfully: {filepath}")
            
            return {
                'success': True,
                'message': 'Excel file created successfully',
                'filepath': filepath,
                'filename': output_filename,
                'size': os.path.getsize(filepath),
                'rows': len(df),
                'columns': len(df.columns)
            }
            
        except Exception as e:
            logger.error(f"Error creating Excel file: {str(e)}")
            return {
                'success': False,
                'message': f'Error creating Excel file: {str(e)}'
            }
    
    @staticmethod
    def pdf_to_excel(pdf_path, output_filename=None):
        """
        Convert PDF file to Excel
        
        Args:
            pdf_path (str): Path to PDF file
            output_filename (str): Output filename
            
        Returns:
            dict: Status and filepath
        """
        try:
            if not os.path.exists(pdf_path):
                return {'success': False, 'message': 'PDF file not found'}
            
            # Read PDF tables
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            
            if not tables:
                return {'success': False, 'message': 'No tables found in PDF'}
            
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f'Converted_{timestamp}.xlsx'
            
            filepath = os.path.join(Config.EXCEL_FOLDER, output_filename)
            
            # Write multiple tables to Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for idx, table in enumerate(tables):
                    sheet_name = f'Table_{idx + 1}'
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"PDF converted to Excel successfully: {filepath}")
            
            return {
                'success': True,
                'message': 'PDF converted to Excel successfully',
                'filepath': filepath,
                'filename': output_filename,
                'tables_found': len(tables),
                'size': os.path.getsize(filepath)
            }
            
        except Exception as e:
            logger.error(f"Error converting PDF to Excel: {str(e)}")
            return {
                'success': False,
                'message': f'Error converting PDF to Excel: {str(e)}'
            }
