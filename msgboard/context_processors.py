from .models import BadUser


def user_context(request):
    user = None
    user_id = None
    uid = request.COOKIES.get("user_id")

    if uid:
        user_id = uid.split("_")[0]
    
    if user_id:
        try:
            user = BadUser.objects.get(id=user_id)
        except BadUser.DoesNotExist:
            pass  # User not found, keep user as None
    if not user:
        return {"user": None}
    return {"user": user.username}  

