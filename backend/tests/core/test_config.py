import pytest
import os
from unittest.mock import patch

from app.core.config import Settings, settings


class TestSettings:
    """Test cases for the Settings configuration."""
    
    def test_default_settings(self):
        """Test that default settings are correctly set."""
        test_settings = Settings()
        
        assert test_settings.API_HOST == "localhost"
        assert test_settings.API_PORT == 8000
        assert test_settings.API_PREFIX == "/api"
        assert test_settings.DATABASE_PATH == "app/data/vulnerabilities.db"
        assert test_settings.VECTOR_DB_PATH == "app/data/vector_db"
        assert test_settings.SNYK_BASE_URL == "https://security.snyk.io/vuln/pip/"
        assert test_settings.SCRAPER_PAGES_TO_FETCH == 10
        assert test_settings.ALLOWED_ORIGINS == ["http://localhost:3000"]
    
    def test_settings_from_environment(self):
        """Test that settings are correctly loaded from environment variables."""
        with patch.dict(os.environ, {
            "API_HOST": "0.0.0.0",
            "API_PORT": "9000",
            "API_PREFIX": "/v1",
            "DATABASE_PATH": "/custom/path/db.sqlite",
            "SCRAPER_PAGES_TO_FETCH": "20"
        }, clear=False):
            test_settings = Settings()
            
            assert test_settings.API_HOST == "0.0.0.0"
            assert test_settings.API_PORT == 9000
            assert test_settings.API_PREFIX == "/v1"
            assert test_settings.DATABASE_PATH == "/custom/path/db.sqlite"
            assert test_settings.SCRAPER_PAGES_TO_FETCH == 20
    
    def test_azure_openai_settings(self):
        """Test Azure OpenAI configuration from environment."""
        with patch.dict(os.environ, {
            "AZURE_OPENAI_API_KEY": "test-key-123",
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com",
            "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT": "text-embedding-ada-002",
            "AZURE_OPENAI_COMPLETIONS_DEPLOYMENT": "gpt-35-turbo"
        }, clear=False):
            test_settings = Settings()
            
            assert test_settings.AZURE_OPENAI_API_KEY == "test-key-123"
            assert test_settings.AZURE_OPENAI_ENDPOINT == "https://test.openai.azure.com"
            assert test_settings.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT == "text-embedding-ada-002"
            assert test_settings.AZURE_OPENAI_COMPLETIONS_DEPLOYMENT == "gpt-35-turbo"
    
    def test_allowed_origins_parsing(self):
        """Test that ALLOWED_ORIGINS is correctly parsed from comma-separated string."""
        with patch.dict(os.environ, {
            "ALLOWED_ORIGINS": "http://localhost:3000,https://example.com,https://app.example.com"
        }, clear=False):
            test_settings = Settings()
            
            expected_origins = [
                "http://localhost:3000",
                "https://example.com",
                "https://app.example.com"
            ]
            assert test_settings.ALLOWED_ORIGINS == expected_origins
    
    def test_invalid_port_number(self):
        """Test handling of invalid port number in environment."""
        with patch.dict(os.environ, {
            "API_PORT": "invalid_port"
        }, clear=False):
            with pytest.raises(ValueError):
                Settings()
    
    def test_invalid_scraper_pages(self):
        """Test handling of invalid scraper pages value."""
        with patch.dict(os.environ, {
            "SCRAPER_PAGES_TO_FETCH": "not_a_number"
        }, clear=False):
            with pytest.raises(ValueError):
                Settings()
    
    def test_settings_singleton(self):
        """Test that the settings instance is properly initialized."""
        assert isinstance(settings, Settings)
        assert settings.API_HOST is not None
        assert settings.API_PORT is not None
    
    def test_database_path_type(self):
        """Test that database path is a string."""
        assert isinstance(settings.DATABASE_PATH, str)
        assert len(settings.DATABASE_PATH) > 0
    
    def test_vector_db_path_type(self):
        """Test that vector database path is a string."""
        assert isinstance(settings.VECTOR_DB_PATH, str)
        assert len(settings.VECTOR_DB_PATH) > 0
    
    def test_snyk_base_url_format(self):
        """Test that Snyk base URL has correct format."""
        assert settings.SNYK_BASE_URL.startswith("https://")
        assert "snyk.io" in settings.SNYK_BASE_URL
    
    def test_api_prefix_format(self):
        """Test that API prefix starts with slash."""
        assert settings.API_PREFIX.startswith("/")