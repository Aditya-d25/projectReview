# backend/email_service.py
"""
Email service for sending OTPs.
Supports both development mode (console logging) and production mode (actual SMTP).
"""

import os
import logging
from datetime import datetime
from backend.otp_storage import otp_storage

logger = logging.getLogger(__name__)

class EmailService:
    """Handles email sending for OTP verification"""
    
    def __init__(self):
        """Initialize email service with configuration"""
        # Check if we should use actual SMTP
        self.use_smtp = os.getenv('USE_SMTP', 'False').lower() == 'true'
        
        # SMTP Configuration (from .env file)
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.smtp_use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
        self.email_from = os.getenv('EMAIL_FROM', 'noreply@college.edu')
        
        self.app_name = "Project Review System"
    
    def send_otp_email(self, email, otp, purpose='registration'):
        """
        Send OTP email to user
        
        Args:
            email: Recipient email address
            otp: The OTP code
            purpose: 'registration' or 'password_reset'
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Generate email content
        subject, body = self._generate_email_content(otp, purpose)
        
        # Development mode - just log to console
        if not self.use_smtp:
            return self._log_email_to_console(email, otp, purpose, subject, body)
        
        # Production mode - send actual email
        return self._send_smtp_email(email, subject, body)
    
    def _generate_email_content(self, otp, purpose):
        """Generate email subject and body"""
        if purpose == 'registration':
            subject = f"Verify Your Email - {self.app_name}"
            body = f"""
Welcome to {self.app_name}!

Your verification code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
{self.app_name} Team
"""
        else:  # password_reset
            subject = f"Password Reset Code - {self.app_name}"
            body = f"""
Hello,

You requested to reset your password for {self.app_name}.

Your password reset code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email and your password will remain unchanged.

Best regards,
{self.app_name} Team
"""
        
        return subject, body
    
    def _log_email_to_console(self, email, otp, purpose, subject, body):
        """
        Log email to console (development mode)
        This is perfect for local testing and college servers without SMTP
        """
        print("\n" + "="*60)
        print("📧 EMAIL SENT (Development Mode)")
        print("="*60)
        print(f"To: {email}")
        print(f"Purpose: {purpose}")
        print(f"Subject: {subject}")
        print("-"*60)
        print(f"🔐 YOUR OTP CODE: {otp}")
        print("-"*60)
        print(body)
        print("="*60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        logger.info(f"OTP sent to {email} (purpose: {purpose}): {otp}")
        
        return True, "OTP sent successfully (check console)"
    
    def _send_smtp_email(self, to_email, subject, body):
        """
        Send actual email via SMTP (production mode)
        Configure SMTP settings in .env file
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Create message
            message = MIMEMultipart()
            message['From'] = self.email_from
            message['To'] = to_email
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            
            # Login and send
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
            
            server.send_message(message)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True, "Email sent successfully"
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False, f"Failed to send email: {str(e)}"
    
    def send_registration_otp(self, email):
        """
        Generate and send OTP for registration
        
        Args:
            email: User's email address
        
        Returns:
            tuple: (success: bool, message: str, otp: str or None)
        """
        # Generate OTP
        otp = otp_storage.generate_otp()
        
        # Store OTP
        otp_storage.store_otp(email, otp, purpose='registration', expiry_minutes=10)
        
        # Send email
        success, message = self.send_otp_email(email, otp, purpose='registration')
        
        if success:
            return True, message, otp
        else:
            return False, message, None
    
    def send_password_reset_otp(self, email):
        """
        Generate and send OTP for password reset
        
        Args:
            email: User's email address
        
        Returns:
            tuple: (success: bool, message: str, otp: str or None)
        """
        # Generate OTP
        otp = otp_storage.generate_otp()
        
        # Store OTP
        otp_storage.store_otp(email, otp, purpose='password_reset', expiry_minutes=10)
        
        # Send email
        success, message = self.send_otp_email(email, otp, purpose='password_reset')
        
        if success:
            return True, message, otp
        else:
            return False, message, None
    
    def verify_otp(self, email, otp, purpose='registration'):
        """
        Verify an OTP
        
        Args:
            email: User's email address
            otp: The OTP to verify
            purpose: 'registration' or 'password_reset'
        
        Returns:
            tuple: (success: bool, message: str)
        """
        return otp_storage.verify_otp(email, otp, purpose)


# Global instance
email_service = EmailService()