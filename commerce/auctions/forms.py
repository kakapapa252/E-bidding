from django import forms


from django.forms import ModelForm
from .models import *


class CreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['thumbnail'].required = True
        self.fields['title'].required = True
        self.fields['price'].required = True
        self.fields['category'].required = True

    class Meta:
        model = Listing
        fields = ['title','summary','price','thumbnail','category']
    

class BidForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid'].required = True

    class Meta:
        model = BiddingList
        fields = ['bid']


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].required = True
    
    class Meta:
        model = CommentList
        fields = ['comment']
