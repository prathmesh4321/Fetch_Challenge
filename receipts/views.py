import json
import uuid
import math
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_receipts(request):
    if request.method == 'POST':
        try:
            receipt_data = json.loads(request.body)
            receipt_id = str(uuid.uuid4())
            receipt_storage[receipt_id] = receipt_data
            response_data = {'id': receipt_id}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON payload.', status=400)
    else:
        return HttpResponse('Method not allowed.', status=405)

def get_points(request, id):
    if request.method == 'GET':
        receipt_data = receipt_storage[id]
        if receipt_data:
            points = calculate_points(receipt_data)
            response_data = {'points': points}
            return JsonResponse(response_data)
        else:
            return HttpResponse('Receipt not found.', status=404)
    else:
        return HttpResponse('Method not allowed.', status=405)

def calculate_points(receipt_data):
    points = 0
    # Rule 1: One point for every alphanumeric character in the retailer name
    points += sum(char.isalnum() for char in receipt_data['retailer'])
    

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    if float(receipt_data['total']).is_integer():
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    if float(receipt_data['total']) % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    item_count = len(receipt_data['items'])
    points += (item_count // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item_data in receipt_data['items']:
        trimmed_description = item_data['shortDescription'].strip()
        if len(trimmed_description) % 3 == 0:
            points += math.ceil(float(item_data['price']) * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd
    if int(receipt_data['purchaseDate'].split('-')[2]) % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00 pm and before 4:00 pm
    purchase_time = receipt_data['purchaseTime'].split(':')
    if 14 <= int(purchase_time[0]) < 16:
        points += 10


    return points

# In-memory storage for receipt data
receipt_storage = {}
