from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('receptionist', 'Receptionist'),
        ('member', 'Member'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='users/%Y/%m', null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True)


    def __str__(self):
        return f"{self.username} - {self.role}"

    class Meta:
        abstract = True


# Bảng hội viên
class Member(User):
    payment_status = models.CharField(max_length=10, default='unpaid')


    def __str__(self):
        return f"{self.user.username} - {self.membership_type}"

# Bảng huấn luyện viên
class Trainer(User):
    SPECIALIZATIONS = [
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('swimming', 'Swimming'),
        ('dance', 'Dance'),
    ]

    specialization = models.CharField(max_length=20, choices=SPECIALIZATIONS)
    experience_years = models.IntegerField()


    def __str__(self):
        return f"{self.user.username} - {self.specialization}"

# Bảng nhân viên lễ tân
class Receptionist(User):
    WORK_SHIFTS = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    work_shift = models.CharField(max_length=10, choices=WORK_SHIFTS)


    def __str__(self):
        return f"{self.user.username} - {self.work_shift}"

# Bảng lớp học
class Class(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    max_members = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('completed', 'Completed')])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Bảng đăng ký lớp học
class Enrollment(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return f"{self.member.user.username} - {self.gym_class.name}"

# Bảng tiến độ tập luyện
class Progress(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    progress_note = models.TextField()


    def __str__(self):
        return f"{self.member.user.username} - {self.trainer.user.username}"

# Bảng lịch tư vấn riêng
class Appointment(BaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.member.user.username} - {self.date_time}"

# Bảng thanh toán
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('momo', 'Momo'),
        ('vnpay', 'VNPAY'),
        ('stripe', 'Stripe'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')])
    transaction_id = models.CharField(max_length=50, unique=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.user.username} - {self.status}"

# Bảng thông báo
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('class_schedule', 'Class Schedule'),
        ('promotion', 'Promotion'),
        ('reminder', 'Reminder'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

# Bảng tin nội bộ
class InternalNews(BaseModel):
    author = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

