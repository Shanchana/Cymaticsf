from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import F,Sum,Q
from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncDate,TruncWeek
from django.utils.timezone import now,localdate
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseBadRequest,HttpResponse,JsonResponse
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import timedelta

from dateutil import parser
from django.utils.dateparse import parse_datetime
import random
import requests
from django.conf import settings  # Assuming the Google API key is stored in settings
from calendar import month_name
from django.core.paginator import Paginator

# global objects
clobj = Client.objects.all()
incobj = Income.objects.all()
probj = Project.objects.all()
asobj = Assets.objects.all()
exsobj = Expense.objects.all()

# clients page
@csrf_exempt
def clients(request):

    if request.method == 'POST':
        # Handle new entertainment creation
            try:
                i_name = request.POST.get('newName', '').strip()
                i_company = request.POST.get('newCompany', '').strip()
                i_number = request.POST.get('newNumber', '').strip()
                i_email = request.POST.get('newEmail', '').strip()
                i_image = request.POST.get('newImage', '').strip()
                
               
                 # Create and save the new client object
                new_obj = Client(
                    name=i_name,
                    company=i_company,
                    number=i_number,
                    email = i_email,
                    img = i_image,
                    
                )
                new_obj.save()

                return redirect('clients')

            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)


# search box
    query = request.GET.get('q', '')
    if query:
        clobj = Client.objects.filter(
            Q(name__icontains=query)|
            Q(company__icontains=query)|
            Q(number__icontains=query)|
            Q(email__icontains=query)
        )
    else:
        clobj = Client.objects.all()

    return render(request, 'clients.html', {'objs' : clobj ,'query': query , 'is_admin':request.user.is_superuser})

@csrf_exempt
def get_client_data(request, clt_id):
    try:
        client = Client.objects.get(id = clt_id)
        data = {
            'name': client.name,
            'company': client.company,
            'number': client.number,
            'email': client.email,
            'image' : client.img.url if client.img else None
        }

        return JsonResponse(data)
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    
@csrf_exempt
def edit_client(request, clt_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id = clt_id)
    
            i_name = request.POST.get('editName', '').strip()
            i_number = request.POST.get('editNumber', '').strip()
            i_email = request.POST.get('editEmail' , '').strip()
            i_company = request.POST.get('editCompany' , '').strip()
            
            if 'editImage' in request.FILES:
                client.img = request.FILES['editImage'] # saves the image
    
           
            client.name = i_name
            client.company = i_company
            client.email = i_email
            client.number = i_number
        
            client.save()
    
            return JsonResponse({'success': True})

        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'client not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# outclients page
@csrf_exempt
def outclients(request):

    if request.method == 'POST':
         # Handle new outclients creation
            try:
                i_name = request.POST.get('newName', '').strip()
                i_company = request.POST.get('newCompany', '').strip()
                i_number = request.POST.get('newNumber', '').strip()
                i_email = request.POST.get('newEmail', '').strip()
                i_image = request.FILES.get('newImage', '')
                
               
                 # Create and save the new clients object
                new_oobj = Outclient(
                    name=i_name,
                    company=i_company,
                    number=i_number,
                    email = i_email,
                    img = i_image,
                    
                )
                new_oobj.save()

                return redirect('outclients')

            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)


# search box
    query = request.GET.get('q', '')
    if query:
        oclobj = Outclient.objects.filter(
            Q(name__icontains=query)|
            Q(company__icontains=query)|
            Q(number__icontains=query)|
            Q(email__icontains=query)
        )
    else:
        oclobj = Outclient.objects.all()

    return render(request, 'outclients.html', {'objso' : oclobj ,'query': query ,'is_admin':request.user.is_superuser})

@csrf_exempt
def get_outclient_data(request, oclt_id):
    try:
        oclient = Outclient.objects.get(id = oclt_id)
        data = {
            'name': oclient.name,
            'company': oclient.company,
            'number': oclient.number,
            'email': oclient.email,
            'image' : oclient.img.url if oclient.img else None
        }

        return JsonResponse(data)
    except Outclient.DoesNotExist:
        return JsonResponse({'error': 'Outclient not found'}, status=404)
    
@csrf_exempt
def edit_outclient(request, oclt_id):
    if request.method == 'POST':
        try:
            oclient = Outclient.objects.get(id = oclt_id)
    
            i_name = request.POST.get('editName', '').strip()
            i_number = request.POST.get('editNumber', '').strip()
            i_email = request.POST.get('editEmail' , '').strip()
            i_company = request.POST.get('editCompany' , '').strip()
            
            if 'editImage' in request.FILES:
                oclient.img = request.FILES['editImage'] # saves the image
    
           
            oclient.name = i_name
            oclient.company = i_company
            oclient.email = i_email
            oclient.number = i_number
        
            oclient.save()
    
            return JsonResponse({'success': True})

        except Outclient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'client not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


#details for outclient 
def outclientd(request, name):
    oprojects = Project.objects.filter(out_client = name)

    oclient = get_object_or_404(Outclient, name=name)

    total = oprojects.aggregate(total = Sum('amount'))['total']

    # Aggregate the frequency of each company
    clientpro_counts = oprojects.count()

    context = {'projects' : oprojects ,
               'total': total ,
                 'count' : clientpro_counts ,
                 'client': oclient}

    return render(request , 'outclientd.html' , context)


# project page
from django.http import JsonResponse

