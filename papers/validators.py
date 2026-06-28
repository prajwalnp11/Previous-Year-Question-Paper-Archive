import os
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_pdf_file(value):
    """
    Validates that the uploaded file:
    1. Has a .pdf file extension.
    2. Does not exceed the configured maximum upload size (default 10MB).
    3. Contains the standard PDF magic number header (%PDF) at the very start.
    """
    # 1. Check extension
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError('Only PDF files are allowed. Please convert your file to PDF format.')

    # 2. Check file size
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if value.size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(f'File size exceeds the limit. Maximum allowed size is {max_mb:.1f} MB.')

    # 3. Check file signature (magic number)
    try:
        # Save current position and seek to start
        value.seek(0)
        header = value.read(4)
        # Reset stream pointer
        value.seek(0)

        if header != b'%PDF':
            raise ValidationError('Security Alert: The uploaded file has a .pdf extension but its content is not a valid PDF document.')
    except Exception as e:
        raise ValidationError(f'Could not validate file integrity: {str(e)}')
