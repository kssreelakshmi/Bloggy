from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model for blog authors, readers, and OAuth-based logins.
    """

    # Basic Info
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    # Profile Details
    display_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # OAuth Info
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    oauth_id = models.CharField(max_length=200, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    # Author Stats
    total_posts = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    verified_author = models.BooleanField(default=False)

    # AI Preferences
    preferred_language = models.CharField(max_length=30, default='English')
    writing_style = models.CharField(
        max_length=50,
        choices=[
            ('formal', 'Formal'),
            ('informal', 'Informal'),
            ('creative', 'Creative'),
            ('technical', 'Technical'),
            ('funny', 'Funny'),
        ],
        default='formal'
    )
    ai_content_opt_in = models.BooleanField(default=True)
    theme_preference = models.CharField(max_length=20, default='light')

    # Activity Tracking
    last_seen = models.DateTimeField(auto_now=True)
    login_count = models.PositiveIntegerField(default=0)
    post_read_count = models.PositiveIntegerField(default=0)
    ai_generated_posts = models.PositiveIntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    # System Control
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Django flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def ban(self, reason=None):
        self.is_banned = True
        self.ban_reason = reason
        self.save()

    def unban(self):
        self.is_banned = False
        self.ban_reason = None
        self.save()


class OAuthAccount(models.Model):
    """Stores OAuth details for users who log in via Google, GitHub, etc."""
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oauth_accounts')
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    provider_user_id = models.CharField(max_length=200, unique=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    token_type = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')
        verbose_name = "OAuth Account"
        verbose_name_plural = "OAuth Accounts"

    def __str__(self):
        return f"{self.user.username} ({self.provider})"

    def is_expired(self):
        return self.expires_at and timezone.now() >= self.expires_at
