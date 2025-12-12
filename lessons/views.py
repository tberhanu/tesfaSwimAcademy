from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserRequest

# Create your views here.

def home(request):
    user_email = request.session.get('user_email', None)
    return render(request, 'lessons/home.html', {'user_email': user_email})

def signup(request):
    user_email = request.session.get('user_email', None)
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone', '')
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')
        
        # Validation
        if not email or not name or not password:
            messages.error(request, 'Email, Name, and Password are required fields.')
            return render(request, 'lessons/signup.html', {'user_email': user_email})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'lessons/signup.html', {'user_email': user_email})
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'lessons/signup.html', {'user_email': user_email})
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'lessons/signup.html', {'user_email': user_email})
        
        # Create new user
        try:
            user = User(
                email=email,
                name=name,
                phone=phone if phone else None,
                country=country if country else None,
                city=city if city else None
            )
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration successful! Please sign in.')
            return redirect('signin')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'lessons/signup.html', {'user_email': user_email})
    
    return render(request, 'lessons/signup.html', {'user_email': user_email})

def signin(request):
    user_email = request.session.get('user_email', None)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email and Password are required.')
            return render(request, 'lessons/signin.html', {'user_email': user_email})
        
        # Check if user exists and verify password
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_email'] = user.email
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'lessons/signin.html', {'user_email': user_email})
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'lessons/signin.html', {'user_email': user_email})
    
    return render(request, 'lessons/signin.html', {'user_email': user_email})

def signout(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    messages.success(request, 'You have been signed out successfully.')
    return redirect('home')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'Admin' and password == 'Admin':
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'lessons/admin_login.html')

def admin_dashboard(request):
    if not request.session.get('admin_logged_in', False):
        return redirect('admin_login')
    
    users = User.objects.all().order_by('name')
    return render(request, 'lessons/admin_dashboard.html', {'users': users})

def admin_logout(request):
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    messages.success(request, 'You have been logged out.')
    return redirect('admin_login')

def about_us(request):
    user_email = request.session.get('user_email', None)
    return render(request, 'lessons/about.html', {'user_email': user_email})

def contact_us(request):
    user_email = request.session.get('user_email', None)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        # Validation
        if not name or not email or not message:
            messages.error(request, 'Name, Email, and Message are required fields.')
            return render(request, 'lessons/contact.html', {'user_email': user_email})
        
        # Email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'lessons/contact.html', {'user_email': user_email})
        
        # Create user request
        try:
            UserRequest.objects.create(
                name=name,
                email=email,
                phone=phone if phone else None,
                message=message
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'lessons/contact.html', {'user_email': user_email})
    
    return render(request, 'lessons/contact.html', {'user_email': user_email})
