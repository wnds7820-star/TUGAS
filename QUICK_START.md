# Quick Start Guide - Omega Terminal

## Installation & Setup

### 1. Verify Python Environment
The application requires Python 3.8+ with the following packages:
- tkinter (included with Python)
- matplotlib
- reportlab
- pillow

These have been automatically installed in your virtual environment.

### 2. Run the Application
```bash
cd "c:\Users\user\Documents\Tugas\TUGAS"
.venv\Scripts\python.exe wnds_stats_pro.py
```

### 3. Login
- Username: `tes`
- Password: `1234`

## Key Features at a Glance

### 🎨 New Visual Design
- Dark terminal theme (Onyx Black) with bright accents (Phosphor Green)
- Monospace font for professional computer terminal look
- Elegant card-based layout with proper spacing

### 📊 Dashboard (Overview)
See at a glance:
- 👥 Total number of students
- 📊 Average grade
- 🏆 Highest score
- 📉 Lowest score
- ✅ Pass rate percentage

### 📝 Master Data Management
- **Left side:** Input form for adding/editing students
- **Right side:** Live student list with real-time search
- Score validation (0-100) with visual feedback
- Red highlight for invalid scores

### 📈 Advanced Analytics
- Pass/Fail comparison bar chart
- Statistical summary cards
- Color-coded visualization

### 📋 System Tools
- **Activity Log:** Complete history of all actions
- **Export Options:**
  - PDF reports (professional format)
  - JSON export (for data analysis)
  - Activity log export (for auditing)

### 🔔 Notifications
Toast notifications confirm:
- ✓ Record added
- ✓ Record updated
- ✓ Record deleted
- ✓ Export successful

## Common Tasks

### Add a New Student
1. Go to "📝 Master Data"
2. Fill form: Name, Class, Score, Status
3. Click "[ + ADD ]"
4. Green notification appears

### Search for a Student
1. In Master Data, use "🔍 Search Student" field
2. Type name or class
3. Results filter automatically

### Export Student Report
1. Click "💾 Export Report" in sidebar
2. Choose format:
   - PDF (professional)
   - JSON (data analysis)
   - Activity Log (system history)
3. File saves automatically

### View System History
1. Click "📋 Activity Log"
2. See all actions with timestamps
3. Export log if needed

## Customization

### Change Pass Threshold (default: 75)
Edit `wnds_stats_pro.py` line with:
```python
self.pass_threshold = 75
```

### Change Login Credentials
Edit `wnds_stats_pro.py` verify_login() method

### Change Color Scheme
Edit `create_styles()` method in `wnds_stats_pro.py`

## Files Generated

When you use the application, these files are created:
- `database.json` - Student records (auto-saved)
- `activity_log.json` - System history (auto-saved)
- Export files (PDFs, JSONs) - Created when you export

## Troubleshooting

**Application won't start?**
- Ensure .venv virtual environment is activated
- Check Python version: `.venv\Scripts\python.exe --version`

**Charts not showing?**
- Matplotlib may need additional system dependencies
- Install again: `pip install matplotlib --upgrade`

**PDF export fails?**
- Ensure reportlab is installed: `pip install reportlab`
- Check folder permissions

**Search not working?**
- Make sure you're in Master Data section
- Type in the search field (updates automatically)

## Performance Tips

- Keep student database under 1000 records for best performance
- Export and archive old activity logs periodically
- Close and reopen app if it slows down

## Support

For issues or questions, check:
1. README.md - Full documentation
2. Application tooltips - Hover over elements
3. System Activity Log - Track what's happening

---
**Ready to use!** 🚀 Login with `tes` / `1234` and start managing students!
