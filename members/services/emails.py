from django.conf import settings
from django.core.mail import send_mail

from members.models import Member


def send_mutual_like_email(to_email: str, liking_member: Member):
    """Liking member (Member): member that liked another member"""
    send_mail(
        subject='Взаимная симпатия',
        message=f'Вы понравились {liking_member.name}! Почта участника: {liking_member.email}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email]
    )
