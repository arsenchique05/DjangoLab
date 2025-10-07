#Python modules + Third party models
from catalogs.models import Restaurant,MenuItem
#Django models
from django.db.models import (
    Model,
    CharField,
    TextField,
    ForeignKey,
    IntegerField,
    BooleanField,
    ManyToManyField,
    UniqueConstraint,
    CASCADE,
    )

from django.contrib.auth.models import User

#Project modules
class Address(Model):
    """
    Address database (table) model.
    """
    MAX_LEN = 200
    address = CharField(max_length=MAX_LEN)
    user = ForeignKey(to=User,on_delete=CASCADE)
    
class Order(Model):
    """
    Order database (table) model.
    """
    STATUS_NEW = 1
    STATUS_NEW_LABEL = "New"
    STATUS_CONFIRMED = 2
    STATUS_CONFIRMED_LABEL = "Confirmed"
    STATUS_DELIVERING = 3
    STATUS_DELIVERING_LABEL = "Delivering"
    STATUS_DONE = 4
    STATUS_DONE_LABEL = "Done"
    STATUS_CHOICES = {
        STATUS_NEW:STATUS_NEW_LABEL,
        STATUS_CONFIRMED: STATUS_CONFIRMED_LABEL,
        STATUS_DELIVERING: STATUS_DELIVERING_LABEL,
        STATUS_DONE: STATUS_DONE_LABEL,
    }
    
    user = ForeignKey(to=User,on_delete=CASCADE)
    restaurant = ForeignKey(to=Restaurant,on_delete=CASCADE)
    status = IntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)
    subtotal = IntegerField()
    discount_total = IntegerField()
    total = IntegerField()
    
    promocode = ManyToManyField(
        to = "PromoCode",
        through="OrderPromo",
        through_fields=("order", "promocode"),
    )
    
class OrderItem(Model):
    """
    OrderItem database (table) model.
    """
    ITEMNAME_MAX_LEN = 100
    order = ForeignKey(to=Order,on_delete=CASCADE)
    menuitem = ForeignKey(to=MenuItem,on_delete=CASCADE)
    item_name = CharField(max_length=ITEMNAME_MAX_LEN)
    item_price = IntegerField()
    quantity = IntegerField()
    line_total = IntegerField()
    
class PromoCode(Model):
    """
    PromoCode database (table) model.
    """
    CODE_MAX_LEN = 50
    code = CharField(max_length=CODE_MAX_LEN,unique=True)
    
class OrderItemOption(Model):
    """
    OrderItemOption database (table) model.
    """
    OPTIONNAME_MAX_LEN = 100
    orderitem = ForeignKey(to=OrderItem,on_delete=CASCADE)
    option_name = CharField(max_length=OPTIONNAME_MAX_LEN)
    price_delta = IntegerField()    
    
    
class OrderPromo(Model):
    """
    OrderPromo database (table) model.
    """
    order = ForeignKey(to=Order,on_delete=CASCADE)
    promocode = ForeignKey(to=PromoCode,on_delete=CASCADE) 
    applied_amount = IntegerField()
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["order", "promocode"],
                name="unique_order_promocode",
            ),
        ]
        
