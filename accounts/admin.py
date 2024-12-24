import json

from django.contrib import admin,messages
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.query import QuerySet
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.urls import path
from django.db.models import Count
from dateutil.relativedelta import relativedelta # type: ignore
from django.core.serializers.json import DjangoJSONEncoder
from accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.

admin.site.site_header = "Micro Loan"
admin.site.site_title = "Microloan"
admin.site.index_title = "microloan"



User = get_user_model()


class UserAdmin(OSMGeoAdmin, BaseUserAdmin, admin.ModelAdmin,):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = (
        "telephone",
   
        "first_name",
        "last_name",
        "user_type",
        "is_active",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "user_type",
        "is_active",
   

    )
    fieldsets = (
        (None, {"fields": (
            "telephone",
            "user_type",
            "password"
        )}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active", 'user_permissions',

                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "telephone",
            "password1",
            "password2"
        )}),
    )
    search_fields = (
        "telephone",
        "first_name",
        "last_name",

    )

    ordering = ("first_name",)
    filter_horizontal = ()
    actions = [
        "disable_users",
        "enable_users",
    ]
   

    def disable_users(self, request, queryset):
        queryset.update(is_active=False)

    def enable_users(self, request, queryset):
        queryset.update(is_active=True)



    def has_add_permission(self, request) -> bool:
      
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            User.objects.filter().distinct().annotate(
                date=TruncDay("created_at__date"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"),
            User.objects.filter().distinct().annotate(
                date=TruncDay("created_at__date"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"),
        )
        if len(chart_data) == 2:
            data = {
                "users": list(chart_data[0])
            }
            as_json = json.dumps(data, cls=DjangoJSONEncoder)
        else:
            # Serialize and attach the chart data to the template context
            as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data", self.admin_site.admin_view(
                self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        period = request.GET.get("dataFrom")
        try:
            chart_data = self.chart_data(int(period))
        except ValueError:
            chart_data = self.chart_data(None)
        if len(chart_data) == 2:
            data = {
                "users": list(chart_data[0]),
                "owners": list(chart_data[-1])
            }

        return JsonResponse(data=data, safe=False)

    def delete_queryset(self, request, queryset: QuerySet):
        if len(queryset) > 1:
            messages.success(
                request, f"{len(queryset)} users' Jambo Shop account have been successfully deleted.")
        else:
            messages.success(
                request, f"{queryset[0]}'s Jambo Shop account has been successfully deleted.")
        return super().delete_queryset(request, queryset)

    def message_user(self, *args):
        pass

    def save_model(self, request, obj, form, change):
        if change:
            messages.success(
                request, f"{obj.telephone}'s profile updated successfully.")
        else:
            messages.success(
                request, "A user has been added successfully. Kindly proceed to update his/her profile.")
        super(UserAdmin, self).save_model(request, obj, form, change)

    def chart_data(self, period=None):
        if period == 0:
            return (
                User.objects.filter(created_on__date__month=(
                    now() - relativedelta(months=1)).month, created_on__date__year=now().year, restaurant_owner__isnull=True)
                .annotate(date=TruncDay("created_at"))
                .values("date").annotate(y=Count("id"))
                .order_by("-date").distinct(),
                User.objects.filter(created_on__date__month=(
                    now() - relativedelta(months=1)).month, created_on__date__year=now().year, restaurant_owner__isnull=False).distinct()
                .annotate(date=TruncDay("created_at"))
                .values("date").annotate(y=Count("id"))
                .order_by("-date")
            )
        elif period == 6:
            return (
                User.objects.filter(created_on__date__range=[
                                    (now() - relativedelta(months=1)) - relativedelta(months=6), now()], restaurant_owner__isnull=True).distinct()
                    .annotate(date=TruncDay("created_at"))
                    .values("date")
                    .annotate(y=Count("id"))
                    .order_by("-date"),
                User.objects.filter(created_on__date__range=[
                                    (now() - relativedelta(months=1)) - relativedelta(months=6), now()], restaurant_owner__isnull=False).distinct()
                    .annotate(date=TruncDay("created_at"))
                    .values("date")
                    .annotate(y=Count("id"))
                    .order_by("-date")
            )
        else:
            return (
                User.objects.filter().distinct().annotate(
                    date=TruncDay("created_on"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date"),
                User.objects.filter().distinct().annotate(
                    date=TruncDay("created_on"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
            )

admin.site.register(User, UserAdmin)



