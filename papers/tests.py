from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Subject, QuestionPaper, SubjectNote
from .validators import validate_pdf_file
import os

class JSSArchiveTests(TestCase):
    
    def setUp(self):
        # Set up a test subject
        self.subject = Subject.objects.create(name="Computer Architecture", code="CS302")
        
        # Create an approved question paper
        self.approved_paper = QuestionPaper.objects.create(
            course="BSC",
            subject=self.subject,
            year=2024,
            semester="SEM3",
            file=SimpleUploadedFile(
                "exam_2024.pdf", 
                b"%PDF-1.4 content of testing doc", 
                content_type="application/pdf"
            ),
            is_approved=True
        )
        
        # Create an unapproved question paper
        self.unapproved_paper = QuestionPaper.objects.create(
            course="BSC",
            subject=self.subject,
            year=2023,
            semester="SEM2",
            file=SimpleUploadedFile(
                "exam_2023.pdf", 
                b"%PDF-1.4 content of hidden doc", 
                content_type="application/pdf"
            ),
            is_approved=False
        )

        # Create an approved subject note
        self.approved_note = SubjectNote.objects.create(
            title="Intro to Calculus Notes",
            course="BSC",
            subject=self.subject,
            file=SimpleUploadedFile(
                "calculus_notes.pdf",
                b"%PDF-1.4 notes test",
                content_type="application/pdf"
            ),
            is_approved=True
        )

    def tearDown(self):
        # Clean up disk files created during unit tests
        for paper in QuestionPaper.objects.all():
            if paper.file:
                try:
                    if os.path.exists(paper.file.path):
                        os.remove(paper.file.path)
                except Exception:
                    pass
        for note in SubjectNote.objects.all():
            if note.file:
                try:
                    if os.path.exists(note.file.path):
                        os.remove(note.file.path)
                except Exception:
                    pass

    def test_search_view_approved_only(self):
        """
        Verify that search lists approved documents only, 
        and filters out any papers pending moderator approval.
        """
        response = self.client.get(reverse('paper_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Computer Architecture")
        # Should not display the unapproved file name/details
        self.assertNotContains(response, "exam_2023.pdf")

    def test_search_filtering_logic(self):
        """
        Test filtering search results by specific inputs (year/semester).
        """
        # Filter by year 2024
        response = self.client.get(reverse('paper_list'), {'year': '2024'})
        self.assertContains(response, "Computer Architecture")

        # Filter by year 2023 (Approved matches only; 2023 is unapproved, so this returns empty)
        response = self.client.get(reverse('paper_list'), {'year': '2023'})
        self.assertContains(response, "No Question Papers Found")

    def test_secure_upload_logic(self):
        """
        Verify that:
        1. Form submissions are saved.
        2. Uploads are marked 'is_approved=False' by default.
        3. Filenames are randomized to prevent script injection/collisions.
        """
        mock_pdf = SimpleUploadedFile(
            "student_submission.pdf", 
            b"%PDF-1.5 test upload", 
            content_type="application/pdf"
        )
        
        response = self.client.post(reverse('paper_upload'), {
            'course': 'MSC',
            'subject': self.subject.id,
            'year': 2025,
            'semester': 'SEM4',
            'file': mock_pdf
        })
        
        # Verify redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Retrieve the newly created paper
        new_paper = QuestionPaper.objects.get(course="MSC")
        
        # Verify moderation queue status
        self.assertFalse(new_paper.is_approved)
        
        # Verify filename has been randomized using UUID
        filename = os.path.basename(new_paper.file.name)
        self.assertNotEqual(filename, "student_submission.pdf")
        self.assertTrue(filename.endswith(".pdf"))

    def test_validator_accepts_valid_pdf(self):
        """
        Check that validator allows a genuine PDF starting with b'%PDF'.
        """
        valid_file = SimpleUploadedFile("valid.pdf", b"%PDF-1.4 contents", content_type="application/pdf")
        try:
            validate_pdf_file(valid_file)
        except ValidationError:
            self.fail("validate_pdf_file raised ValidationError unexpectedly for a valid PDF document.")

    def test_validator_rejects_non_pdf_extension(self):
        """
        Check that validator blocks non-pdf extensions even if content starts with %PDF.
        """
        fake_file = SimpleUploadedFile("fake_pdf.txt", b"%PDF-1.4 text contents", content_type="text/plain")
        with self.assertRaises(ValidationError) as context:
            validate_pdf_file(fake_file)
        self.assertIn("Only PDF files are allowed", str(context.exception))

    def test_validator_rejects_spoofed_pdf_contents(self):
        """
        Verify that a malicious executable or script masquerading as a PDF 
        (e.g., shell.pdf starting with PHP or HTML code) is blocked by signature checking.
        """
        spoofed_file = SimpleUploadedFile("malicious.pdf", b"<?php echo 'hacker_shell'; ?>", content_type="application/pdf")
        with self.assertRaises(ValidationError) as context:
            validate_pdf_file(spoofed_file)
        self.assertIn("content is not a valid PDF document", str(context.exception))

    def test_notes_view_filters(self):
        response = self.client.get(reverse('notes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Intro to Calculus Notes")

    def test_notes_upload_moderation(self):
        mock_pdf = SimpleUploadedFile("study_guide.pdf", b"%PDF-1.5 test data", content_type="application/pdf")
        response = self.client.post(reverse('notes_upload'), {
            'title': 'Quantum Physics Notes',
            'course': 'MSC',
            'subject': self.subject.id,
            'file': mock_pdf
        })
        self.assertEqual(response.status_code, 302)
        new_note = SubjectNote.objects.get(title="Quantum Physics Notes")
        self.assertFalse(new_note.is_approved)
        self.assertTrue(new_note.file.name.endswith('.pdf'))

    def test_compliance_views_status_code(self):
        """
        Check that all compliance pages return HTTP 200 OK.
        """
        for route_name in ['privacy_policy', 'disclaimer', 'terms_conditions', 'about']:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200)

    def test_contact_form_submission_success(self):
        """
        Check that submitting the contact form with valid data:
        1. Saves the record to database.
        2. Redirects correctly.
        """
        response = self.client.post(reverse('contact_us'), {
            'name': 'Ramesh Kumar',
            'email': 'ramesh@jss.edu',
            'subject': 'Broken Link Report',
            'message': 'The Calculus unit 1 note throws a 404.'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify saved object
        from .models import ContactMessage
        msg = ContactMessage.objects.get(email='ramesh@jss.edu')
        self.assertEqual(msg.name, 'Ramesh Kumar')
        self.assertEqual(msg.subject, 'Broken Link Report')
        self.assertFalse(msg.is_resolved)

    def test_contact_form_submission_invalid(self):
        """
        Verify that submitting invalid form data does not save a record and displays errors.
        """
        response = self.client.post(reverse('contact_us'), {
            'name': '',
            'email': 'invalid-email',
            'subject': '',
            'message': 'Short msg'
        })
        self.assertEqual(response.status_code, 200)
        from .models import ContactMessage
        self.assertFalse(ContactMessage.objects.filter(email='invalid-email').exists())

    def test_mca_course_option_exists(self):
        """
        Verify that MCA exists as a valid course choice.
        """
        choices = [choice[0] for choice in QuestionPaper.COURSE_CHOICES]
        self.assertIn('MCA', choices)

    def test_ads_txt_endpoint(self):
        """
        Verify that /ads.txt serves the correct digital seller records.
        """
        response = self.client.get('/ads.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')
        self.assertIn('google.com, pub-8995537400969198, DIRECT, f08c47fec0942fa0', response.content.decode())



