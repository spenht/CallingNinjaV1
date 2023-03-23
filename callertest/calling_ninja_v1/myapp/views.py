from django.shortcuts import render, redirect
from twilio.rest import Client
from .models import Call
from .forms import UploadFilesForm
import csv
import io
from django.core.files.storage import default_storage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def index(request):
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            audio_file = request.FILES['audio_file']
            call_numbers(request, csv_file, audio_file)
            return redirect('results')
    else:
        form = UploadFilesForm()
    return render(request, 'myapp/upload.html', {'form': form})

@login_required
def results(request):
    calls = Call.objects.all()
    return render(request, 'myapp/results.html', {'calls': calls})

@login_required
def call_numbers(request, csv_file, audio_file):
    account_sid = 'AC00310fea74c24ba50e53717714fcc85c'
    auth_token = 'e7b7048c1af396caff9843cc90b8c61c'
    twilio_number = '+525593020309'
    client = Client(account_sid, auth_token)
    csv_file_in_text_mode = io.TextIOWrapper(io.BytesIO(csv_file.read()), encoding='utf-8')
    csv_reader = csv.reader(csv_file_in_text_mode)
    audio_file_path = default_storage.save(audio_file.name, audio_file)
    audio_file_url = request.build_absolute_uri(default_storage.url(audio_file_path))
    for row in csv_reader:
        phone_number = row[0]
        twiml_string = f'<Response><Play>{audio_file_url}</Play></Response>'
        print(f'TwiML: {twiml_string}')
        call = client.calls.create(
            twiml=twiml_string,
            to=phone_number,
            from_=twilio_number
        )

