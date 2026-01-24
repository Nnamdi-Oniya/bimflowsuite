"""Utility functions for apps, including email notifications."""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import secrets


def send_admin_notification(subject, body, recipient_email=None):
    """
    Send email notification to admin with customizable content.

    Args:
        subject: Email subject line
        body: Email body content
        recipient_email: Optional recipient email (defaults to ADMIN_EMAIL setting)

    Returns:
        True if email sent successfully, False otherwise
    """
    admin_email = recipient_email or getattr(
        settings, "ADMIN_EMAIL", "admin@bimflowsuite.com"
    )

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Failed to send admin notification: {str(e)}")
        return False


def format_submission_email(data):
    """
    Format request submission data into email subject and body.

    Args:
        data: Dictionary with request submission fields:
            - firstname, lastname
            - email, phone_number, job_title
            - company_name, company_address, country, sector
            - request_type_display (one of: Request a Demo, General Enquiries, Compliance Validation, Other)
            - additional_details (optional)
            - consent_marketing, consent_privacy (boolean)
            - created_at (string)

    Returns:
        Tuple of (subject, body)
    """
    request_type = data.get("request_type_display", "Demo")
    subject = f"New {request_type} from {data.get('firstname')} {data.get('lastname')}"

    body = f"""
New Request Received
====================

Request Type: {request_type}

Personal Information:
- Name: {data.get("firstname")} {data.get("lastname")}
- Email: {data.get("email")}
- Phone: {data.get("phone_number")}
- Job Title: {data.get("job_title")}

Company Information:
- Company Name: {data.get("company_name")}
- Company Address: {data.get("company_address")}
- Country: {data.get("country")}
- Sector: {data.get("sector")}

Additional Details:
{data.get("additional_details") or "No additional details provided"}

Consents:
- Marketing Communications: {"Yes" if data.get("consent_marketing") else "No"}
- Privacy Policy Agreed: {"Yes" if data.get("consent_privacy") else "No"}

Submitted On: {data.get("created_at")}

---
This is an automated email from BIM Automation Toolkits
    """

    return subject, body


def send_request_notification(submission):
    """
    Send email notification to admin about a new request submission.
    Updates the email_sent flag on the DemoRequest instance after sending.

    Args:
        submission: DemoRequest instance

    Returns:
        True if email sent successfully, False otherwise
    """
    data = {
        "firstname": submission.firstname,
        "lastname": submission.lastname,
        "request_type_display": submission.get_request_type_display(),
        "email": submission.email,
        "phone_number": submission.phone_number,
        "job_title": submission.job_title,
        "company_name": submission.company_name,
        "company_address": submission.company_address,
        "country": submission.country,
        "sector": submission.sector,
        "additional_details": submission.additional_details,
        "consent_marketing": submission.consent_marketing,
        "consent_privacy": submission.consent_privacy,
        "created_at": submission.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    subject, body = format_submission_email(data)
    email_sent = send_admin_notification(subject, body)

    # Update the email_sent flag on the database record
    submission.email_sent = email_sent
    submission.save(update_fields=["email_sent"])

    return email_sent


def create_onboarding_user(submission):
    """
    Create a user account from a request submission and send onboarding email.

    Args:
        submission: RequestSubmission instance

    Returns:
        Tuple of (user, onboarding_email_sent)
    """
    try:
        # Generate unique username from email
        email_prefix = submission.email.split("@")[0]
        base_username = email_prefix
        username = base_username
        counter = 1

        # Ensure username is unique
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create user with unusable password (must be set via email link)
        user = User.objects.create_user(
            username=username,
            email=submission.email,
            first_name=submission.firstname,
            last_name=submission.lastname,
        )
        user.set_unusable_password()
        user.save()

        # Generate password reset token for activation
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Create activation link - points to backend API endpoint
        activation_url = f"{settings.BASE_URL}/api/v1/auth/activate/"

        # Send onboarding email with instructions
        subject = f"Welcome to BIMFlow Suite - Set Your Password"
        body = f"""Dear {submission.firstname} {submission.lastname},

Welcome to BIMFlow Suite! Your account has been created by our team.

To complete your registration and set your password, use the following credentials:

**User ID (UID):** {uid}
**Activation Token:** {token}

Instructions:
1. Go to your BIMFlow Suite account page
2. Click "Activate Account" 
3. Enter the UID and Token above
4. Create a new password (minimum 8 characters)
5. Click "Activate" to complete registration

Alternatively, you can use the API endpoint directly:
POST {activation_url}

Request body:
{{
  "uid": "{uid}",
  "token": "{token}",
  "password": "your-new-password",
  "password_confirm": "your-new-password"
}}

This token will expire in 24 hours.

If you have any questions, please contact us.

Best regards,
BIMFlow Suite Team

If you did not request this account or have any questions, please contact us.

Best regards,
BIMFlow Suite Team
        """

        email_sent = send_admin_notification(
            subject, body, recipient_email=submission.email
        )

        if email_sent:
            submission.onboarded_user = user
            submission.onboarding_email_sent = True
            submission.save(update_fields=["onboarded_user", "onboarding_email_sent"])

        return user, email_sent

    except Exception as e:
        print(f"Failed to create onboarding user: {str(e)}")
        return None, False


def send_onboarding_email(user, email):
    """
    Resend onboarding email with activation link.

    Args:
        user: User instance
        email: Email address

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = f"{settings.BASE_URL}/api/v1/auth/activate/"

        subject = f"Welcome to BIMFlow Suite - Set Your Password"
        body = f"""Dear {user.first_name} {user.last_name},

Your BIMFlow Suite account has been created.

To complete your registration and set your password, use the following credentials:

**User ID (UID):** {uid}
**Activation Token:** {token}

Instructions:
1. Go to your BIMFlow Suite account page
2. Click "Activate Account" 
3. Enter the UID and Token above
4. Create a new password (minimum 8 characters)
5. Click "Activate" to complete registration

Alternatively, you can use the API endpoint directly:
POST {activation_url}

Request body:
{{
  "uid": "{uid}",
  "token": "{token}",
  "password": "your-new-password",
  "password_confirm": "your-new-password"
}}

This token will expire in 24 hours.

If you have any questions, please contact us.

Best regards,
BIMFlow Suite Team
        """

        return send_admin_notification(subject, body, recipient_email=email)

    except Exception as e:
        print(f"Failed to send onboarding email: {str(e)}")
        return False
