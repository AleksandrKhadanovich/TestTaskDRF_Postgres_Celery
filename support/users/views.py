from celtasks.tasks import comm_created
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Comm
from users.permissions import IsOwnerOnly
from users.serializers import CommDetailSerializer, CommListSerializer, CommCreateSerializer, CommListSerializerAdmin
from users.serializers import UserSerializer, LoginSerializer


# View for creating new users
class CreateUserView (APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# View for creating tickets
class CommCreateView (generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        commid = serializer.data["id"]
        comm_created.delay(commid)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# View for listing all comments for adminuser
class CommListViewAdmin (generics.ListAPIView):
    serializer_class = CommListSerializerAdmin
    queryset = Comm.objects.all()
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']


# View to list to user his own tickets and support answers
class CommListView (generics.ListAPIView):
    serializer_class = CommListSerializer
    queryset = Comm.objects.all()
    permission_classes = (IsOwnerOnly,)

    def get_queryset(self):
        user1 = self.request.user
        return Comm.objects.filter(user_id=user1.id)


# View for adminuser to answer tickets, change its status
class CommDetailView (generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommDetailSerializer
    queryset = Comm.objects.all()
    permission_classes = (IsAdminUser,)


# View for getting JWT token
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
