import requests
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializers.features import UserSerializer


class MoneyInOutAPIView(GenericAPIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        account_no = request.data.get('accountNo')
        token = request.data.get('token')  # Assume that the token is sent in the request body

        if not all([account_no, token]):
            return Response({"error": "Account number and token are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        url = 'http://34.101.154.14:8175/hackathon/bankAccount/transaction/info'
        data = {
            "accountNo": account_no,
            "traxType": ["TRANSFER_IN", "TRANSFER_OUT"],
            "pageNumber": 1,
            "recordsPerPage": 10
        }
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get('success') and 'data' in response_data:
            transactions = response_data['data']['transactions']
            total_in = sum(t['amount'] for t in transactions if t['traxType'] == 'Transfer In')
            total_out = sum(t['amount'] for t in transactions if t['traxType'] == 'Transfer Out')

            return Response({"total_in": total_in, "total_out": total_out}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to fetch transaction data."}, status=status.HTTP_400_BAD_REQUEST)


class GetUserAPIView(GenericAPIView):
    def get(self, request):
        account_no = request.data.get('accountNo')
        user = User.objects.filter(account_no=account_no).first()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
