import os
from settings import get_settings


def test_settings_default():
    settings = get_settings()
    assert settings.app_name == "GeoIP App"
    assert settings.circl_api_url == "https://ip.circl.lu"


def test_settings_override():
    os.environ["APP_NAME"] = "Test App"
    # We need to clear cache to test override or reload module,
    # but pydantic settings read env vars at instantiation.
    # get_settings is lru_cached.
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.app_name == "Test App"

    # Cleanup
    del os.environ["APP_NAME"]
    get_settings.cache_clear()
