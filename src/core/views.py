from django.http import JsonResponse
from django.shortcuts import render
from .models import Item

def item_list(request):
    items = Item.objects.all()
    return render(request, 'core/item_list.html', {'items': items})

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
    return render(request, 'core/api_demo.html')