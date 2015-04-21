from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from videos.views import VideoViewSet, GenderViewSet
from django.conf import settings
from django.conf.urls.static import static

# Serializers define the API representation/
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provides an easy way of automatically determining URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'genders', GenderViewSet)

urlpatterns = patterns('',
    # Examples:
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/token/auth$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/token/refresh$', 'rest_framework_jwt.views.refresh_jwt_token'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)