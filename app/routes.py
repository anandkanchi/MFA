"""
Flask Routes
Handle all web requests and responses
"""

from flask import Blueprint, render_template, request, jsonify, send_file
from app.mutual_fund_handler import MutualFundHandler
from app.pdf_generator import PDFGeneratorService
from app.excel_converter import ExcelConverterService
from app.projections import ProjectionsCalculator
import pandas as pd
import logging
import os
import json
import numpy as np

logger = logging.getLogger(__name__)

# Custom JSON encoder to handle NaN and Infinity
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.float64, np.float32)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        elif pd.isna(obj):
            return None
        return super().default(obj)

main_bp = Blueprint('main', __name__)

# Global handler instance
mf_handler = MutualFundHandler()


@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@main_bp.route('/api/funds', methods=['GET'])
def get_funds():
    """Get list of available mutual funds"""
    try:
        result = mf_handler.get_fund_list()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting funds: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/fetch-data', methods=['POST'])
def fetch_data():
    """Fetch mutual fund data for given parameters"""
    try:
        data = request.get_json()
        
        fund_name = data.get('fundName')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        
        if not all([fund_name, start_date, end_date]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: fundName, startDate, endDate'
            }), 400
        
        result = mf_handler.fetch_fund_data(fund_name, start_date, end_date)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF report from current data"""
    try:
        data = request.get_json()
        
        current_data = mf_handler.get_current_data()
        if not current_data:
            return jsonify({
                'success': False,
                'message': 'No data available. Please fetch data first.'
            }), 400
        
        df = pd.DataFrame(current_data)
        
        fund_name = data.get('fundName', 'Mutual Fund')
        date_range = {
            'start': data.get('startDate', 'N/A'),
            'end': data.get('endDate', 'N/A')
        }
        
        result = PDFGeneratorService.generate_report(df, fund_name, date_range)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/generate-excel', methods=['POST'])
def generate_excel():
    """Generate Excel file from current data"""
    try:
        current_data = mf_handler.get_current_data()
        if not current_data:
            return jsonify({
                'success': False,
                'message': 'No data available. Please fetch data first.'
            }), 400
        
        df = pd.DataFrame(current_data)
        result = ExcelConverterService.dataframe_to_excel(df)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating Excel: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/preview-data', methods=['GET'])
def preview_data():
    """Get preview of current data"""
    try:
        data = mf_handler.get_current_data()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data available'
            })
        
        # Return limited preview (first 10 rows)
        preview = data[:10]
        total = len(data)
        
        return jsonify({
            'success': True,
            'preview': preview,
            'total_records': total
        })
        
    except Exception as e:
        logger.error(f"Error getting preview: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/download/<file_type>/<filename>', methods=['GET'])
def download_file(file_type, filename):
    """Download generated PDF or Excel file"""
    try:
        from config import Config
        
        if file_type == 'pdf':
            filepath = os.path.join(Config.PDF_FOLDER, filename)
        elif file_type == 'excel':
            filepath = os.path.join(Config.EXCEL_FOLDER, filename)
        else:
            return jsonify({'success': False, 'message': 'Invalid file type'}), 400
        
        if not os.path.exists(filepath):
            logger.error(f"File not found: {filepath}")
            return jsonify({'success': False, 'message': 'File not found'}), 404
        
        logger.info(f"Downloading file: {filepath}")
        
        # Determine MIME type
        if file_type == 'pdf':
            mimetype = 'application/pdf'
        else:
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/convert-pdf-to-excel', methods=['POST'])
def convert_pdf():
    """Convert PDF file to Excel"""
    try:
        data = request.get_json()
        pdf_filename = data.get('pdfFilename')
        
        if not pdf_filename:
            return jsonify({'success': False, 'message': 'PDF filename required'}), 400
        
        pdf_path = os.path.join('data/pdfs', pdf_filename)
        result = ExcelConverterService.pdf_to_excel(pdf_path)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error converting PDF: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Mutual Fund Analyzer'})


@main_bp.route('/api/projections', methods=['POST'])
def get_projections():
    """Calculate and return fund projections"""
    try:
        data = request.get_json()
        projection_days = data.get('projectionDays', 30)
        
        current_data = mf_handler.get_current_data()
        if not current_data:
            return jsonify({
                'success': False,
                'message': 'No data available. Please fetch data first.'
            }), 400
        
        df = pd.DataFrame(current_data)
        
        # Calculate projection
        projection = ProjectionsCalculator.calculate_nav_projection(df, projection_days)
        
        if projection:
            return jsonify({
                'success': True,
                'projection': projection
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not calculate projections'
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting projections: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/analytics', methods=['POST'])
def get_analytics():
    """Calculate and return analytics metrics"""
    try:
        current_data = mf_handler.get_current_data()
        if not current_data:
            return jsonify({
                'success': False,
                'message': 'No data available. Please fetch data first.'
            }), 400
        
        df = pd.DataFrame(current_data)
        
        # Calculate metrics
        metrics = ProjectionsCalculator.calculate_performance_metrics(df)
        
        if metrics:
            return jsonify({
                'success': True,
                'metrics': metrics
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not calculate metrics'
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@main_bp.route('/api/chart-data', methods=['POST'])
def get_chart_data():
    """Get chart data for visualization"""
    try:
        current_data = mf_handler.get_current_data()
        if not current_data:
            return jsonify({
                'success': False,
                'message': 'No data available'
            }), 400
        
        df = pd.DataFrame(current_data)
        chart_data = ProjectionsCalculator.prepare_chart_data(df, group_by_fund=True)
        
        if chart_data:
            return jsonify({
                'success': True,
                'chartData': chart_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not prepare chart data'
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting chart data: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
