"""
Projections and Analytics Module
Calculates future projections and trends based on historical fund data
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ProjectionsCalculator:
    """Calculate fund projections and analytics"""
    
    @staticmethod
    def calculate_nav_projection(dataframe, projection_days=30):
        """
        Calculate future NAV projections using linear regression
        
        Args:
            dataframe: Historical fund data
            projection_days: Number of days to project forward
            
        Returns:
            dict with projection data
        """
        try:
            if dataframe is None or len(dataframe) < 3:
                return None
            
            # Prepare data
            df = dataframe.copy()
            
            # Extract numeric NAV values
            if 'nav' in df.columns:
                nav_col = 'nav'
            elif 'NAV' in df.columns:
                nav_col = 'NAV'
            else:
                return None
            
            # Convert to numeric
            df['nav_numeric'] = pd.to_numeric(df[nav_col], errors='coerce')
            df = df.dropna(subset=['nav_numeric'])
            
            if len(df) < 3:
                return None
            
            # Create numeric date index
            df['days'] = np.arange(len(df))
            
            # Calculate trend using polyfit (degree 2 for curved trend)
            coeffs = np.polyfit(df['days'], df['nav_numeric'], 2)
            poly = np.poly1d(coeffs)
            
            # Generate projection
            last_day = df['days'].max()
            future_days = np.arange(last_day, last_day + projection_days)
            projected_navs = poly(future_days)
            
            # Generate dates for projection
            if 'Date' in df.columns:
                last_date = pd.to_datetime(df['Date'].iloc[-1])
            else:
                last_date = datetime.now()
            
            future_dates = [
                (last_date + timedelta(days=int(d - last_day))).strftime('%Y-%m-%d')
                for d in future_days
            ]
            
            # Calculate growth rate
            current_nav = df['nav_numeric'].iloc[-1]
            avg_growth = (df['nav_numeric'].iloc[-1] - df['nav_numeric'].iloc[0]) / len(df)
            growth_rate = (avg_growth / current_nav) * 100 if current_nav > 0 else 0
            
            return {
                'success': True,
                'current_nav': float(current_nav),
                'projected_navs': [float(nav) for nav in projected_navs],
                'future_dates': future_dates,
                'growth_rate': float(growth_rate),
                'projection_days': projection_days,
                'projected_nav_end': float(projected_navs[-1]),
                'expected_gain': float(projected_navs[-1] - current_nav),
                'expected_return_percent': float(((projected_navs[-1] - current_nav) / current_nav) * 100) if current_nav > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating projection: {str(e)}")
            return None
    
    @staticmethod
    def calculate_performance_metrics(dataframe):
        """
        Calculate performance metrics for the fund
        
        Args:
            dataframe: Historical fund data
            
        Returns:
            dict with performance metrics
        """
        try:
            if dataframe is None or len(dataframe) < 2:
                return None
            
            df = dataframe.copy()
            
            # Find NAV column
            if 'nav' in df.columns:
                nav_col = 'nav'
            elif 'NAV' in df.columns:
                nav_col = 'NAV'
            else:
                return None
            
            df['nav_numeric'] = pd.to_numeric(df[nav_col], errors='coerce')
            df = df.dropna(subset=['nav_numeric'])
            
            if len(df) < 2:
                return None
            
            # Calculate metrics
            opening_nav = df['nav_numeric'].iloc[0]
            closing_nav = df['nav_numeric'].iloc[-1]
            max_nav = df['nav_numeric'].max()
            min_nav = df['nav_numeric'].min()
            avg_nav = df['nav_numeric'].mean()
            std_dev = df['nav_numeric'].std()
            
            # Total return
            total_return = closing_nav - opening_nav
            total_return_percent = (total_return / opening_nav) * 100 if opening_nav > 0 else 0
            
            # Calculate volatility
            volatility = (std_dev / avg_nav) * 100 if avg_nav > 0 else 0
            
            # Sharpe ratio (simplified, assuming 5% risk-free rate)
            excess_return = total_return_percent - 5
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0
            
            return {
                'opening_nav': float(opening_nav),
                'closing_nav': float(closing_nav),
                'total_return': float(total_return),
                'total_return_percent': float(total_return_percent),
                'max_nav': float(max_nav),
                'min_nav': float(min_nav),
                'average_nav': float(avg_nav),
                'volatility': float(volatility),
                'sharpe_ratio': float(sharpe_ratio),
                'days_tracked': len(df),
                'best_day_return': float(df['nav_numeric'].diff().max()),
                'worst_day_return': float(df['nav_numeric'].diff().min())
            }
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return None
    
    @staticmethod
    def prepare_chart_data(dataframe, group_by_fund=True):
        """
        Prepare data for chart visualization
        
        Args:
            dataframe: Historical fund data
            group_by_fund: Group by fund name if True
            
        Returns:
            dict with chart data
        """
        try:
            if dataframe is None or len(dataframe) == 0:
                return None
            
            df = dataframe.copy()
            
            # Find NAV column
            if 'nav' in df.columns:
                nav_col = 'nav'
            elif 'NAV' in df.columns:
                nav_col = 'NAV'
            else:
                return None
            
            df['nav_numeric'] = pd.to_numeric(df[nav_col], errors='coerce')
            
            # Prepare date
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            else:
                df['Date'] = pd.date_range(end=datetime.now(), periods=len(df))
            
            chart_data = {
                'labels': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
                'values': df['nav_numeric'].tolist()
            }
            
            # If grouping by fund
            if group_by_fund and 'Fund Name' in df.columns:
                grouped = df.groupby('Fund Name')
                datasets = []
                
                colors = [
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(230, 126, 34, 0.8)',
                    'rgba(231, 76, 60, 0.8)'
                ]
                
                for idx, (fund_name, group) in enumerate(grouped):
                    datasets.append({
                        'label': fund_name,
                        'data': group['nav_numeric'].tolist(),
                        'borderColor': colors[idx % len(colors)],
                        'backgroundColor': colors[idx % len(colors)].replace('0.8', '0.2'),
                        'fill': True,
                        'tension': 0.4
                    })
                
                chart_data['datasets'] = datasets
                chart_data['grouped'] = True
            else:
                chart_data['datasets'] = [{
                    'label': 'NAV',
                    'data': df['nav_numeric'].tolist(),
                    'borderColor': 'rgba(52, 152, 219, 0.8)',
                    'backgroundColor': 'rgba(52, 152, 219, 0.2)',
                    'fill': True,
                    'tension': 0.4
                }]
                chart_data['grouped'] = False
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Error preparing chart data: {str(e)}")
            return None
