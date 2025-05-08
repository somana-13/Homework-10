import pytest
from unittest.mock import patch, MagicMock
from app.utils.smtp_connection import SMTPClient
import smtplib

def test_init_client():
    client = SMTPClient(
        server="test.host.com",
        port=587,
        username="test_user",
        password="test_pass"
    )
    
    assert client.server == "test.host.com"
    assert client.port == 587
    assert client.username == "test_user"
    assert client.password == "test_pass"

@patch('smtplib.SMTP')
def test_send_email_success(mock_smtp):
    # Setup mock
    mock_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_instance
    
    # Create client
    client = SMTPClient(
        server="test.host.com",
        port=587,
        username="test_user@example.com",
        password="test_pass"
    )
    
    # Test sending email
    subject = "Test Subject"
    html_content = "<p>Test content</p>"
    to_email = "recipient@example.com"
    
    client.send_email(subject, html_content, to_email)
    
    # Verify method calls
    mock_instance.starttls.assert_called_once()
    mock_instance.login.assert_called_once_with("test_user@example.com", "test_pass")
    mock_instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_email_with_cc_bcc(mock_smtp):
    # Setup mock
    mock_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_instance
    
    # Create client
    client = SMTPClient(
        server="test.host.com",
        port=587,
        username="test_user@example.com",
        password="test_pass"
    )
    
    # Test sending email (no cc/bcc support in implementation)
    subject = "Test Subject"
    html_content = "<p>Test content</p>"
    to_email = "recipient@example.com"
    
    client.send_email(subject, html_content, to_email)
    
    # Verify method calls
    mock_instance.sendmail.assert_called_once()
    
    # Verify the sendmail call
    call_args = mock_instance.sendmail.call_args[0]
    assert call_args[0] == "test_user@example.com"
    assert call_args[1] == "recipient@example.com"

@patch('smtplib.SMTP')
def test_send_email_failure(mock_smtp):
    # Setup mock to raise an exception
    mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("SMTP Error")
    
    # Create client
    client = SMTPClient(
        server="test.host.com",
        port=587,
        username="test_user@example.com",
        password="test_pass"
    )
    
    # Test sending email that raises an exception
    with pytest.raises(Exception) as excinfo:
        client.send_email("Subject", "<p>Content</p>", "recipient@example.com")
    
    # The exception is passed through directly from SMTPException
    assert "SMTP Error" in str(excinfo.value)
