"""
PDF Generator
Generates professional PDF reports from mutual fund data
"""

from fpdf import FPDF
from datetime import datetime
import os
from config import Config
import logging

logger = logging.getLogger(__name__)


class MFPDFGenerator(FPDF):
    """Custom PDF class for Mutual Fund reports"""
    
    def header(self):
        """Add header to each page"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Mutual Fund Analysis Report', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
        self.ln(5)
    
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
    
    def add_table(self, df, title=None):
        """Add a table from DataFrame"""
        if title:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, ln=True)
            self.ln(3)
        
        self.set_font('Arial', '', 9)
        
        # Column widths
        col_width = self.w / (len(df.columns) + 1)
        
        # Header
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 9)
        for col in df.columns:
            self.cell(col_width, 8, str(col)[:15], border=1, fill=True)
        self.ln()
        
        # Data rows
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 8)
        for idx, row in df.iterrows():
            for col in df.columns:
                value = str(row[col])[:15]
                self.cell(col_width, 8, value, border=1)
            self.ln()


class PDFGeneratorService:
    """Service to generate PDF reports"""
    
    @staticmethod
    def generate_report(fund_data, fund_name, date_range, output_filename=None):
        """
        Generate PDF report from fund data
        
        Args:
            fund_data (DataFrame): Mutual fund data
            fund_name (str): Name of the fund
            date_range (dict): {'start': date, 'end': date}
            output_filename (str): Output filename
            
        Returns:
            dict: Status and filepath
        """
        try:
            if fund_data is None or fund_data.empty:
                return {'success': False, 'message': 'No data to generate report'}
            
            # Generate filename if not provided
            if not output_filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f'MF_Report_{fund_name}_{timestamp}.pdf'
            
            filepath = os.path.join(Config.PDF_FOLDER, output_filename)
            
            # Create PDF
            pdf = MFPDFGenerator()
            pdf.add_page()
            
            # Title section
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f'Fund Analysis: {fund_name}', ln=True)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, f'Period: {date_range.get("start")} to {date_range.get("end")}', ln=True)
            pdf.ln(5)
            
            # Summary statistics
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, 'Summary Statistics', ln=True)
            pdf.set_font('Arial', '', 10)
            
            summary_data = {
                'Total Records': len(fund_data),
                'Date Range': f'{date_range.get("start")} to {date_range.get("end")}'
            }
            
            # Add numeric statistics if available
            numeric_cols = fund_data.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_cols[:5]:  # First 5 numeric columns
                if len(fund_data) > 0:
                    summary_data[f'{col} (Avg)'] = f'{fund_data[col].mean():.2f}'
            
            for key, value in summary_data.items():
                pdf.cell(0, 8, f'{key}: {value}', ln=True)
            
            pdf.ln(5)
            
            # Data table
            pdf.add_page()
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, 'Fund Data Details', ln=True)
            pdf.ln(3)
            
            # Limit rows for PDF (to avoid huge files)
            display_data = fund_data.head(30)
            pdf.add_table(display_data)
            
            # Save PDF
            pdf.output(filepath)
            
            logger.info(f"PDF generated successfully: {filepath}")
            
            return {
                'success': True,
                'message': 'PDF generated successfully',
                'filepath': filepath,
                'filename': output_filename,
                'size': os.path.getsize(filepath)
            }
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return {
                'success': False,
                'message': f'Error generating PDF: {str(e)}'
            }
