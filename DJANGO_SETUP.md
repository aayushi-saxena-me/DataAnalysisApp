# Django Statistical Analysis Dashboard

This is a Django port of the R Shiny statistical analysis application, providing the same functionality with modern web technologies.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation & Setup

1. **Create and activate a virtual environment:**
   ```bash
   # Using venv (recommended)
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Copy your data file:**
   ```bash
   # Copy the brain tumor dataset to the project root
   cp ../brain_tumor_dataset.csv .
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser:**
   Navigate to `http://127.0.0.1:8000/` to access the dashboard.

## 📁 Project Structure

```
statistical_analysis/
├── analysis/                    # Main Django app
│   ├── models.py               # Data models
│   ├── views.py                # View functions
│   ├── forms.py                # Form definitions
│   ├── utils.py                # Statistical utility functions
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin interface
├── templates/analysis/         # HTML templates
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   └── about.html             # About page
├── statistical_analysis/       # Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI application
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## 🔧 Features

### Data Sources
- **Random Data**: Generate synthetic datasets for testing
- **File Upload**: Upload CSV, Excel (.xlsx, .xls) files
- **Local Dataset**: Use the brain tumor dataset

### Visualizations
- **Interactive Histograms**: Distribution analysis with customizable bins
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
- **Real-time Updates**: Form changes trigger automatic analysis updates
- **Tabbed Interface**: Organized sections for plots, statistics, and data
- **Loading Indicators**: Visual feedback during processing

## 🛠️ Technical Stack

### Backend
- **Django 4.2+**: Web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical functions
- **Statsmodels**: Advanced statistical modeling
- **Scikit-learn**: Machine learning utilities
- **Plotly**: Interactive visualization backend

### Frontend
- **Bootstrap 5**: UI framework
- **Plotly.js**: Interactive charts
- **jQuery**: JavaScript utilities
- **Font Awesome**: Icons
- **AJAX**: Asynchronous data loading

## 📊 Usage Guide

### 1. Select Data Source
- Choose from the radio buttons in the sidebar:
  - **Random Data**: Generates sample data for testing
  - **Upload CSV**: Upload your own data file
  - **Tumor Dataset**: Use the included brain tumor dataset

### 2. Configure Analysis
- **Column Selection**: Choose which column to analyze (for uploaded/local data)
- **Sample Size**: Set the number of random samples (for random data)
- **Visualization Options**:
  - Color scheme for plots
  - Number of histogram bins (1-50)
- **Display Options**:
  - Toggle plots, statistics, and correlation analysis

### 3. Explore Results
- **Plots Tab**: View interactive visualizations
- **Statistics Tab**: See detailed statistical analysis
- **Data Tab**: Preview your dataset

## 🔄 Migrating from R Shiny

### Feature Mapping

| R Shiny Feature | Django Equivalent |
|----------------|-------------------|
| `fluidPage()` | Bootstrap layout |
| `reactive()` | AJAX endpoints |
| `renderPlot()` | Plotly.js rendering |
| `verbatimTextOutput()` | HTML templates |
| `fileInput()` | Django forms |
| `ggplot2` | Plotly visualizations |
| R statistical functions | Pandas/SciPy/Statsmodels |

### Key Differences
1. **Reactivity**: Django uses AJAX calls instead of R's reactive programming
2. **Plotting**: Interactive Plotly.js charts instead of static R plots
3. **Data Persistence**: Django models can store analysis sessions
4. **Deployment**: Standard web application deployment options

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production Options

1. **Heroku**:
   ```bash
   # Add Procfile and runtime.txt
   git add .
   git commit -m "Deploy to Heroku"
   heroku create your-app-name
   git push heroku main
   ```

2. **Docker**:
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8000
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

3. **Traditional Server** (with Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn statistical_analysis.wsgi:application
   ```

## 🛡️ Security Notes

For production deployment:

1. **Change SECRET_KEY** in `settings.py`
2. **Set DEBUG = False**
3. **Configure ALLOWED_HOSTS**
4. **Use environment variables** for sensitive settings
5. **Set up HTTPS**
6. **Configure database** (PostgreSQL recommended)

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database errors**: Run migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **File upload issues**: Check media settings in `settings.py`

4. **Plot rendering issues**: Ensure Plotly.js is loaded correctly

### Debug Mode
Set `DEBUG = True` in `settings.py` for detailed error messages during development.

## 📈 Performance Considerations

- **Large datasets**: Consider pagination for data preview
- **File uploads**: Implement file size limits
- **Database**: Use PostgreSQL for production
- **Caching**: Implement Redis for session caching
- **CDN**: Use CDN for static files in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project maintains the same license as the original R Shiny application.

## 🔗 Related Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Plotly.js Documentation](https://plotly.com/javascript/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Note**: This Django application provides equivalent functionality to the original R Shiny app with modern web technologies and improved scalability. 