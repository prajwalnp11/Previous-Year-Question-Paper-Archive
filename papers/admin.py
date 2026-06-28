from django.contrib import admin
from .models import Subject, QuestionPaper, SubjectNote, ContactMessage

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'year', 'semester', 'is_approved', 'uploaded_at')
    list_filter = ('is_approved', 'course', 'year', 'semester')
    search_fields = ('subject__name', 'subject__code')
    actions = ['approve_papers', 'reject_papers']
    ordering = ('-uploaded_at',)

    @admin.action(description="Approve selected question papers (Make public)")
    def approve_papers(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"Successfully approved {updated} question papers.")

    @admin.action(description="Reject selected question papers (Hide from public)")
    def reject_papers(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"Successfully revoked approval for {updated} question papers.")


@admin.register(SubjectNote)
class SubjectNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'course', 'is_approved', 'uploaded_at')
    list_filter = ('is_approved', 'course')
    search_fields = ('title', 'subject__name', 'subject__code')
    actions = ['approve_notes', 'reject_notes']
    ordering = ('-uploaded_at',)

    @admin.action(description="Approve selected notes (Make public)")
    def approve_notes(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"Successfully approved {updated} subject notes.")

    @admin.action(description="Reject selected notes (Hide from public)")
    def reject_notes(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"Successfully revoked approval for {updated} subject notes.")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    actions = ['mark_as_resolved', 'mark_as_unresolved']
    ordering = ('-created_at',)

    @admin.action(description="Mark selected messages as resolved")
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f"Successfully marked {updated} messages as resolved.")

    @admin.action(description="Mark selected messages as unresolved")
    def mark_as_unresolved(self, request, queryset):
        updated = queryset.update(is_resolved=False)
        self.message_user(request, f"Successfully marked {updated} messages as unresolved.")

