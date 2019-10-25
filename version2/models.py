from django.db import models

# Create your models here.
class Respondent(models.Model):
    # primary key will be autogenerated
    age = models.PositiveSmallIntegerField() # up to 32767
    # add rest of demographics
    
class Algorithm(models.Model):
    name = models.CharField(max_length=10)

class Query(models.Model):
    # do we want to store the name of the query or the id for it?
    query_name = models.CharField(max_length=100)
    
class Response(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    chosen_alg = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="chosen")
    unchosen_alg = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="unchosen")
    # if we want to store more accurate time data, change this
    time_elapsed = models.PositiveSmallIntegerField()
    

    