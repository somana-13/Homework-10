import pytest
from unittest.mock import patch, MagicMock
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager
from app.utils.smtp_connection import SMTPClient

@pytest.fixture
def mock_email_service():
    template_manager = TemplateManager()
    # Create a mock for the SMTP client
    with patch.object(SMTPClient, 'send_email') as mock_send:
        mock_send.return_value = True
        email_service = EmailService(template_manager=template_manager)
        # Replace the real SMTP client with our mock
        email_service.smtp_client = MagicMock()
        email_service.smtp_client.send_email = mock_send
        yield email_service
    
@pytest.mark.asyncio
async def test_send_markdown_email(mock_email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",  # Template expects 'name', not first_name/last_name
        "verification_url": "http://example.com/verify?token=abc123"
    }
    # Send the email with our mocked service
    await mock_email_service.send_user_email(user_data, 'email_verification')
    
    # Verify the mock was called with the correct parameters
    mock_email_service.smtp_client.send_email.assert_called_once()
    # The first arg to the first call
    call_args = mock_email_service.smtp_client.send_email.call_args[0]
    # Check that the email contains expected info
    assert "Verify" in call_args[0]  # Subject contains 'Verify'
    assert "test@example.com" in call_args[2]  # Email address is correct
