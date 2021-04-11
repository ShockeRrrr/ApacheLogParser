from django.db import models

class LogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)

    def __str__(self):
        return self.id
