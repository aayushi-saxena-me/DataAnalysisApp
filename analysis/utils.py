import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
from scipy import stats
from scipy.stats import normaltest, shapiro
import io
import base64
from sklearn.preprocessing import StandardScaler


def generate_random_data(sample_size=1000):
    """Generate random data similar to R's rnorm"""
    np.random.seed(123)
    return pd.DataFrame({
        'x': np.random.normal(0, 1, sample_size),
        'y': np.random.normal(0, 1, sample_size),
        'z': np.random.normal(0, 1, sample_size)
    })


def load_csv_file(file_path):
    """Load CSV file with error handling"""
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                return df, None
            except UnicodeDecodeError:
                continue
        return None, "Unable to decode file with common encodings"
    except Exception as e:
        return None, f"Error loading file: {str(e)}"


def get_summary_statistics(data, column=None):
    """Calculate summary statistics for a column or dataset"""
    if column and column in data.columns:
        series = data[column]
    elif len(data.columns) == 1:
        series = data.iloc[:, 0]
    else:
        # For multiple columns, return summary for all numeric columns
        return data.describe().to_dict()
    
    if not pd.api.types.is_numeric_dtype(series):
        return {"error": "Selected column is not numeric"}
    
    stats_dict = {
        'count': int(len(series)),
        'mean': float(series.mean()),
        'median': float(series.median()),
        'std': float(series.std()),
        'var': float(series.var()),
        'min': float(series.min()),
        'max': float(series.max()),
        'q25': float(series.quantile(0.25)),
        'q75': float(series.quantile(0.75)),
        'skewness': float(stats.skew(series)),
        'kurtosis': float(stats.kurtosis(series))
    }
    return stats_dict


def perform_hypothesis_test(data, column=None, test_value=0):
    """Perform one-sample t-test"""
    if column and column in data.columns:
        series = data[column]
    elif len(data.columns) == 1:
        series = data.iloc[:, 0]
    else:
        series = data.iloc[:, 0]  # Default to first column
    
    if not pd.api.types.is_numeric_dtype(series):
        return {"error": "Selected column is not numeric"}
    
    # One-sample t-test
    t_stat, p_value = stats.ttest_1samp(series, test_value)
    
    # Normality tests
    shapiro_result = shapiro(series[:5000] if len(series) > 5000 else series)  # Shapiro limited to 5000 samples
    shapiro_stat, shapiro_p = shapiro_result
    
    try:
        return {
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'test_value': float(test_value),
            'sample_mean': float(series.mean()),
            'shapiro_statistic': float(shapiro_stat),
            'shapiro_p_value': float(shapiro_p),
            'is_normal': bool(shapiro_p > 0.05)
        }
    except (TypeError, ValueError):
        # Fallback for any conversion issues
        return {
            't_statistic': str(t_stat),
            'p_value': str(p_value),
            'test_value': float(test_value),
            'sample_mean': float(series.mean()),
            'shapiro_statistic': str(shapiro_stat),
            'shapiro_p_value': str(shapiro_p),
            'is_normal': bool(shapiro_p > 0.05)
        }


def create_histogram_plotly(data, column, bins=30, color='blue'):
    """Create histogram using Plotly"""
    if column not in data.columns:
        return None
    
    series = data[column]
    if not pd.api.types.is_numeric_dtype(series):
        return None
    
    fig = px.histogram(
        data, 
        x=column, 
        nbins=bins,
        title=f'Distribution of {column}',
        color_discrete_sequence=[color.lower()]
    )
    
    fig.update_layout(
        xaxis_title="Value",
        yaxis_title="Count",
        template="plotly_white"
    )
    
    return fig.to_json()


def create_boxplot_plotly(data, column=None):
    """Create box plot using Plotly"""
    if column and column in data.columns:
        if not pd.api.types.is_numeric_dtype(data[column]):
            return None
        
        fig = go.Figure()
        fig.add_trace(go.Box(y=data[column], name=column))
        fig.update_layout(
            title=f'Box Plot of {column}',
            yaxis_title="Value",
            template="plotly_white"
        )
    else:
        # Multiple columns - show all numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return None
        
        fig = go.Figure()
        for col in numeric_cols:
            fig.add_trace(go.Box(y=data[col], name=col))
        
        fig.update_layout(
            title='Box Plot',
            yaxis_title="Value",
            template="plotly_white"
        )
    
    return fig.to_json()


def create_qq_plot_plotly(data, column):
    """Create Q-Q plot using Plotly"""
    if column not in data.columns:
        return None
    
    series = data[column].dropna()
    if not pd.api.types.is_numeric_dtype(series):
        return None
    
    # Generate theoretical quantiles
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(series)))
    sample_quantiles = np.sort(series)
    
    fig = go.Figure()
    
    # Add scatter plot
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sample_quantiles,
        mode='markers',
        name='Sample Quantiles',
        marker=dict(color='blue', size=4)
    ))
    
    # Add reference line
    min_val = min(theoretical_quantiles.min(), sample_quantiles.min())
    max_val = max(theoretical_quantiles.max(), sample_quantiles.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='Reference Line',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title=f'Q-Q Plot of {column}',
        xaxis_title="Theoretical Quantiles",
        yaxis_title="Sample Quantiles",
        template="plotly_white"
    )
    
    return fig.to_json()


def create_correlation_plot_plotly(data):
    """Create correlation heatmap using Plotly"""
    numeric_data = data.select_dtypes(include=[np.number])
    if len(numeric_data.columns) < 2:
        return None
    
    corr_matrix = numeric_data.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Correlation Matrix',
        template="plotly_white",
        width=600,
        height=600
    )
    
    return fig.to_json()


def get_data_info(data):
    """Get basic information about the dataset"""
    info = {
        'shape': data.shape,
        'columns': list(data.columns),
        'dtypes': dict(data.dtypes.astype(str)),
        'missing_values': dict(data.isnull().sum()),
        'numeric_columns': list(data.select_dtypes(include=[np.number]).columns),
        'categorical_columns': list(data.select_dtypes(include=['object']).columns)
    }
    return info 