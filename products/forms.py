from django import forms

class ContactForm(forms.Form):
    fullname    = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    email       = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    content     = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder': 'Your content'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError('Email has to be gmail.com')
        return email
    