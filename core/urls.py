from django.urls import path
from .views import (
    register_tutor, register_student,
    UserLoginView, UserLogoutView,
    dashboard, pending_tutors, approve_tutor, assign_tutor,
    make_payment, payment_history, edit_student_profile, remove_assignment, view_tutor_profile
)

urlpatterns = [
    # Default route — redirects to dashboard (can be changed)
    path('', dashboard, name='home'),

    # Auth
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Registration
    path('register/tutor/', register_tutor, name='register_tutor'),
    path('register/student/', register_student, name='register_student'),

    # Dashboard + Admin Features
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/pending-tutors/', pending_tutors, name='pending_tutors'),
    path('dashboard/approve-tutor/<int:tutor_id>/', approve_tutor, name='approve_tutor'),
    path('dashboard/assign-tutor/', assign_tutor, name='assign_tutor'),
    path('dashboard/payments/make/', make_payment, name='make_payment'),
    path('dashboard/payments/history/', payment_history, name='payment_history'),

    path('dashboard/remove-assignment/<int:assignment_id>/', remove_assignment, name='remove_assignment'),

    path('tutor/profile/<int:tutor_id>/', view_tutor_profile, name='view_tutor_profile'),



]


urlpatterns += [
    path('student/profile/edit/', edit_student_profile, name='edit_student_profile'),
]