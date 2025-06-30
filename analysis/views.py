from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import pandas as pd
import json
import os
import uuid
from .forms import AnalysisForm, FileUploadForm
from .models import UploadedFile, AnalysisSession
from .utils import (
    generate_random_data, load_csv_file, get_summary_statistics,
    perform_hypothesis_test, create_histogram_plotly, create_boxplot_plotly,
    create_qq_plot_plotly, create_correlation_plot_plotly, get_data_info
)


def dashboard(request):
    """Main dashboard view"""
    session_id = request.session.get('analysis_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['analysis_session_id'] = session_id
    
    # Get or create analysis session
    analysis_session, created = AnalysisSession.objects.get_or_create(
        session_id=session_id,
        defaults={
            'data_source': 'local',
            'sample_size': 1000,
            'color': 'blue',
            'bins': 30,
            'show_plot': True,
            'show_stats': True,
            'show_correlation': True
        }
    )
    
    # Load initial data
    data, error = load_data(analysis_session)
    column_choices = []
    
    if data is not None:
        if analysis_session.data_source == 'random':
            column_choices = [('x', 'X'), ('y', 'Y'), ('z', 'Z')]
            analysis_session.selected_column = 'x'
        else:
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            column_choices = [(col, col.replace('_', ' ').title()) for col in numeric_columns]
            if not analysis_session.selected_column and column_choices:
                analysis_session.selected_column = column_choices[0][0]
        analysis_session.save()
    
    # Initialize form
    form_data = {
        'data_source': analysis_session.data_source,
        'sample_size': analysis_session.sample_size,
        'selected_column': analysis_session.selected_column,
        'color': analysis_session.color,
        'bins': analysis_session.bins,
        'show_plot': analysis_session.show_plot,
        'show_stats': analysis_session.show_stats,
        'show_correlation': analysis_session.show_correlation,
    }
    
    form = AnalysisForm(initial=form_data, column_choices=column_choices)
    
    context = {
        'form': form,
        'data_info': get_data_info(data) if data is not None else None,
        'error': error,
        'session_id': session_id
    }
    
    return render(request, 'analysis/dashboard.html', context)


def update_analysis(request):
    """Handle form submission and update analysis"""
    if request.method == 'POST':
        session_id = request.session.get('analysis_session_id')
        if not session_id:
            return redirect('analysis:dashboard')
        
        try:
            analysis_session = AnalysisSession.objects.get(session_id=session_id)
        except AnalysisSession.DoesNotExist:
            return redirect('analysis:dashboard')
        
        # Get column choices based on new data source
        new_data_source = request.POST.get('data_source', 'local')
        column_choices = []
        
        print(f"DEBUG: Switching to data source: {new_data_source}")
        print(f"DEBUG: Current selected_column: {analysis_session.selected_column}")
        
        if new_data_source == 'random':
            column_choices = [('x', 'X'), ('y', 'Y'), ('z', 'Z')]
        else:
            # Try to load data to get column choices
            temp_session = AnalysisSession(
                data_source=new_data_source,
                uploaded_file=analysis_session.uploaded_file
            )
            temp_data, temp_error = load_data(temp_session)
            if temp_data is not None:
                numeric_columns = temp_data.select_dtypes(include=['number']).columns.tolist()
                column_choices = [(col, col.replace('_', ' ').title()) for col in numeric_columns]
                print(f"DEBUG: Found numeric columns: {numeric_columns}")
            else:
                print(f"DEBUG: Failed to load data: {temp_error}")
        
        print(f"DEBUG: Column choices: {column_choices}")
        
        # Clear selected column if it doesn't exist in new data source
        current_selected = request.POST.get('selected_column') or analysis_session.selected_column
        valid_columns = [choice[0] for choice in column_choices]
        
        if current_selected and current_selected not in valid_columns:
            print(f"DEBUG: Current column '{current_selected}' not valid, clearing")
            # Don't pass the invalid column to the form
            post_data = request.POST.copy()
            if column_choices:
                post_data['selected_column'] = column_choices[0][0]
                print(f"DEBUG: Setting selected_column to: {column_choices[0][0]}")
            else:
                post_data['selected_column'] = ''
        else:
            post_data = request.POST
        
        form = AnalysisForm(post_data, request.FILES, column_choices=column_choices)
        
        if form.is_valid():
            # Update analysis session
            analysis_session.data_source = form.cleaned_data['data_source']
            analysis_session.sample_size = form.cleaned_data.get('sample_size', 1000)
            
            # Handle column selection based on data source
            new_selected_column = form.cleaned_data.get('selected_column')
            if new_selected_column:
                analysis_session.selected_column = new_selected_column
            else:
                # Set default column based on data source
                if column_choices:
                    analysis_session.selected_column = column_choices[0][0]
                else:
                    analysis_session.selected_column = None
            
            analysis_session.color = form.cleaned_data['color']
            analysis_session.bins = form.cleaned_data['bins']
            analysis_session.show_plot = form.cleaned_data['show_plot']
            analysis_session.show_stats = form.cleaned_data['show_stats']
            analysis_session.show_correlation = form.cleaned_data['show_correlation']
            
            # Handle file upload
            if form.cleaned_data['data_source'] == 'upload' and form.cleaned_data.get('uploaded_file'):
                uploaded_file = form.cleaned_data['uploaded_file']
                file_obj = UploadedFile.objects.create(
                    file=uploaded_file,
                    original_name=uploaded_file.name,
                    file_size=uploaded_file.size
                )
                analysis_session.uploaded_file = file_obj
            
            analysis_session.save()
            messages.success(request, 'Analysis updated successfully!')
        else:
            # Debug form errors
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            messages.error(request, 'Please correct the errors in the form.')
    
    return redirect('analysis:dashboard')


def get_plots(request):
    """AJAX endpoint to get plot data"""
    session_id = request.session.get('analysis_session_id')
    if not session_id:
        return JsonResponse({'error': 'No session found'})
    
    try:
        analysis_session = AnalysisSession.objects.get(session_id=session_id)
    except AnalysisSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'})
    
    # Load data
    data, error = load_data(analysis_session)
    if data is None:
        return JsonResponse({'error': error or 'Unable to load data'})
    
    plots = {}
    column = analysis_session.selected_column
    
    if analysis_session.show_plot:
        # Histogram
        if column and column in data.columns:
            plots['histogram'] = create_histogram_plotly(
                data, column, analysis_session.bins, analysis_session.color
            )
        
        # Box plot
        plots['boxplot'] = create_boxplot_plotly(data, column)
        
        # Q-Q plot
        if column and column in data.columns:
            plots['qqplot'] = create_qq_plot_plotly(data, column)
        
        # Correlation plot
        if analysis_session.show_correlation:
            plots['correlation'] = create_correlation_plot_plotly(data)
    
    return JsonResponse(plots)


def get_statistics(request):
    """AJAX endpoint to get statistical analysis"""
    session_id = request.session.get('analysis_session_id')
    if not session_id:
        return JsonResponse({'error': 'No session found'})
    
    try:
        analysis_session = AnalysisSession.objects.get(session_id=session_id)
    except AnalysisSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'})
    
    # Load data
    data, error = load_data(analysis_session)
    if data is None:
        return JsonResponse({'error': error or 'Unable to load data'})
    
    stats = {}
    column = analysis_session.selected_column
    
    if analysis_session.show_stats:
        # Summary statistics
        stats['summary'] = get_summary_statistics(data, column)
        
        # Hypothesis test
        stats['hypothesis_test'] = perform_hypothesis_test(data, column)
    
    return JsonResponse(stats)


def get_data_preview(request):
    """AJAX endpoint to get data preview"""
    session_id = request.session.get('analysis_session_id')
    if not session_id:
        return JsonResponse({'error': 'No session found'})
    
    try:
        analysis_session = AnalysisSession.objects.get(session_id=session_id)
    except AnalysisSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'})
    
    # Load data
    data, error = load_data(analysis_session)
    if data is None:
        return JsonResponse({'error': error or 'Unable to load data'})
    
    # Get first 100 rows for preview
    preview_data = data.head(100)
    
    # Convert to dict for JSON serialization
    data_dict = {
        'columns': list(preview_data.columns),
        'data': preview_data.values.tolist(),
        'total_rows': len(data),
        'preview_rows': len(preview_data)
    }
    
    return JsonResponse(data_dict)


def get_column_choices(request):
    """AJAX endpoint to get available columns for selection"""
    session_id = request.session.get('analysis_session_id')
    if not session_id:
        return JsonResponse({'error': 'No session found'})
    
    try:
        analysis_session = AnalysisSession.objects.get(session_id=session_id)
    except AnalysisSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'})
    
    # Load data
    data, error = load_data(analysis_session)
    if data is None:
        return JsonResponse({'error': error or 'Unable to load data'})
    
    if analysis_session.data_source == 'random':
        columns = [
            {'value': 'x', 'label': 'X'},
            {'value': 'y', 'label': 'Y'},
            {'value': 'z', 'label': 'Z'}
        ]
    else:
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        columns = [
            {'value': col, 'label': col.replace('_', ' ').title()}
            for col in numeric_columns
        ]
    
    return JsonResponse({'columns': columns})


def load_data(analysis_session):
    """Helper function to load data based on analysis session"""
    try:
        if analysis_session.data_source == 'random':
            data = generate_random_data(analysis_session.sample_size or 1000)
            return data, None
        
        elif analysis_session.data_source == 'upload':
            if analysis_session.uploaded_file:
                file_path = analysis_session.uploaded_file.file.path
                return load_csv_file(file_path)
            else:
                return None, "No file uploaded"
        
        elif analysis_session.data_source == 'local':
            # Look for the brain tumor dataset in the project root
            dataset_path = os.path.join(settings.BASE_DIR, 'brain_tumor_dataset.csv')
            if os.path.exists(dataset_path):
                return load_csv_file(dataset_path)
            else:
                # Fallback to random data if local file not found
                data = generate_random_data(1000)
                return data, "Local dataset not found, using random data"
        
        else:
            return None, "Invalid data source"
    
    except Exception as e:
        return None, f"Error loading data: {str(e)}"


# API Views for more complex operations
@require_http_methods(["POST"])
def upload_file(request):
    """Handle file upload via AJAX"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return JsonResponse({
                'success': True,
                'file_id': uploaded_file.id,
                'filename': uploaded_file.original_name
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def about(request):
    """About page view"""
    return render(request, 'analysis/about.html') 