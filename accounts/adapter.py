from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        # Get social account data
        social_data = sociallogin.account.extra_data

        # Update user information if available
        if user:
            if 'name' in social_data:
                name_parts = social_data['name'].split(' ', 1)
                if len(name_parts) > 0:
                    user.first_name = name_parts[0]
                if len(name_parts) > 1:
                    user.last_name = name_parts[1]

            # Save user data
            user.save()


        return user