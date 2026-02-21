from django.db import models

class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.

    Useful for auditability and temporal tracking.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e ora di creazione del record."
    )
    
    update_at = models.DateTimeField(
        auto_now=True,
        help_text="Data e l'ora di l'ultima modifica."
    )
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]