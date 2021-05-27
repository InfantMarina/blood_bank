from django.db import models


# Create your models here.
class Donor(models.Model):
    donor_name = models.CharField(max_length=40,null=False,blank=False)
    location = models.CharField(max_length=40,null=False,blank=False)
    mobile = models.IntegerField()
    blood_group = models.CharField(max_length=7,null=False,blank=False)
    added_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'donor'

    def __str__(self):
        return self.donor_name


class DonorTransaction(models.Model):
    transaction_date = models.DateTimeField()
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donated_to = models.CharField(max_length=50,null=False,blank=False)
    receiver_mobile =  models.IntegerField()

    class Meta:
        db_table = 'donor_transaction'
