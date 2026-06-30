from django.db import models
import os
import uuid
from .validators import validate_pdf_file

def question_paper_upload_path(instance, filename):
    """
    Generates a secure, randomized path for uploaded question papers.
    Renaming files to random UUIDs prevents:
    - Path traversal attacks (e.g., using '../../' in filename)
    - Filename collisions
    - Executable upload execution
    Organizes files on storage as: question_papers/<year>/<course>/<uuid>.pdf
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext != '.pdf':
        ext = '.pdf'
    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    # Organize by year and course on the disk
    return os.path.join('question_papers', str(instance.year), instance.course, unique_name)


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="e.g. Software Engineering, Financial Accounting")
    code = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="e.g. CS501 (Optional)")

    class Meta:
        ordering = ['name']

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


class QuestionPaper(models.Model):
    COURSE_CHOICES = [
        ('BSC', 'Bachelor of Science (B.Sc)'),
        ('MSC', 'Master of Science (M.Sc)'),
        ('MCA', 'Master of Computer Applications (M.C.A)'),
    ]

    SEMESTER_CHOICES = [
        ('SEM1', 'Semester 1'),
        ('SEM2', 'Semester 2'),
        ('SEM3', 'Semester 3'),
        ('SEM4', 'Semester 4'),
        ('SEM5', 'Semester 5'),
        ('SEM6', 'Semester 6'),
    ]

    course = models.CharField(max_length=20, choices=COURSE_CHOICES, help_text="Select the degree/course")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='papers', help_text="Select the subject")
    year = models.IntegerField(help_text="Enter the exam year (e.g. 2024)")
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, help_text="Select the semester")
    
    file = models.FileField(
        upload_to=question_paper_upload_path,
        validators=[validate_pdf_file],
        help_text="Upload the question paper (PDF format only, max 10MB)"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(
        default=False, 
        help_text="Designates whether this paper is approved to display on the public listing."
    )

    class Meta:
        ordering = ['-year', 'semester', 'subject']

    def __str__(self):
        return f"{self.get_course_display()} - {self.subject.name} ({self.year} - {self.get_semester_display()})"


def subject_note_upload_path(instance, filename):
    """
    Generates a secure randomized path for uploaded notes: subject_notes/<course>/<uuid>.pdf
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext != '.pdf':
        ext = '.pdf'
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return os.path.join('subject_notes', instance.course, unique_name)


class SubjectNote(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Calculus Unit 1, Organic Chemistry notes")
    course = models.CharField(max_length=20, choices=QuestionPaper.COURSE_CHOICES, help_text="Select the course")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes', help_text="Select the subject")
    
    file = models.FileField(
        upload_to=subject_note_upload_path,
        validators=[validate_pdf_file],
        help_text="Upload notes in PDF format (max 10MB)"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether this note is approved to display on the public listing."
    )

    class Meta:
        ordering = ['subject', 'title']

    def __str__(self):
        return f"{self.get_course_display()} - {self.subject.name} - {self.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, help_text="User's full name")
    email = models.EmailField(help_text="User's email address")
    subject = models.CharField(max_length=200, help_text="Subject of the message/report")
    message = models.TextField(help_text="Detailed message content")
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(
        default=False, 
        help_text="Designates whether this issue has been resolved by an administrator."
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

