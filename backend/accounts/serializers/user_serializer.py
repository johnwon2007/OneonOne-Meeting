
from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer is used to convert User model instances into JSON
    representations and vice versa. It specifies the fields to be included
    in the serialized output and provides validation for the input data.

    Attributes:
        model (class): The User model class.
        fields (str): A string specifying the fields to be included in the
            serialized output. The value "__all__" indicates that all fields
            should be included.

    """
    class Meta:
        model = User
        fields = "__all__"