from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import Contact  
from accounts.serializers.contact_serializer import ContactSerializer 

class ContactUpdateDeleteView(APIView):
    """
    API view for updating and deleting a contact.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve a contact object by its primary key and owner.

        Args:
            pk (int): The primary key of the contact.

        Returns:
            Contact: The contact object if found, None otherwise.
        """
        try:
            return Contact.objects.get(pk=pk, owner=self.request.user)
        except Contact.DoesNotExist:
            return None

    def patch(self, request, pk):
        """
        Update a contact.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the contact.

        Returns:
            Response: The updated contact data if successful, error message otherwise.
        """
        contact = self.get_object(pk)
        if contact is None:
            return Response({'message': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a contact.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the contact.

        Returns:
            Response: Success message if successful, error message otherwise.
        """
        contact = self.get_object(pk)
        if contact is None:
            return Response({'message': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        contact.delete()
        return Response({'message': 'Contact deleted successfully'}, status=status.HTTP_200_OK)