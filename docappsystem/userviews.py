from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page,OnlineConsultation
import random
from datetime import datetime
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dasapp.utils import send_appointment_confirmation_email

stripe.api_key = settings.STRIPE_SECRET_KEY

def USERBASE(request):
    
    return render(request, 'userbase.html',context)

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'index.html',context)




def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        try:
            appointmentnumber = random.randint(100000000, 999999999)
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            mobilenumber = request.POST.get('mobilenumber')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            doctor_id = request.POST.get('doctor_id')
            appointment_type = request.POST.get('appointment_type')
            additional_msg = request.POST.get('additional_msg')

            doc_instance = DoctorReg.objects.get(id=doctor_id)

            try:
                appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
                today_date = datetime.now().date()
                if appointment_date <= today_date:
                    messages.error(request, "Please select a date in the future for your appointment")
                    return redirect('appointment')
            except ValueError:
                messages.error(request, "Invalid date format")
                return redirect('appointment')

            # Check if there's already an appointment at this time slot
            existing_appointment = Appointment.objects.filter(
                doctor_id=doc_instance,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                status__in=['0', 'Approved']  # Check only pending and approved appointments
            ).first()

            if existing_appointment:
                messages.error(request, f"This time slot ({time_of_appointment}) is already booked. Please choose a different time.")
                return redirect('appointment')

            # Create the appointment first
            appointment = Appointment.objects.create(
                appointmentnumber=appointmentnumber,
                fullname=fullname,
                email=email,
                mobilenumber=mobilenumber,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                doctor_id=doc_instance,
                appointment_type=appointment_type,
                additional_msg=additional_msg,
                status='0',  # Set initial status as pending
                payment_status='pending'
            )

            # Set price based on appointment type (you can adjust these values)
            amount = 2500 if appointment_type == 'online' else 3000  # Online: $25, Offline: $30
            currency = 'usd'
            
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': f'{appointment_type.title()} Appointment with {doc_instance.admin.first_name} {doc_instance.admin.last_name}',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=email,
                success_url=request.build_absolute_uri('/payment-success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/appointment/'),
                metadata={
                    'appointment_id': appointment.id,
                    'appointmentnumber': appointmentnumber,
                }
            )

            # Send confirmation email
            try:
                send_appointment_confirmation_email(appointment)
            except Exception as e:
                # Log the error but don't stop the appointment creation
                print(f"Failed to send confirmation email: {str(e)}")

            return redirect(session.url)
        except Exception as e:
            messages.error(request, f"Error creating appointment: {str(e)}")
            return redirect('appointment')

    context = {'doctorview': doctorview, 'page':page}
    return render(request, 'appointment.html', context)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_REPLACE_WITH_YOUR_ENDPOINT_SECRET'
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session['metadata']
        try:
            # Update the appointment status after payment
            appointment = Appointment.objects.get(id=metadata['appointment_id'])
            appointment.payment_status = 'paid'
            appointment.stripe_payment_intent_id = session['payment_intent']
            appointment.save()
        except Appointment.DoesNotExist:
            print(f"Appointment {metadata['appointment_id']} not found")
        except Exception as e:
            print(f"Error updating appointment: {str(e)}")
            
    return HttpResponse(status=200)

def payment_success(request):
    messages.success(request, "Your payment was successful and your appointment has been booked!")
    return redirect('appointment')

def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            # Fetch online consultation details for each appointment
            online_consultations = OnlineConsultation.objects.filter(appointment__in=patient)
            messages.info(request, "Search against " + query)
            print(f"Search query: {query}, Results found: {patient.count()}")
            context = {'patient': patient, 'query': query, 'page': page, 'online_consultations': online_consultations}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)

def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)

def schedule_online_consultation(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        # Generate a unique meeting ID (you can use a UUID or any unique identifier)
        meeting_id = f"meet-{appointment.appointmentnumber}-{random.randint(1000, 9999)}"
        # Construct a Google Meet link
        meeting_link = f"https://meet.google.com/{meeting_id}"
        meeting_password = "password123"  # You can generate a random password if needed
        scheduled_at = datetime.now()

        OnlineConsultation.objects.create(
            appointment=appointment,
            meeting_link=meeting_link,
            meeting_id=meeting_id,
            meeting_password=meeting_password,
            scheduled_at=scheduled_at
        )
        messages.success(request, "Online consultation scheduled successfully!")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
    return redirect('viewappointmentdetails', id=appointment_id)




