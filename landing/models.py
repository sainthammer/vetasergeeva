from django.db import models
from django.urls import reverse


# =========================== Portfolio ===========================
class Project(models.Model):
    title = models.CharField("Название проекта", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    short_description = models.TextField("Короткое описание", max_length=300)
    full_description = models.TextField("Полное описание", blank=True)
    category = models.CharField("Категория", max_length=100, blank=True)
    client = models.CharField("Клиент", max_length=150, blank=True)
    cover_image = models.ImageField("Обложка", upload_to="projects/covers/")
    is_featured = models.BooleanField("Показывать в портфолио", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("landing:project_detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Проект",
    )
    image = models.ImageField("Изображение", upload_to="projects/examples/")
    caption = models.CharField("Подпись", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображения проекта"

    def __str__(self) -> str:
        return f"{self.project.title} — {self.caption or self.id}"


# =========================== About ===========================
class AboutPage(models.Model):

    hero_eyebrow = models.CharField(
        "Надпись над заголовком", max_length=100, default="обо мне"
    )

    hero_title = models.CharField("Главный заголовок", max_length=255)

    hero_text = models.TextField("Текст под заголовком")

    values_title = models.CharField(
        "Заголовок блока ценностей", max_length=255, default="Что мне близко"
    )

    timeline_eyebrow = models.CharField(
        "Надпись над опытом", max_length=100, default="опыт"
    )

    timeline_title = models.CharField("Заголовок блока опыта", max_length=255)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Страница About"

        verbose_name_plural = "Страница About"

    def __str__(self):

        return "Страница «Обо мне»"


class AboutValue(models.Model):

    page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name="Страница",
    )

    title = models.CharField("Заголовок", max_length=100)

    description = models.TextField("Описание")

    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:

        ordering = ["order", "id"]

        verbose_name = "Ценность / принцип"

        verbose_name_plural = "Ценности / принципы"

    def __str__(self):

        return self.title


class AboutTimelineItem(models.Model):

    page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="timeline_items",
        verbose_name="Страница",
    )

    period = models.CharField("Период", max_length=100)

    title = models.CharField("Заголовок", max_length=200)

    description = models.TextField("Описание")

    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:

        ordering = ["order", "id"]

        verbose_name = "Элемент таймлайна"

        verbose_name_plural = "Элементы таймлайна"

    def __str__(self):

        return f"{self.period} — {self.title}"


# =========================== Contacts ===========================
class ContactsPage(models.Model):
    hero_eyebrow = models.CharField(
        "Надпись над заголовком", max_length=100, default="контакты"
    )
    hero_title = models.CharField("Главный заголовок", max_length=255)
    hero_text = models.TextField("Текст под заголовком")

    card_kicker = models.CharField(
        "Надпись в карточке", max_length=100, default="контакты"
    )
    card_title = models.CharField(
        "Заголовок карточки", max_length=255, default="Давайте обсудим проект"
    )

    email = models.EmailField("Email", blank=True)
    telegram_url = models.URLField("Ссылка на Telegram", blank=True)
    telegram_label = models.CharField("Текст Telegram", max_length=100, blank=True)

    instagram_url = models.URLField("Ссылка на Instagram", blank=True)
    instagram_label = models.CharField("Текст Instagram", max_length=100, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страница Contacts"
        verbose_name_plural = "Страница Contacts"

    def __str__(self):
        return "Страница «Контакты»"


class ContactRequest(models.Model):
    name = models.CharField("Имя", max_length=120)
    contact = models.CharField("Контакт", max_length=255)
    message = models.TextField("Сообщение")

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    is_processed = models.BooleanField("Обработано", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} — {self.contact}"


# =========================== Homepage ===========================
class HomePage(models.Model):
    hero_eyebrow = models.CharField("Hero eyebrow", max_length=150)
    hero_title = models.CharField("Hero title", max_length=255)
    hero_text = models.TextField("Hero text")

    hero_primary_button_text = models.CharField(
        "Текст первой кнопки", max_length=100, default="Смотреть работы"
    )
    hero_primary_button_url = models.CharField(
        "URL первой кнопки", max_length=255, default="/portfolio/"
    )

    hero_secondary_button_text = models.CharField(
        "Текст второй кнопки", max_length=100, default="Обсудить проект"
    )
    hero_secondary_button_url = models.CharField(
        "URL второй кнопки", max_length=255, default="/contacts/"
    )

    hero_card_kicker = models.CharField(
        "Hero card kicker", max_length=100, default="selected focus"
    )
    hero_card_title = models.CharField(
        "Hero card title", max_length=150, default="Brand mood"
    )
    hero_card_text = models.TextField("Hero card text")

    services_eyebrow = models.CharField(
        "Eyebrow блока услуг", max_length=100, default="чем я занимаюсь"
    )
    services_title = models.CharField("Заголовок блока услуг", max_length=255)

    approach_eyebrow = models.CharField(
        "Eyebrow блока подхода", max_length=100, default="подход"
    )
    approach_title = models.CharField("Заголовок блока подхода", max_length=255)

    cta_eyebrow = models.CharField(
        "CTA eyebrow", max_length=100, default="готовы начать"
    )
    cta_title = models.CharField("CTA title", max_length=255)
    cta_button_text = models.CharField(
        "CTA button text", max_length=100, default="Связаться"
    )
    cta_button_url = models.CharField(
        "CTA button URL", max_length=255, default="/contacts/"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Главная страница"


class HomeStat(models.Model):
    page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="stats",
        verbose_name="Страница",
    )
    value = models.CharField("Значение", max_length=50)
    description = models.CharField("Описание", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return f"{self.value} — {self.description}"


class HomeService(models.Model):
    page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Страница",
    )
    title = models.CharField("Заголовок", max_length=150)
    description = models.TextField("Описание")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Услуга на главной"
        verbose_name_plural = "Услуги на главной"

    def __str__(self):
        return self.title


class HomeApproachStep(models.Model):
    page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="approach_steps",
        verbose_name="Страница",
    )
    number = models.CharField("Номер", max_length=10, default="01")
    description = models.TextField("Описание")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Шаг подхода"
        verbose_name_plural = "Шаги подхода"

    def __str__(self):
        return f"{self.number}"


# =========================== Services ===========================
class ServicesPage(models.Model):
    hero_eyebrow = models.CharField("Hero eyebrow", max_length=100, default="услуги")
    hero_title = models.CharField("Hero title", max_length=255)
    hero_text = models.TextField("Hero text")

    cta_eyebrow = models.CharField(
        "CTA eyebrow", max_length=100, default="формат работы"
    )
    cta_title = models.CharField("CTA title", max_length=255)
    cta_button_text = models.CharField(
        "CTA button text", max_length=100, default="Оставить заявку"
    )
    cta_button_url = models.CharField(
        "CTA button URL", max_length=255, default="/contacts/"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страница Services"
        verbose_name_plural = "Страница Services"

    def __str__(self):
        return "Страница «Услуги»"


class ServiceItem(models.Model):
    page = models.ForeignKey(
        ServicesPage,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Страница",
    )
    kicker = models.CharField("Номер / kicker", max_length=20, default="01")
    title = models.CharField("Заголовок", max_length=150)
    description = models.TextField("Описание")
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):
    service = models.ForeignKey(
        ServiceItem,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Услуга",
    )
    text = models.CharField("Пункт", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Пункт услуги"
        verbose_name_plural = "Пункты услуги"

    def __str__(self):
        return self.text