@csrf_exempt
def projects(request):
    if request.method == 'POST':
        try:
            # Extract form data as before
            i_type = request.POST.get('addProjectType', '').strip()
            i_status = request.POST.get('addstatus', '').strip()
            i_name = request.POST.get('addProjectName', '').strip()
            i_company = request.POST.get('addCustomerCompany', '').strip()
            i_start = request.POST.get('addShootStart', '').strip()
            i_end = request.POST.get('addShootEnd', '').strip()
            i_amount = request.POST.get('addProjectAmount', '').strip()
            i_location = request.POST.get('addProjectLocation', '').strip()
            i_address = request.POST.get('address', '').strip()
            i_reference = request.POST.get('addReference', '').strip()
            i_out = request.POST.get('addoutsourcing', False) 
            i_ofor = request.POST.get('addoutsourcingFor', '').strip()
            i_oamount = request.POST.get('addoutsourcingAmount', '').strip()
            i_ocus = request.POST.get('addoutsourcingCustomer', '').strip()
            i_opaid = request.POST.get('addoutsourcingPaid', False)

            # Use either location or address
            final_address = i_location if i_location else i_address

            # Fetch latitude and longitude from address
            lat, lng = get_lat_lng_from_address(final_address)

            # Parse datetime fields as before
            formatted_sdatetime = datetime.strptime(i_start, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S') if i_start else None
            formatted_edatetime = datetime.strptime(i_end, '%d-%m-%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S') if i_end else None

            # Handle boolean fields for outsourcing and outsourcing_paid
            i_out = True if i_out == 'on' else False
            i_opaid = True if i_opaid == 'on' else False

            # Attempt to convert amounts to integer
            i_amount = int(i_amount) if i_amount else 0
            i_oamount = int(i_oamount) if i_oamount else 0

            # Create and save the new Project object with latitude and longitude
            new_obj = Project(
                type=i_type,
                status=i_status,
                name=i_name,
                company=i_company,
                shoot_start_date=formatted_sdatetime,
                shoot_end_date=formatted_edatetime,
                amount=i_amount,
                location=final_address,
                latitude=lat,
                longitude=lng,
                address=i_address,
                outsourcing=i_out,
                reference=i_reference,
                out_for=i_ofor,
                outsourcing_amt=i_oamount,
                out_client=i_ocus,
                outsourcing_paid=i_opaid
            )
            new_obj.save()

            return redirect('projects')

        except ValueError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # Filter functions and search
    query = request.GET.get('q', '')
    type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    customer_company = request.GET.get('company', '')

    filters = Q()
    if query:
        filters &= (
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(company__icontains=query) |
            Q(type__icontains=query) |
            Q(status__icontains=query) |
            Q(shoot_start_date__icontains=query) |
            Q(shoot_end_date__icontains=query) |
            Q(amount__icontains=query) |
            Q(location__icontains=query) |
            Q(outsourcing__icontains=query) |
            Q(reference__icontains=query) |
            Q(pending_amt__icontains=query) |
            Q(received_amt__icontains=query) |
            Q(address__icontains=query) |
            Q(profit__icontains=query) |
            Q(outsourcing_amt__icontains=query) |
            Q(outsourcing_paid__icontains=query) |
            Q(client__name__icontains=query)
        )
    if type:
        type_list = type.split(',')
        filters &= Q(type__in=type_list)
    if status:
        status_list = status.split(',')
        filters &= Q(status__in=status_list)
    if customer_company:
        company_list = customer_company.split(',')
        filters &= Q(company__in=company_list)

    objs5 = Project.objects.filter(filters)


    context = {
        'objs': objs5,
        'query': query,
        'type': type,
        'status': status,
        'company': customer_company,
        'is_admin': request.user.is_superuser
    }

    return render(request, 'project.html', context)

@csrf_exempt
def get_model_data(request, code):
    try:
        project = Project.objects.get(code=code)
        data = {
            'projectType': project.type,
            'projectStatus': project.status,
            'projectName': project.name,
            'customerCompany': project.company,
            'shootStart': project.shoot_start_date.strftime('%Y-%m-%d %H:%M')if project.shoot_start_date else None,
            'shootEnd': project.shoot_end_date.strftime('%Y-%m-%d %H:%M')if project.shoot_end_date else None,
            'projectAmount': project.amount,
            'projectLocation': project.location,
            'address':project.address,
            'outsourcing': project.outsourcing,
            'outfor':project.out_for,
            'outamt': project.outsourcing_amt,
            'outcus': project.out_client,
            'outpaid': project.outsourcing_paid,
            'reference': project.reference
        }
        return JsonResponse(data)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@csrf_exempt
def edit_model(request, code):
    if request.method == 'POST':
        try:
            project = Project.objects.get(code=code)
            
            i_type = request.POST.get('projectType', '').strip()
            i_status = request.POST.get('editstatus', '').strip()
            i_name = request.POST.get('projectName', '').strip()
            i_company = request.POST.get('customerCompany', '').strip()
            i_start = request.POST.get('shootStart', '').strip()
            i_end = request.POST.get('shootEnd', '').strip()
            i_amount = request.POST.get('projectAmount', '').strip()
            i_location = request.POST.get('projectLocation', '').strip()
            i_address = request.POST.get('address', '').strip()
            i_reference = request.POST.get('reference', '').strip()
            i_out = request.POST.get('outsourcing', False)
            i_ofor = request.POST.get('outsourcingFor', '').strip()
            i_oamount = request.POST.get('outsourcingAmount', '').strip()
            i_ocus = request.POST.get('outsourcingCustomer', '').strip()
            i_opaid = request.POST.get('outsourcingPaid', False) 

            if i_out == 'on':
                i_out = True
            else:
                i_out = False

            if i_opaid == 'on':
                i_opaid = True
            else:
                i_opaid = False

            

              # Attempt to convert the string to an integer
            try:
                i_oamount = int(i_oamount)
            except ValueError:
                raise ValueError("Invalid oamount value")

            # Attempt to convert the string to an integer
            try:
                i_amount = int(i_amount)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid value'})

            # Update and save the existing Project object
            project.type = i_type
            project.status = i_status
            project.name = i_name
            project.company = i_company
            project.shoot_start_date = i_start
            project.shoot_end_date = i_end
            project.amount = i_amount
            project.location = i_location
            project.address = i_address
            project.outsourcing = i_out
            project.reference = i_reference
            project.out_for = i_ofor
            project.out_client = i_ocus
            project.outsourcing_amt = i_oamount
            project.outsourcing_paid = i_opaid
            project.save()

            return JsonResponse({'success': True})

        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        print(f"Deleted project with ID {project_id}")  # Debugging log

        return redirect('projects')  # Redirect to a list view or some other page
    else:
        return redirect('projects') 

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from datetime import datetime
import json

# income page
@csrf_exempt
def incomef_view(request):
    if request.user.is_superuser:

        if request.method == 'POST':
              
           # Handle new income creation
                try:
                    i_date_income = request.POST.get('date', '').strip()
                    i_desc = request.POST.get('description', '').strip()
                    i_amount = request.POST.get('amount', '').strip()
                    i_note = request.POST.get('note', '').strip()
                    i_project_income = request.POST.get('outsourcing', False)
                    i_p_code = request.POST.get('projectCode', '').strip()
    
                    # Convert amount to integer
                    try:
                        i_amount = int(i_amount)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid amount value'}, status=400)
    
                    if i_project_income == 'on':
                        i_project_income = True
                    else:
                        i_project_income = False
    
                    # Handle project_code as ForeignKey
                    project_instance = None
                    if i_p_code:
                        try:
                            project_instance = Project.objects.get(pk=i_p_code)
                        except Project.DoesNotExist:
                            return JsonResponse({'error': 'Invalid project code'}, status=400)
    
                    try:
                        # Parse the date string to a datetime object
                        parsed_date = datetime.strptime(i_date_income, '%d-%m-%Y')
                        # Format it back to the desired format
                        formatted_date = parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        # Handle the case where the date format is invalid
                        formatted_date = None  # or handle it as you need (e.g., return an error)
     
                    # Create and save the new Income object
                    new_obj = Income(
                        date=formatted_date,
                        project_income=i_project_income,
                        note=i_note,
                        amount=i_amount,
                        description=i_desc,
                        project_code=project_instance
                    )
                    new_obj.save()
    
                    if project_instance:
                        project_instance.update_project_finances()
                        project_instance.save()
    
                    months, original_values, received_values = get_incomechart()
    
                    return redirect('incomef_view')
    
                except ValueError as e:
                    return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
        # Handle search box
        query = request.GET.get('q', '')
    
        if query:
            inobj = Income.objects.filter(
                Q(date__icontains=query) |
                Q(description__icontains=query) |
                Q(amount__icontains=query) |
                Q(note__icontains=query) |
                Q(project_income__icontains=query) |
                Q(project_code__code__icontains=query)
            )
        else:
            inobj = Income.objects.all()
    
        months, original_values, received_values = get_incomechart()
        total = inobj.aggregate(total=Sum('amount'))['total']  # total income
    
        context = {
            'months': json.dumps(months),
            'original_values': json.dumps(original_values),
            'received_values': json.dumps(received_values),
            'total': total,
            'objs': inobj,
            'query': query
        }
    
        return render(request, 'incomef.html', context)
    else:
        return render(request , 'access_denied.html')




def get_incomechart():
    # Get the current year
    current_year = datetime.now().year

    # Fetch the data and group by month
    # Sum 'amount' as 'original_value' and 'received_amt' as 'received_value' for each month
    projects = Project.objects.filter(shoot_start_date__year=current_year).annotate(
        month=TruncMonth('shoot_start_date')  # Grouping by month of 'shoot_start_date'
    ).values('month').annotate(
        original_value=Sum('amount'),  # Sum total project amounts for each month
        received_value=Sum('received_amt')  # Sum total received amounts for each month
    ).order_by('month')

    # Prepare data for all months of the current year
    months = []
    original_values = []
    received_values = []

    # Iterate through all months from January to December
    for month in range(1, 13):
        # Convert the month number to the month's name (e.g., January, February)
        month_name = datetime(current_year, month, 1).strftime('%B')
        months.append(month_name)

        # Find data for the current month in the projects queryset
        project = next((p for p in projects if p['month'].month == month), None)

        # If data exists for the month, append the aggregated values to the lists
        if project:
            original_values.append(project['original_value'] or 0)  # Handle null cases by appending 0
            received_values.append(project['received_value'] or 0)  # Handle null cases by appending 0
        else:
            # If no project data exists for the month, append 0 for both values
            original_values.append(0)
            received_values.append(0)
    print(original_values)
    print(received_values)
    # Return the months, original values (total project amount), and received values
    return months, original_values, received_values


@csrf_exempt
def get_income_data(request, inc_id):
    try:
        income = Income.objects.get(id=inc_id)

        # Convert related Project model instance to a dictionary
        project_data = None
        if income.project_code:
            project_data = {
                'id': income.project_code.id,
                'name': str(income.project_code),  # Assuming __str__ method is defined for display name
            }

        data = {
            'date': income.date.strftime('%Y-%m-%dT%H:%M'),
            'desc': income.description,
            'amount': income.amount,
            'project_income': income.project_income,
            'note': income.note,
            'project_code': project_data,
        }

        return JsonResponse(data)
    except Income.DoesNotExist:
        return JsonResponse({'error': 'Income not found'}, status=404)


@csrf_exempt
def edit_income(request, inc_id):
    if request.method == 'POST':
        try:
            income = Income.objects.get(id=inc_id)

            i_date_income = request.POST.get('date', '').strip()
            i_desc = request.POST.get('description', '').strip()
            i_amount = request.POST.get('amount', '').strip()
            i_project_income = request.POST.get('outsourcing', False)
            i_note = request.POST.get('editnote' , '').strip()
            i_p_code = request.POST.get('projectCode', '').strip()

            # Convert amount to integer
            try:
                i_amount = int(i_amount)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid amount value'})

            # Handle project_code as ForeignKey
            project_instance = None
            if i_p_code:
                try:
                    project_instance = Project.objects.get(pk=i_p_code)
                except Project.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid project code'})
                
            if i_project_income == 'on':
                i_project_income = True
            else:
                i_project_income = False

            income.date = i_date_income
            income.description = i_desc
            income.amount = i_amount
            income.project_income = i_project_income
            income.project_code = project_instance
            income.note = i_note
            income.save()

            if project_instance:
                    project_instance.update_project_finances()
                    project_instance.save()


            #income.save()

            return JsonResponse({'success': True})

        except Income.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Income not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def save_income_notes(request):
    
    if request.method == 'POST':
        try:
            income_id = request.POST.get('income_id')  # Get the income ID from the AJAX request
            notes = request.POST.get('notes', '') 

            # Update the income note in your database here
            income = Income.objects.get(id=income_id)
            income.note = notes
            income.save()

            return JsonResponse({'status': 'success', 'message': 'Note saved.'})
        except Income.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Income not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@csrf_exempt
def expense(request):
    if request.user.is_superuser:
        # Aggregate calculations
    
        # current balance
        currentbalance()
    
        tincome = Income.objects.aggregate(tincome=Sum('amount'))['tincome']
        tproamt = Project.objects.aggregate(total=Sum('amount'))['total']
        tout = Project.objects.aggregate(total=Sum('outsourcing_amt'))['total']
    
        if request.method == 'POST':
            
        # Handle new expense creation
                try:
                    i_date = request.POST.get('date', '').strip()
                    i_desc = request.POST.get('description', '').strip()
                    i_amount = request.POST.get('amount', '').strip()
                    i_note = request.POST.get('note', '').strip()
                    i_p_expense = request.POST.get('addoutsourcing', False)
                    i_p_code = request.POST.get('projectCode', '').strip()
                    i_category = request.POST.get('category', '').strip()
    
                    try:
                        # Parse the date string to a datetime object
                        parsed_date = datetime.strptime(i_date, '%d-%m-%Y')
                        # Format it back to the desired format
                        formatted_date = parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        # Handle the case where the date format is invalid
                        formatted_date = None  # or handle it as you need (e.g., return an error)
     
                    if i_p_expense == 'on':
                        i_p_expense = True
                    else:
                        i_p_expense = False
    
                    # Convert amount to integer
                    try:
                        i_amount = int(i_amount)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid amount value'}, status=400)
    
                    # Handle project_code as ForeignKey
                    project_instance = None
                    if i_p_code:
                        try:
                            project_instance = Project.objects.get(pk=i_p_code)
                        except Project.DoesNotExist:
                            return JsonResponse({'error': 'Invalid project code'}, status=400)
    
                    # Create and save the new Expense object
                    new_obj = Expense(
                        date=formatted_date,
                        description=i_desc,
                        amount=i_amount,
                        notes=i_note,
                        project_expense=i_p_expense,
                        project_code=project_instance,
                        category=i_category,
                    )
                    new_obj.save()
                    currentbalance()
                    return redirect('expense')
    
                except ValueError as e:
                    return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
        # Search functionality
        query = request.GET.get('q', '')
        if query:
            exobj = Expense.objects.filter(
                Q(date__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query) |
                Q(amount__icontains=query) |
                Q(project_expense__icontains=query) |
                Q(project_code__code__icontains=query)
            )
        else:
            exobj = Expense.objects.all()
    
        # Total expense calculation
        texpense = exobj.aggregate(total=Sum('amount'))['total']
    
        context = {
            'objs': exobj,
            'tincome': tincome,
            'texpense': texpense,
            'tproamt': tproamt,
            'tout': tout,
            'curbal': int(total_current_balance),
            'query': query
        }
    
        return render(request, 'expense.html', context)
    else:
        return render(request , 'access_denied.html')


@csrf_exempt
def get_expense_data(request, exp_id):
    try:
        expense = Expense.objects.get(id=exp_id)

        # Convert related Project model instance to a dictionary
        project_data = None
        if expense.project_code:
            project_data = {
                'id': expense.project_code.id,
                'name': str(expense.project_code),  # Assuming __str__ method is defined for display name
            }

        data = {
            'editdate': expense.date.strftime('%Y-%m-%dT%H:%M'),
            'editcategory': expense.category,
            'editdescription': expense.description, 
            'editamount': expense.amount,
            'editProjectExpense': expense.project_expense,
            'project_code': project_data,
        }

        
        return JsonResponse(data)
    except Expense.DoesNotExist:
        return JsonResponse({'error': 'Expense not found'}, status=404)


@csrf_exempt
def edit_expense(request, exp_id):
    if request.method == 'POST':
        try:
            expense = Expense.objects.get(id=exp_id)

            i_date = request.POST.get('editdate', '').strip()
            i_category = request.POST.get('editcategory', '').strip()
            i_desc = request.POST.get('editdescription', '').strip()
            i_amount = request.POST.get('editamount', '').strip()
            i_p_expense = request.POST.get('outsourcing', False)
            i_p_code = request.POST.get('projectCode', '').strip()

            # Convert amount to integer
            try:
                i_amount = int(i_amount)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid aa value'})
            
            if i_p_expense == 'on':
                i_p_expense = True
            else:
                i_p_expense = False

            # Handle project_code as ForeignKey
            project_instance = None
            if i_p_code:
                try:
                    project_instance = Project.objects.get(pk=i_p_code)
                except Project.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid project code'})

            # Update and save the existing Expense object
            expense.date = i_date
            expense.category = i_category
            expense.description = i_desc
            expense.amount = i_amount
            expense.project_expense = i_p_expense
            expense.project_code = project_instance
            expense.save()

            currentbalance()

            return JsonResponse({'success': True})

        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# assets page
@csrf_exempt
def assets(request):
    if request.user.is_superuser:

        if request.method == 'POST':
        # Handle new asset creation
                try:
                    i_name = request.POST.get('name', '').strip()
                    i_date = request.POST.get('date', '').strip()
                    i_type = request.POST.get('type', '').strip()
                    i_qty = request.POST.get('qty', '').strip()
                    i_buy = request.POST.get('buyprice', '').strip()
                    i_note = request.POST.get('note', '').strip()
                    i_image = request.FILES.get('image', '')
    
                      # Attempt to convert the string to an integer
                    try:
                        i_qty = Decimal(i_qty)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid qty value'}, status=400)
    
                   # Attempt to convert the string to an integer
                    try:
                        i_buy = Decimal(i_buy)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid buy value'}, status=400)
    
                    try:
                        # Parse the date string to a datetime object
                        parsed_date = datetime.strptime(i_date, '%d-%m-%Y')
                        # Format it back to the desired format
                        formatted_date = parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        # Handle the case where the date format is invalid
                        formatted_date = None  # or handle it as you need (e.g., return an error)
     
                   
                     # Create and save the new Expense object
                    new_obj = Assets(
                        name=i_name,
                        date=formatted_date,
                        type=i_type,
                        quantity = i_qty,
                        image = i_image,
                        buy_price = i_buy,
                        note = i_note
                        
                    )
                    new_obj.save()
    
                    return redirect('assets')
    
                except ValueError as e:
                    return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    
    
        # search box
        query = request.GET.get('q', '')
    
        if query:
            objs5 = Assets.objects.filter(
                Q(name__icontains=query) | 
                Q(date__icontains=query) |
                Q(type__icontains=query) |
                Q(quantity__icontains=query) |
                Q(buy_price__icontains=query) |
                Q(value__icontains=query) |
                Q(note__icontains=query) 
                )
        else:
            objs5 = Assets.objects.all()
    
        # update the value field = quantity * buy price
        Assets.objects.update(
            value = F('quantity') * F('buy_price') 
        )
    
         # calculate the total value of assets
        total = asobj.aggregate(total=Sum('value'))['total']
    
        return render (request , 'assets.html' ,{'objs' : objs5 , 'total' : total , 'query':query})
    else:
        return render(request , 'access_denied.html')

@csrf_exempt
def get_asset_data(request, ast_id):
    try:
        asset = Assets.objects.get(id = ast_id)
        data = {
            'name': asset.name,
            'date': asset.date.strftime('%Y-%m-%dT%H:%M'),
            'type': asset.type,
            'qty': asset.quantity,
            'buy': asset.buy_price,
            'value': asset.value,
            'note': asset.note,
            'image' : asset.image.url if asset.image else None
        }
        print(data)

        return JsonResponse(data)
    except Assets.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    
@csrf_exempt
def edit_asset(request, ast_id):
    if request.method == 'POST':
        try:
            asset = Assets.objects.get(id = ast_id)
    
            i_name = request.POST.get('editName', '').strip()
            i_date = request.POST.get('editdate', '').strip()
            i_type = request.POST.get('editcategory', '').strip()
            i_qty = request.POST.get('editqty', '').strip()
            i_buy = request.POST.get('editbuyprice', '').strip()
            i_value = request.POST.get('editvalue', '').strip()
            i_note = request.POST.get('editnote' , '').strip()

            if 'editimage' in request.FILES:
                asset.image = request.FILES['editimage']  # Save the new image if provided
    

           # Attempt to convert the string to an integer
            try:
                i_qty = Decimal(i_qty)
            except ValueError:
                return JsonResponse({'error': 'Invalid qty value'}, status=400)
            
           # Attempt to convert the string to an decimal
            try:
                i_buy = Decimal(i_buy)
            except ValueError:
                return JsonResponse({'error': 'Invalid buy value'}, status=400)
            
            # Attempt to convert the string to an integer
            try:
                i_value = int(i_value)
            except ValueError:
                return JsonResponse({'error': 'Invalid value -- value'}, status=400)
            
            
            asset.name = i_name
            asset.date = i_date
            asset.type = i_type
            asset.quantity = i_qty
            asset.buy_price = i_buy
            asset.value = i_value
            asset.note = i_note

            asset.save()
    
            return JsonResponse({'success': True})

        except Assets.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'asset not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def delete_asset(request, ast_id):
    if request.method == 'POST':
        asset = get_object_or_404(Assets, id=ast_id)
        asset.delete()
        return redirect('assets')  # Redirect to a list view or some other page
    else:
        return redirect('assets') 

# clientsbook page
def clientsbook(request):

# Aggregate the frequency of each company
    company_counts = Project.objects.values('company', 'client__name').annotate(count=Count('company'))

# search box
    query = request.GET.get('q', '')
    project_count = request.GET.get('project_count', '')
    company = request.GET.get('company' , '')
    
    filters = Q()
    if query:
        filters &= (
            Q(company__icontains=query)|
            Q(client__name__icontains=query)|
            Q(count__icontains=query)

        )

    if company:
        com_list = company.split(',')
        filters &= Q(company__in = com_list)

     # Check for the filter on project count
    
    if project_count:
        try:
            # Split project_count into a list (in case of multiple comma-separated values)
            project_count_values = project_count.split(',')
            
            # Separate values for filtering
            numeric_values = [int(count) for count in project_count_values if count.isdigit()]
            greater_than_5_flag = 'greater_than_5' in project_count_values
    
            # Apply numeric filtering
            if numeric_values:
                filters &= Q(count__in=numeric_values)
    
            # Handle 'greater_than_5' case separately
            if greater_than_5_flag:
                filters &= Q(count__gt=5)

        except ValueError:
            pass

    objscc = company_counts.filter(filters)
    
    context = {
        'query' : query ,
        'project_count' : project_count,
        'company' : company,
        'objs' : objscc
    }

    

   
    return render(request , 'clientsbook.html' , context)

# status page
def status(request):

# search box
    query = request.GET.get('q', '')

# group the projects based on status
    statuses = Project.objects.values_list('status', flat = True).distinct()
    grouped_projects = {}

    for status in statuses:
        projects = Project.objects.filter(status=status)
        if query:
            projects = projects.filter(
                Q(code__icontains=query) |
                Q(name__icontains=query) |
                Q(company__icontains=query) |
                Q(type__icontains=query) |
                Q(status__icontains=query) |
                Q(shoot_start_date__icontains=query) |
                Q(shoot_end_date__icontains=query) |
                Q(amount__icontains=query) |
                Q(location__icontains=query) |
                Q(outsourcing__icontains=query) |
                Q(reference__icontains=query) |
                Q(pending_amt__icontains=query) |
                Q(received_amt__icontains=query) |
                Q(address__icontains=query) |
                Q(profit__icontains=query) |
                Q(outsourcing_amt__icontains=query) |
                Q(outsourcing_paid__icontains=query) |
                Q(client__name__icontains=query) 

            )
        grouped_projects[status] = projects

    context = {
        'objs' : grouped_projects,
        'query' : query,
        'is_admin' : request.user.is_superuser
    }

    return render(request,'status.html',context)

# pending payment page
def pending_pay(request):
    if request.user.is_superuser:

        # search box
        query = request.POST.get('q','')
    
        # filter based on pending amount > 0
        projects = Project.objects.filter(pending_amt__gt = 0)
    
        if query:
            projects = projects.filter(
                Q(code__icontains=query) |
                Q(name__icontains=query) |
                Q(company__icontains=query) |
                Q(type__icontains=query) |
                Q(status__icontains=query) |
                Q(shoot_start_date__icontains=query) |
                Q(shoot_end_date__icontains=query) |
                Q(amount__icontains=query) |
                Q(location__icontains=query) |
                Q(outsourcing__icontains=query) |
                Q(reference__icontains=query) |
                Q(pending_amt__icontains=query) |
                Q(received_amt__icontains=query) |
                Q(address__icontains=query) |
                Q(profit__icontains=query) |
                Q(outsourcing_amt__icontains=query) |
                Q(outsourcing_paid__icontains=query) |
                Q(client__name__icontains=query)  # Foreign key field lookup
            )
    
        projects = projects.order_by('-pending_amt') 
    
        context = {
            'objs': projects,
            'query' : query}
        
        return render(request,'pending_pay.html' ,context)
    else:
        return render(request , 'access_denied.html')

# entertainment page
@csrf_exempt
def entertainment(request):

    if request.method == 'POST':
    
      # Handle new entertainment creation
            try:
                i_type = request.POST.get('type', '').strip()
                i_lang = request.POST.get('language', '').strip()
                i_rating = request.POST.get('rating', '').strip()
                i_name = request.POST.get('name', '').strip()
                i_source = request.POST.get('source', '').strip()
                i_image = request.FILES.get('addimage')
                # Convert amount to integer
                try:
                    i_rating = int(i_rating)
                except ValueError:
                    return JsonResponse({'error': 'Invalid rating value'}, status=400)
                
                 # Create and save the new Expense object
                new_obj = Entertainment(
                    type=i_type,
                    language=i_lang,
                    rating=i_rating,
                    name = i_name,
                    source = i_source,
                    image = i_image
                    
                )
                new_obj.save()

                return redirect('entertainment')

            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)


    # search box
    query = request.GET.get('q','')

    if query:
        objs6 = Entertainment.objects.filter(
            Q(date__icontains = query)|
            Q(type__icontains=query)|
            Q(language__icontains=query)|
            Q(rating__icontains=query)|
            Q(name__icontains=query)|
            Q(source__icontains=query)

        )
    else:
         objs6 = Entertainment.objects.all()


    return render(request , 'entertainment.html' , {'objs' : objs6 , 'query' : query})

