from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Profile, PalRequest
from django.contrib.auth.decorators import login_required
from django.views.generic.list import View, ListView

User = get_user_model()

# Create your views here.

# @login_required
class ProfileListView(View):
    def get(self, request, *args, **kwargs):
        user_profiles_with_logged_in_user = Profile.objects.all()
        user_profiles_without_logged_in_user = Profile.objects.all().exclude(user=request.user)
        context = {
            'user_profiles': user_profiles_without_logged_in_user 
        }
        return render(request, "core/home.html", context)


def send_pal_request(request, id):
    """
        Creates a PalRequest instance
        **args**
            1. id -> The id of the user you're sending the pal request too
        **return**
            redirects to list of all users
    """
    # use request.user to confirm if logged in, cause a request  can only be sent by the logged-in user
    if request.user.is_authenticated:
        user_to_send_to = get_object_or_404(User, id=id)
        pal_request, created = PalRequest.objects.get_or_create(
                                        from_user=request.user,
                                        to_user=user_to_send_to                                        
                                                ) # use get_or_create for scenarios where you send but it already exists
        return HttpResponseRedirect(reverse("get_users_list"))    

def cancel_pal_request(request, id):
    """
        cancels a pal request you'd previously sent
        **args**
            1. id -> The id of the user you sent the request to
        **return**
            redirects to list of all users
    """
    # use request.user to confirm if logged in, cause the sent request  can only be cancelled by the logged-in user
    if request.user.is_authenticated:
        user_of_sent_pal_request = get_object_or_404(User, id=id)
        pal_request = PalRequest.objects.filter(
                                from_user=request.user,
                                to_user=user_of_sent_pal_request                                
                                        )
        pal_request_instance = pal_request.first()
        pal_request_instance.delete()
        return HttpResponseRedirect(reverse('get_users_list'))


def ignore_pal_request(request, id):
    """
        Ignores/deletes a pal request you dont want to accept
        **args**
            1. id -> The id of the user youre deleting the pal request of
        **return**
            redirects to list of all users
    """
    # NB, this doesnt require you be logged-in user like the previous three above so no need for request.user.is_authenticated
    # pal_request.from_user is other entity
    user_of_sent_pal_request = get_object_or_404(User, id=id)
    pal_request = PalRequest.objects.filter(
                            from_user=user_of_sent_pal_request,
                            to_user=request.user                                
                                    )
    pal_request_instance = pal_request.first()
    pal_request_instance.delete()
    return HttpResponseRedirect(reverse('get_users_list'))


def accept_pal_request(request, id):
    """
        Accepts pal request from other users of the app
        **args**
            1. id -> The id of the user youre accepting the pal request of
        **return**
            redirects to list of all users
    """
    # NB, this doesnt require you be logged-in user like the previous three above so no need for request.user.is_authenticated
    # pal_request.from_user is other entity
    user_of_sent_pal_request = get_object_or_404(User, id=id)

    pal_request = PalRequest.objects.filter(
                            from_user=user_of_sent_pal_request,
                            to_user=request.user                                
                                    )
    pal_request_instance = pal_request.first()
    # Enable the `pal_request_instance` object access the `to_user` attribute
    user_one = pal_request_instance.to_user
    print("User One: ", user_one)
    print("User One Profile: ", user_one.profile)
    user_two = user_of_sent_pal_request
    print("User Two: ", user_two)
    print("User Two Profile: ", user_two.profile)

    # add the user who sent the friend request to current user's list of pals
    user_one.profile.pals.add(user_two)     # link the user_one to the profile since User can forward relation to profile model                     
    user_two.profile.pals.add(user_one)     # link the user_two to the profile since User can forward relation to profile model                     
    pal_request_instance.delete()           # delete after youre done adding
    return HttpResponseRedirect(reverse('get_users_list'))


def fetch_profile(request, slug):
    """
        NB, acts like the detail view for a profile in the list of profiles
        Displays the profile details: shows sent_pal_request, received_pal_request & pals
        Also, if not on currently_logged_in_user's page: show `add pal`. if `add pal` is clicked,
        the button should show `pal_request_sent`
    """
    print(f"SLUG: {slug}")
    # profile clicked on from the list of profiles (may be currently-authenticated user or other users )
    profile_currently_clicked_on = Profile.objects.filter(
                                                    slug=slug
                                                        ).first()
    print(profile_currently_clicked_on)                                                        

    # get the user via that profile instance
    user_currently_clicked_on  = profile_currently_clicked_on.user
    print(user_currently_clicked_on)

    # show all friends of the currently_logged_in_user i.e, only profile model has attribute pals
    all_pals_of_clicked_on_profile = profile_currently_clicked_on.pals.all()

    # show sent friend requests using currently_logged_in_user
    all_sent_pal_requests = PalRequest.objects.filter(
                                        from_user=user_currently_clicked_on                            
                                                )   # we use user who's been clicked on instead of request.user cause 

    # show sent friend requests using currently_logged_in_user
    all_received_pal_requests = PalRequest.objects.filter(
                                        to_user=user_currently_clicked_on                            
                                                )
    print(f"ALL RECEIVED: {PalRequest.objects.all()}")                                                

    # This section shows if the user is not the currently_logged_in_user
    # (i.e, shows when the currently logged in user clicks on another's profile)
    button_status = None
    # if the user of that profile is not in the list of pals of the currently_logged_in_user, button status-> add pal
    if user_currently_clicked_on not in request.user.profile.pals.all():
        button_status = 'not_a_pal'

        # if currently_logged_in_user already sent a request to said profile
        print("Count: ",PalRequest.objects.filter(to_user=user_currently_clicked_on).count())
        if PalRequest.objects.filter(to_user=user_currently_clicked_on).count() == 1:
            button_status= 'pal_request_sent'
    else:
        button_status = 'pal'
    

    context = {
        "user_currently_clicked_on": user_currently_clicked_on,
        "all_pals_of_clicked_on_profile": all_pals_of_clicked_on_profile,
        "all_sent_pal_requests": all_sent_pal_requests,
        "all_received_pal_requests": all_received_pal_requests,
        "button_status": button_status,
    }                                    
    return render(request, "core/profile.html", context)