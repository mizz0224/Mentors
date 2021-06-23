from django import forms
from . import models

class CreateReviewForm(forms.ModelForm):
    score = forms.IntegerField(max_value=5, min_value=1)
    
    class Meta:
        model = models.Review
        fields = (
            "review",
            "score",
        )
    
    def save(self):
        review = super().save(commit=False)
        return review