@csrf_exempt
def get_entertainment_data(request, ent_id):
    try:
        entertainment = Entertainment.objects.get(id = ent_id)
        data = {
            'date': entertainment.date.strftime('%Y-%m-%dT%H:%M'),
            'type': entertainment.type,
            'language': entertainment.language,
            'rating': entertainment.rating,
        }

        return JsonResponse(data)
    except Entertainment.DoesNotExist:
        return JsonResponse({'error': 'Entertainment not found'}, status=404)
    

@csrf_exempt
def edit_entertainment(request, ent_id):
    if request.method == 'POST':
        try:
            entertainment = Entertainment.objects.get(id = ent_id)
    
            i_date = request.POST.get('editdate', '').strip()
            i_type = request.POST.get('edittype', '').strip()
            i_lang = request.POST.get('editlanguage' , '').strip()
            i_rating = request.POST.get('editrating' , '').strip()
    
            # Convert rating to integer
            try:
                i_rating = int(i_rating)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid rate value'})
            
            entertainment.date = i_date
            entertainment.type = i_type
            entertainment.language = i_lang
            entertainment.rating = i_rating
            entertainment.save()
    
            return JsonResponse({'success': True})

        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_entertainment(request, ent_id):
    if request.method == 'POST':
        ent = get_object_or_404(Entertainment, id=ent_id)
        ent.delete()
        return redirect('entertainment')  # Redirect to a list view or some other page
    else:
        return redirect('entertainment') 


