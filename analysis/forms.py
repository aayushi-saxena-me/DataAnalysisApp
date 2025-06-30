from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import UploadedFile


class AnalysisForm(forms.Form):
    DATA_SOURCE_CHOICES = [
        ('random', 'Random Data'),
        ('upload', 'Upload CSV'),
        ('local', 'Tumor Dataset'),
    ]
    
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
    ]
    
    data_source = forms.ChoiceField(
        choices=DATA_SOURCE_CHOICES,
        initial='local',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # File upload field
    uploaded_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': '.csv,.xlsx,.xls',
            'class': 'form-control'
        }),
        help_text='Upload a CSV, Excel (.xlsx), or Excel (.xls) file'
    )
    
    # Sample size for random data
    sample_size = forms.IntegerField(
        initial=1000,
        min_value=100,
        max_value=10000,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # Column selection (will be populated dynamically)
    selected_column = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Visualization options
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        initial='blue',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    bins = forms.IntegerField(
        initial=30,
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'class': 'form-range',
            'oninput': 'this.nextElementSibling.value = this.value'
        })
    )
    
    # Display options
    show_plot = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    show_stats = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    show_correlation = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        column_choices = kwargs.pop('column_choices', [])
        super().__init__(*args, **kwargs)
        
        if column_choices:
            self.fields['selected_column'].choices = column_choices
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header"><h5>Analysis Configuration</h5></div>'),
            HTML('<div class="card-body">'),
            
            # Data Source Section
            HTML('<h6 class="text-primary">Data Source</h6>'),
            'data_source',
            
            # Conditional fields based on data source
            HTML('<div id="upload-section" style="display:none;">'),
            'uploaded_file',
            HTML('</div>'),
            
            HTML('<div id="random-section" style="display:none;">'),
            Row(Column('sample_size', css_class='col-md-6')),
            HTML('</div>'),
            
            HTML('<div id="column-section" style="display:none;">'),
            Row(Column('selected_column', css_class='col-md-6')),
            HTML('</div>'),
            
            HTML('<hr>'),
            
            # Visualization Options
            HTML('<h6 class="text-primary">Visualization Options</h6>'),
            Row(
                Column('color', css_class='col-md-4'),
                Column('bins', css_class='col-md-4'),
            ),
            
            HTML('<div class="d-flex align-items-center mb-3">'),
            HTML('<span class="me-2">Bins:</span>'),
            HTML('<output class="form-control-plaintext">30</output>'),
            HTML('</div>'),
            
            HTML('<hr>'),
            
            # Display Options
            HTML('<h6 class="text-primary">Display Options</h6>'),
            Row(
                Column('show_plot', css_class='col-md-4'),
                Column('show_stats', css_class='col-md-4'),
                Column('show_correlation', css_class='col-md-4'),
            ),
            
            HTML('</div>'),
            HTML('</div>'),
            
            HTML('<div class="mt-3">'),
            Submit('submit', 'Update Analysis', css_class='btn btn-primary btn-lg'),
            HTML('</div>'),
        )
    
    def clean(self):
        cleaned_data = super().clean()
        data_source = cleaned_data.get('data_source')
        selected_column = cleaned_data.get('selected_column')
        
        if data_source == 'upload' and not cleaned_data.get('uploaded_file'):
            raise forms.ValidationError('Please upload a file when using "Upload CSV" option.')
        
        # Handle column validation for different data sources
        if data_source == 'random':
            # For random data, ensure we have a valid column
            if not selected_column or selected_column not in ['x', 'y', 'z']:
                cleaned_data['selected_column'] = 'x'
        elif data_source in ['local', 'upload']:
            # For local/upload data, if selected column is invalid, clear it
            # The view will set a default valid column
            if selected_column in ['x', 'y', 'z']:  # These are only valid for random data
                cleaned_data['selected_column'] = None
        
        return cleaned_data

    def clean_selected_column(self):
        selected_column = self.cleaned_data.get('selected_column')
        data_source = self.cleaned_data.get('data_source')
        
        # If no column is selected, that's OK for some cases
        if not selected_column:
            return selected_column
        
        # For random data, ensure the column is valid
        if data_source == 'random' and selected_column not in ['x', 'y', 'z']:
            # Don't raise error, just return a default
            return 'x'
        
        return selected_column


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': '.csv,.xlsx,.xls',
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            'file',
            Submit('upload', 'Upload File', css_class='btn btn-success')
        ) 