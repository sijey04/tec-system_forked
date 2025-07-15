import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from .models import OTPVerification

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

def save_otp(email):
    """
    Generate and save OTP for a user
    Returns the generated OTP
    """
    # Generate a random 6-digit OTP
    otp = generate_otp()
    
    # Set expiry time (10 minutes from now) using timezone-aware datetime
    expiry_time = timezone.now() + timedelta(minutes=10)
    
    # Delete any existing OTP for this email
    OTPVerification.objects.filter(email=email).delete()
    
    # Create new OTP record
    OTPVerification.objects.create(
        email=email,
        otp_code=otp,
        expires_at=expiry_time
    )
    
    return otp

def send_otp_email(email, otp):
    """Send OTP via Django's built-in email system with Gmail SMTP"""
    try:
        from django.core.mail import send_mail
        
        subject = "TEC Registration - Email Verification Code"
        
        # HTML email template
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #dc2626; margin-bottom: 10px;">TEC Registration System</h2>
                <h3 style="color: #333; margin-top: 0;">Email Verification</h3>
            </div>
            
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin-bottom: 15px; color: #555;">Hello,</p>
                <p style="margin-bottom: 15px; color: #555;">You have requested to register for the TEC (Testing and Evaluation Center) system.</p>
                
                <div style="text-align: center; margin: 25px 0;">
                    <p style="margin-bottom: 10px; color: #333; font-weight: bold;">Your verification code is:</p>
                    <div style="background-color: #dc2626; color: white; padding: 15px 25px; border-radius: 8px; font-size: 32px; font-weight: bold; letter-spacing: 8px; display: inline-block;">
                        {otp}
                    </div>
                </div>
                
                <p style="margin-bottom: 15px; color: #555;">This code will expire in <strong>10 minutes</strong>.</p>
                <p style="margin-bottom: 15px; color: #555;">If you did not request this code, please ignore this email.</p>
            </div>
            
            <div style="text-align: center; padding: 20px 0; border-top: 1px solid #eee;">
                <p style="color: #888; font-size: 14px; margin: 0;">
                    Best regards,<br/>
                    <strong>TEC Registration Team</strong><br/>
                    Western Mindanao State University
                </p>
            </div>
        </div>
        """
        
        # Plain text version
        text_message = f"""
TEC Registration System - Email Verification

Hello,

You have requested to register for the TEC (Testing and Evaluation Center) system.

Your verification code is: {otp}

This code will expire in 10 minutes.

If you did not request this code, please ignore this email.

Best regards,
TEC Registration Team
Western Mindanao State University
        """
        
        print(f"Sending email to {email} with OTP {otp}")
        print(f"Using Gmail SMTP: {settings.EMAIL_HOST_USER}")
        print(f"From email: {settings.DEFAULT_FROM_EMAIL}")
        
        # Send the email using Django's send_mail with Gmail SMTP
        result = send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        if result == 1:
            print("Email sent successfully via Gmail SMTP!")
            return True
        else:
            print("Failed to send email via Gmail SMTP")
            return False
            
    except Exception as e:
        print(f"Exception sending email via Gmail SMTP: {str(e)}")
        return False

def verify_otp(email, otp):
    """
    Verify if the provided OTP is valid
    Returns True if valid, False otherwise
    """
    try:
        # Get the OTP record for this email
        otp_record = OTPVerification.objects.get(email=email)
        
        # Check if OTP has expired - use timezone-aware datetime for comparison
        if timezone.now() > otp_record.expires_at:
            # Delete expired OTP
            otp_record.delete()
            return False
        
        # Check if OTP matches
        if otp_record.otp_code == otp:
            # Mark as verified
            otp_record.is_verified = True
            otp_record.save()
            return True
        
        return False
    except OTPVerification.DoesNotExist:
        return False 