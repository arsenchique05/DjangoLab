#Python modules + Third party models

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

#Project modules
class Cuisine(Model):
    """
    Cuisine database (table) model.
    """
    NAME_MAX_LEN = 100  
    name = CharField(max_length=NAME_MAX_LEN)
    
class Restaurant(Model):
    """
    Restaurant database (table) model.
    """
    NAME_MAX_LEN = 100
    PHONE_MAX_LEN = 20
    name = CharField(max_length=NAME_MAX_LEN)
    address = TextField() 
    phone = CharField(max_length=PHONE_MAX_LEN)
    cuisine = ForeignKey(to=Cuisine,on_delete=CASCADE)
    
class Delivery_Zone(Model):
    """
    Delivery_Zone database (table) model.
    """
    NAME_MAX_LEN = 100
    name = CharField(max_length=NAME_MAX_LEN)
    restaurant = ForeignKey(to=Restaurant,on_delete=CASCADE)
    
class MenuItem(Model):
    """
    MenuItem database (table) model.
    """
    NAME_MAX_LEN = 100
    name = CharField(max_length=NAME_MAX_LEN)
    description = TextField()
    base_price = IntegerField()
    categories = ManyToManyField(
        to="Category",
        through="ItemCategory",
        through_fields=("menuitem", "category"),
    )
    options = ManyToManyField(
        to="Option",
        through="ItemOption",
        through_fields=("menuitem", "option"),
    )
    is_available = BooleanField(default=True)
    restaurant = ForeignKey(to=Restaurant,on_delete=CASCADE)
    
class Category(Model):
    """
    Category database (table) model.
    """
    NAME_MAX_LEN = 100
    name = CharField(max_length=NAME_MAX_LEN)
    
class Option(Model):
    """
    Option database (table) model.
    """
    NAME_MAX_LEN = 100
    name = CharField(max_length=NAME_MAX_LEN)
    
class ItemCategory(Model):
    """
    ItemCategory database (table) model.
    """
    menuitem = ForeignKey(to=MenuItem,on_delete=CASCADE)
    category = ForeignKey(to=Category,on_delete=CASCADE)
    position = IntegerField()
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["menuitem", "category"],
                name="unique_menuitem_category",
            ),
        ]
    
class ItemOption(Model):
    """
    ItemOption database (table) model.
    """
    menuitem = ForeignKey(to=MenuItem,on_delete=CASCADE)
    option = ForeignKey(to=Option,on_delete=CASCADE)
    price_delta = IntegerField()
    is_default = BooleanField(default=False)
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["menuitem", "option"],
                name="unique_menuitem_option",
            ),
        ]