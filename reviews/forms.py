from django import forms
from django.forms import widgets
from . import models

class CreateReviewForm(forms.ModelForm):
    score = forms.IntegerField(max_value=5, min_value=1)
    
    class Meta:
        model = models.Review
        fields = [
            "review",
            "score",
        ]
        widgets = {
            "review": forms.Textarea(
                attrs = {"class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
            "scroe": forms.NumberInput(
                attrs = {"class":"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"}
            ),
        }
    
    def save(self):
        review = super().save(commit=False)
        return review