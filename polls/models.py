from django.db import models
# Create your models here.
# FCL = "FCL"
# LCL = "LCL"
# AIR = "Air"
# DANGEROUS = "dangerous"
# NON_DANGEROUS = "non_dangerous"
# GC = "GC"
# OT = "OT"
# REEF = "REEF"
# FR = "FR"
# FB = "FB"
# FORTY_FEET = '40"'
# TWEENTY_FEET = '20"'
# FORTY_FEET_HC = '40"HC'


# TYPE_OF_BOOKING = ((FCL, "FCL"), (LCL, "LCL"), (AIR, "Air"))
# TYPE_OF_CARGO = ((DANGEROUS, "dangerous"),
#                  (NON_DANGEROUS, "non-dangerous"))
# TYPE_OF_CONTAINER = ((GC, "GC"), (OT, "OT"),
#                      (REEF, "REEF"), (FR, "FR"), (FB, "FB"))
# TYPE_OF_CONTAINER_SIZE = ((TWEENTY_FEET, '20"'),
#                           (FORTY_FEET, '40"'), (FORTY_FEET_HC, '40"HC'))

# TYPE_OF_USER = (("ad", "ADMIN"),("cr","CUSTOMER"),("vn","VENDOR"),("pr","PARTNER"))


# class Enquiry(models.Model):
#     enquiry_id = models.AutoField(
#         primary_key=True, default=0, unique=True, editable=False)
#     customer = models.CharField(max_length=128)
#     type_of_booking = models.CharField(max_length=32, choices=TYPE_OF_BOOKING)
#     door_pickup = models.BooleanField(default=False)
#     door_delivery = models.BooleanField(default=False)
#     cargo_ready_date = models.DateField(null=True)
#     origin_port = models.CharField(max_length=64)
#     destination_port = models.CharField(max_length=64)
#     type_of_cargo = models.CharField(max_length=32, choices=TYPE_OF_CARGO)

#     def __str__(self):
#         return str(self.enquiry_id)


# class Container(models.Model):
#     enquiry_id = models.ForeignKey(
#         "Enquiry", db_column="enquiry_id", default=0, on_delete=models.CASCADE)
#     type = models.CharField(max_length=32, choices=TYPE_OF_CONTAINER)
#     hs_code = models.CharField(max_length=32)
#     size = models.CharField(max_length=32, choices=TYPE_OF_CONTAINER_SIZE)
#     count = models.IntegerField()
#     weight = models.CharField(max_length=32)

#     def __str__(self):
#         return str(self.enquiry_id)

# # tables dependent on each other will come first 




# class Enquiry_Rates(models.Model):
#     valid_till = models.DateField()
#     liners = models.CharField(max_length=64)
#     vessel_name  = models.CharField(max_length=64)
#     total_transit_days = models.IntegerField(max_length=5)
#     free_days = models.IntegerField(max_length=5)
#     route_type = models.CharField(max_length=10)
#     origin_date = models.DateField()
#     arrival_date = models.DateField()


#     # connections to another table to be placed at bottom
#     vendor_id = models.ForeignKey(
#         "Vendor", db_column="id", default=0 ,on_delete=models.CASCADE
#     )