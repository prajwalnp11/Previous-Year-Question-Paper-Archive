from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from papers.models import Subject, QuestionPaper, SubjectNote
import random

class Command(BaseCommand):
    help = 'Seeds JSS Archive database with subjects and mock question papers for all courses.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding academic subjects...')
        
        # Subject definitions mapped to courses
        subjects_data = [
            ("Mathematics", "MAT101"),
            ("Computer Science", "CS101"),
            ("Physics", "PHY101"),
            ("Biology", "BIO101"),
            ("Technology", "TECH101"),
            ("Chemistry", "CHE101"),
            ("Zoology", "ZOO101"),
            ("Biochemistry", "BC101"),
            ("Bio-Technology", "BT101"),
            ("Microbiology", "MB101"),
            ("Botany", "BOT101"),
        ]

        subjects = []
        for name, code in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=name,
                defaults={'code': code}
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'  Created Subject: {name} ({code})')

        self.stdout.write('Seeding mock question papers...')
        
        # Stand-in PDF file bytes
        mock_pdf_content = b"%PDF-1.4\n%mock pdf file content for JSS Archive testing\n%%EOF"
        
        courses_list = [
            ('BSC', [
                "Mathematics", "Computer Science", "Physics", "Biology", 
                "Technology", "Chemistry", "Zoology", "Biochemistry", 
                "Bio-Technology", "Microbiology", "Botany"
            ]),
            ('MSC', [
                "Mathematics", "Physics", "Chemistry", "Biochemistry", 
                "Bio-Technology", "Microbiology"
            ]),
        ]

        semesters = ['SEM1', 'SEM2', 'SEM3', 'SEM4', 'SEM5', 'SEM6']
        years = [2022, 2023, 2024, 2025]

        count = 0
        for course_code, subject_names in courses_list:
            for sub_name in subject_names:
                subj = Subject.objects.get(name=sub_name)
                
                # Create a few papers per subject
                for offset in range(2):
                    year = random.choice(years)
                    sem = random.choice(semesters)
                    
                    filename = f"exam_{course_code.lower()}_{subj.code.lower()}_{year}.pdf"
                    file_obj = SimpleUploadedFile(filename, mock_pdf_content, content_type="application/pdf")
                    
                    # Prevent duplicate creation
                    if not QuestionPaper.objects.filter(course=course_code, subject=subj, year=year, semester=sem).exists():
                        QuestionPaper.objects.create(
                            course=course_code,
                            subject=subj,
                            year=year,
                            semester=sem,
                            file=file_obj,
                            is_approved=True  # Automatically approved for demonstration
                        )
                        count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {count} question papers across courses!'))

        self.stdout.write('Seeding mock subject notes...')
        notes_count = 0
        for course_code, subject_names in courses_list:
            for sub_name in subject_names:
                subj = Subject.objects.get(name=sub_name)
                # Create a set of notes for this subject
                title = f"{subj.name} Unit 1 Study Guide"
                filename = f"notes_{course_code.lower()}_{subj.code.lower()}_u1.pdf"
                file_obj = SimpleUploadedFile(filename, mock_pdf_content, content_type="application/pdf")
                
                if not SubjectNote.objects.filter(course=course_code, subject=subj, title=title).exists():
                    SubjectNote.objects.create(
                        course=course_code,
                        subject=subj,
                        title=title,
                        file=file_obj,
                        is_approved=True
                    )
                    notes_count += 1
                    
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {notes_count} subject notes!'))
