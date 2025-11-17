CustomUser.objects.filter(is_active=True)
CustomUser.objects.filter(email__endswith="@gmail.com")
CustomUser.objects.filter(city="Almaty") 
CustomUser.objects.exclude(city="Almaty")
CustomUser.objects.filter(salary__gt=500000)
CustomUser.objects.filter(department="IT", country="Kazakhstan") 
CustomUser.objects.filter(birth_date__isnull=True)
CustomUser.objects.filter(first_name__istartswith="A")
CustomUser.objects.count()
CustomUser.objects.order_by("-date_joined")[:20]
CustomUser.objects.values_list("city", flat=True).distinct()
CustomUser.objects.filter(department="Sales").count()
CustomUser.objects.filter(last_login__gte=Now() - timedelta(days=7))
CustomUser.objects.filter(Q(first_name__icontains="bek") | Q(last_name__icontains="bek"))
CustomUser.objects.filter(salary__gte=300000, salary__lte=700000)
CustomUser.objects.filter(department__in=["HR", "Finance", "IT"])
CustomUser.objects.values("department").annotate(total=Count("id"))
CustomUser.objects.values("department").annotate(total=Count("id")).order_by("-total")
CustomUser.objects.values("city").annotate(total=Count("id")).order_by("-total")[:5]
CustomUser.objects.filter(last_login__isnull=True)
CustomUser.objects.aggregate(Avg("salary"))
CustomUser.objects.aggregate(Max("salary"), Min("salary"))
CustomUser.objects.filter(phone__contains="+7")
CustomUser.objects.annotate(full_name=Concat(F("first_name"), Value(" "), F("last_name")))
CustomUser.objects.annotate(birth_year=ExtractYear("birth_date"))
CustomUser.objects.filter(birth_date__month=5)
CustomUser.objects.filter(role="manager", salary__gt=400000)
CustomUser.objects.filter((Q(role="employee") | Q(department="HR")))
CustomUser.objects.filter(is_active=True).values("city").annotate(total=Count("id"))
CustomUser.objects.order_by("date_joined")[:10]
CustomUser.objects.filter(city__startswith="A", salary__gt=300000)
CustomUser.objects.filter(Q(department__isnull=True) | Q(department=""))
CustomUser.objects.values("country").annotate(count=Count("id"), avg_salary=Avg("salary"))
CustomUser.objects.filter(is_staff=True).order_by("-last_login")
CustomUser.objects.exclude(email__contains="example.com")
#36
avg_salary=CustomUser.objects.aggregate(avg=Avg("salary"))["avg"]
CustomUser.objects.filter(salary__gt=avg_salary)
#37
CustomUser.objects.values("email").annotate(c=Count("id")).filter(c__gt=1)
#38
CustomUser.objects.annotate( salary_level=Case( When(salary__lt=300000,then=Value("low")), When(salary__lte=700000, then=Value("medium")), default=Value("high"), output_field=CharField(), ) ).order_by("salary_level")
CustomUser.objects.filter(date_joined__year=date.today().year)
CustomUser.objects.values("department").annotate(total_salary=Sum("salary"))
#41
CustomUser.objects.filter(department="IT", last_login__isnull=True)
#42
CustomUser.objects.filter(country="Kazakhstan").filter(Q(city__isnull=True) | Q(city=""))
CustomUser.objects.filter(birth_date__lt=date(1990,1,1), salary__isnull=False)
CustomUser.objects.annotate(years_since_joined=ExpressionWrapper(Now() - F("date_joined"), output_field= CharField()))
CustomUser.objects.filter(department="Sales", email__endswith="@gmail.com", salary__gt=350000)
CustomUser.objects.order_by("country", "-salary")
CustomUser.objects.values("role").annotate(c=Count("id")).filter(c__gt=100)



from django.forms import CharField
from django.db.models.functions import ExtractYear
from datetime import datetime, date, timedelta
from django.db.models.functions import Concat
from accounts.models import CustomUser
from django.db.models import Q, F
from django.db.models import (Avg, Sum, Max, Min, Count,Case, When, Value, IntegerField,)
from django.db.models import ExpressionWrapper
