from django.contrib import admin
from django.utils.html import format_html

from . import models


class EnvironmentCredentials(admin.StackedInline):
    model = models.EnvironmentCredentials
    extra = 0


class EnvironmentInline(admin.StackedInline):
    model = models.Environment
    extra = 0


class EnvironmentLocationInline(admin.StackedInline):
    model = models.EnvironmentLocation
    extra = 0


class RelationInline(admin.StackedInline):
    model = models.Relation
    fields = ['application', 'person', 'owner', 'emergency', 'notes']
    extra = 0


class EngagementInline(admin.StackedInline):
    model = models.Engagement
    fieldsets = [
        (None, {'fields': ['application', 'start_date', 'end_date']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    extra = 0


class ActivityInline(admin.StackedInline):
    model = models.Activity
    fieldsets = [
        (None, {'fields': ['activity_type', 'users']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    extra = 0


class EngagementCommentInline(admin.StackedInline):
    model = models.EngagementComment
    extra = 0


class ActivityCommentInline(admin.StackedInline):
    model = models.ActivityComment
    extra = 0


class ApplicationFileUploadInline(admin.StackedInline):
    model = models.ApplicationFileUpload
    extra = 0


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['^name']

admin.site.register(models.Tag, TagAdmin)


admin.site.register(models.Organization)


class DataElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'weight']
    list_filter = ['category']
    search_fields = ['^name']

admin.site.register(models.DataElement, DataElementAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date','modified_date']
    fieldsets = [
        (None, {'fields': ['organization', 'name', 'description']}),
        ('Metadata', {
            'classes': ['collapse'],
            'fields': ['platform', 'lifecycle', 'origin', 'business_criticality', 'user_records', 'revenue', 'external_audience', 'internet_accessible']
        }),
        ('Tags', {
            'classes': ['collapse'],
            'fields': ['tags']
        }),
        ('Data Classification', {
            'classes': ['collapse'],
            'fields': ['data_elements']
        }),
        ('ThreadFix', {
            'classes': ['collapse'],
            'fields': ['threadfix', 'threadfix_team_id', 'threadfix_application_id']
        }),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['created_date', 'modified_date']
        }),
    ]
    list_display = ['name', 'platform', 'lifecycle', 'origin', 'business_criticality', 'external_audience', 'internet_accessible', 'data_elements_list', 'data_sensitivity_value', 'data_classification_level']
    list_filter = ('external_audience', 'internet_accessible')
    inlines = [EnvironmentInline, RelationInline, EngagementInline, ApplicationFileUploadInline]
    search_fields = ['^name']

    @staticmethod
    def data_elements_list(obj):
        return ", ".join([data_element.name for data_element in obj.data_elements.all()])

admin.site.register(models.Application, ApplicationAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    fields = ['application', 'environment_type', 'description', 'testing_approved']
    list_display = ['__str__', 'environment_type', 'application', 'testing_approved']
    inlines = [EnvironmentLocationInline, EnvironmentCredentials]

admin.site.register(models.Environment, EnvironmentAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'phone_work', 'phone_mobile']
    search_fields = ['^first_name', '^last_name', '^email']
    inlines = [RelationInline]

admin.site.register(models.Person, PersonAdmin)


class EngagementAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['application', 'start_date', 'end_date']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    list_display = ['__str__', 'start_date', 'end_date', 'status', 'application']
    inlines = [ActivityInline, EngagementCommentInline]

admin.site.register(models.Engagement, EngagementAdmin)


admin.site.register(models.ActivityType)


class ActivityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['engagement', 'activity_type', 'users']}),
        ('Advanced options', {
            'classes': ['collapse'],
            'fields': ['status', 'open_date', 'close_date']
        }),
    ]
    list_display = ['__str__', 'status', 'activity_type']
    inlines = [ActivityCommentInline]

admin.site.register(models.Activity, ActivityAdmin)

admin.site.register(models.ThreadFix)


class RegulationAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'category_display', 'jurisdiction', 'reference_link']

    def category_display(self, obj):
        return obj.get_category_display()
    category_display.admin_order_field = 'category'
    category_display.short_description = 'Category'

    def reference_link(self, obj):
        return format_html('<a href="{}" rel="nofollow" target="_blank">{}</a>', obj.reference, obj.reference)
    reference_link.admin_order_field = 'reference'
    reference_link.allow_tags = True
    reference_link.short_description = 'Reference'


admin.site.register(models.Regulation, RegulationAdmin)