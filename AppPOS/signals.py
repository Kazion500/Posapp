from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


from django.contrib.auth.models import User
from .models import ( SalesPerson, Sale, Stock )

@receiver(post_save,sender=User)
def post_save_create_sales_person(sender,instance,created,**kwargs):
    if created:
        SalesPerson.objects.create(user=instance)    

    instance.salesperson.save()
    

    



