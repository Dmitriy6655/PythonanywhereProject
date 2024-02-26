from django import forms
from .models import Goods, Image


class EditGoodForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(
        label=False, widget=forms.Textarea(attrs={"placeholder": "Description"})
    )
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField(min_value=0)
    image = forms.ImageField(widget=forms.FileInput(attrs={"placeholder": "Image"}))

    class Meta:
        model = Goods
        fields = ('title', 'description', 'price', 'quantity', 'image')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']
