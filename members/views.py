from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import MemberFilter
from .models import Member
from .serializers import MemberSerializer
from .services.images import add_member_photo_watermark
from .services.members import like_member, check_member_like_availability


class MemberListCreateApi(ListCreateAPIView):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filterset_class = MemberFilter

    def perform_create(self, serializer):
        serializer.save()
        add_member_photo_watermark(serializer.instance)


class MemberLikeApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        """Like a member. Add him to current user 'liked_members' relation"""
        check_member_like_availability(request.user, pk)
        like_member(request.user, pk)
        return Response({'success': True}, status=status.HTTP_200_OK)
