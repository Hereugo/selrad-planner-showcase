import os 

def export_keys(request):
    data = {}
    data['YANDEX_API_KEY'] = os.environ['YANDEX_API_KEY']
    return data
