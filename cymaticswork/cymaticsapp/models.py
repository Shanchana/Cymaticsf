from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
import requests
from io import BytesIO
from django.core.files import File



# Clients
class Client(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100 , blank = True)
    img = models.ImageField(upload_to = 'media' ,blank = True)  

# outsourcing Clients
class Outclient(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100 , blank = True)
    img = models.ImageField(upload_to = 'media' ,blank = True) 

#project details
class Project(models.Model):
    code = models.TextField(unique=True ,blank=True ,null=True)
    name = models.CharField(max_length=100,  blank=True)

    company = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=50 , blank=True)
    status = models.CharField(max_length=50 ,blank=True , default='pending')

    shoot_start_date = models.DateTimeField(blank=True , null=True)
    shoot_end_date = models.DateTimeField(blank=True ,null=True)
    amount = models.IntegerField(default=0)
    location = models.CharField(max_length=200 ,blank=True)
    latitude = models.FloatField(default=0.0)  # To store the latitude for the map
    longitude = models.FloatField(default=0.0)
    outsourcing = models.BooleanField(default=False)
    reference = models.TextField(blank=True)
    image = models.ImageField(upload_to='media' , blank=True)
    pending_amt = models.IntegerField(default= 0)
    received_amt = models.IntegerField(default=0)
    address = models.CharField(max_length=500,blank=True)
    map = models.CharField(max_length=200 ,blank=True)
    profit = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    #blank = true ,so default 0
    outsourcing_amt = models.IntegerField(default=0)
    out_for = models.CharField(max_length=100 , blank=True)
    out_client = models.CharField(max_length=100 ,blank=True)
    outsourcing_paid = models.BooleanField(default=False)
    #client
    client = models.ForeignKey(Client, on_delete=models.CASCADE , null=True, blank=True)  # Assuming 1 is a valid Client ID

    def save(self, *args, **kwargs):
        # Set the client based on company name
        self.assign_client()
    
        # Convert the status to uppercase
        if self.status:
            self.status = self.status.upper()
        
        # Fetch the static map if image is empty and either location or address is provided
        if not self.image and (self.location or self.address):
            self.image = self.generate_static_map()

        # Save once to generate an ID if necessary
        if not self.code:
            super().save(*args, **kwargs)
            self.code = f'CYM-{self.id}'
            # Save code update separately
            super().save(update_fields=['code'])
    
        # Update financial fields
        self.update_project_finances()
    
        # Final save with all updates
        super().save(*args, **kwargs)
    
    def assign_client(self):
        if self.company:
            try:
                self.client = Client.objects.get(company=self.company)
            except Client.DoesNotExist:
                self.client = Client.objects.get(id=1)
    

    def update_project_finances(self):
        # Calculate financial fields based on expenses and income
        expenses_total = Expense.objects.filter(project_code=self).aggregate(total=Sum('amount'))['total'] or 0
        income_total = Income.objects.filter(project_code=self).aggregate(total=Sum('amount'))['total'] or 0
        self.profit = self.amount - (self.outsourcing_amt + expenses_total)
        self.received_amt = income_total
        self.pending_amt = self.amount - self.received_amt

    def get_google_maps_url(self):
        """Generate Google Maps URL for redirection based on latitude and longitude."""
        return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
    
    def generate_static_map(self):
        """Fetches the static map image from Google Maps API and saves it to the model's image field."""
        # Use either location or address to fetch the map
        if self.location:
            map_query = self.location
        elif self.address:
            map_query = self.address
        else:
            return None  # No valid query for the map
        
        # Construct the map URL using the location or address
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={map_query}&zoom=14&size=400x300&maptype=roadmap&markers=color:red%7C{map_query}&key=AIzaSyAqIalCM0rqsXeHiyRP4ImBbVgqwMSv8D8"
        
        response = requests.get(map_url)
        
        if response.status_code == 200:
            img_name = f"{self.name}_map.png"
            return File(BytesIO(response.content), name=img_name)
        return None

#income
class Income(models.Model):
    date = models.DateField()
    description = models.TextField()
    amount = models.IntegerField()
    note = models.TextField(blank= True)
    project_income = models.BooleanField(default=False)
    project_code = models.ForeignKey(Project, on_delete = models.CASCADE, related_name= 'received' , null = True, blank=True)


    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Incomes"
        ordering = ['-date']


#expense
class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.IntegerField()
    notes = models.TextField(blank=True)
    project_expense = models.BooleanField(default=False)
    project_code = models.ForeignKey(Project, on_delete = models.CASCADE, related_name= 'expense_expenses' , null = True, blank=True)

#assets
class Assets(models.Model):
    date = models.DateField()
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(decimal_places=50 , max_digits= 100)
    buy_price = models.DecimalField(decimal_places=50 , max_digits= 100)
    value = models.IntegerField(default=0)
    note = models.TextField(blank=True)
    image = models.ImageField(upload_to='media' , blank=True , null=True)

#entertainment
class Entertainment(models.Model):
    date= models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length = 100)
    language = models.CharField(max_length=100)
    rating = models.IntegerField()
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100 ,blank=True)
    image = models.ImageField(upload_to='media' , blank=True , null=True)



class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )  # Link to the User model
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.email} - {self.otp}"






