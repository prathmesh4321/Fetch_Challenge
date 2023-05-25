import json
from django.test import RequestFactory, TestCase
from .views import process_receipts, get_points, calculate_points, receipt_storage

class ReceiptsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_process_receipts_valid_payload(self):
        # Create a POST request with a valid payload
        data = {
            'retailer': 'Target',
            'purchaseDate': '2022-01-01',
            'purchaseTime': '13:01',
            'items': [
                {
                    'shortDescription': 'Mountain Dew 12PK',
                    'price': '6.49'
                },
                {
                    'shortDescription': 'Emils Cheese Pizza',
                    'price': '12.25'
                },
                {
                    'shortDescription': 'Knorr Creamy Chicken',
                    'price': '1.26'
                },
                {
                    'shortDescription': 'Doritos Nacho Cheese',
                    'price': '3.35'
                },
                {
                    'shortDescription': '   Klarbrunn 12-PK 12 FL OZ  ',
                    'price': '12.00'
                }
            ],
            'total': '35.35'
        }
        request = self.factory.post('/receipts/process', json.dumps(data), content_type='application/json')

        # Call the view function
        response = process_receipts(request)

        # Assert that the response is successful and contains an ID
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', json.loads(response.content))

    def test_process_receipts_invalid_payload(self):
        # Create a POST request with an invalid payload
        invalid_payload = '{"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zipcode": 12345}, "hobbies": ["reading", "swimming", "coding"}' 

        request = self.factory.post('/receipts/process', data=invalid_payload, content_type='application/json')

        # Call the view function
        response = process_receipts(request)

        # Assert that the response has status code 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

    def test_get_points_receipt_found(self):
        # Add a receipt to the storage
        receipt_id = '7fb1377b-b223-49d9-a31a-5a02701dd310'
        receipt_storage[receipt_id] = {
            'retailer': 'Target',
            'purchaseDate': '2022-01-01',
            'purchaseTime': '13:01',
            'items': [
                {
                    'shortDescription': 'Mountain Dew 12PK',
                    'price': '6.49'
                },
                {
                    'shortDescription': 'Emils Cheese Pizza',
                    'price': '12.25'
                },
                {
                    'shortDescription': 'Knorr Creamy Chicken',
                    'price': '1.26'
                },
                {
                    'shortDescription': 'Doritos Nacho Cheese',
                    'price': '3.35'
                },
                {
                    'shortDescription': '   Klarbrunn 12-PK 12 FL OZ  ',
                    'price': '12.00'
                }
            ],
            'total': '35.35'
        }

        # Create a GET request with the receipt ID
        request = self.factory.get(f'/receipts/{receipt_id}/points')

        # Call the view function
        response = get_points(request, receipt_id)

        # Assert that the response is successful and contains the points
        self.assertEqual(response.status_code, 200)
        self.assertIn('points', json.loads(response.content))

    def test_get_points_receipt_not_found(self):
        # Create a GET request with a non-existent receipt ID
        receipt_id = 'invalid_receipt_id'
        request = self.factory.get(f'/receipts/{receipt_id}/points')

        # Call the view function
        response = get_points(request, receipt_id)

        # Assert that the response has status code 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    def test_calculate_points(self):
        # Test the calculate_points function with a sample receipt data
        receipt_data = {
            'retailer': 'Target',
            'purchaseDate': '2022-01-01',
            'purchaseTime': '13:01',
            'items': [
                {
                    'shortDescription': 'Mountain Dew 12PK',
                    'price': '6.49'
                },
                {
                    'shortDescription': 'Emils Cheese Pizza',
                    'price': '12.25'
                },
                {
                    'shortDescription': 'Knorr Creamy Chicken',
                    'price': '1.26'
                },
                {
                    'shortDescription': 'Doritos Nacho Cheese',
                    'price': '3.35'
                },
                {
                    'shortDescription': '   Klarbrunn 12-PK 12 FL OZ  ',
                    'price': '12.00'
                }
            ],
            'total': '35.35'
        }

        # Calculate the points
        points = calculate_points(receipt_data)

        # Assert that the calculated points are correct
        self.assertEqual(points, 28)
