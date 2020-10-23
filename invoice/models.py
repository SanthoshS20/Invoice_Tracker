from django.db import models

class UserDetail(models.Model):
  ADMIN = 'ADMIN'
  NORMAL = 'NORMAL'
  user_type_choices = [(ADMIN, 'Admin'), (NORMAL, 'Normal')]
  username = models.CharField(max_length=20, unique=True)
  email_id = models.EmailField(max_length=100, unique=True)
  password = models.CharField(max_length=15)
  user_type = models.CharField(max_length=6, default=NORMAL, choices=user_type_choices)

  class Meta:
    db_table = "user_details"


class Invoice(models.Model):
  PENDING = 'PENDING'
  APPROVED = 'APPROVED'
  REJECTED = 'REJECTED'
  status_choices = [(PENDING, 'Pending'), (APPROVED, 'Approved'), (REJECTED, 'Rejected')]
  user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  date = models.DateField()
  amount = models.FloatField()
  image = models.ImageField()
  status = models.CharField(max_length=10, default=PENDING, choices=status_choices)

  class Meta:
    db_table = "invoices"