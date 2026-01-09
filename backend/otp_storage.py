# backend/otp_storage.py
"""
File-based OTP storage system for local development and college servers.
No external dependencies required - completely self-contained.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import random
import string

class OTPStorage:
    """Manages OTP storage in local JSON files"""
    
    def __init__(self, storage_dir='backend/otp_storage'):
        """Initialize OTP storage directory"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.otp_file = self.storage_dir / 'otps.json'
        self._ensure_storage_file()
    
    def _ensure_storage_file(self):
        """Create storage file if it doesn't exist"""
        if not self.otp_file.exists():
            self._write_otps({})
    
    def _read_otps(self):
        """Read all OTPs from storage"""
        try:
            with open(self.otp_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _write_otps(self, otps):
        """Write OTPs to storage"""
        with open(self.otp_file, 'w') as f:
            json.dump(otps, f, indent=2, default=str)
    
    def generate_otp(self, length=6):
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    def store_otp(self, email, otp, purpose='registration', expiry_minutes=10):
        """
        Store OTP for an email address
        
        Args:
            email: User's email address
            otp: The OTP code
            purpose: 'registration' or 'password_reset'
            expiry_minutes: How long the OTP is valid
        
        Returns:
            dict: OTP information
        """
        otps = self._read_otps()
        
        # Clean expired OTPs first
        self._clean_expired_otps()
        
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        
        otp_data = {
            'otp': otp,
            'purpose': purpose,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'attempts': 0,
            'verified': False
        }
        
        # Store with email as key
        key = f"{email}_{purpose}"
        otps[key] = otp_data
        
        self._write_otps(otps)
        
        return otp_data
    
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
        otps = self._read_otps()
        key = f"{email}_{purpose}"
        
        if key not in otps:
            return False, "No OTP found for this email"
        
        otp_data = otps[key]
        
        # Check if already verified
        if otp_data.get('verified'):
            return False, "OTP already used"
        
        # Check expiration
        expires_at = datetime.fromisoformat(otp_data['expires_at'])
        if datetime.now() > expires_at:
            del otps[key]
            self._write_otps(otps)
            return False, "OTP has expired"
        
        # Check attempts
        if otp_data['attempts'] >= 3:
            return False, "Too many failed attempts"
        
        # Verify OTP
        if otp_data['otp'] == otp:
            otp_data['verified'] = True
            otps[key] = otp_data
            self._write_otps(otps)
            return True, "OTP verified successfully"
        else:
            otp_data['attempts'] += 1
            otps[key] = otp_data
            self._write_otps(otps)
            remaining = 3 - otp_data['attempts']
            return False, f"Invalid OTP. {remaining} attempts remaining"
    
    def get_otp(self, email, purpose='registration'):
        """
        Get stored OTP for debugging/development
        
        Args:
            email: User's email address
            purpose: 'registration' or 'password_reset'
        
        Returns:
            str or None: The OTP if exists and valid
        """
        otps = self._read_otps()
        key = f"{email}_{purpose}"
        
        if key not in otps:
            return None
        
        otp_data = otps[key]
        
        # Check expiration
        expires_at = datetime.fromisoformat(otp_data['expires_at'])
        if datetime.now() > expires_at:
            return None
        
        return otp_data['otp']
    
    def delete_otp(self, email, purpose='registration'):
        """Delete OTP after successful use"""
        otps = self._read_otps()
        key = f"{email}_{purpose}"
        
        if key in otps:
            del otps[key]
            self._write_otps(otps)
    
    def _clean_expired_otps(self):
        """Remove expired OTPs from storage"""
        otps = self._read_otps()
        now = datetime.now()
        
        # Filter out expired OTPs
        valid_otps = {
            key: data for key, data in otps.items()
            if datetime.fromisoformat(data['expires_at']) > now
        }
        
        if len(valid_otps) != len(otps):
            self._write_otps(valid_otps)
    
    def get_all_otps(self):
        """Get all active OTPs (for debugging)"""
        self._clean_expired_otps()
        return self._read_otps()


# Global instance
otp_storage = OTPStorage()