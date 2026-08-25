from django.http import JsonResponse
from django.shortcuts import render
from .models import Item

def item_list(request):
    items = Item.objects.all()
    return render(request, 'semana1/item_list.html', {'items': items})

def item_list_api(request):
    items = Item.objects.all().order_by('-created_at')
    data = [
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'created_at': item.created_at.isoformat(),
        }
        for item in items
    ]
    return JsonResponse(data, safe=False)

def api_demo(request):
    return render(request, 'semana1/api_demo.html')