from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


# Create your models here.
class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    slug    = models.SlugField(max_length=255, blank=True, null=True)
    pals    = models.ManyToManyField(User, blank=True, related_name="pals")

    def get_number_of_pals(self):
        return self.pals.all().count()

    def get_absolute_url(self):
    	return "/{}".format(self.slug)

    def __str__(self):
        return self.user.username


def post_save_create_profile_receiver(sender, instance, created, *args, **kwargs):
    """Once user is created, a profile will also be created"""
    if created:
        print("<< CREATING PROFILE FOR USER >>")
        print("Instance: ", instance)
        slug=instance
        try:
            profile = Profile.objects.create(user=instance)
            profile.slug=slug
            print('profile.slug: ', profile.slug)
            profile.save()
        except Exception as e:
            pass

post_save.connect(receiver=post_save_create_profile_receiver, sender=User)


class PalRequest(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)
    

    