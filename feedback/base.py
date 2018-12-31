import uuid
from django.db import models
from django.conf import settings


class BaseFeedbackModel(models.Model):
    """
    Base abstract model for most Feedback form models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    last_modified = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True

    def to_dict(self):
        """
        Return a JSON ready dict representation of the model.
        If the implementing model defines a _to_dict method, it will be merged into the output
        """
        _dict = {
            'id': str(self.id),
            'created_at': self.created_at.strftime(
                getattr(settings, 'API_DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S%z')),
            'last_modified': self.created_at.strftime(
                getattr(settings, 'API_DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S%z'))
        }
        if hasattr(self, '_to_dict'):
            _dict.update(self._to_dict())
        return _dict
