"""
Mutual Fund Data Handler
Fetches and processes mutual fund data from various sources
"""

import pandas as pd
from datetime import datetime, timedelta
import json
import os
from mftool import Mftool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MutualFundHandler:
    """Handle mutual fund data operations"""
    
    def __init__(self):
        self.mf_tool = Mftool()
        self.fund_data = None
    
    def fetch_fund_data(self, fund_name, start_date, end_date):
        """
        Fetch mutual fund data for a given company and date range
        
        Args:
            fund_name (str): Name of the mutual fund
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            dict: Status and data
        """
        try:
            # Validate dates
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start > end:
                return {
                    'success': False,
                    'message': 'Start date cannot be after end date'
                }
            
            if (end - start).days > 365:
                return {
                    'success': False,
                    'message': 'Date range cannot exceed 365 days'
                }
            
            logger.info(f"Fetching data for {fund_name} from {start_date} to {end_date}")
            
            # Fetch all available scheme codes
            schemes = self.mf_tool.get_scheme_codes()
            
            # Filter by fund name (case-insensitive)
            matching_schemes = []
            for scheme_code, scheme_name in schemes.items():
                # Skip header row
                if scheme_code == 'Scheme Code':
                    continue
                
                scheme_name_lower = scheme_name.lower() if isinstance(scheme_name, str) else ''
                if fund_name.lower() in scheme_name_lower:
                    matching_schemes.append({
                        'code': scheme_code,
                        'name': scheme_name,
                        'category': 'Mutual Fund'
                    })
            
            if not matching_schemes:
                return {
                    'success': False,
                    'message': f'No funds found matching: {fund_name}'
                }
            
            # Collect data for all matching funds
            all_data = []
            for scheme in matching_schemes[:5]:  # Limit to first 5 matches for performance
                try:
                    scheme_code = scheme['code']
                    scheme_name_full = scheme['name']
                    
                    # Convert date format to DD-MM-YYYY for mftool API
                    start_fmt = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
                    end_fmt = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
                    
                    # Fetch historical NAV data using the correct method
                    hist_data = self.mf_tool.get_scheme_historical_nav_for_dates(
                        scheme_code,
                        start_fmt,
                        end_fmt,
                        as_dataframe=True
                    )
                    
                    if hist_data is not None and len(hist_data) > 0:
                        # If it's already a DataFrame
                        if hasattr(hist_data, 'columns'):
                            df = hist_data
                        else:
                            df = pd.DataFrame(hist_data)
                        
                        df['Fund Name'] = scheme_name_full
                        df['Fund Code'] = scheme_code
                        all_data.append(df)
                        logger.info(f"Fetched {len(df)} records for {scheme_name_full}")
                        
                except Exception as e:
                    logger.warning(f"Error fetching data for {scheme['name']}: {str(e)}")
                    continue
            
            if not all_data:
                return {
                    'success': False,
                    'message': 'Could not fetch historical data for the selected funds'
                }
            
            # Combine all data
            self.fund_data = pd.concat(all_data, ignore_index=True)
            
            # Sort by date if available
            if 'Date' in self.fund_data.columns:
                self.fund_data['Date'] = pd.to_datetime(self.fund_data['Date'], format='%d-%m-%Y', errors='coerce')
                self.fund_data = self.fund_data.sort_values('Date')
            
            # Clean data: replace NaN and Inf with None/null
            self.fund_data = self.fund_data.replace({
                'NaN': None,
                float('nan'): None,
                float('inf'): None,
                float('-inf'): None
            })
            
            # Convert to dictionary with proper handling
            data_dict = self.fund_data.to_dict('records')
            
            # Clean each record
            for record in data_dict:
                for key, value in list(record.items()):
                    # Handle NaN, Inf values
                    if pd.isna(value) or (isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf'))):
                        record[key] = None
                    # Convert numpy types to Python types
                    elif hasattr(value, 'item'):
                        record[key] = value.item()
                    # Keep datetime as string
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.strftime('%Y-%m-%d')
                    elif isinstance(value, (int, float)):
                        # Try to keep numeric precision but avoid NaN
                        try:
                            if pd.isna(value):
                                record[key] = None
                            else:
                                record[key] = float(value) if isinstance(value, float) else int(value)
                        except:
                            record[key] = None
            
            logger.info(f"Successfully fetched {len(self.fund_data)} total records")
            
            return {
                'success': True,
                'message': 'Data fetched successfully',
                'record_count': len(self.fund_data),
                'funds_found': len(matching_schemes),
                'data': data_dict
            }
            
        except ValueError as e:
            return {
                'success': False,
                'message': f'Invalid date format. Use YYYY-MM-DD: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Error fetching fund data: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching data: {str(e)}'
            }
    
    def get_fund_list(self):
        """Get list of available mutual funds"""
        try:
            schemes = self.mf_tool.get_scheme_codes()
            
            # Format for frontend (limit to first 100 for performance)
            fund_list = []
            count = 0
            for scheme_code, scheme_name in schemes.items():
                # Skip header row
                if scheme_code == 'Scheme Code':
                    continue
                
                if count >= 100:
                    break
                fund_list.append({
                    'id': scheme_code,
                    'name': scheme_name,
                    'category': 'Mutual Fund'
                })
                count += 1
            
            return {
                'success': True,
                'funds': fund_list,
                'total': len(schemes) - 1  # Exclude header
            }
        except Exception as e:
            logger.error(f"Error fetching fund list: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching fund list: {str(e)}'
            }
    
    def get_current_data(self):
        """Get the currently loaded fund data"""
        if self.fund_data is not None:
            # Clean data before returning
            data_dict = self.fund_data.to_dict('records')
            
            for record in data_dict:
                for key, value in list(record.items()):
                    if pd.isna(value) or (isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf'))):
                        record[key] = None
                    elif hasattr(value, 'item'):
                        record[key] = value.item()
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.strftime('%Y-%m-%d')
            
            return data_dict
        return []
    
    def export_to_csv(self, filename):
        """Export current data to CSV"""
        try:
            if self.fund_data is None or self.fund_data.empty:
                return {'success': False, 'message': 'No data to export'}
            
            filepath = os.path.join('data', filename)
            self.fund_data.to_csv(filepath, index=False)
            
            return {'success': True, 'filepath': filepath}
        except Exception as e:
            return {'success': False, 'message': str(e)}
