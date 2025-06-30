# Statistical Analysis Dashboard Using Django / Python 

A powerful web-based statistical analysis application built with Django, offering interactive data visualization and comprehensive statistical analysis tools. This application was ported from R Shiny to provide better performance, scalability, and modern web capabilities.

## 🚀 Quick Start for New Developers

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** - [Download from python.org](https://www.python.org/downloads/)
- **pip** (Python package installer) - Usually comes with Python
- **Git** (optional, for version control) - [Download from git-scm.com](https://git-scm.com/)

### Step-by-Step Setup

#### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd "Data Analysis App"

# Or download and extract the ZIP file, then navigate to the folder
```

#### 2. Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**⚠️ Important**: You should see `(venv)` at the beginning of your command prompt when the virtual environment is active.

#### 3. Install Dependencies
```bash
# Make sure your virtual environment is activated first!
pip install -r requirements.txt
```

#### 4. Set Up the Database
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

#### 5. (Optional) Create Admin User
```bash
# Create a superuser for admin access
python manage.py createsuperuser
```

#### 6. Run the Development Server
```bash
# Start the Django development server
python manage.py runserver
```

#### 7. Access the Application
Open your web browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/ (if you created a superuser)

## 🛠️ Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Make sure your virtual environment is activated. You should see `(venv)` in your command prompt.

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then try running the server again
python manage.py runserver
```

### Issue: PowerShell errors with `&&` commands
**Solution**: Run commands separately in PowerShell:

```powershell
# Don't use: cd "Data Analysis App" && venv\Scripts\activate && python manage.py runserver
# Instead, run each command separately:
cd "Data Analysis App"
venv\Scripts\activate
python manage.py runserver
```

### Issue: "This site can't be reached" in browser
**Solutions**:
1. Make sure the Django server is running (you should see output in the terminal)
2. Check the correct URL: http://127.0.0.1:8000/ or http://localhost:8000/
3. Ensure no firewall is blocking port 8000

## 📁 Project Structure

```
Data Analysis App/
├── analysis/                    # Main Django app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Form definitions
│   ├── utils.py                # Statistical utility functions
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin interface
├── templates/analysis/         # HTML templates
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   └── about.html             # About page
├── static/                     # Static files (CSS, JS, images)
├── media/uploads/              # User uploaded files
├── statistical_analysis/       # Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI application
├── venv/                       # Virtual environment (don't modify)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database
├── brain_tumor_dataset.csv    # Sample dataset
└── README.md                  # This file
```

## 🎯 Features

### Data Sources
- **Random Data Generation**: Create synthetic datasets for testing
- **File Upload**: Support for CSV, Excel (.xlsx, .xls) files
- **Pre-loaded Dataset**: Brain tumor dataset included

### Interactive Visualizations
- **Histograms**: Distribution analysis with customizable bins
- **Box Plots**: Quartile and outlier visualization
- **Q-Q Plots**: Normality assessment
- **Correlation Heatmaps**: Correlation matrix visualization

### Statistical Analysis
- **Descriptive Statistics**: Mean, median, standard deviation, etc.
- **Distribution Analysis**: Skewness, kurtosis, quantiles
- **Hypothesis Testing**: One-sample t-tests
- **Normality Testing**: Shapiro-Wilk test

### User Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Interactive analysis with AJAX
- **Tabbed Interface**: Organized sections for plots, statistics, and data
- **Modern Bootstrap UI**: Clean and professional interface

## 🔧 Technology Stack

### Backend
- **Django 5.2+**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Database (for development)
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **SciPy**: Statistical functions
- **Statsmodels**: Advanced statistical modeling
- **Scikit-learn**: Machine learning utilities

### Frontend
- **Bootstrap 5**: UI framework
- **Plotly.js**: Interactive charts
- **jQuery**: JavaScript utilities
- **AJAX**: Asynchronous data loading

## 📖 Usage Guide

1. **Start the Application**: Follow the setup steps above
2. **Select Data Source**: Choose from random data, file upload, or the included dataset
3. **Configure Analysis**: 
   - Select columns for analysis
   - Choose visualization options
   - Set parameters like histogram bins
4. **Explore Results**: 
   - View interactive plots
   - Examine statistical summaries
   - Download results

## 🚀 Development

### Making Changes
1. Activate the virtual environment: `venv\Scripts\activate`
2. Make your changes to the code
3. The development server will automatically reload
4. Test your changes in the browser

### Adding New Packages
```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Running Tests
```bash
python manage.py test
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Getting Help

If you encounter issues:
1. Check this README's troubleshooting section
2. Review the Django documentation: https://docs.djangoproject.com/
3. Open an issue on the project repository
4. Contact the development team

---

**Happy Analyzing! 📊** 