from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer


@api_view(['GET'])
def endpoints(request):
    data = ['/advocates', 'advocates/:username']
    return Response(data)


@api_view(['GET', 'POST'])      #so we can use all functions of rest and response (not jsonresponse)
# @permission_classes([IsAuthenticated])   
def advocate_list(request):
    #Handles GET requests
    if request.method == 'GET':
        # data = ['Sapir', 'Dennis', 'Max']
        query = request.GET.get('query')        #getting data from url
        if query == None:       #if theres no query then well set this to an empty string
            query = ''

        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))   #thats an object. if we'll return this as a response we'll get an error( we need to turn this into json) icontains filters whatsever in the query and is not casesensitive
        serializer = AdvocateSerializer(advocates, many=True)       #im calling the serializer that i created in serializers module, and we pass in the object to be serialized
        return Response(serializer.data)        #return the data of the serialized object 

    if request.method == 'POST':
        #Handles POST request (adding user)
        advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
            )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)


class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise JsonResponse('Advocate doesnt exists')

    def get(self, request, username):
        advocate = self.get_object(username)

        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):
        advocate = Advocate.objects.get(username=username)

        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def delete(self, request, username):
        advocate = Advocate.objects.get(username=username)

        advocate.delete()
        return Response('user was deleted')


#function based views
# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(request, username):
#     advocate = Advocate.objects.get(username=username)
#     # return Response('hi')
#     if request.method == 'GET':
#         # data = username
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']

#         advocate.save()
        
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     if request.method == 'DELETE':
#         advocate.delete()
#         return redirect('advocates')
        

@api_view(['GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)
