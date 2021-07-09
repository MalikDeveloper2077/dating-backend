from django.contrib.auth import get_user_model
from django.db.models.expressions import RawSQL
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from members.models import Member
from members.services.emails import send_mutual_like_email


def check_mutual_like(current_member_id: int, liked_member: Member):
    return liked_member.liked_members.filter(id=current_member_id).exists()


def _like_member(user: Member, target_member_id: int) -> Member:
    user_to_like = get_object_or_404(get_user_model(), id=target_member_id)
    user.liked_members.add(user_to_like)
    return user_to_like


def like_member(user: Member, target_member_id: int):
    """Add target member to user.liked_members relation
    If the likes are mutual, send the email to the liked_member
    """
    liked_member = _like_member(user, target_member_id)
    if check_mutual_like(user.id, liked_member):
        send_mutual_like_email(to_email=liked_member.email, liking_member=user)


def check_member_like_availability(user: Member, target_member_id: int):
    if user.liked_members.filter(id=target_member_id).exists():
        raise ValidationError({'error': 'You already liked the user'})
    elif user.id == target_member_id:
        raise ValidationError({'error': 'You cannot like yourself'})


def get_raw_sql_gcd_formula(longitude: float, latitude: float) -> RawSQL:
    """Great-circle distance formula RawSQL"""
    gcd_formula = '6371 * acos(least(greatest(\
            cos(radians(%s)) * cos(radians(latitude)) \
            * cos(radians(longitude) - radians(%s)) + \
            sin(radians(%s)) * sin(radians(latitude)) \
            , -1), 1))'
    return RawSQL(gcd_formula, (latitude, longitude, latitude))


def find_member_by_location_distance(longitude: float, latitude: float, distance: int,
                                     qs: QuerySet = Member.objects.all()) -> QuerySet:
    """Distance (int): max distance between members in km"""
    return qs \
        .annotate(distance=get_raw_sql_gcd_formula(longitude, latitude)) \
        .filter(distance__lt=distance) \
        .order_by('distance')
