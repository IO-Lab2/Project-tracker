#aborts images and media requests
async def abort_image_requests(request):
    if request.resource_type in ["image", "media"]:
        return True
    return False