@csrf_exempt  # If CSRF issues, ensure CSRF token is handled
def update_rating(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            rating = request.POST.get('rating')
    
            # Fetch the object and update its rating
            try:
                obj = Entertainment.objects.get(id=item_id)
                obj.rating = int(rating)
                obj.save()
    
                return JsonResponse({'success': True})
            except Entertainment.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Item not found'})
    
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def get_rating(request, item_id):
    try:
        rate = Project.objects.get(item_id=item_id)
        return JsonResponse({'rating': rate.rating})  # Assuming 'value' is the field storing the rating
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Rating not found'}, status=404)
    
# allproject page
def allproject(request):
    # Get filter values from the POST request
    query = request.POST.get('q', '')
    type_values = request.POST.get('type', '')
    status_values = request.POST.get('status', '')
    outsourcing_values = request.POST.get('outsourcing', '')
    pending_amnt_min = request.POST.get('pending_amnt_min','')
    pending_amnt_max = request.POST.get('pending_amnt_max', '')

    filters = Q()

    # Searching across multiple fields
    if query:
        filters &= (Q(name__icontains=query) | 
                    Q(code__icontains=query) |
                    Q(company__icontains=query) |
                    Q(type__icontains=query) |
                    Q(status__icontains=query) |
                    Q(shoot_start_date__icontains=query) |
                    Q(shoot_end_date__icontains=query) |
                    Q(amount__icontains=query) |
                    Q(location__icontains=query) |
                    Q(outsourcing__icontains=query) |
                    Q(reference__icontains=query) |
                    Q(pending_amt__icontains=query) |
                    Q(received_amt__icontains=query) |
                    Q(address__icontains=query) |
                    Q(profit__icontains=query) |
                    Q(outsourcing_amt__icontains=query) |
                    Q(outsourcing_paid__icontains=query) |
                    Q(client__name__icontains=query))

    # Filter for status (if multiple, split by comma)
    if status_values:
        status_list = status_values.split(',')
        filters &= Q(status__in=status_list)
    
    # Filter for type (if multiple, split by comma)
    if type_values:
        type_list = type_values.split(',')
        filters &= Q(type__in=type_list)
    
    # Filter for outsourcing
    if outsourcing_values:
        outsourcing_list = outsourcing_values.split(',')
        filters &= Q(outsourcing__in=outsourcing_list)

    
    # Filter based on pending amount range
    if pending_amnt_min or pending_amnt_max:
        try:
            if pending_amnt_min:
                pending_amnt_min_val = float(pending_amnt_min)
                filters &= Q(pending_amt__gte=pending_amnt_min_val)
            if pending_amnt_max:
                pending_amnt_max_val = float(pending_amnt_max)
                filters &= Q(pending_amt__lte=pending_amnt_max_val)
        except ValueError:
            pass  # handle invalid number format gracefully 

    """
    # Apply multiple pending amount range filters
    pending_amnt_filters = Q()
    
    for min_val, max_val in zip(pending_amnt_min, pending_amnt_max):
        try:
            # Convert min/max values to float and apply the filter for each range
            if min_val and max_val:
                pending_amnt_min_val = float(min_val)
                pending_amnt_max_val = float(max_val)
                pending_amnt_filters |= Q(pending_amt_gte=pending_amnt_min_val, pending_amt_lte=pending_amnt_max_val)
        except ValueError:
            pass  # Handle invalid number format gracefully
    
    # Combine pending amount filters with other filters
    if pending_amnt_filters:
        filters &= pending_amnt_filters  """
    
    # Apply the filters to the Project model
    objs5 = Project.objects.filter(filters)

    project_expenses = []
    for project in objs5:
        total_expense = Expense.objects.filter(project_code=project).aggregate(total=Sum('amount'))['total'] or 0
        project_expenses.append({
            'project': project,
            'total_expense': total_expense
        })

    context = {
        'objs': objs5,
        'project_expenses': project_expenses,  
        'query': query,
        'type': type_values,
        'status': status_values,
        'outsourcing': outsourcing_values,
        'pending_amnt_min': pending_amnt_min,
        'pending_amnt_max': pending_amnt_max,
        'is_admin' : request.user.is_superuser
    }
    
    return render(request, 'allproject.html', context)


from calendar import month_name

from django.core.paginator import Paginator

# dashboard page
def dashboard(request):

    # total income
    tincome = incobj.aggregate(tincome = Sum('amount'))['tincome']

    # total expense
    texpense = exsobj.aggregate(total = Sum('amount'))['total']

    # total pending amount
    tpending = probj.aggregate(total = Sum('pending_amt'))['total']

    # pending amount project counts
    pending_count = Project.objects.filter(pending_amt__gt = 0).count()


    # current balance from fuction
    currentbalance()

    # filter based on pending amount > 0
    projects = Project.objects.filter(pending_amt__gt = 0)
    projects = projects.order_by('-pending_amt') 

    #pagination

    paginator = Paginator(projects,24)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    
    # pending projects
    pendpro = Project.objects.filter(
    Q(status='ONGOING') | Q(status='PENDING')
     ).order_by('status')

    #pendinng pagination
    penpage = Paginator(pendpro,24)
    pen_num = request.GET.get('page',1)
    pendpage_obj = penpage.get_page(pen_num)



    # Check if the request is an AJAX call
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Identify if the request is for "projects" or "pending projects"
        data_type = request.GET.get('data_type', 'projects')  # Expecting 'projects' or 'pending_projects'
    
        if data_type == 'projects':
            data = list(page_obj.object_list.values())  # Serialize queryset data
            return JsonResponse({
                'items': data,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
                'num_pages': page_obj.paginator.num_pages,
                'page_number': page_obj.number,
            })
    
        elif data_type == 'pending_projects':
            data = [
                {
                    'code': project.code,
                    'company': project.company,
                    'name': project.name,
                    'status': project.status,
                    'image_url': project.image.url  # Ensure you provide the full image URL
                }
                for project in pendpage_obj.object_list
            ]  # Serialize queryset data
    
            return JsonResponse({
                'itemsp': data,
                'has_previousp': pendpage_obj.has_previous(),
                'has_nextp': pendpage_obj.has_next(),
                'previous_page_numberp': pendpage_obj.previous_page_number() if pendpage_obj.has_previous() else None,
                'next_page_numberp': pendpage_obj.next_page_number() if pendpage_obj.has_next() else None,
                'num_pagesp': pendpage_obj.paginator.num_pages,
                'page_numberp': pendpage_obj.number,
            })


    # today shoot
    today = localdate()
    todayshoot = Project.objects.annotate(shoot_date=TruncDate('shoot_start_date')).filter(shoot_date=today)

    # upcoming 7 days shoot
    # Get today's date
    today = timezone.now().date()
    
    # Get the date 7 days from today
    end_date = today + timedelta(days=7)
    
    # Query for projects within the next 7 days, excluding today's shoots
    weekshoot = Project.objects.annotate(
        shoot_date=TruncWeek('shoot_start_date')
    ).filter(
        shoot_start_date__range=[today, end_date]
    ).exclude(
        pk__in=todayshoot.values('pk')
    )
    #weekshoot = Project.objects.annotate(shoot_date = TruncWeek('shoot_start_date')).filter(shoot_date =TruncWeek(today)).exclude(pk__in=todayshoot.values('pk'))

    # data for income and expense chart

    # current year
    current_year = datetime.now().year

      # Fetch the data and group by month
    income = Income.objects.filter(date__year=current_year).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        income_value=Sum('amount'),
    ).order_by('month')

    expense = Expense.objects.filter(date__year=current_year).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        expense_value=Sum('amount'),
    ).order_by('month')

    # prepare data for all months of the current year
    months = []
    income_values = []
    expense_values = []

         # income
    for month in range(1,13):
        month_name = datetime(current_year, month , 1).strftime('%B')
        months.append(month_name)
            # data for current month in income
        inc = next((i for i in income if i['month'].month == month), None)
        if inc:
            income_values.append(inc['income_value'])
        else:
            income_values.append(0)
        # data for current month in expense
        exp = next((e for e in expense if e['month'].month == month), None)
        if exp:
            expense_values.append(exp['expense_value'])
        else:
            expense_values.append(0)

    # line plot data for number of projects
    # group my month
    proc = Project.objects.filter(shoot_start_date__year = current_year).annotate(
        month=TruncMonth('shoot_start_date')
    ).values('month').annotate(
        count=Count('id'),
    ).order_by('month')
    # data preparation
    pro_c = []
    for month in range(1,13):
        # project counts
        pro = next((p for p in proc if p['month'].month == month), None)
        if pro:
            pro_c.append(pro['count'])
        else:
            pro_c.append(0)

    # pie chart
    pie_cat , pie_amt = get_pie_chart_data()

    # piechart end  ...x...

    total_expenses = Expense.objects.values('category').annotate(total_amount=Sum('amount')).order_by('category')
    
    # Prepare data as a dictionary with category as key and total amount as value
    category_expenses = {expense['category']: expense['total_amount'] for expense in total_expenses}
    
     # Fetch bar chart data
    month_names, bar_datasets = get_bar_chart_data()

    cat_bar2 , data_bar2 = category_expense_chart_view()


    context = {'tincome' : tincome , # total income
               'texpense': texpense , # total expense
               'curbal' : int(total_current_balance), # current balance
                'tpending' : tpending , # total pending amount
                'page_obj' : page_obj , # pending payments
                'pendpage_obj' : pendpage_obj, # pending projects
                'todayshoot' : todayshoot, # today shoot
                'weekshoot' : weekshoot, # week shoot
                'months': json.dumps(months),
              'income_values': json.dumps(income_values), # bar plot for income and expense
              'expense_values': json.dumps(expense_values),
              'pro_c' : json.dumps(pro_c) , # project counts
              'pie_cat': json.dumps(pie_cat), # category for pie chart
              'pie_amt': json.dumps(pie_amt), # amount for pie chart
              'category_expenses': category_expenses, # category wise total expense for list
              'datasets': json.dumps(bar_datasets), # bar chart 1
              'month_name' : json.dumps(month_names),
              'cat_bar2':json.dumps(cat_bar2), # barchart 2
              'data_bar2':json.dumps(data_bar2),
              'pending_count':pending_count,
              'is_admin':request.user.is_superuser

             }

    
    return render(request,'dashboard.html' , context)
