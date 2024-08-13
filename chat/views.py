from django.shortcuts import render
import os 
import openai
# from openai import OpenAI 
from django.http import JsonResponse
from .models import Chat


api_key = os.getenv('OPENAI_KEY')
if not api_key:
    raise ValueError('API key is not set')

# client = OpenAI(api_key)

openai.api_key = api_key
                

# Create your views here.
def index(request):
    return render(request, 'index.html')

def response(request):
    if request.method == 'POST':
        message = request.POST.get('message', 'your-api-key') 
        
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ]
        )
        
        answer = completion.choices[0].message.content 
        new_chat = Chat(message=message, response=answer)
        new_chat.save()
        return JsonResponse({'response': answer})
    return JsonResponse({'response': 'Invalid request'}, status=400)
            
        
        
