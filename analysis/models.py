from django.db import models
from django.core.validators import FileExtensionValidator
import os


class UploadedFile(models.Model):
    """Model to store uploaded CSV files"""
    file = models.FileField(
        upload_to='uploads/',
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'xls'])]
    )
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField()
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_name} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
    
    def delete(self, *args, **kwargs):
        # Delete the file from filesystem when model is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)


class AnalysisSession(models.Model):
    """Model to store analysis sessions and parameters"""
    session_id = models.CharField(max_length=100, unique=True)
    data_source = models.CharField(max_length=20, choices=[
        ('random', 'Random Data'),
        ('upload', 'Upload CSV'),
        ('local', 'Tumor Dataset')
    ])
    sample_size = models.IntegerField(null=True, blank=True)
    selected_column = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=20, default='blue')
    bins = models.IntegerField(default=30)
    show_plot = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True)
    show_correlation = models.BooleanField(default=True)
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.data_source}" 