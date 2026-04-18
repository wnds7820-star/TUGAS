# Omega Terminal - Advanced Student Management System

## Overview
A sophisticated Python-based student grade management system featuring a futuristic Onyx Black and Phosphor Green terminal-style interface. Built with Tkinter for cross-platform compatibility.

## New Features Implemented

### 1. Visual Appearance (UI Transformation)
✅ **Futuristic Theme**
- Complete redesign from Onyx Black (#0a0a0a) with Phosphor Green (#00ff41) accents
- Professional Courier New/Monospace font throughout for terminal aesthetics
- Enhanced contrast and visual hierarchy

✅ **Glow Effects & Visual Polish**
- Glowing effects on header titles
- Rounded corner buttons and input fields for modern appearance
- Smooth transitions and hover effects on interactive elements

✅ **Color Scheme Enhancements**
- Primary: Onyx Black (#0a0a0a) - Deep, professional background
- Accent: Phosphor Green (#00ff41, #00ff80) - Vibrant, eye-catching
- Highlight: Bright Green (#00ff80) - For emphasis and focus states
- Borders: Gray (#1a1a1a, #2a2a2a) - Subtle separation

### 2. Overview Section (Dashboard)
✅ **Prominent Visual Cards**
- Data summary displayed in large, easy-to-read card format
- Five key metrics with icons:
  - 👥 Total Students
  - 📊 Average Score
  - 🏆 Highest Score
  - 📉 Lowest Score
  - ✅ Pass Rate percentage

✅ **Statistical Icons**
- Emoji-based icons next to each metric for visual clarity
- Professional card design with padding and spacing

✅ **Spacious Layout**
- Generous padding between elements (20-30px)
- Clean separation between cards
- Improved readability with larger font sizes for stats

### 3. Master Data Section (Record Editor)
✅ **Side-by-Side Layout**
- Input form positioned on the left side
- Student data table displayed on the right
- Users can view the student list while editing

✅ **Input Validation**
- Real-time validation of score input (0-100 range)
- Input boxes highlight in red (#ff4444) when invalid format detected
- Clear error messaging with validation feedback

✅ **Professional Labels**
- Fixed label: "✏️ Student Record Data" (was "Recor Murid")
- More descriptive field names and hints
- Improved form organization

✅ **Live Search Filter**
- 🔍 Search field above student table
- Real-time filtering by student name or class
- No need to press a button - results update automatically

### 4. Advanced Features
✅ **PDF Export**
- Generate professional grade reports in PDF format
- Includes summary statistics and complete student table
- Custom styling with theme colors
- Automatic file naming with timestamps

✅ **Excel/JSON Export**
- Export student data to JSON with statistics
- Preserves all data structure for data analysis
- Timestamped exports for version control

✅ **Notification System**
- Toast notifications appear in bottom-right corner
- Display confirmation messages on:
  - Student added successfully
  - Record updated
  - Data deleted
  - Export completed
- Auto-disappear after 3 seconds

✅ **Pass/Fail Bar Chart**
- Visual comparison graph showing:
  - Number of students who PASSED
  - Number of students who FAILED
- Configurable pass threshold (default: 75)
- Color-coded bars: Green for pass, Red for fail
- Matplotlib integration for professional charts

✅ **Activity Log**
- Complete system history recording all actions
- Tracked events:
  - Login/Logout
  - Records added/updated/deleted
  - Database saves
  - Exports
  - Failed login attempts
- Timestamps for every action
- Dedicated view page with sortable log entries
- Export activity log to JSON

### 5. System Settings & Auto-Save
✅ **Automatic Data Persistence**
- Data automatically saved to database.json on every change
- No data loss when application closes
- Immediate persistence with timestamps

✅ **Activity Log Database**
- Stored in activity_log.json
- Complete audit trail of all system operations
- Timestamped entries with action details

## File Structure
```
TUGAS/
├── wnds_stats_pro.py          # Main application (enhanced)
├── database.json              # Student records (auto-created)
├── activity_log.json          # System activity log (auto-created)
├── README.md                  # Documentation
└── testing.py                 # Test utilities
```

## Usage

### Running the Application
```bash
cd "c:\Users\user\Documents\Tugas\TUGAS"
.venv\Scripts\python.exe wnds_stats_pro.py
```

### Login Credentials
- **Username:** `tes`
- **Password:** `1234`

### Navigation Menu
- **📊 Overview** - Dashboard with key metrics
- **📝 Master Data** - Add, edit, delete student records
- **📈 Analytics** - Statistics and pass/fail distribution chart
- **📋 Activity Log** - Complete system history
- **💾 Export Report** - Export data in various formats

### Features Guide

#### Adding Students
1. Navigate to Master Data section
2. Fill in the form: Name, Class, Score (0-100), Status
3. Score validation provides real-time feedback
4. Click [ + ADD ] to add the record
5. Green notification confirms successful addition

#### Searching
1. Use the search field in Master Data
2. Type student name or class
3. Table filters automatically in real-time

#### Exporting
1. Click 💾 Export Report in sidebar
2. Choose format:
   - **PDF** - Professional grade report
   - **JSON** - Raw data with statistics
   - **Activity Log** - System history

#### Viewing Analytics
1. Navigate to Analytics section
2. See summary statistics cards
3. View Pass/Fail bar chart
4. Filter threshold: 75 (pass)

#### Activity Log
1. Click 📋 Activity Log in sidebar
2. View all system actions with timestamps
3. See who did what and when
4. Export log for auditing

## Requirements
- Python 3.8+
- tkinter (usually included with Python)
- matplotlib - For charts
- reportlab - For PDF generation
- pillow - For image processing

### Install Dependencies
```bash
pip install matplotlib reportlab pillow
```

## Technical Improvements

### Code Quality
- Enhanced documentation with detailed docstrings
- Improved error handling and validation
- Better separation of concerns with logical method organization
- Type hints and parameter validation

### UI/UX
- Consistent font family (Courier New/Monospace)
- Uniform color scheme throughout
- Professional spacing and padding
- Accessible notification system
- Responsive layout

### Data Management
- Automatic persistence with timestamps
- Complete audit trail
- Multiple export formats
- Efficient filtering and searching
- Activity logging for accountability

## Customization

### Adjust Pass Threshold
```python
self.pass_threshold = 75  # Change in __init__ method
```

### Modify Color Scheme
Edit in `create_styles()` method:
```python
onyx_black = "#0a0a0a"
phosphor_green = "#00ff41"
```

### Change Default Credentials
Edit in `verify_login()` method:
```python
if username == "your_username" and password == "your_password":
```

## Features Checklist

### Visual Appearance ✅
- [x] Onyx Black + Phosphor Green theme
- [x] Monospace font throughout
- [x] Glow effects on titles
- [x] Rounded buttons and inputs
- [x] Modern color scheme

### Overview Section ✅
- [x] Prominent visual cards
- [x] Icons next to statistics
- [x] Spacious layout with padding

### Master Data Section ✅
- [x] Form positioned next to table
- [x] Input validation with red highlight
- [x] Fixed labels ("Student Record Data")
- [x] Live search filter

### Advanced Features ✅
- [x] PDF export button
- [x] Live search (no button needed)
- [x] Toast notifications
- [x] Pass/Fail bar chart
- [x] Excel/JSON export

### System Settings ✅
- [x] Auto-save on every change
- [x] Activity log with timestamps
- [x] Persistent data storage

## Support & Troubleshooting

### Chart Not Displaying?
- Ensure matplotlib is installed: `pip install matplotlib`
- Some systems may require additional dependencies

### PDF Export Fails?
- Install reportlab: `pip install reportlab`
- Check write permissions in the application directory

### Slow Performance?
- Keep database size reasonable
- Archive old activity logs periodically

## Version History
- **v2.0** (Current) - Complete UI overhaul with advanced features
- **v1.0** - Initial release with basic CRUD operations

---
**Last Updated:** 2026-04-18
**Status:** Fully Enhanced with All Requested Features ✅