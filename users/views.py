from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
  """Register a new user."""
  if request.method != 'POST':
    # Display blank registration form.
    form = UserCreationForm()
  else:
    # Process completed form.

    # 2 form is an instance of UserCreationForm
    form = UserCreationForm(data=request.POST)

    if form.is_valid():
      # save username and password hash to db
      new_user = form.save()

      # 5 Log the user in - ask for two passwords
      authenticated_user = authenticate(
        username=new_user.username,
        password=request.POST['password1'])
      # 6 create valid session
      login(request, authenticated_user)

      # 7 redirect user to our home page
      return HttpResponseRedirect(
        reverse('learning_logs:index'))

  # not a POST request, render the login form
  context = {'form': form}
  return render(request,
                'users/register.html',
                context)


def logout_view(request):
  """Log the user out."""
  logout(request)

  return HttpResponseRedirect(
    reverse('learning_logs:index'))
