from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


bad_words = [ "abuse", "idiot","stupid","dumb","fool","nonsense","hate","kill","trash","ugly"]

class PostForm(forms.ModelForm):

    title = forms.CharField(required=False)
    content = forms.CharField(required=False)
    


    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:  # checks for None or empty string
            raise forms.ValidationError("Title cannot be empty")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:  # checks for None or empty string
            raise forms.ValidationError("Content cannot be empty")
        found_bad_words = []

        for word in bad_words:
            if word in content:
                found_bad_words.append(word)

        if len(found_bad_words)>0:
            raise forms.ValidationError(f"Content cannot contain foul word(s): {", ".join(found_bad_words)}")
        return content
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False) #not necessary

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "profile_picture"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email cannot be empty")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username cannot be empty")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if (first_name == ""):
            raise forms.ValidationError("First name cannot be empty")
        return first_name
    
    def clean_last_name(self):  
        last_name = self.cleaned_data.get("last_name")
        if  (last_name == ""):
            raise forms.ValidationError("Last name cannot be empty")
        return last_name
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile_picture = self.cleaned_data.get("profile_picture")

        if commit and profile_picture:
            # Assign uploaded pic to the profile created by signal
            user.profile.profile_picture = profile_picture
            user.profile.save()

        return user
    
class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 2,
        "placeholder": "Write a comment..."
    }))

    class Meta:
        model = Comment
        fields = ["content"]