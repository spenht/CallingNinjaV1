from django import forms

class UploadFilesForm(forms.Form):
    audio_file = forms.FileField(label='Audio file')
    csv_file = forms.FileField(label='Csv file')
