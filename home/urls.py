from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('main/', views.index, name='main'),
    path('about/', views.about, name='about'),
    path('caption/', views.caption, name='caption'),
    path('caption/<int:videoid>', views.generateCaption, name='genCaption'),
    path('editor/', views.editor, name='editor'),
    path('editor/<int:videoid>',views.videoEditor,name='videoEditor'),
    path('user/', views.user, name='user'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_us, name='logout'),
    path('signup',views.signup,name='signup'),
    path('addText/<int:videoid>',views.addText,name='addText'),
    path('deleteText/<int:textid>',views.deleteText,name='delText')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)