<<<<<<< HEAD
# Mutual Fund Data Analyzer - Capstone Project

A professional web application for analyzing mutual fund data with PDF generation and Excel export capabilities.

## Features

✅ **Data Fetching**: Connect to financial APIs to fetch mutual fund data for any company and date range
✅ **Data Preview**: View data in an interactive table before generation
✅ **PDF Generation**: Create professional PDF reports of fund analysis
✅ **Excel Export**: Export data to Excel format for detailed analysis
✅ **PDF to Excel Conversion**: Convert PDF tables directly to Excel
✅ **Modern UI**: Beautiful, responsive interface with smooth animations
✅ **Professional Design**: Industry-standard layout and styling

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, OpenPyXL
- **PDF Generation**: FPDF2
- **Mutual Fund API**: mftool
- **PDF Extraction**: Tabula-py
- **Server**: Flask Development Server (Gunicorn for production)

## Project Structure

```
MFA/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # API routes and endpoints
│   ├── mutual_fund_handler.py # Fund data fetching logic
│   ├── pdf_generator.py       # PDF report generation
│   ├── excel_converter.py     # Excel conversion logic
│   ├── templates/
│   │   └── index.html         # Main frontend page
│   └── static/
│       ├── css/
│       │   └── style.css      # Styling with animations
│       └── js/
│           └── main.js        # Frontend JavaScript
├── data/                      # Data storage folder
├── config.py                  # Configuration settings
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file

```

## Installation & Setup

1. **Clone/Create Project**
   ```bash
   cd path/to/MFA
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Environment Variables**
   ```bash
   # Edit .env file with your settings
   ```

6. **Run Application**
   ```bash
   python run.py
   ```

7. **Access Website**
   Open browser and go to: `http://localhost:5000`

## Usage Guide

### 1. Fetch Fund Data
- Enter fund company name (e.g., HDFC, SBI, Axis)
- Select start and end dates
- Click "Fetch Data"
- System will retrieve all available fund data for the period

### 2. Preview Results
- Data displays in an interactive table
- Shows first 10 records
- Total record count displayed
- Scroll to view all columns

### 3. Generate PDF Report
- Click "Generate PDF" button
- Professional report generated with:
  - Fund name and period
  - Summary statistics
  - Detailed data table
  - Page numbers and header/footer

### 4. Export to Excel
- Click "Generate Excel" button
- Data exported with:
  - All records and columns
  - Formatted headers
  - Ready for analysis in Excel

### 5. Convert PDF to Excel
- Use "PDF to Excel" feature
- Extracts tables from PDF files
- Converts to Excel format
- Useful for third-party PDFs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/api/funds` | GET | List available mutual funds |
| `/api/fetch-data` | POST | Fetch fund data for date range |
| `/api/generate-pdf` | POST | Generate PDF report |
| `/api/generate-excel` | POST | Generate Excel file |
| `/api/preview-data` | GET | Preview current data |
| `/api/convert-pdf-to-excel` | POST | Convert PDF table to Excel |
| `/download/<type>/<filename>` | GET | Download generated file |
| `/health` | GET | Health check |

## Frontend Features

- **Responsive Design**: Works perfectly on desktop, tablet, mobile
- **Smooth Animations**: Professional fade-in, slide-in effects
- **Real-time Feedback**: Instant alerts for success/error
- **Loading States**: Visual feedback during processing
- **Data Validation**: Client-side input validation
- **Modern UI Elements**: Cards, gradients, shadows, hover effects

## Future Enhancements

- [ ] Export to CSV format
- [ ] Historical data caching
- [ ] Advanced filtering options
- [ ] Data visualization charts
- [ ] User authentication
- [ ] Database integration
- [ ] Batch processing
- [ ] Email report delivery
- [ ] API key management
- [ ] Advanced analytics dashboard

## Troubleshooting

### Port Already in Use
If port 5000 is in use, modify `config.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Change to 5001
```

### API Errors
- Verify internet connection for API calls
- Check date format (YYYY-MM-DD)
- Ensure fund name is spelled correctly

### PDF Generation Issues
- Check write permissions in data/ folder
- Ensure sufficient disk space
- Verify PDF2 installation

### Excel Export Problems
- Verify openpyxl is installed
- Check data folder permissions
- Ensure enough free disk space

## Performance Notes

- Data preview limited to 10 rows for responsiveness
- PDF generation includes first 30 rows
- File downloads may take time for large datasets
- Consider optimizing for production with caching

## Security Notes

For production deployment:
1. Change SECRET_KEY in .env
2. Set DEBUG=False
3. Use environment variables for sensitive data
4. Implement user authentication
5. Add CORS headers if needed
6. Use HTTPS
7. Set up proper logging
8. Implement rate limiting

## Author

Built as a Capstone Project - 2026

## License

Proprietary - All Rights Reserved

---

**Questions or Issues?** Review logs in the console and check the API responses in browser DevTools.
=======
# MFA
>>>>>>> c15c6da90f2cb7341d35348b3690e59f366401fe
