from django.db import models
from django.utils import timezone

TYPE_OF_ALLOWED_LANGS = (
    ('py', 'Python'),
    ('java', 'Java'),
    ('c', 'C'),
)
class User(models.Model):
    id = models.AutoField(
        primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(User, self).save(*args, **kwargs)


class Problem(models.Model):
    id = models.AutoField(
        primary_key=True)
    name = models.CharField(max_length=128,unique=True, default="some problem")
    des = models.TextField(default="problem description")
    rating = models.FloatField(max_length=5,default=0.0)
    problem = models.TextField()
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())


    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Problem, self).save(*args, **kwargs)

class ProblemSolutionUser(models.Model):
    id = models.AutoField(
        primary_key=True)
    sol = models.TextField()
    lang = models.CharField(max_length=8, choices=TYPE_OF_ALLOWED_LANGS, default='py')
    pid = models.ForeignKey(
        "Problem", default=0 ,on_delete=models.CASCADE
    )
    uid = models.ForeignKey(
        "User", default=0 ,on_delete=models.CASCADE
    )
    rating = models.CharField(max_length=5,default=0.0)
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())

    class Meta:
        unique_together = ('uid', 'pid',)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(ProblemSolutionUser, self).save(*args, **kwargs)

class ProblemTestCase(models.Model):
    id = models.AutoField(
        primary_key=True)
    inp = models.TextField()
    out = models.TextField()
    pid = models.ForeignKey(
        "Problem", default=0 ,on_delete=models.CASCADE
    )
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(ProblemTestCase, self).save(*args, **kwargs)

class ProblemSolutionTestCase(models.Model):
    id = models.AutoField(
        primary_key=True)
    attempted = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    sid = models.ForeignKey(
        "ProblemSolutionUser", default=0 ,on_delete=models.CASCADE
    )
    tid = models.ForeignKey(
        "ProblemTestCase", on_delete=models.CASCADE, to_field="id"
    )
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())


    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(ProblemSolutionTestCase, self).save(*args, **kwargs)

class ProblemType(models.Model):
    id = models.AutoField(
        primary_key=True)
    type = models.CharField(max_length=128, default="strings")
    pid = models.ForeignKey(
        "Problem", default=0 ,on_delete=models.CASCADE
    )
    created_at     = models.DateTimeField(editable=False)
    modified_at    = models.DateTimeField(default=timezone.now())


    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(ProblemType, self).save(*args, **kwargs)

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