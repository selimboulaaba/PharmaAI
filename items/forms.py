from django import forms
from items.models import Cart, CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'item']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control col-md-12'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'min': 1})

class ImageUploadForm(forms.Form):
    image = forms.ImageField()