## pie chart data
def get_pie_chart_data():
    # Fetch the expenses data from the database for the pie chart
    expenses = Expense.objects.values('category').annotate(total_amount=Sum('amount')).order_by('category')
    
    # Prepare data for the pie chart
    categories = [expense['category'] for expense in expenses]
    amounts = [expense['total_amount'] for expense in expenses]

    return categories, amounts


## first bar chart
def get_bar_chart_data():
    current_year = datetime.now().year
    
    # Fetch expenses grouped by category and month, and sum their amounts
    expenses = Expense.objects.filter(date__year=current_year) \
        .values('category', 'date__month') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('date__month')
    
    # Initialize data structure for storing expenses by month and category
    monthly_category_expenses = defaultdict(lambda: defaultdict(float))
    
    # Process the expenses to group by month and category
    for expense in expenses:
        month = str(expense['date__month'])  # Extract month as string
        category = expense['category']
        amount = expense['total_amount']
        monthly_category_expenses[month][category] += amount
    
    # Static month names for the chart
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Prepare data for the bar chart
    categories = sorted({cat for month_dict in monthly_category_expenses.values() for cat in month_dict})
    
    # Create data structure for Chart.js datasets
    datasets = []
    for category in categories:
        data = [monthly_category_expenses[str(i+1)].get(category, 0) for i in range(12)]  # Get category values for each month
        datasets.append({
            'label': category,
            'data': data,
            'backgroundColor': f'rgba({int(75*0.6)}, {int(192*0.6)}, {int(192*0.6)}, 0.6)',  # Example color
            'borderWidth': 0
        })
    
    return month_names, datasets


def category_expense_chart_view():
    current_year = datetime.now().year
    
    # Fetch expenses grouped by category and month, and sum their amounts
    expenses = Expense.objects.filter(date__year=current_year) \
        .values('category', 'date__month') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('date__month')
    
    # Initialize data structure to store expenses by month and category
    monthly_category_expenses = defaultdict(lambda: [0] * 12)  # Each category gets a list with 12 zeros (one for each month)
    
    # Process the expense data and store it by category and month
    for expense in expenses:
        month_index = expense['date__month'] - 1  # Adjust for 0-based index
        category = expense['category']
        total_amount = expense['total_amount']
        monthly_category_expenses[category][month_index] += total_amount  # Add the amount to the correct month
    
    # Convert defaultdict to regular dict for rendering in the template
    category_expenses_by_month = dict(monthly_category_expenses)
    
    # Categories will be used as x-axis labels
    categories = list(category_expenses_by_month.keys())
    
    # Convert the data into a format suitable for the frontend
    data = {str(i + 1): [category_expenses_by_month[category][i] for category in categories] for i in range(12)}

    return categories , data


# project details page
def projectd(request, code):
    project = get_object_or_404(Project, code=code)
    outclient_details = get_object_or_404(Outclient, name=project.out_client)
    
    # project's expense
    expenses = Expense.objects.filter(project_code = project)
    tote = expenses.aggregate(total = Sum('amount'))['total'] or 0


    # project's income received amount
    incomes = Income.objects.filter(project_code = project)
    toti = incomes.aggregate(total = Sum('amount'))['total'] or 0

    # Update pending amount and profit using F expressions

    # Update pending amount and profit using F expressions
    project.profit = project.amount - (project.outsourcing_amt + tote)
    project.received_amt = toti
    project.pending_amt = project.amount - project.received_amt
    
    # Save the updated project
    project.save()

    # edit functions

    if request.method == 'POST':
        if request.POST.get('edit_code'):  # Check if it's an edit request
            try:
                project_code = request.POST.get('edit_code').strip()
                instance = get_object_or_404(Project, code=project_code)

                i_type = request.POST.get('addProjectType', '').strip()
                i_status = request.POST.get('addProjectStatus', '').strip()
                i_name = request.POST.get('addProjectName', '').strip()
                i_company = request.POST.get('addCustomerCompany', '').strip()
                i_start = request.POST.get('addShootStart', '').strip()
                i_end = request.POST.get('addShootEnd', '').strip()
                i_amount = request.POST.get('addProjectAmount', '').strip()
                i_location = request.POST.get('addProjectLocation', '').strip()
                i_out = request.POST.get('addOutsourcing', '').strip()
                i_reference = request.POST.get('addReference', '').strip()




                # Attempt to convert the string to an integer
                try:
                    i_amount = int(i_amount)
                except ValueError:
                    return JsonResponse({'error': 'Invalid a value'}, status=400)

                # Convert the outsourcing field to a boolean
                i_out = i_out.lower() in ['true', '1', 'on']

                # Update and save the existing Project object
                instance.type = i_type
                instance.status = i_status
                instance.name = i_name
                instance.company = i_company
                instance.shoot_start_date = i_start
                instance.shoot_end_date = i_end
                instance.amount = i_amount
                instance.location = i_location
                instance.outsourcing = i_out
                instance.reference = i_reference


                instance.save()

                # Return success response for AJAX
                if request.is_ajax():
                    return JsonResponse({'success': True})

                # Redirect to the same page to prevent resubmission on refresh
                return redirect('projectd')  # Assuming 'projects' is the name of the URL pattern

            except ValueError as e:
                if request.is_ajax():
                    return JsonResponse({'success': False, 'error': str(e)})
                return render(request, 'project.html', {'error': str(e)})

    return render(request, 'projectd.html' , {'objs' : project , 'expenses' : expenses ,'totalex':tote , 'is_admin' : request.user.is_superuser ,'outcd':outclient_details})


