from django import forms

from .models import *


#class ListingForm(forms.Form):
#    list_item = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}), label='Item', max_length=60, strip=True, required=True)
#    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Decription', 'style': 'width: 300px; height:400px;', 'class': 'form-control'}), label='Description', max_length=500, required=False)
#    current_bid = forms.DecimalField(decimal_places=2, min_value=0.00)
#    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}), label='Item', max_length=200, strip=True, required=True)
#    image = forms.ImageField()

class ListingForm(forms.ModelForm):
    
    class Meta:

        model = Listing
        fields = ['list_item', 'description', 'current_bid', 'categoryType','image', ]
        #class form control creates a uniform look on a form
        widgets = {
                    'list_item': forms.TextInput(attrs={'class': 'form-control'}),
                    'description': forms.Textarea(attrs={'rows':2, 'maxlength': 1000, 'class': 'form-control'}),
                    'current_bid': forms.NumberInput(attrs={'class': 'form-control', 'min':0.00}),
                    'categoryType': forms.Select(attrs={'class': 'form-control'})
                    
                    }
        labels = {
            #change the label name of form fields instead of using default one from models.py
            "list_item": "Item Name",
            "current_bid": "Starting Bid"
        }
        #coding the category line in the same indent as field overrides the field

    # categoryType = forms.ModelChoiceField(
    #         queryset=Category.objects.all(),
    #         to_field_name='category',
    #         required=False,  
    #         widget=forms.Select(attrs={'class': 'form-control'})
    #   )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control',}),
            }
        labels = {
            #change the label name of form fields instead of using default one from models.py
            "comment": "",
        }


# class CommentForm(forms.Form):
#     bid = forms.DecimalField(label='Bid', initial=Listing.objects.get(pk=selectedListing.id))

