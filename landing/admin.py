from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Project,
    ProjectImage,
    AboutPage,
    AboutValue,
    AboutTimelineItem,
    ContactsPage,
    ContactRequest,
    HomePage,
    HomeStat,
    HomeService,
    HomeApproachStep,
    ServicesPage,
    ServiceItem,
    ServiceFeature,
)

# =========================== Shared helpers ===========================


class SingletonAdminMixin:
    """Разрешает только одну запись модели."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class OrderedTabularInline(admin.TabularInline):
    extra = 0
    ordering = ("order", "id")


# =========================== Portfolio ===========================


class ProjectImageInline(OrderedTabularInline):
    model = ProjectImage
    fields = ("order", "caption", "image", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 10px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "Превью"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "client",
        "is_featured",
        "order",
        "created_at",
        "cover_preview",
    )
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured", "category", "created_at")
    search_fields = (
        "title",
        "category",
        "client",
        "short_description",
        "full_description",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "cover_preview")
    inlines = [ProjectImageInline]

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "client",
                    "is_featured",
                    "order",
                ),
            },
        ),
        (
            "Описание",
            {
                "fields": ("short_description", "full_description"),
            },
        ),
        (
            "Обложка",
            {
                "fields": ("cover_image", "cover_preview"),
            },
        ),
        (
            "Служебное",
            {
                "fields": ("created_at",),
            },
        ),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 10px;" />',
                obj.cover_image.url,
            )
        return "—"

    cover_preview.short_description = "Превью обложки"


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "order", "image_preview")
    list_editable = ("order",)
    search_fields = ("project__title", "caption")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 8px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "Превью"


# =========================== About ===========================


class AboutValueInline(OrderedTabularInline):
    model = AboutValue
    fields = ("order", "title", "description")


class AboutTimelineItemInline(OrderedTabularInline):
    model = AboutTimelineItem
    fields = ("order", "period", "title", "description")


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Hero",
            {
                "fields": ("hero_eyebrow", "hero_title", "hero_text"),
            },
        ),
        (
            "Блок ценностей",
            {
                "fields": ("values_title",),
            },
        ),
        (
            "Блок опыта",
            {
                "fields": ("timeline_eyebrow", "timeline_title"),
            },
        ),
    )
    inlines = [AboutValueInline, AboutTimelineItemInline]


@admin.register(AboutValue)
class AboutValueAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "page")
    list_editable = ("order",)
    search_fields = ("title", "description")


@admin.register(AboutTimelineItem)
class AboutTimelineItemAdmin(admin.ModelAdmin):
    list_display = ("period", "title", "order", "page")
    list_editable = ("order",)
    search_fields = ("period", "title", "description")


# =========================== Contacts ===========================


@admin.register(ContactsPage)
class ContactsPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Hero",
            {
                "fields": ("hero_eyebrow", "hero_title", "hero_text"),
            },
        ),
        (
            "Карточка контактов",
            {
                "fields": ("card_kicker", "card_title"),
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    "email",
                    ("telegram_label", "telegram_url"),
                    ("instagram_label", "instagram_url"),
                ),
            },
        ),
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "contact", "message")
    list_editable = ("is_processed",)
    readonly_fields = ("name", "contact", "message", "created_at")
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Контакт",
            {
                "fields": ("name", "contact", "created_at"),
            },
        ),
        (
            "Сообщение",
            {
                "fields": ("message",),
            },
        ),
        (
            "Статус",
            {
                "fields": ("is_processed",),
            },
        ),
    )


# =========================== Homepage ===========================


class HomeStatInline(OrderedTabularInline):
    model = HomeStat
    fields = ("order", "value", "description")


class HomeServiceInline(OrderedTabularInline):
    model = HomeService
    fields = ("order", "title", "description")


class HomeApproachStepInline(OrderedTabularInline):
    model = HomeApproachStep
    fields = ("order", "number", "description")


@admin.register(HomePage)
class HomePageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Hero",
            {
                "fields": (
                    "hero_eyebrow",
                    "hero_title",
                    "hero_text",
                ),
            },
        ),
        (
            "Hero buttons",
            {
                "fields": (
                    ("hero_primary_button_text", "hero_primary_button_url"),
                    ("hero_secondary_button_text", "hero_secondary_button_url"),
                ),
            },
        ),
        (
            "Hero card",
            {
                "fields": (
                    "hero_card_kicker",
                    "hero_card_title",
                    "hero_card_text",
                ),
            },
        ),
        (
            "Блок услуг",
            {
                "fields": (
                    "services_eyebrow",
                    "services_title",
                ),
            },
        ),
        (
            "Блок подхода",
            {
                "fields": (
                    "approach_eyebrow",
                    "approach_title",
                ),
            },
        ),
        (
            "CTA",
            {
                "fields": (
                    "cta_eyebrow",
                    "cta_title",
                    ("cta_button_text", "cta_button_url"),
                ),
            },
        ),
    )
    inlines = [HomeStatInline, HomeServiceInline, HomeApproachStepInline]


@admin.register(HomeStat)
class HomeStatAdmin(admin.ModelAdmin):
    list_display = ("value", "description", "order")
    list_editable = ("order",)
    search_fields = ("value", "description")


@admin.register(HomeService)
class HomeServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    search_fields = ("title", "description")


@admin.register(HomeApproachStep)
class HomeApproachStepAdmin(admin.ModelAdmin):
    list_display = ("number", "order")
    list_editable = ("order",)
    search_fields = ("number", "description")


# =========================== Services ===========================


class ServiceFeatureInline(OrderedTabularInline):
    model = ServiceFeature
    fields = ("order", "text")


class ServiceItemInline(admin.StackedInline):
    model = ServiceItem
    extra = 0
    ordering = ("order", "id")
    show_change_link = True
    fields = ("order", "kicker", "title", "description")


@admin.register(ServicesPage)
class ServicesPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Hero",
            {
                "fields": ("hero_eyebrow", "hero_title", "hero_text"),
            },
        ),
        (
            "CTA",
            {
                "fields": (
                    "cta_eyebrow",
                    "cta_title",
                    ("cta_button_text", "cta_button_url"),
                ),
            },
        ),
    )
    inlines = [ServiceItemInline]


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "kicker", "order", "page")
    list_editable = ("order",)
    search_fields = ("title", "description")
    inlines = [ServiceFeatureInline]

    fieldsets = (
        (
            "Основное",
            {
                "fields": ("page", "order", "kicker", "title", "description"),
            },
        ),
    )


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("text", "service", "order")
    list_editable = ("order",)
    search_fields = ("text", "service__title")