#details for clients book
def bookd(request, company):
    projects = Project.objects.filter(company = company)
    total = projects.aggregate(total = Sum('amount'))['total']
    # Aggregate the frequency of each company
    company_counts = projects.values('company', 'client__name' ,'client__email' , 'client__number').annotate(count=Count('company'))
    context = {'projects' : projects , 'total': total , 'objs' : company_counts ,
               'is_admin':request.user.is_superuser}

    return render(request , 'bookd.html' , context)

#details for client 
def clientd(request, name):
    projects = Project.objects.filter(client__name = name)
    client = get_object_or_404(Client, name=name)

    total = projects.aggregate(total = Sum('amount'))['total']
    # Aggregate the frequency of each company
    company_counts = projects.values('company', 'client__name' ,'client__email' , 'client__number').annotate(count=Count('company'))
    context = {'projects' : projects ,
               'is_admin' : request.user.is_superuser,
               'total': total ,
                 'objs' : company_counts ,
                 'client': client}

    return render(request , 'clientsd.html' , context)


# dynamic project codes for dropdown
def get_project_codes(request):
    projects = Project.objects.all()
    data = [{"id" : proj.id ,"name": proj.name} for proj in projects]
    return JsonResponse(data, safe=False)


# entertainment details page
def entertainmentd(request, ent_id):
    entertainment = get_object_or_404(Entertainment, id = ent_id)
    return render(request,'entertainmentd.html' , {'objs':entertainment})

# assets details
def assetd(request, ast_id):
    if request.user.is_superuser:

        asset = get_object_or_404(Assets, id = ast_id)
        # Format the fields to 5 decimal places
        f_quantity = f"{asset.quantity:.5f}"
        f_buy_price = f"{asset.buy_price:.5f}"
    
        # edit functions
        if request.method == 'POST':
            if request.POST.get('ast_id'):
                try:
                    asset = Assets.objects.get(id = ast_id)
            
                    i_name = request.POST.get('editName', '').strip()
                    i_date = request.POST.get('editdate', '').strip()
                    i_type = request.POST.get('editcategory', '').strip()
                    i_qty = request.POST.get('editqty', '').strip()
                    i_buy = request.POST.get('editbuyprice', '').strip()
                    i_value = request.POST.get('editvalue', '').strip()
                    i_note = request.POST.get('editnote' , '').strip()
        
                    if 'editimage' in request.FILES:
                        asset.image = request.FILES['editimage']  # Save the new image if provided
            
        
                   # Attempt to convert the string to an integer
                    try:
                        i_qty = Decimal(i_qty)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid qty value'}, status=400)
                    
                   # Attempt to convert the string to an decimal
                    try:
                        i_buy = Decimal(i_buy)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid buy value'}, status=400)
                    
                    # Attempt to convert the string to an integer
                    try:
                        i_value = int(i_value)
                    except ValueError:
                        return JsonResponse({'error': 'Invalid value -- value'}, status=400)
                    
        
                    asset.name = i_name
                    asset.date = i_date
                    asset.type = i_type
                    asset.quantity = i_qty
                    asset.buy_price = i_buy
                    asset.value = i_value
                    asset.note = i_note
        
                    asset.save()
            
                    return JsonResponse({'success': True})
        
                except Assets.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'asset not found'})
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    
    
        context = {
            'objs' : asset,
            'quantity' : f_quantity,
            'buy_price': f_buy_price
        }
        return render(request,'assetd.html' , context)
    
    else:
        return render(request,'access_denied.html')




    
# budget page
# global var for current balance
total_current_balance = 0
cym_curbal = 0
gad_curbal = 0
ent_curbal = 0
inv_curbal = 0
yaso_curbal = 0
gopi_curbal = 0
adi_curbal = 0
oth_curbal = 0

# current balance calculation
def currentbalance():
    global total_current_balance 
    global cym_curbal 
    global gad_curbal 
    global ent_curbal 
    global inv_curbal 
    global yaso_curbal 
    global gopi_curbal 
    global adi_curbal 
    global oth_curbal 

    # Get the current year (or specify the year)
    year = datetime.now().year
    
    # Filter income records for the given year and calculate the total sum
    tal_income = Income.objects.filter(date__year=year).aggregate(total=Sum('amount'))['total']
    
    if tal_income:
        fo_san = Expense.objects.filter(date__year = year , category = "Food & Snacks").aggregate(total = Sum('amount'))['total'] or 0
        fu_tra = Expense.objects.filter(date__year = year , category = "Fuel & Travel").aggregate(total = Sum('amount'))['total'] or 0
        out = Expense.objects.filter(date__year = year , category = "Outsourcing").aggregate(total = Sum('amount'))['total'] or 0

        total_income = tal_income - fo_san - fu_tra - out
    else:
        total_income = 0

     # budget for a year
    cymbud = (36/100)*total_income
    gadbud = (10/100)*total_income
    entbud = (5/100)*total_income
    invbud = (15/100)*total_income
    othbud = (5/100)*total_income
    yasobud = (12.5/100)*total_income
    gopibud = (12.5/100)*total_income
    adibud = (4/100)*total_income

    # expense for a category per year
    expenses_by_category = {}

    catlist = ['Entertainment' ,'Investments' ,'Yaso' ,'Gopi','Adithyan','Others']

    for cat in catlist:
        total_expense = Expense.objects.filter(category=cat, date__year=year).aggregate(total=Sum('amount'))['total']
    
        # Set total_expense to 0 if no records exist
        total_expense = total_expense or 0
        
        # Store the result in the dictionary
        expenses_by_category[cat] = total_expense

    # cymatics budget page = cym + sal + loan
    cybudexplst= ['Cymatics' ,'Salary' ,'Loan Repayment']
    cyexp = Expense.objects.filter(category__in = cybudexplst , date__year = year).aggregate(total = Sum('amount'))['total'] or 0

    # gadgets budget page sum = gad + asset
    gadbudexplst = ['Gadgets' , 'Asset']
    gadexp = Expense.objects.filter(category__in = gadbudexplst , date__year = year).aggregate(total = Sum('amount'))['total'] or 0



    cym_curbal = cymbud - cyexp
    gad_curbal = gadbud - gadexp
    ent_curbal = entbud - expenses_by_category['Entertainment']
    inv_curbal = invbud - expenses_by_category['Investments']
    yaso_curbal = yasobud - expenses_by_category['Yaso']
    gopi_curbal = gopibud - expenses_by_category['Gopi']
    adi_curbal = adibud - expenses_by_category['Adithyan']
    oth_curbal = othbud - expenses_by_category['Others']

    total_current_balance = cym_curbal+gad_curbal+ent_curbal+inv_curbal+yaso_curbal+gopi_curbal+adi_curbal+oth_curbal


    
