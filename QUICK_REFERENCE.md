# 🎯 Quick Reference Card

## Installation & Running

### First Time Setup
```bash
# 1. Install dependencies
python install_dependencies.py

# 2. Run the app
python "early access.py"

# 3. Login
Username: tes
Password: 1234
```

---

## 📥 Download Features

### Download Options Popup

| Button | Color | Function |
|--------|-------|----------|
| 📄 PDF | Red (#cc0000) | Export to PDF with professional layout |
| 📊 EXCEL | Excel Green (#70ad47) | Export to Excel with auto-columns |

### File Dialog
- ✅ Choose save location
- ✅ Custom filename support
- ✅ Automatic timestamp in filename
- ✅ Cancel anytime

---

## 📊 Excel Export Features

| Feature | Details |
|---------|---------|
| **Format** | .xlsx (Excel 2007+) |
| **Column Width** | Auto-adjusted based on content |
| **Headers** | Green background (#70ad47) |
| **Alignment** | Centered text |
| **File Dialog** | Yes (user selects location) |

### Excel Example:
```
┌──────────────┬──────────┬────────┬─────────┐
│ Name         │ Class    │ Score  │ Status  │
├──────────────┼──────────┼────────┼─────────┤
│ Lara Adams   │ 12A      │ 89     │ Pass    │
│ Rian Hart    │ 11C      │ 74     │ Pass    │
│ Mia Chen     │ 10B      │ 95     │ Pass    │
└──────────────┴──────────┴────────┴─────────┘
```

---

## 📄 PDF Export Features

| Feature | Details |
|---------|---------|
| **Format** | .pdf |
| **Header Color** | Red (#cc0000) |
| **Includes** | Title, Summary Stats, Data Table |
| **Print-Ready** | Yes |
| **File Dialog** | Yes (user selects location) |

### PDF Example:
```
╔═══════════════════════════════════╗
║  📄 STUDENT GRADE REPORT         ║
╚═══════════════════════════════════╝

📊 Report Generated: 2024-04-19 14:30:22
📊 Total Students: 3
📊 Average Score: 86.00
📊 Highest Score: 95
📊 Lowest Score: 74

┌──────────────┬──────────┬────────┬─────────┐
│ Name         │ Class    │ Score  │ Status  │
├──────────────┼──────────┼────────┼─────────┤
│ Lara Adams   │ 12A      │ 89     │ Pass    │
│ Rian Hart    │ 11C      │ 74     │ Pass    │
│ Mia Chen     │ 10B      │ 95     │ Pass    │
└──────────────┴──────────┴────────┴─────────┘
```

---

## 🎨 Color Scheme

```
┌─────────────────────────────┐
│  UI COLORS                  │
├─────────────────────────────┤
│ PDF Button      #cc0000 🔴  │
│ Excel Button    #70ad47 🟢  │
│ "early access"  #00ff80 🟢  │
│ Background      #0a0a0a ⬛  │
│ Accent Text     #00ff41 🟢  │
└─────────────────────────────┘
```

---

## 📋 Step-by-Step Guide

### To Export as PDF:

```
1. Click "💾 Download Report" (Sidebar)
     ↓
2. Click "📄 PDF" button (Red)
     ↓
3. Choose location & filename
     ↓
4. Click "Save"
     ↓
5. ✅ Success notification appears
```

### To Export as Excel:

```
1. Click "💾 Download Report" (Sidebar)
     ↓
2. Click "📊 EXCEL" button (Green)
     ↓
3. Choose location & filename
     ↓
4. Click "Save"
     ↓
5. ✅ Success notification appears
```

---

## 🔧 Dependencies

### Required
- `reportlab` - PDF generation
- `pandas` or `openpyxl` - Excel export

### Installation Command
```bash
pip install reportlab pandas openpyxl
```

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Import error on startup | Run `python install_dependencies.py` |
| PDF button not working | Install: `pip install reportlab` |
| Excel button not working | Install: `pip install pandas openpyxl` |
| File dialog missing | Ensure tkinter installed |
| Login fails | Username: `tes`, Password: `1234` |
| Empty database | Add students first via "Master Data" |

---

## 📝 File Naming Convention

### Automatic Filename Format:
```
PDF:   student_report_20240419_143022.pdf
Excel: student_data_20240419_143022.xlsx
```

Where: `YYYYMMDD_HHMMSS` = Date and time of export

### Example:
- `student_report_20240419_143022.pdf` = April 19, 2024 at 2:30:22 PM
- `student_data_20240419_143022.xlsx` = Same time

---

## 🎯 Navigation Guide

```
┌─────────────────────────────────────┐
│        STUDENT MANAGEMENT APP       │
├─────────────────────────────────────┤
│ NAVIGATION:                         │
│ ├── 📊 Overview                     │
│ ├── 📝 Master Data                  │
│ ├── 📈 Analytics                    │
│ └── 💾 Download Report ⭐ NEW      │
│                                     │
│ STATUS:                             │
│ └── Records: [count]                │
└─────────────────────────────────────┘
```

---

## ✨ What's New

| # | Feature | Status |
|---|---------|--------|
| 1 | "Export" → "Download" | ✅ |
| 2 | "JSON" → "EXCEL" button | ✅ |
| 3 | PDF Red styling | ✅ |
| 4 | Excel Green styling | ✅ |
| 5 | File dialogs | ✅ |
| 6 | Auto-column width | ✅ |
| 7 | Professional formatting | ✅ |

---

## 📞 Need Help?

1. **Detailed Info**: See `MODIFICATIONS_SUMMARY.md`
2. **Full Guide**: See `README_UPDATES.md`
3. **Auto-Install**: Run `install_dependencies.py`
4. **Error Messages**: Read the popup carefully!

---

**Version:** 2.0 Enhanced
**Last Updated:** April 19, 2026
