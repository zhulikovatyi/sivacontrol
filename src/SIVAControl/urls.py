from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, decorators, response
from videos.views import VideoViewSet, GenderViewSet, BannerWeightViewSet, AgeGroupViewSet, BannerWeightViewSet
from django.conf import settings
from django.conf.urls.static import static

# Serializers define the API representation/
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'first_name', 'last_name', 'is_superuser', 'date_joined')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @decorators.detail_route(methods=['get', ])
    def current(self, request):
        serializer = UserSerializer(request.user)
        return response.Response(serializer.data)

# Routers provides an easy way of automatically determining URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'genders', GenderViewSet)
router.register(r'agegroup', AgeGroupViewSet)
router.register(r'weight', BannerWeightViewSet)

user_current = UserViewSet.as_view({
    'get': 'current'
})

urlpatterns = patterns('',
    # Examples:
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/token/auth$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/token/refresh$', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^user/current$', user_current, name='user-current'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)