from django import forms
from .models import CompressImage

class CompressImageForm(forms.ModelForm):
    class Meta:
        model = CompressImage
        fields = ['original_image', 'quality']

    original_image = forms.ImageField(label='Select an image to compress')