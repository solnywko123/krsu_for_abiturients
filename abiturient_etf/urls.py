"""abiturient_etf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.chat.views import ChatHistoryAPIView, ChatSendMessageAPIView, \
    FAQListAPIView
from apps.common.views import OnboardGetAPIView
from apps.professions.views import ProfessionListAPIView, \
    ProfessionRetrieveAPIView, ProfessionAdmissionRetrieveAPIView
from apps.users.views import AbiturientObtainAuthToken, \
    AbiturientRegistrationApplicationCreateAPIView, \
    AbiturientRegistrationApplicationConfirmAPIView, AbiturientProfileUpdateAPIView

admin.site.site_header = "Естественно-технический факультет"
admin.site.site_title = "Административная панель Естественно-технический факультет"
admin.site.index_title = "index Естественно-технический факультет"

schema_view = get_schema_view(
    openapi.Info(
        title="Естественно-технический факультет API",
        default_version='v1',
        description="RESTful API for Android mobile application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="toktosunalphadev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),

    path('api/v1/onboard/', OnboardGetAPIView.as_view()),
    path('api/v1/professions/', ProfessionListAPIView.as_view(), name='profession-list-url'),
    path('api/v1/professions/<int:pk>/', ProfessionRetrieveAPIView.as_view(), name='profession-retrieve-url'),
    path('api/v1/professions/<int:pk>/admission/', ProfessionAdmissionRetrieveAPIView.as_view(),
         name='profession-admission-url'),

    path('api/v1/abiturients/auth/', AbiturientObtainAuthToken.as_view(), name='abiturient-auth-url'),
    path('api/v1/abiturients/application/', AbiturientRegistrationApplicationCreateAPIView.as_view(),
         name='abiturient-registration-url'),
    path('api/v1/abiturients/application/confirmation/', AbiturientRegistrationApplicationConfirmAPIView.as_view()),
    path('api/v1/abiturients/profile/', AbiturientProfileUpdateAPIView.as_view()),

    path('api/v1/faq/', FAQListAPIView.as_view(), name='faq-list-url'),
    path('api/v1/chat/send/', ChatSendMessageAPIView.as_view(), name='chat-send-msg-url'),
    path('api/v1/chat/', ChatHistoryAPIView.as_view(), name='chat-history-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
