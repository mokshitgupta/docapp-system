from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_appointment_confirmation_email(appointment):
    """
    Send appointment confirmation email to the patient
    """
    subject = f'Appointment Confirmation - #{appointment.appointmentnumber}'
    
    # Prepare email context
    context = {
        'appointment': appointment,
        'doctor_name': f"{appointment.doctor_id.admin.first_name} {appointment.doctor_id.admin.last_name}",
        'specialization': appointment.doctor_id.specialization_id.sname,
    }
    
    # Render email template
    html_message = render_to_string('emails/appointment_confirmation.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        html_message=html_message,
        fail_silently=False,
    ) 