from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

Usuario = get_user_model()

class RegistroForm(forms.ModelForm):
    """Formulario de registro de usuarios con Bootstrap y validaciones mejoradas."""
    
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Debe contener al menos 8 caracteres, incluyendo letras y números.",
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Usuario
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_password1(self):
        """Verifica la seguridad de la contraseña."""
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8 or password1.isdigit():
            raise ValidationError("La contraseña debe tener al menos 8 caracteres y no ser solo números.")
        return password1

    def clean_password2(self):
        """Verifica que las contraseñas coincidan."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        """Guarda el usuario con la contraseña encriptada."""
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario


class LoginForm(AuthenticationForm):
    """Formulario de login con Bootstrap y autenticación mejorada."""
    
    username = forms.CharField(
        label="Usuario o Correo",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        """Autenticación con username o email en una sola consulta."""
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            try:
                user = Usuario.objects.get(email=username_or_email)
            except Usuario.DoesNotExist:
                try:
                    user = Usuario.objects.get(username=username_or_email)
                except Usuario.DoesNotExist:
                    raise forms.ValidationError("Las credenciales ingresadas no son válidas.")
            
            self.user_cache = authenticate(username=user.username, password=password)
            if not self.user_cache:
                raise forms.ValidationError("Las credenciales ingresadas no son válidas.")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class CambioPasswordForm(PasswordChangeForm):
    """Formulario para cambiar la contraseña con Bootstrap y validaciones mejoradas."""
    
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        error_messages={"required": "Debes ingresar tu contraseña actual."},
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Debe contener al menos 8 caracteres, incluyendo letras y números.",
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_new_password1(self):
        """Verifica que la nueva contraseña sea segura."""
        password1 = self.cleaned_data.get("new_password1")
        if len(password1) < 8 or password1.isdigit():
            raise ValidationError("La nueva contraseña debe tener al menos 8 caracteres y no ser solo números.")
        return password1

    def clean_new_password2(self):
        """Verifica que las nuevas contraseñas coincidan."""
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las nuevas contraseñas no coinciden.")
        return password2


class PerfilForm(forms.ModelForm):
    """Formulario para actualizar datos del usuario con validación de imagen."""

    imagen_perfil = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'imagen_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_imagen_perfil(self):
        """Verifica que la imagen subida sea de un formato permitido."""
        imagen = self.cleaned_data.get("imagen_perfil")
        if imagen:
            if not imagen.name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise ValidationError("Formato de imagen no permitido. Usa PNG, JPG o GIF.")
            if imagen.size > 2 * 1024 * 1024:  # 2 MB
                raise ValidationError("El tamaño de la imagen debe ser menor a 2MB.")
        return imagen
