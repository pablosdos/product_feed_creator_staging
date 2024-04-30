from django import forms
from product_feed_generator.models import FeedConfiguration

class SftpXmlCredentialsForm(forms.Form):
    xml_user = forms.CharField(widget=forms.TextInput)
    xml_pass = forms.CharField(widget=forms.PasswordInput)
    sftp_url = forms.CharField(widget=forms.PasswordInput)