# budget page
def budget(request):
    if request.user.is_superuser:

        # current balance
        currentbalance()
    
        # Get the current month
        month = datetime.now().month
        
        # Aggregate the total income for the current month and year
        cur_received = Income.objects.filter(date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        cur_fo_san = Expense.objects.filter(date__month = month , category = "Food & Snacks").aggregate(total = Sum('amount'))['total'] or 0
        cur_fu_tra = Expense.objects.filter(date__month = month , category = "Fuel & Travel").aggregate(total = Sum('amount'))['total'] or 0
        cur_out = Expense.objects.filter(date__month = month , category = "Outsourcing").aggregate(total = Sum('amount'))['total'] or 0
    
        received = cur_received - cur_fo_san - cur_fu_tra - cur_out
    
        # Handle the case where no income is found
        if received is None:
            received = 0
    
        
        # monthly expense 
        expenses_by_category = {}
    
        catlist =['Entertainment' ,'Investments' ,'Yaso' ,'Gopi','Adithyan','Others']
    
        for cat in catlist:
            total_expense = Expense.objects.filter(category=cat, date__month=month).aggregate(total=Sum('amount'))['total']
        
            # Set total_expense to 0 if no records exist
            total_expense = total_expense or 0
            
            # Store the result in the dictionary
            expenses_by_category[cat] = total_expense
    
    
        # cymatics budget page = cym + sal + loan
        cybudexplst= ['Cymatics' ,'Salary' ,'Loan Repayment']
        cyexp = Expense.objects.filter(category__in = cybudexplst , date__month = month).aggregate(total = Sum('amount'))['total'] or 0
    
        # gadgets budget page sum = gad + asset
        gadbudexplst = ['Gadgets' , 'Asset']
        gadexp = Expense.objects.filter(category__in = gadbudexplst , date__month = month).aggregate(total = Sum('amount'))['total'] or 0
    
    
    
         # budget for a month
        cymbud = (36/100)*received
        gadbud = (10/100)*received
        entbud = (5/100)*received
        invbud = (15/100)*received
        othbud = (5/100)*received
        yasobud = (12.5/100)*received
        gopibud = (12.5/100)*received
        adibud = (4/100)*received
    
     
        # current balance for a month --- monthh  budget - monthly expense
        cymcurbal = cymbud - cyexp
        gadcurbal = gadbud - gadexp
        entcurbal = entbud - expenses_by_category['Entertainment']
        invcurbal = invbud - expenses_by_category['Investments']
        othcurbal = othbud - expenses_by_category['Others']
        yasocurbal = yasobud - expenses_by_category['Yaso']
        gopicurbal = gopibud - expenses_by_category['Gopi']
        adicurbal = adibud - expenses_by_category['Adithyan']
    
        # line plot data
    
        year = datetime.now().year
        month_amt = []
        for i in range(1,13):
            receive = Income.objects.filter(date__year = year , date__month = i).aggregate(total= Sum('amount'))['total']
    
            if receive:
                mon_fo_san = Expense.objects.filter(date__month = i , category = "Food & Snacks").aggregate(total = Sum('amount'))['total'] or 0
                mon_fu_tra = Expense.objects.filter(date__month = i , category = "Fuel & Travel").aggregate(total = Sum('amount'))['total'] or 0
                mon_out = Expense.objects.filter(date__month = i , category = "Outsourcing").aggregate(total = Sum('amount'))['total'] or 0
            
                received_mon = receive - mon_fo_san - mon_fu_tra - mon_out
            
            else:
                received_mon = 0
    
            month_amt.append(received_mon)
        
        months = []
        for month in range(1,13):
            month_name = datetime(year, month , 1).strftime('%B')
            months.append(month_name)
    
    
        
        context = {
            'curbal':  int(total_current_balance), # total cur bal
            'received':received, # month received
            'cym': int(cym_curbal),
            'gad':int(gad_curbal),
            'ent': int(ent_curbal),
            'inv': int(inv_curbal),
            'yaso': int(yaso_curbal),
            'gopi': int(gopi_curbal),
            'adi': int(adi_curbal),
            'oth': int(oth_curbal), # cur bal ends
    
            'cymbud': int(cymbud),
            'gadbud': int(gadbud),
            'entbud': int(entbud),
            'invbud': int(invbud),
            'othbud': int(othbud),
            'yasobud': int(yasobud),
            'gopibud': int(gopibud),
            'adibud': int(adibud), # budget for months ends here
    
            'cymexp': cyexp,
            'gadexp': gadexp,
            'entexp': expenses_by_category['Entertainment'],
            'invexp': expenses_by_category['Investments'],
            'othexp': expenses_by_category['Others'],
            'yasoexp': expenses_by_category['Yaso'],
            'gopiexp': expenses_by_category['Gopi'],
            'adiexp': expenses_by_category['Adithyan'], # monthly expense ends here
            
            'cymcurbalm': int(cymcurbal),
            'gadcurbalm': int(gadcurbal),
            'entcurbalm': int(entcurbal),
            'invcurbalm': int(invcurbal),
            'othcurbalm': int(othcurbal),
            'yasocurbalm':int(yasocurbal),
            'gopicurbalm':int(gopicurbal),
            'adicurbalm':int(adicurbal), # monthly current balance ends here
    
            'receivedamt':json.dumps(month_amt), # line plot for received amount
            'months': json.dumps(months)
            
        }
        return render (request,'budget.html', context)
    else:
        return render(request , 'access_denied.html')


def budgetd(request ,budgetcat):
    if request.user.is_superuser:
        # Get the current month
        month = datetime.now().month
        
        # Aggregate the total income for the current month and year
        curin_received = Income.objects.filter(date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        in_fo_san = Expense.objects.filter(date__month = month , category = "Food & Snacks").aggregate(total = Sum('amount'))['total'] or 0
        in_fu_tra = Expense.objects.filter(date__month = month , category = "Fuel & Travel").aggregate(total = Sum('amount'))['total'] or 0
        in_out = Expense.objects.filter(date__month = month , category = "Outsourcing").aggregate(total = Sum('amount'))['total'] or 0
    
        rece = curin_received - in_fo_san - in_fu_tra - in_out
    
        # Handle the case where no income is found
        if rece is None:
            rece = 0
    
        if budgetcat == 'Cymatics':
            # cymatics budget page = cym + sal + loan
            cybudexpplst= ['Cymatics' ,'Salary' ,'Loan Repayment']
            exp = Expense.objects.filter(category__in = cybudexpplst , date__month = month).aggregate(total = Sum('amount'))['total'] or 0
        
        elif budgetcat == 'Gadgets':
            # gadgets budget page sum = gad + asset
            gadbudexpplst = ['Gadgets' , 'Asset']
            exp = Expense.objects.filter(category__in = gadbudexpplst , date__month = month).aggregate(total = Sum('amount'))['total'] or 0
        
        else:
            exp = Expense.objects.filter(category=budgetcat, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        
        investmentdone =Expense.objects.filter(category="Investments", date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    
        month_name = datetime.now().strftime('%B')
    
        context = {
            'received' :rece,
            'monthly_exp':exp,
            'invdone':investmentdone,
            'category':budgetcat,
            'month' : month_name
    
        }
        
        return render(request , 'budgetd.html' , context)
    else:
        return render(request , 'access_denied.html')


#maps

@csrf_exempt
def add_project(request):
    if request.method == 'POST':
        if request.POST.get('edit_code'):
            try:
                project_code = request.POST.get('edit_code').strip()
                instance = get_object_or_404(Project, code=project_code)

                i_location = request.POST.get('addProjectLocation', '').strip()
                i_address = request.POST.get('address', '').strip()

                # Use either location or address
                final_address = i_location if i_location else i_address

                # Get latitude and longitude using the Google Geocoding API
                lat, lng = get_lat_lng_from_address(final_address)

                # Update and save the existing Project object
                instance.location = final_address
                instance.latitude = lat
                instance.longitude = lng
                instance.save()

                return JsonResponse({'success': True})

            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
        else:
            try:
                # Handle new project creation
                i_type = request.POST.get('addProjectType', '').strip()
                i_status = request.POST.get('addstatus', '').strip()
                i_name = request.POST.get('addProjectName', '').strip()
                i_company = request.POST.get('addCustomerCompany', '').strip()
                i_shootstart = request.POST.get('addShootStart', '').strip()
                i_shootend = request.POST.get('addShootEnd', '').strip()
                i_amount = request.POST.get('addProjectAmount', '').strip()
                i_out = request.POST.get('addoutsourcing', False) 
                i_reference = request.POST.get('addReference', '').strip()
                i_ofor = request.POST.get('addoutsourcingFor', '').strip()
                i_oamount = request.POST.get('addoutsourcingAmount', '').strip()
                i_ocus = request.POST.get('addoutsourcingCustomer', '').strip()
                i_opaid = request.POST.get('addoutsourcingPaid', False) 

                i_location = request.POST.get('addProjectLocation', '').strip()
                i_address = request.POST.get('address', '').strip()
                final_address = i_location if i_location else i_address

                lat, lng = get_lat_lng_from_address(final_address)

                try:
                    # Parse the start datetime string (format: 'dd-mm-yyyyTHH:MM')
                    parsed_sdatetime = datetime.strptime(i_shootstart, '%d-%m-%Y %H:%M')
                    # Format it back to the desired format (e.g., 'YYYY-MM-DD HH:MM' for backend use)
                    formatted_sdatetime = parsed_sdatetime.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Handle the case where the datetime format is invalid
                    formatted_sdatetime = None  # Handle as needed (e.g., return an error)
                    
                try:
                    # Parse the end datetime string (format: 'dd-mm-yyyyTHH:MM')
                    parsed_edatetime = datetime.strptime(i_shootend, '%d-%m-%Y %H:%M')
                    # Format it back to the desired format (e.g., 'YYYY-MM-DD HH:MM:SS' for backend use)
                    formatted_edatetime = parsed_edatetime.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Handle the case where the datetime format is invalid
                    formatted_edatetime = None  # Handle as needed
                
                
                if i_out == 'on':
                    i_out = True
                else:
                    i_out = False

                
                
                if i_opaid == 'on':
                    i_opaid = True
                else:
                    i_opaid = False

                # Attempt to convert the string to an integer
                try:
                    i_amount = int(i_amount) if i_amount else 0
                except ValueError:
                    raise ValueError("Invalid amount value")
                
                 # Attempt to convert the string to an integer
                try:
          
                    i_oamount = int(i_oamount) if i_oamount else 0
                except ValueError:
                    raise ValueError("Invalid oamount value")

                new_obj = Project(
                    type= i_type,
                    status= i_status,
                    name= i_name,
                    company= i_company,
                    shoot_start_date= formatted_sdatetime,
                    shoot_end_date= formatted_edatetime,
                    amount= i_amount,
                    location=final_address,
                    latitude=lat,  # Storing latitude
                    longitude=lng,  # Storing longitude
                    address=i_address,
                    outsourcing= i_out,
                    reference= i_reference,
                    out_for= i_ofor,
                    outsourcing_amt= i_oamount,
                    out_client= i_ocus,
                    outsourcing_paid= i_opaid
                )
                new_obj.save()
                
                return redirect('project_map')

            except ValueError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return render(request, 'map.html' , {'is_admin':request.user.is_superuser})


from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings

@csrf_exempt
def project_map(request):
    query = request.GET.get('q', '')
    print("Search Query:", query)  # Debugging query

    filters = Q()
    if query:
        filters &= Q(name__icontains=query)
        projects = Project.objects.filter(filters)
        print("Filtered Projects Count:", projects.count())  # Debugging filtered count
    else:
        projects = Project.objects.all()
        print("All Projects Count:", projects.count())  # Debugging total count

    # Build project data
    project_data = [
        {
            'name': project.name,
            'location': [project.latitude, project.longitude],
            'client': project.company if project.company else "N/A",
            'code': project.code,
        }
        for project in projects
    ]
    print("Project Data:", project_data)  # Debugging each project data

    # Check if AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return JSON for AJAX requests
        return JsonResponse({'projects': project_data})

    # Render HTML for normal requests
    return render(request, 'map.html', {'projects': project_data, 'query': query})



@csrf_exempt
def get_lat_lng_from_address(address):
    """Get latitude and longitude from an address using Google Geocoding API."""
    api_key = settings.GOOGLE_MAPS_API_KEY
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None


@csrf_exempt
def resolve_url(request):
    short_url = request.GET.get('url')
    try:
        response = requests.head(short_url, allow_redirects=True)
        full_url = response.url
        return JsonResponse({'resolved_url': full_url})
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
def fetch_places(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    api_key = 'AIzaSyAqIalCM0rqsXeHiyRP4ImBbVgqwMSv8D8'  # Replace with your actual API key
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=50&key={api_key}'
    response = requests.get(url)
    return JsonResponse(response.json())


# expense details and text box
@csrf_exempt
def expense_detail(request, expense_id):
    try:
        # Fetch the expense using the expense_id from the database
        expense = Expense.objects.get(id=expense_id)
    except Expense.DoesNotExist:
        # Handle the case where the expense does not exist
        expense = None
    
    # Pass the expense details (especially the notes) to the template
    return render(request, 'expensed.html', {'expense': expense})

@csrf_exempt
def save_expense_notes(request):
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')  # Get the expense ID from the AJAX request
        notes = request.POST.get('notes', '')  # Get the updated notes from text area

        try:
            # Find the correct expense by its ID in the database
            expense = Expense.objects.get(id=expense_id)
            
            # Update the notes field in the database
            expense.notes = notes
            expense.save()

            return JsonResponse({'status': 'success'})
        except Expense.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Expense not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


# income details and text box
@csrf_exempt
def income_detail(request, income_id):
    try:
        # Fetch the income using the expense_id from the database
        income = Income.objects.get(id=income_id)
    except income.DoesNotExist:
        # Handle the case where the income does not exist
        income = None
    
    # Pass the income details (especially the notes) to the template
    return render(request, 'incomed.html', {'income': income})

@csrf_exempt
def save_income_notes(request):
    
    if request.method == 'POST':
        income_id = request.POST.get('income_id')  # Get the income ID from the AJAX request
        notes = request.POST.get('notes', '')  # Get the updated notes from text area

        try:
            # Find the correct expense by its ID in the database
            income = Income.objects.get(id=income_id)
            
            # Update the notes field in the database
            income.note = notes
            income.save()

            return JsonResponse({'status': 'success'})
        except Income.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'income not found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def save_item(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            field = request.POST.get('field')
            value = request.POST.get('value')
    
           
            # Convert checkbox values to Boolean
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            
            # Handle empty values
            if value == '':
                value = None
    
            # Special handling for numeric fields (remove ₹ or any non-numeric characters)
            numeric_fields = ['amount', 'outsourcing_amt', 'received_amt', 'pending_amt', 'profit', 'expenses']
            if field in numeric_fields:
                value = value.replace('₹', '').replace(',', '').strip() if value else '0'
                try:
                    value = float(value)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid numeric value'}, status=400)
    
            # Special handling for date fields
    
            if field in ['shoot_start_date', 'shoot_end_date']:  # Add other datetime fields if needed
                try:
                    value = timezone.make_aware(timezone.datetime.fromisoformat(value))
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid datetime format'}, status=400)
    
            # Get the item instance
            try:
                item = Project.objects.get(id=item_id)  # Replace Project with your model
                setattr(item, field, value)  # Dynamically set the field value
                item.save()  # Save changes to the database
                return JsonResponse({'status': 'success'})
            except Project.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
# type for dropdown
def get_unique_types(request):
    unique_types = Project.objects.values_list('type', flat=True).distinct()
    return JsonResponse(list(unique_types), safe=False)

# company for dropdown
def get_unique_company(request):
    unique_company = Project.objects.values_list('company', flat=True).distinct()
    return JsonResponse(list(unique_company), safe=False)

# client for dropdown
def get_unique_client(request):
    unique_client = Outclient.objects.values_list('name', flat=True).distinct()
    return JsonResponse(list(unique_client), safe=False)

# unique categories for expense
def get_unique_category(request):
    unique_cat = Expense.objects.values_list('category', flat = True).distinct()
    return JsonResponse(list(unique_cat), safe=False)

# dashboard inside

def t_exp_in(request):
    if request.user.is_superuser:
        # search box
        query = request.GET.get('q', '')
        category = request.GET.get('category' , '') # filter
    
    
        # group expenses
        categories = Expense.objects.values_list('category', flat = True).distinct()
        grouped_expense = {}
    
        filters = Q()
    
        if category:
            cat_list = category.split(',')
            filters &= Q(category__in = cat_list)
    
        if query:
                filters &= (
                    Q(date__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query) |
                Q(amount__icontains=query) |
                Q(project_expense__icontains=query) |
                Q(project_code__code__icontains=query)
    
                )
        
        for cate in categories:
            exp = Expense.objects.filter(category = cate).filter(filters)
            paginator = Paginator(exp,1)
            page_number = request.GET.get('page',1)
            page_obj = paginator.get_page(page_number)
    
            expense_data = {
                'items' : list(page_obj.object_list.values('id', 'category', 'description', 'amount')),            
                'page_number': page_obj.number,
                'num_pages': paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            }
    
            grouped_expense[cate] = expense_data
    
    
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'expenses': grouped_expense})
        else:
        
            context = {
                    'cate': grouped_expense,
                    'query': query,
                    'category': category
                }
        
            return render(request , 'expense_cat.html', context)
    else:
        return render(request , 'access_denied.html')




# log in and register
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.contrib import messages
import re
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def extractname(email):
    return re.sub(r'[^a-zA-Z]', '' , email)

def generate_otp():
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    return otp


@csrf_exempt    
def send_otp(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        resend = request.POST.get('resend')  # Check if resend is requested

        # Extract name from email and create or get the user
        name = extractname(email.split('@')[0])
        user, created = User.objects.get_or_create(username=name, email=email)

        if resend:
            # Resend OTP logic
            otp_record = EmailOTP.objects.filter(user=user).last()
            otp = otp_record.otp if otp_record else generate_otp()
        else:
            # Generate a new OTP
            otp = generate_otp()
            # Save new OTP to the database
            EmailOTP.objects.create(user=user, otp=otp)
        
        # Send OTP via email
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP code is {otp}',
            from_email='shanchana2317@gmail.com',
            recipient_list=[email],
        )
        
        return render(request, 'verify_otp.html', {'email': email})  # Pass email for resend button
    
    return render(request, 'send_otp.html')


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            otp_record = EmailOTP.objects.get(otp=otp)
            user = otp_record.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            
            return redirect('dashboard')
        
        except EmailOTP.DoesNotExist:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'verify_otp.html')


@csrf_exempt
def logout_view(request):
    auth.logout(request)  # Log the user out
    return redirect('/') 




@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html' ,{'user' : user})


@login_required
def dashboard_inside(request):
    return render(request, 'dashboard_inside.html' )

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# calendar
@csrf_exempt
def calendar(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            event_title = data.get('eventTitle').strip()  # Retrieve event title
            event_start = data.get('clickedDate')  # Retrieve start time


            # Check for invalid data
            if not event_start or not event_title :
                print("Invalid data received. Title or time is missing.")
                return JsonResponse({'success': False, 'error': 'Invalid event data'}, status=400)

            # Convert the event start and end time to datetime
            try:
                formatted_start_datetime = datetime.fromisoformat(event_start[:-1])  # Use fromisoformat for the start time
            except ValueError:
                print("Invalid date format received:", event_start)
                return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)

            # Save the event in the database
            new_event = Project(
                name=event_title,
                shoot_start_date=formatted_start_datetime,
                shoot_end_date=formatted_start_datetime,
            )
            new_event.save()

            # Return a success response
            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            print("Invalid JSON data received")
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)

    return render(request, 'calendar.html' ,{ 'is_admin': request.user.is_superuser } )


# fetching data for displaying in the calendar
@csrf_exempt
def calendar_view(request):
    # Fetch events from the database
    events = Project.objects.all().values('id', 'name', 'shoot_start_date','shoot_end_date')
    # Return the events as a JSON response
    return JsonResponse(list(events), safe=False)


# get project data for calendar
@csrf_exempt
def get_cal_data(request, id):
    try:
        project = Project.objects.get(id=id)
        data = {
            'projectType': project.type,
            'projectStatus': project.status,
            'projectName': project.name,
            'customerCompany': project.company,
            'shootStart': project.shoot_start_date.strftime('%Y-%m-%d %H:%M')if project.shoot_start_date else None,
            'shootEnd': project.shoot_end_date.strftime('%Y-%m-%d %H:%M')if project.shoot_end_date else None,
            'projectAmount': project.amount,
            'projectLocation': project.location,
            'address':project.address,
            'outsourcing': project.outsourcing,
            'outfor':project.out_for,
            'outamt': project.outsourcing_amt,
            'outcus': project.out_client,
            'outpaid': project.outsourcing_paid,
            'reference': project.reference
        }
        return JsonResponse(data)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@csrf_exempt
def edit_cal(request, id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(id=id)
            
            i_type = request.POST.get('projectType', '').strip()
            i_status = request.POST.get('addstatus', '').strip()
            i_name = request.POST.get('projectName', '').strip()
            i_company = request.POST.get('customerCompany', '').strip()
            i_start = request.POST.get('shootStart', '').strip()
            i_end = request.POST.get('shootEnd', '').strip()
            i_amount = request.POST.get('projectAmount', '').strip()
            i_location = request.POST.get('projectLocation', '').strip()
            i_address = request.POST.get('address', '').strip()
            i_reference = request.POST.get('reference', '').strip()
            i_out = request.POST.get('outsourcing', False)
            i_ofor = request.POST.get('outsourcingFor', '').strip()
            i_oamount = request.POST.get('outsourcingAmount', '').strip()
            i_ocus = request.POST.get('outsourcingCustomer', '').strip()
            i_opaid = request.POST.get('outsourcingPaid', False) 

            if i_out == 'on':
                i_out = True
            else:
                i_out = False

            if i_opaid == 'on':
                i_opaid = True
            else:
                i_opaid = False   

              # Attempt to convert the string to an integer
            try:
                i_oamount = int(i_oamount) if i_oamount else 0
            except ValueError:
                raise ValueError("Invalid oamount value")

            # Attempt to convert the string to an integer
            try:
                i_amount = int(i_amount) if i_amount else 0
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid value'})



            # Update and save the existing Project object
            project.type = i_type
            project.status = i_status
            project.name = i_name
            project.company = i_company
            project.shoot_start_date = i_start
            project.shoot_end_date = i_end
            project.amount = i_amount
            project.location = i_location
            project.address = i_address
            project.outsourcing = i_out
            project.reference = i_reference
            project.out_for = i_ofor
            project.out_client = i_ocus
            project.outsourcing_amt = i_oamount
            project.outsourcing_paid = i_opaid

         
            project.save()

            return JsonResponse({'success': True})

        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})