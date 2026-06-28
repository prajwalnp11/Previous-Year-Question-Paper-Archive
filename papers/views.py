from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import QuestionPaper, Subject, SubjectNote
from .forms import QuestionPaperUploadForm, SubjectNoteUploadForm, ContactForm

def paper_list(request):
    """
    Lists all approved question papers, with multiple filter/search options.
    """
    papers = QuestionPaper.objects.filter(is_approved=True)

    # Retrieve filters from GET request
    q = request.GET.get('q', '').strip()
    course = request.GET.get('course', '').strip()
    subject_id = request.GET.get('subject', '').strip()
    year = request.GET.get('year', '').strip()
    semester = request.GET.get('semester', '').strip()

    # Apply search query
    if q:
        papers = papers.filter(
            Q(subject__name__icontains=q) |
            Q(subject__code__icontains=q)
        )
    
    # Apply filters
    if course:
        papers = papers.filter(course=course)
    if subject_id:
        papers = papers.filter(subject_id=subject_id)
    if year:
        papers = papers.filter(year=year)
    if semester:
        papers = papers.filter(semester=semester)

    # Fetch data for drop-downs
    subjects = Subject.objects.all()
    # List of unique years available in database to populate dynamic filter list
    available_years = QuestionPaper.objects.filter(is_approved=True).values_list('year', flat=True).distinct().order_by('-year')

    context = {
        'papers': papers,
        'subjects': subjects,
        'years': available_years,
        'courses': QuestionPaper.COURSE_CHOICES,
        'semesters': QuestionPaper.SEMESTER_CHOICES,
        
        # Preserve search values in form inputs
        'selected_q': q,
        'selected_course': course,
        'selected_subject': int(subject_id) if subject_id.isdigit() else '',
        'selected_year': int(year) if year.isdigit() else '',
        'selected_semester': semester,
    }
    return render(request, 'papers/search.html', context)


def paper_upload(request):
    """
    Handles student file uploads safely.
    Uploads are queued in an unapproved state for moderation.
    """
    if request.method == 'POST':
        form = QuestionPaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            # Enforce unapproved state
            paper.is_approved = False
            paper.save()
            messages.success(
                request,
                "Thank you! Your question paper has been submitted successfully. "
                "It is now in the queue for review and will be live once an administrator verifies it."
            )
            return redirect('paper_upload')
        else:
            messages.error(request, "Upload failed. Please correct the errors highlighted below.")
    else:
        form = QuestionPaperUploadForm()

    return render(request, 'papers/upload.html', {'form': form})


def paper_detail(request, pk):
    """
    Dedicated detail and download page.
    Implements a landing zone configured for Google AdSense blocks.
    Only allows accessing approved papers to prevent viewing pending submissions.
    """
    paper = get_object_or_404(QuestionPaper, pk=pk, is_approved=True)
    return render(request, 'papers/download.html', {'paper': paper})


def notes_list(request):
    """
    Search and filter approved subject notes.
    """
    notes = SubjectNote.objects.filter(is_approved=True)

    # Retrieve filters from GET request
    q = request.GET.get('q', '').strip()
    course = request.GET.get('course', '').strip()
    subject_id = request.GET.get('subject', '').strip()

    # Apply search query
    if q:
        notes = notes.filter(
            Q(title__icontains=q) |
            Q(subject__name__icontains=q) |
            Q(subject__code__icontains=q)
        )
    
    # Apply filters
    if course:
        notes = notes.filter(course=course)
    if subject_id:
        notes = notes.filter(subject_id=subject_id)

    # Fetch data for drop-downs
    subjects = Subject.objects.all()

    context = {
        'notes': notes,
        'subjects': subjects,
        'courses': QuestionPaper.COURSE_CHOICES,
        
        # Preserve search values in form inputs
        'selected_q': q,
        'selected_course': course,
        'selected_subject': int(subject_id) if subject_id.isdigit() else '',
    }
    return render(request, 'papers/notes_list.html', context)


def notes_upload(request):
    """
    Handles student notes uploads safely.
    Uploads are queued in an unapproved state for moderation.
    """
    if request.method == 'POST':
        form = SubjectNoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.is_approved = False
            note.save()
            messages.success(
                request,
                "Thank you! Your subject notes have been submitted successfully. "
                "They are now in the queue for review and will be live once an administrator verifies them."
            )
            return redirect('notes_upload')
        else:
            messages.error(request, "Upload failed. Please correct the errors highlighted below.")
    else:
        form = SubjectNoteUploadForm()

    return render(request, 'papers/notes_upload.html', {'form': form})


def notes_detail(request, pk):
    """
    Dedicated detail page for notes.
    Implements a landing zone configured for Google AdSense blocks and countdown locker.
    Only allows accessing approved notes.
    """
    note = get_object_or_404(SubjectNote, pk=pk, is_approved=True)
    return render(request, 'papers/notes_download.html', {'note': note})


def privacy_policy(request):
    """
    Renders the privacy policy page required by Google AdSense policies.
    """
    return render(request, 'papers/privacy_policy.html')


def disclaimer(request):
    """
    Renders the website legal disclaimer of university affiliation.
    """
    return render(request, 'papers/disclaimer.html')


def terms_conditions(request):
    """
    Renders the terms and conditions regarding user-uploaded materials.
    """
    return render(request, 'papers/terms_conditions.html')


def about(request):
    """
    Renders the About Us page detailing the archive project's purpose.
    """
    return render(request, 'papers/about.html')


def contact_us(request):
    """
    Renders and processes the Contact Us inquiry/reporting form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been sent successfully. If necessary, a moderator will contact you shortly."
            )
            return redirect('contact_us')
        else:
            messages.error(request, "Failed to send message. Please review the details below.")
    else:
        form = ContactForm()
    
    return render(request, 'papers/contact.html', {'form': form})

