from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

class TransactionRelationship(models.Model):
    ancestor = models.ForeignKey(Transaction, related_name='descendant_links', on_delete=models.CASCADE)
    descendant = models.ForeignKey(Transaction, related_name='ancestor_links', on_delete=models.CASCADE)
    depth = models.PositiveIntegerField()  # Distance between ancestor and descendant