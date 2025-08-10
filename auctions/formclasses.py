from django import forms
from .models import AuctionListing, Bid, Comment

class Create(forms.ModelForm):

    class Meta:
        model = AuctionListing
        fields = [
            "title",
            "description",
            "starting_bid",
            "image",
            "categories"
        ]

        widgets = {
            'title': forms.TextInput (attrs= {'placeholder': "Enter the name of the item", 'class': "form-control inputoverride"}),
            'description': forms.Textarea (attrs= {
                                                'placeholder': "Enter a short description for the item", 
                                                'class': "form-control inputoverride",
                                                'rows': 5,
                                                'cols': 20
                                            }),

            'image': forms.TextInput (attrs= {'placeholder': "Enter URL", 'class': "form-control inputoverride"}),
            'starting_bid': forms.TextInput (attrs= {'placeholder': "in USD", 'class': "form-control inputoverride"}),
            'categories': forms.SelectMultiple (attrs= {'class': "form-control inputoverride"})
        }

class Bids(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            "bid_amount"
        ]

        widgets = {
            'bid_amount': forms.NumberInput (attrs= {'placeholder': "Enter your bid", 'class': "bid-input", 'min': 0})
        }

class Comments(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment"
        ]

        widgets = {
            'comment': forms.TextInput (attrs= {'placeholder': "How do you feel about this product? ", 'class': "form-control inputoverride"})
        }