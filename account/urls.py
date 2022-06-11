from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('complete-provisional-registration/', views.CompleteProvisionalRegistration.as_view(), name='complete_provisional_registration'),
    path('activated/<token>/', views.Activated.as_view(), name='activated'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('send-password-reset/', views.AcceptPasswordReset.as_view(), name='accept_password_reset'),
    path('set-password/<uidb64>/<token>/', views.SetPassword.as_view(), name='set_password'),
    path('complete-password-reset/', views.CompletePasswordReset.as_view(), name='complete_password_reset'),
    # NOTE: internal url of dashboard
    path('user-detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('update-user/<int:pk>/', views.UpdateUser.as_view(), name='update_user'),
    path('password-change/<int:pk>', views.PasswordChange.as_view(), name='password_change'),
]
