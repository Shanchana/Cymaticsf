from django.urls import path,include
from . import views

urlpatterns = [

    # log in page
    path('', views.send_otp, name='send_otp'),
    
    path('clients',views.clients, name="clients"),
    path('projects/' ,views.projects, name="projects"),
    # edit functions
    path('get_model_data/<str:code>/', views.get_model_data, name='get_model_data'),
    path('edit_model/<str:code>/', views.edit_model, name='edit_model'),
    # project details page
    path('project/<str:code>/' , views.projectd , name="projectd"),
    # edit pattern for project
    path('get_model_data/<str:code>/', views.get_model_data, name='get_model_data'),
    path('edit_model/<str:code>/', views.edit_model, name='edit_model'),
    # delete project
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

    

    path('income',views.incomef_view,name="incomef_view"),
    path('get_income_data/<int:inc_id>/', views.get_income_data, name='get_income_data'),
    path('edit_income/<int:inc_id>/', views.edit_income, name='edit_income'),


    path('expense',views.expense,name="expense"),

    path('assets' , views.assets , name="assets"),

    path('clientsbook' , views.clientsbook , name ="clientsbook"),
    # clients book detail page
    path('bookd/<str:company>/' , views.bookd , name="bookd"),

    path('status',views.status,name="status"),
    path('pending_pay' , views.pending_pay,name="pending_pay"),
    path('entertainment' ,views.entertainment,name="entertainment"),
    # rating
    path('update_rating/', views.update_rating, name='update_rating'),
    path('get_rating/<int:item_id>/', views.get_rating, name='get_rating'),
    path('allproject' , views.allproject , name="allproject"),
    path('budget', views.budget,name="budget"),
    path('budget/<str:budgetcat>/', views.budgetd, name='budgetd'),  # Display the budget detail
    path('dashboard' ,views.dashboard,name="dashboard"),

    # edit pattern for expense
    path('get_expense_data/<int:exp_id>/', views.get_expense_data, name='get_expense_data'),
    path('edit_expense/<int:exp_id>/', views.edit_expense, name='edit_expense'),

    # entertainment edit patterns
    path('get_entertainment_data/<int:ent_id>/', views.get_entertainment_data, name='get_entertainment_data'),
    path('edit_entertainment/<int:ent_id>/', views.edit_entertainment, name='edit_entertainment'),

    # delete entertainment
    path('delete_entertainment/<int:ent_id>/', views.delete_entertainment, name='delete_entertainment'),

    # entertainment details page
    path('entertainmentd/<int:ent_id>/' , views.entertainmentd , name="entertainmentd"),

    #path('get_rating/<int:item_id>/', views.get_rating, name='get_rating'),
    #path('update_rating/', views.update_rating, name='update_rating'),

    # client edit
    path('get_client_data/<int:clt_id>/', views.get_client_data, name='get_client_data'),
    path('edit_client/<int:clt_id>/', views.edit_client, name='edit_client'),
    # clients detail
    path('clientd/<str:name>/' , views.clientd , name="clientd"),

    # asset edit
    path('get_asset_data/<int:ast_id>/', views.get_asset_data, name='get_asset_data'),
    path('edit_asset/<int:ast_id>/', views.edit_asset, name='edit_asset'),
    # asset details page
    path('assetd/<int:ast_id>/' , views.assetd , name="assetd"),
    # asset delete
    path('delete_asset/<int:ast_id>/', views.delete_asset, name='delete_asset'),


    
    # project code dropdown
    path('get_project_codes/', views.get_project_codes, name='get_project_codes'),
    # map 
    path('map/', views.project_map, name='project_map'),
    path('add_project/' ,views.add_project, name="add_project"),
    #path('api/projects/', views.get_project_data, name='get_project_data'),  # Returns project data in JSON

    path('resolve-url/', views.resolve_url, name='resolve-url'),
    path('fetch-places/', views.fetch_places, name='fetch-places'),

    # text box data in expense and details page
    path('expense/<int:expense_id>/', views.expense_detail, name='expense_detail'),  # Display the expense
    path('save-expense-notes/', views.save_expense_notes, name='save_expense_notes'), 

    # text box data in income and details page
    path('income/<int:income_id>/', views.income_detail, name='income_detail'),  # Display the income
    path('save-income-notes/', views.save_income_notes, name='save_income_notes'), 
    path('save-income-notes/', views.save_income_notes, name='save_income_notes'),  
    # allproject table edit 
    path('save-item/',views.save_item, name ='save_item'),

    # type dropdown
    path('get-unique-types/', views.get_unique_types, name='get_unique_types'),

     # company dropdown
    path('get-unique-company/', views.get_unique_company, name='get_unique_company'),

     #client dropdown
    path('get-unique-client/', views.get_unique_client, name='get_unique_client'),

    # unique category for expense
    path('get-unique-category/', views.get_unique_category, name='get_unique_category'),


    # total expense inside
    path('total-expense/' , views.t_exp_in, name="t_exp_in"),

    # register and logout
    path('verification' , views.verify_otp , name='verify_otp'),
    


    # profile page
    path('profile' , views.profile , name="profile"),
    path("logout", views.logout_view, name="logout_view"),
    path('dashboard_in' , views.dashboard_inside , name="dashboard_inside"),

     # calendar 
    path('calendar/' , views.calendar , name="calendar"),
    path('calendar/events/' , views.calendar_view , name="calendar_view"),

    # edit pattern for calendar
    path('get_cal_data/<int:id>/', views.get_cal_data, name='get_cal_data'),
    path('edit_cal/<int:id>/', views.edit_cal, name='edit_cal'),

    path('outclients',views.outclients, name="outclients"),

 # out clients
    path('get_outclient_data/<int:oclt_id>/', views.get_outclient_data, name='get_outclient_data'),
    path('edit_outclient/<int:oclt_id>/', views.edit_outclient, name='edit_outclient'),

    path('outclientd/<str:name>/' , views.outclientd , name="outclientd"),





]



"""
    path('', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'), """

