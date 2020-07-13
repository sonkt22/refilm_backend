from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.views import createUser, \
    getUserByToken, \
    updateUser,\
    sendRecoveryCode, \
    forgotPasswordUser,\
    uploadAvatar,\
    rankingUser

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', createUser, name='create_user'),
    path('me/', getUserByToken, name='get_user_by_token'),
    path('update/', updateUser, name='update_user'),
    path('send-recovery-code/', sendRecoveryCode, name='send-recovery-code'),
    path('forgot-password/', forgotPasswordUser, name='forgot-password-user'),
    path('upload-avatar/', uploadAvatar, name='upload-avatar'),
    path('rank/', rankingUser, name='rank_of_user'),

]