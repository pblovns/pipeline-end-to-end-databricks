"""
Tests for data generation module (Camada Raw)
"""
import pytest
from faker import Faker
from faker.config import AVAILABLE_LOCALES


class TestFakerConfiguration:
    """Test Faker library configuration"""

    def test_pt_br_locale_available(self):
        """Validate that pt_BR locale is available"""
        assert 'pt_BR' in AVAILABLE_LOCALES

    def test_faker_generates_valid_cpf(self):
        """Test that Faker generates valid CPF format"""
        fake = Faker('pt_BR')
        cpf = fake.cpf()
        # CPF should have 14 characters (11 digits + 2 dots + 1 dash)
        assert len(cpf) == 14
        assert cpf[3] == '.'
        assert cpf[7] == '.'
        assert cpf[11] == '-'

    def test_faker_generates_valid_phone(self):
        """Test that Faker generates valid phone number"""
        fake = Faker('pt_BR')
        phone = fake.phone_number()
        # Phone should not be empty
        assert phone is not None
        assert len(phone) > 0

    def test_faker_generates_valid_email(self):
        """Test that Faker generates valid email"""
        fake = Faker('pt_BR')
        email = fake.email()
        # Email should contain @
        assert '@' in email
        assert '.' in email

    def test_faker_profile_contains_required_fields(self):
        """Test that profile contains all required fields"""
        fake = Faker('pt_BR')
        
        required_fields = [
            'nome', 'cpf', 'telefone', 'dataNascimento',
            'email', 'endereco', 'cargo', 'empresa', 'website'
        ]
        
        profile = {
            'nome': fake.name(),
            'cpf': fake.cpf(),
            'telefone': fake.phone_number(),
            'dataNascimento': fake.date_of_birth(),
            'email': fake.email(),
            'endereco': fake.address(),
            'cargo': fake.job(),
            'empresa': fake.company(),
            'website': fake.url()
        }
        
        for field in required_fields:
            assert field in profile
            assert profile[field] is not None

    def test_faker_generates_multiple_unique_profiles(self):
        """Test that Faker generates different profiles each time"""
        fake = Faker('pt_BR')
        
        profiles = [fake.cpf() for _ in range(10)]
        unique_profiles = set(profiles)
        
        # Should have at least some variation
        assert len(unique_profiles) > 5
