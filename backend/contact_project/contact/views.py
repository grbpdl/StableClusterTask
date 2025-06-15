from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings

class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            subject = serializer.validated_data['subject']
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

            try:
                send_mail(
                    subject,
                    full_message,
                    settings.EMAIL_HOST_USER,  # From email
                    [email],  # To email (e.g., your admin email)
                    fail_silently=False,
                )
                return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
