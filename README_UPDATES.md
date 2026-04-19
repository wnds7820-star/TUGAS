# Student Data Management Application - Early Access Edition

## 🎯 Quick Start Guide

### Installation (First Time Only)

1. **Install Dependencies:**
   ```bash
   python install_dependencies.py
   ```
   Or manually install:
   ```bash
   pip install reportlab pandas openpyxl
   ```

2. **Run the Application:**
   ```bash
   python "early access.py"
   ```

3. **Login Credentials:**
   - Username: `tes`
   - Password: `1234`

---

## ✨ New Features & Modifications

### 1️⃣ UI Changes

#### Renamed "Export" to "Download"
- Sidebar button now reads: **"💾 Download Report"**
- Creates a more intuitive user experience

#### Download Options Popup
The new popup window features:
- **Modern Styling**: Symmetric, clean layout
- **Two Export Options**:
  - 📄 **PDF Button** (Red #cc0000)
  - 📊 **EXCEL Button** (Excel Green #70ad47)

#### Brand Colors
| Component | Color | Use |
|-----------|-------|-----|
| PDF Button | Red (#cc0000) | PDF header and styling |
| Excel Button | Excel Green (#70ad47) | Excel headers |
| "early access" Text | Neon Green (#00ff80) | App title (unchanged) |

---

### 2️⃣ Excel Export Function

**Feature: Automatic Column Width Adjustment**

```python
download_excel()
```

**What it does:**
- ✅ Exports all student data to `.xlsx` format
- ✅ Auto-adjusts column widths based on content
- ✅ Professional header styling (green background)
- ✅ Centered text alignment
- ✅ File dialog to choose save location
- ✅ Dual support: pandas or openpyxl

**Output Example:**
```
Name          | Class    | Score | Status
--------------+----------+-------+--------
Lara Adams    | 12A      | 89    | Pass
Rian Hart     | 11C      | 74    | Pass
Mia Chen      | 10B      | 95    | Pass
```

---

### 3️⃣ PDF Export Function

**Feature: Professional Report Generation**

```python
download_pdf()
```

**What it does:**
- ✅ Exports all student data to `.pdf` format
- ✅ Includes professional header with red branding
- ✅ Automatic summary statistics section
- ✅ Professional data table with formatting
- ✅ Print-ready layout
- ✅ File dialog to choose save location

**PDF Contents:**
- Report title with emoji
- Summary statistics (total students, average score, etc.)
- Student data table with formatting
- Red header row for branding

---

### 4️⃣ File Dialog Integration

Both export functions now include `filedialog.asksaveasfilename()`:

**Benefits:**
- 🎯 User chooses save location
- 📝 Custom filename support
- ⏰ Automatic timestamp in default filename
- ❌ Cancel operation support

**Example Dialog:**
```
Default Filename: student_report_20240419_143022.pdf
or
Default Filename: student_data_20240419_143022.xlsx
```

---

## 📋 Complete Function Reference

### Download Options Popup

```python
def show_download_dialog(self):
    """Show download options dialog with modern styling."""
    # Creates a Toplevel window with:
    # - Title: "▶ DOWNLOAD OPTIONS ◀"
    # - PDF Button (Red) 
    # - EXCEL Button (Excel Green)
    # - Close button
    # - Symmetric layout with proper padding
```

**Window Details:**
- Size: 450x350 pixels
- Background: Onyx Black (#0a0a0a)
- Always-on-top behavior
- Modal (grabs focus)

---

### Excel Export Function

```python
def download_excel(self):
    """Download student records to Excel file with auto-adjusted columns."""
    # Supports two backends:
    # 1. pandas (preferred if available)
    # 2. openpyxl (fallback)
    
    # Features:
    # - File dialog with default filename + timestamp
    # - Auto-width calculation for all columns
    # - Green header row (#70ad47)
    # - Centered cell alignment
    # - Professional formatting
    # - Error handling with installation hints
```

**Return Value:** Success/error notification shown to user

---

### PDF Export Function

```python
def download_pdf(self):
    """Download student records to PDF file with file dialog."""
    # Uses reportlab library for professional PDF generation
    
    # Features:
    # - File dialog with default filename + timestamp
    # - Red header styling (#cc0000)
    # - Summary statistics section
    # - Professional table formatting
    # - Print-ready output
    # - Error handling with installation hints
```

**Return Value:** Success/error notification shown to user

---

## 🔧 Technical Details

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| reportlab | Latest | PDF generation |
| pandas | Latest | Excel export (recommended) |
| openpyxl | Latest | Excel handling |

### Import Handling

The application uses try-except blocks for all optional libraries:

```python
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
```

This means:
- ✅ Application always starts even if libraries are missing
- ⚠️ Export features show helpful error messages
- 📦 Users can install packages on-demand

### File Dialog Integration

```python
from tkinter import filedialog

filepath = filedialog.asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
    initialfile=f"student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
)
```

---

## 📊 Feature Comparison

### Before vs After

| Feature | Before | After |
|---------|--------|-------|
| Export Label | "Export" | "Download" ✅ |
| Export Formats | PDF, JSON | PDF, EXCEL ✅ |
| PDF Export | Basic | Professional + Red styling ✅ |
| Excel Export | ❌ Missing | ✅ Auto-columns |
| File Dialog | ❌ No | ✅ Yes |
| Column Width | N/A | ✅ Auto-adjusted |
| Header Styling | Green | ✅ Brand colors (Red/Green) |

---

## 🐛 Error Handling

### Scenario: Library Not Installed

**User Action:** Click "EXCEL" button
**Result:** 
```
❌ Download Error
Excel export requires pandas or openpyxl.

Install with:
pip install pandas openpyxl
```

### Scenario: Empty Database

**User Action:** Try to download with no student records
**Result:**
```
⚠️ No Data
There are no student records to download.
```

### Scenario: User Cancels File Dialog

**User Action:** Click cancel in save dialog
**Result:** Operation cancelled gracefully (no error)

---

## 🎨 Color Guide

### UI Element Colors

```
PDF Button:
  - Background: Red (#cc0000)
  - Text: White (#ffffff)
  - Icon: 📄

EXCEL Button:
  - Background: Excel Green (#70ad47)
  - Text: White (#ffffff)
  - Icon: 📊

Application Title ("early access"):
  - Color: Neon Green (#00ff80)
  - Font: Bold, 20pt, Courier New

Dialog Background:
  - Color: Onyx Black (#0a0a0a)

Dialog Title:
  - Color: Bright Green (#00ff80)

Description Text:
  - Color: Phosphor Green (#00ff41)
```

---

## 📝 Usage Examples

### Example 1: Export to Excel

1. Click **"💾 Download Report"** sidebar button
2. In popup, click **"📊 EXCEL"** button
3. Choose filename and location
4. File saved with auto-adjusted columns ✅

### Example 2: Export to PDF

1. Click **"💾 Download Report"** sidebar button
2. In popup, click **"📄 PDF"** button
3. Choose filename and location
4. PDF with professional formatting saved ✅

---

## ⚠️ Important Notes

- **Timestamps**: All exported files include automatic timestamp in filename
- **Default Location**: Files save to selected directory by user
- **Database**: Original database.json remains unchanged
- **Multiple Exports**: You can export multiple times to different locations
- **File Overwrite**: You'll be warned if attempting to overwrite existing files

---

## 📦 Files in This Project

```
TUGAS/
├── early access.py                 # Main application (MODIFIED)
├── database.json                   # Student data storage
├── install_dependencies.py         # Package installer (NEW)
├── MODIFICATIONS_SUMMARY.md        # Detailed changes (NEW)
├── README.md                       # This file (UPDATED)
└── testing.py                      # Testing utilities
```

---

## 🚀 Troubleshooting

### Issue: Import errors on startup

**Solution:** Run `python install_dependencies.py`

### Issue: PDF export button doesn't work

**Cause:** reportlab not installed
**Solution:** `pip install reportlab`

### Issue: Excel export button doesn't work

**Cause:** pandas/openpyxl not installed
**Solution:** `pip install pandas openpyxl`

### Issue: File dialog doesn't appear

**Cause:** tkinter filedialog issue
**Solution:** Ensure tkinter is installed (`pip install tk`)

---

## 📞 Support

For issues or questions:
1. Check MODIFICATIONS_SUMMARY.md for detailed technical info
2. Verify all dependencies are installed
3. Review error messages for specific guidance
4. Check that username/password are correct (tes/1234)

---

## ✅ Verification Checklist

After modifications, verify:

- [ ] Application starts without errors
- [ ] Login works (tes/1234)
- [ ] "Download Report" button appears in sidebar
- [ ] Download Options popup has PDF and EXCEL buttons
- [ ] PDF button is red, EXCEL button is green
- [ ] File dialog appears when buttons clicked
- [ ] PDF exports with red header
- [ ] Excel exports with green header
- [ ] Column widths auto-adjust in Excel
- [ ] "early access" text is neon green
- [ ] Notifications show on successful download

---

**Last Updated:** April 19, 2026
**Version:** 2.0 (Enhanced with Download Features)
