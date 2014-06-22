from rest_framework import viewsets, serializers
from dibs.models import Item
from dibs.twresource import sse_resource
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response


class CanLockItemApiPerm(DjangoModelPermissions):
    perms_map = {'POST': ['dibs.lock_item']}


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',)


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    locked_by = UserSerializer(read_only=True)
    children_count = serializers.IntegerField(read_only=True, source='children.count')
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'url', 'name', 'parent', 'locked_by', 'desc', 'can_be_locked',
                  'children_count', 'created', 'modified',)


class ItemViewSet(viewsets.ModelViewSet):
    model = Item
    serializer_class = ItemSerializer

    @action(permission_classes=[CanLockItemApiPerm])
    def lock(self, request, pk=None):
        item = self.get_object()
        locked_count = item.lock(request.user)
        if locked_count > 0:
            sse_resource.broadcast_message_async(str(item.pk), 'itemChange')
            return Response({'status': 'item locked'})
        else:
            return Response({'status': 'item not locked'}, status=status.HTTP_403_FORBIDDEN)

    @action(permission_classes=[CanLockItemApiPerm])
    def unlock(self, request, pk=None):
        item = self.get_object()
        unlocked_count = item.unlock(request.user)
        if unlocked_count > 0:
            sse_resource.broadcast_message_async(str(item.pk), 'itemChange')
            return Response({'status': 'item unlocked'})
        else:
            return Response({'status': 'item not unlocked'}, status=status.HTTP_403_FORBIDDEN)
