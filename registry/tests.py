from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Application


class ApplicationModelTest(TestCase):
    """Test cases for the Application model."""

    def setUp(self):
        """Set up test data for each test method."""
        self.valid_application_data = {
            'protocol': 'https',
            'url': 'https://example.com',
            'port': 443
        }

    def test_create_application_with_valid_data(self):
        """Test creating an application with valid data."""
        app = Application.objects.create(**self.valid_application_data)

        self.assertEqual(app.protocol, 'https')
        self.assertEqual(app.url, 'https://example.com')
        self.assertEqual(app.port, 443)
        self.assertIsNotNone(app.id)

    def test_application_str_method(self):
        """Test that __str__ method returns the full address."""
        app = Application.objects.create(**self.valid_application_data)
        expected_str = 'https://https://example.com:443'

        self.assertEqual(str(app), expected_str)

    def test_full_address_property(self):
        """Test the full_address property returns correct format."""
        app = Application.objects.create(**self.valid_application_data)
        expected_address = 'https://https://example.com:443'

        self.assertEqual(app.full_address, expected_address)

    def test_full_address_property_with_different_protocols(self):
        """Test full_address property with different protocol types."""
        test_cases = [
            ('http', 'http://localhost', 80, 'http://http://localhost:80'),
            ('https', 'https://secure.com', 443, 'https://https://secure.com:443'),
            ('ftp', 'ftp://files.com', 21, 'ftp://ftp://files.com:21'),
            ('tcp', 'tcp://service.com', 8080, 'tcp://tcp://service.com:8080'),
            ('udp', 'udp://stream.com', 9090, 'udp://udp://stream.com:9090'),
        ]

        for protocol, url, port, expected in test_cases:
            with self.subTest(protocol=protocol):
                app = Application(protocol=protocol, url=url, port=port)
                self.assertEqual(app.full_address, expected)

    def test_protocol_choices_validation(self):
        """Test that only valid protocol choices are accepted."""
        valid_protocols = ['http', 'https', 'ftp', 'tcp', 'udp']

        for protocol in valid_protocols:
            with self.subTest(protocol=protocol):
                app = Application(
                    protocol=protocol,
                    url='https://example.com',
                    port=80
                )
                # This should not raise an exception
                app.full_clean()

    def test_invalid_protocol_choice(self):
        """Test that invalid protocol choices raise validation error."""
        app = Application(
            protocol='invalid_protocol',
            url='https://example.com',
            port=80
        )

        with self.assertRaises(ValidationError):
            app.full_clean()

    def test_port_range_validation(self):
        """Test that port field validates the range (1-65535)."""
        # Test valid port numbers at boundaries and common values
        valid_ports = [1, 21, 22, 80, 443, 8080, 65534, 65535]

        for port in valid_ports:
            with self.subTest(port=port):
                app = Application(
                    protocol='http',
                    url='https://example.com',
                    port=port
                )
                app.full_clean()  # Should not raise exception

    def test_invalid_port_numbers(self):
        """Test that invalid port numbers raise validation error."""
        invalid_ports = [0, -1, -100, 65536, 70000, 100000]

        for port in invalid_ports:
            with self.subTest(port=port):
                app = Application(
                    protocol='http',
                    url='https://example.com',
                    port=port
                )

                with self.assertRaises(ValidationError) as context:
                    app.full_clean()

                # Check that the error message mentions port range
                error_message = str(context.exception)
                self.assertIn('Port number must be between 1 and 65535', error_message)

    def test_port_boundary_values(self):
        """Test port validation at exact boundary values."""
        # Test minimum valid port
        app_min = Application(
            protocol='http',
            url='https://example.com',
            port=1
        )
        app_min.full_clean()  # Should not raise exception

        # Test maximum valid port
        app_max = Application(
            protocol='http',
            url='https://example.com',
            port=65535
        )
        app_max.full_clean()  # Should not raise exception

        # Test just below minimum (should fail)
        app_below_min = Application(
            protocol='http',
            url='https://example.com',
            port=0
        )
        with self.assertRaises(ValidationError):
            app_below_min.full_clean()

        # Test just above maximum (should fail)
        app_above_max = Application(
            protocol='http',
            url='https://example.com',
            port=65536
        )
        with self.assertRaises(ValidationError):
            app_above_max.full_clean()

    def test_url_field_validation(self):
        """Test URL field validation."""
        valid_urls = [
            'https://example.com',
            'http://localhost',
            'https://subdomain.example.com',
            'http://192.168.1.1',
        ]

        for url in valid_urls:
            with self.subTest(url=url):
                app = Application(
                    protocol='http',
                    url=url,
                    port=80
                )
                app.full_clean()  # Should not raise exception

    def test_invalid_url_validation(self):
        """Test that invalid URLs raise validation error."""
        invalid_urls = [
            'not_a_url',
            'ftp://',  # incomplete URL
            '',  # empty string
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                app = Application(
                    protocol='http',
                    url=url,
                    port=80
                )

                with self.assertRaises(ValidationError):
                    app.full_clean()

    def test_model_meta_attributes(self):
        """Test model Meta class attributes."""
        self.assertEqual(Application._meta.verbose_name, "Application")
        self.assertEqual(Application._meta.verbose_name_plural, "Applications")

    def test_field_max_lengths(self):
        """Test field maximum length constraints."""
        # Test protocol max length
        long_protocol = 'a' * 11  # Exceeds max_length of 10
        app = Application(
            protocol=long_protocol,
            url='https://example.com',
            port=80
        )

        with self.assertRaises(ValidationError):
            app.full_clean()

        # Test URL max length
        long_url = 'https://' + 'a' * 250 + '.com'  # Exceeds max_length of 255
        app = Application(
            protocol='http',
            url=long_url,
            port=80
        )

        with self.assertRaises(ValidationError):
            app.full_clean()

    def test_application_creation_and_retrieval(self):
        """Test creating and retrieving applications from database."""
        # Create application
        app = Application.objects.create(**self.valid_application_data)

        # Retrieve from database
        retrieved_app = Application.objects.get(id=app.id)

        self.assertEqual(retrieved_app.protocol, self.valid_application_data['protocol'])
        self.assertEqual(retrieved_app.url, self.valid_application_data['url'])
        self.assertEqual(retrieved_app.port, self.valid_application_data['port'])

    def test_multiple_applications_creation(self):
        """Test creating multiple applications."""
        applications_data = [
            {'protocol': 'http', 'url': 'http://app1.com', 'port': 80},
            {'protocol': 'https', 'url': 'https://app2.com', 'port': 443},
            {'protocol': 'tcp', 'url': 'tcp://service.com', 'port': 8080},
        ]

        for data in applications_data:
            Application.objects.create(**data)

        self.assertEqual(Application.objects.count(), 3)

        # Verify each application
        for i, data in enumerate(applications_data):
            app = Application.objects.filter(protocol=data['protocol']).first()
            self.assertIsNotNone(app)
            self.assertEqual(app.url, data['url'])
            self.assertEqual(app.port, data['port'])

    def test_common_port_numbers(self):
        """Test validation with common port numbers used in applications."""
        common_ports = [
            21,  # FTP
            22,  # SSH
            23,  # Telnet
            25,  # SMTP
            53,  # DNS
            80,  # HTTP
            110,  # POP3
            143,  # IMAP
            443,  # HTTPS
            993,  # IMAPS
            995,  # POP3S
            3306,  # MySQL
            5432,  # PostgreSQL
            6379,  # Redis
            8080,  # HTTP alternate
            8443,  # HTTPS alternate
            9000,  # Various applications
        ]

        for port in common_ports:
            with self.subTest(port=port):
                app = Application(
                    protocol='tcp',
                    url='https://service.com',
                    port=port
                )
                app.full_clean()  # Should not raise exception
