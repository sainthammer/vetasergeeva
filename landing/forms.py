from django import forms
from .models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["name", "contact", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Анна",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "placeholder": "Email / Telegram",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Расскажите, что вам нужно",
                }
            ),
        }
