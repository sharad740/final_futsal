from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        full_name = str(data.get("full_name"))
        batch = data.get("batch")
        
        f_name, *l_name = full_name.split(" ")
        user.first_name = f_name
        user.last_name = " ".join(l_name)

        user  = super(MyAccountAdapter, self).save_user(request, user, form, commit=True)
        user.profile.batch = batch
        user.profile.save()
        
        return user
