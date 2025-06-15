from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer
from django.core.mail import EmailMessage
from django.conf import settings

class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(settings.DEFAULT_FROM_EMAIL)
            # Send email
            email = EmailMessage(
                subject=serializer.validated_data['subject'],
                body=f"From: {serializer.validated_data['name']} <{serializer.validated_data['email']}>\n\n"
                     f"Message:\n{serializer.validated_data['message']}",
                from_email=settings.EMAIL_HOST_USER,
                to=[serializer.validated_data['email']]  
            )
            try:
                email.send()
                return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)