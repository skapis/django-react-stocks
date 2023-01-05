from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, UserAccount
from .serializers import ProfileSerializer, UserSerializer
from stocks.models import Portfolio
from stocks.serializers import PortfolioSerializer


class UserProfile(APIView):
    def get(self, request):
        user = request.GET.get('user', None)
        if user:
            user = UserAccount.objects.get(email=user)
            profile = Profile.objects.get(owner=user.pk)
            portfolios = Portfolio.objects.filter(profile=profile.pk)
            userializer = UserSerializer(user)
            serializer = ProfileSerializer(profile)
            pserializer = PortfolioSerializer(portfolios, many=True)
            response = {
                'user': userializer.data,
                'profile': serializer.data,
                'portfolios': pserializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'errors': 'user is required'}, status=status.HTTP_400_BAD_REQUEST)





