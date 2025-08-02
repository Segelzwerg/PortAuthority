from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model


def validate_port_range(value):
    """
    Validates that the port number is within the valid range (1-65535).
    
    Args:
        value (int): The port number to validate
        
    Raises:
        ValidationError: If the port is not within the valid range
    """
    if value < 1 or value > 65535:
        raise ValidationError(
            f'Port number must be between 1 and 65535. Got: {value}'
        )


class Application(models.Model):
    """
    Model representing an application with network connection details.
    
    This model stores information about applications including their protocol,
    URL, and port number. It provides a convenient property to combine these
    fields into a complete address string.
    
    Attributes:
        protocol (CharField): The network protocol used by the application
            (e.g., HTTP, HTTPS, FTP, TCP, UDP)
        url (URLField): The base URL or hostname of the application
        port (PositiveIntegerField): The port number on which the application runs
            (must be between 1 and 65535)
    
    Properties:
        full_address: Returns a formatted string combining protocol, url, and port
    
    Example:
        >>> app = Application(protocol='https', url='example.com', port=443)
        >>> print(app.full_address)
        'https://example.com:443'
    """

    protocol = models.CharField(max_length=10, choices=[
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
        ('ftp', 'FTP'),
        ('tcp', 'TCP'),
        ('udp', 'UDP'),
    ])
    url = models.URLField(max_length=255)
    port = models.PositiveIntegerField(validators=[validate_port_range])

    @property
    def full_address(self):
        """Combines protocol, url and port into a full address string."""
        return f"{self.protocol}://{self.url}:{self.port}"

    def __str__(self):
        return self.full_address

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
