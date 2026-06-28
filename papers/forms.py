from django import forms
from .models import QuestionPaper, Subject, SubjectNote, ContactMessage
from datetime import datetime

class QuestionPaperUploadForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['course', 'subject', 'year', 'semester', 'file']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2024',
                'min': 2000,
                'max': datetime.now().year + 1
            }),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'id': 'file-upload-input'
            }),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = datetime.now().year
        if not year:
            raise forms.ValidationError("Year is required.")
        if year < 2000 or year > current_year + 1:
            raise forms.ValidationError(f"Please enter a valid year between 2000 and {current_year + 1}.")
        return year


class SubjectNoteUploadForm(forms.ModelForm):
    class Meta:
        model = SubjectNote
        fields = ['title', 'course', 'subject', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Calculus Unit 1, Organic Chemistry notes'
            }),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
                'id': 'note-file-upload-input'
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject / Topic'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your request, issue, or DMCA report here...',
                'rows': 5
            }),
        }

