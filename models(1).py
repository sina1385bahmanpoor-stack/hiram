from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('advisor', 'مشاور'),
        ('admin', 'ادمین'),
        ('student', 'دانش‌اموز'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='student'
    )

    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

class UserRelationship(models.Model):


    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='as_student',
        limit_choices_to={'user_type': 'student'}
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='students_under_admin',
        limit_choices_to={'user_type': 'admin'}
    )
    advisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='students_under_advisor',
        limit_choices_to={'user_type': 'advisor'}
    )

    num_test = {}
    term = {}

    def __str__(self):
        # return f"{self.student.first_name} {self.student.last_name}"
        return self.student.username

    class Meta:
        unique_together = ['student', 'admin', 'advisor']

