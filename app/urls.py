
from django.contrib import admin
from django.urls import path
from app.views import home , logining , signup , add_todo , signout , delete_todo, change_todo,token_send,verify,error_page




urlpatterns = [
   path('' , home , name='home' ), 
   path('login/' ,logining  , name='login'),
   path('signup/' , signup, name='signup' ),
   path('add-todo/' , add_todo ), 
   path('delete-todo/<int:id>' , delete_todo ), 
   path('change-status/<int:id>/<str:status>' , change_todo ), 
   path('logout/' , signout ),
   path('token/' , token_send , name="token_send"),
   path('verify/<auth_token>/' , verify , name="verify"),
   path('error/' , error_page , name="error")
]
