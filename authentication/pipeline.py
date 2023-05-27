from django.contrib.auth.models import User

def create_user(strategy, details, user=None, *args, **kwargs):
    """
    Creates a new user with the extracted extra_data from VK OAuth2.
    """
    if user is None:
        extra_data = details.get('extra_data', {})
        # Extract relevant fields from extra_data
        # Example: email, first_name, last_name
        email = extra_data.get('email')
        first_name = extra_data.get('first_name')
        last_name = extra_data.get('last_name')
        
        # Create a new user with the extracted data
        user = User.objects.create_user(username=email, email=email, password='')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    
    return {'user': user}