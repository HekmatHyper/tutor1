from django.shortcuts import render, redirect
from .forms import TutorRegistrationForm, StudentRegistrationForm
from .models import TutorPayment
from django.shortcuts import render, get_object_or_404
from .models import TutorProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import EmailLoginForm
from django.contrib.auth.decorators import user_passes_test
from .models import TutorProfile, StudentProfile, TutorAssignment, CustomUser
from .forms import StudentProfileEditForm
from django.views.decorators.http import require_POST
from .forms import TutorPaymentForm

def register_tutor(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login or confirmation
    else:
        form = TutorRegistrationForm()
    return render(request, 'register_tutor.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login or confirmation
    else:
        form = StudentRegistrationForm()
    return render(request, 'register_student.html', {'form': form})

# This is for Login and Logout Views



class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = EmailLoginForm

class UserLogoutView(LogoutView):
    next_page = 'login'  # redirect to login after logout


# Admin Views



def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def pending_tutors(request):
    tutors = TutorProfile.objects.filter(approved=False)
    return render(request, 'pending_tutors.html', {'tutors': tutors})

@user_passes_test(is_admin)
def approve_tutor(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    tutor.approved = True
    tutor.save()
    return redirect('pending_tutors')




@user_passes_test(is_admin)
def assign_tutor(request):
    students = StudentProfile.objects.all()
    tutors = TutorProfile.objects.filter(approved=True)
    assignments = TutorAssignment.objects.all()

    if request.method == 'POST':
        student_id = request.POST['student_id']
        tutor_id = request.POST['tutor_id']
        student = get_object_or_404(StudentProfile, id=student_id)
        tutor = get_object_or_404(TutorProfile, id=tutor_id)

        # ✅ Prevent duplicate assignment
        if not TutorAssignment.objects.filter(student=student, tutor=tutor).exists():
            TutorAssignment.objects.create(
                student=student,
                tutor=tutor,
                assigned_by=request.user
            )

        return redirect('assign_tutor')

    return render(request, 'assign_tutor.html', {
        'students': students,
        'tutors': tutors,
        'assignments': assignments,
    })






# Admin things



@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.role == 'tutor':
        tutor_profile = getattr(user, 'tutorprofile', None)
        assignments = TutorAssignment.objects.filter(tutor=tutor_profile)
        context = {
            'user_role': 'Tutor',
            'profile': tutor_profile,
            'assignments': assignments,
        }
        return render(request, 'dashboard_tutor.html', context)

    elif user.role == 'student':
        student_profile = getattr(user, 'studentprofile', None)
        assignments = TutorAssignment.objects.filter(student=student_profile)
        context = {
            'user_role': 'Student',
            'profile': student_profile,
            'assignments': assignments,
        }
        return render(request, 'dashboard_student.html', context)

    elif user.role == 'admin':
        return render(request, 'dashboard_admin.html', {'user_role': 'Admin'})

    else:
        return render(request, 'dashboard_viewer.html', {'user_role': 'Viewer'})




@user_passes_test(is_admin)
def make_payment(request):
    if request.method == 'POST':
        form = TutorPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.approved_by = request.user
            payment.save()
            return redirect('payment_history')
    else:
        form = TutorPaymentForm()
    return render(request, 'make_payment.html', {'form': form})


@user_passes_test(is_admin)
def payment_history(request):
    payments = TutorPayment.objects.all().order_by('-payment_date')
    return render(request, 'payment_history.html', {'payments': payments})




@login_required
def edit_student_profile(request):
    if request.user.role != 'student':
        return redirect('dashboard')  # or show error

    profile = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentProfileEditForm(instance=profile)

    return render(request, 'edit_student_profile.html', {'form': form})



@require_POST
def remove_assignment(request, assignment_id):
    assignment = get_object_or_404(TutorAssignment, id=assignment_id)
    assignment.delete()
    return redirect('assign_tutor')




@login_required
def view_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    return render(request, 'view_tutor_profile.html', {'tutor': tutor})
