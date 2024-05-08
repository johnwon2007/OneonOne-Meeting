from rest_framework import permissions
from rest_framework.exceptions import NotFound
from .models.calendar import Calendar



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `creator`.
        return obj.calendar.creator == request.user


class IsCalendarOwner(permissions.BasePermission):
    message = 'You must be the owner of this calendar to view its meetings.'

    def has_permission(self, request, view):
        calendar_id = view.kwargs.get('calendar_id')
        try:
            # Get the calendar and check if the current user is the creator
            calendar = Calendar.objects.get(pk=calendar_id)
            return calendar.creator == request.user
        except Calendar.DoesNotExist:
            raise NotFound(detail="Calendar not found")
