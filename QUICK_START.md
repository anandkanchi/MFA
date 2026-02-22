# 🚀 Quick Start Guide - Mutual Fund Data Analyzer

## ⚡ Quick Access

**Website**: http://localhost:5000  
**Status**: ✅ Running  

---

## 🎯 Getting Started (First Time Users)

### 1️⃣ **Website is Already Live!**
Your website is running in the background. Just:
- Open your browser
- Go to: **http://localhost:5000**
- You should see the beautiful interface

### 2️⃣ **Use the Website**

**Enter Fund Information:**
- Fund Name: Type any mutual fund company (e.g., HDFC, SBI, Axis, Aditya Birla)
- Start Date: Pick your start date
- End Date: Pick your end date
- Click: "Fetch Data"

**View Results:**
- Data appears in a table below
- Shows fund names, dates, NAV values, etc.

**Export Data:**
- **Generate PDF**: Creates a professional report (try it!)
- **Generate Excel**: Exports data for analysis
- **Convert PDF**: Transform existing PDFs to Excel

---

## 📍 File Locations

**Generated Files:**
- PDF Reports: `data/pdfs/`
- Excel Files: `data/excel/`
- Uploaded Files: `data/uploads/`

---

## 🎨 What Makes This App Special

✨ **Modern Design**
- Smooth animations when loading
- Beautiful gradient colors
- Keyboard-friendly interface

⚡ **Real Data**
- Connects to live mutual fund APIs
- Actual NAV values
- Real historical data

📊 **Professional Output**
- PDF reports with formatting
- Excel files with proper columns
- Multiple export formats

---

## ⚙️ If Server Stops

If the website becomes unreachable:

**Option 1: Restart from Terminal**
```bash
cd d:\CAPSTONE\MFA
python run.py
```

**Option 2: Use PowerShell**
```powershell
cd d:\CAPSTONE\MFA
.\.venv\Scripts\python.exe run.py
```

Then open: http://localhost:5000

---

## 🆘 Troubleshooting

### "Website won't load"
→ Check terminal window - if it shows errors, take note and restart

### "No data after clicking Fetch"
→ Make sure fund name is spelled correctly (HDFC, SBI, etc.)

### "Generated files disappeared"
→ Check `data/pdfs/` and `data/excel/` folders

---

## 📱 Mobile & Tablet

The website works on phones/tablets too!
- Responsive design adapts automatically
- Touch-friendly buttons
- Same features available

---

## 🔄 Normal Workflow

```
1. Enter fund name & dates
   ↓
2. Click "Fetch Data"
   ↓
3. Review data in table
   ↓
4. Click "Generate PDF" or "Generate Excel"
   ↓
5. Files saved automatically
   ↓
6. Download and use!
```

---

## 📚 Learn More

- **Full Documentation**: Read `README.md`
- **Project Report**: See `PROJECT_COMPLETION_REPORT.md`
- **API Details**: Check `app/routes.py`

---

## 💡 Tips & Tricks

**Tip 1**: Start with small date ranges (1-7 days) to test
**Tip 2**: Common fund names: HDFC, SBI, Axis, ICICI, Aditya Birla
**Tip 3**: Excel files are best for further analysis
**Tip 4**: PDF files are great for reports/presentations

---

## 🎓 For Your Capstone

This application demonstrates:
- ✅ Web development (Flask)
- ✅ API integration (mftool)
- ✅ Data processing (Pandas)
- ✅ Modern UI/UX design
- ✅ Report generation (PDF)
- ✅ Data export (Excel)
- ✅ Error handling
- ✅ Professional practices

---

## 📞 Need Help?

Check the browser's developer console (F12) for technical details.

**Questions about features?** → Read README.md  
**Server not starting?** → Check terminal output for errors  
**Data not showing?** → Verify fund name spelling  

---

**Happy analyzing! Good luck with your capstone presentation!** 🎉
