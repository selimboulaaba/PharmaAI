from django import forms
from items.models import Cart, CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'item']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'min': 1})

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
