from django_filters import FilterSet, NumberFilter
from rest_framework.exceptions import ValidationError

from members.models import Member
from members.services.members import find_member_by_location_distance


class MemberFilter(FilterSet):
    distance = NumberFilter(method='filter_distance')

    def filter_distance(self, queryset, _, value):
        try:
            return find_member_by_location_distance(
                longitude=self.request.user.longitude,
                latitude=self.request.user.latitude,
                distance=value,
                qs=queryset
            )
        except AttributeError:
            raise ValidationError({'error': 'You should be authorized for searching people by distance'})

    class Meta:
        model = Member
        fields = ['sex', 'name', 'surname', 'distance']
