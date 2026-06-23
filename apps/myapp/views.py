from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
def home(request):
    posts = PostFiles.objects.select_related('post').order_by('-post__created_at')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    current = timezone.now()

    for post in page_obj:
        post_created = post.post.created_at
        difference = current - post_created
        seconds = int(difference.total_seconds())

        # Define time thresholds
        minute = 60
        hour = minute * 60
        day = hour * 24
        week = day * 7

        # Assign the calculated string back to the object
        if seconds < 0:
            post.instagram_time = "now"
        elif seconds < minute:
            post.instagram_time = f"{seconds}s"
        elif seconds < hour:
            post.instagram_time = f"{seconds // minute}m"
        elif seconds < day:
            post.instagram_time = f"{seconds // hour}h"
        elif seconds < week:
            post.instagram_time = f"{seconds // day}d"
        else:
            post.instagram_time = f"{seconds // week}w"

    # Check if the request expects JSON (e.g., from fetch)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.headers.get('Accept', ''):
        posts_data = []
        for post in page_obj:
            posts_data.append({
                'username': post.post.user.username,
                'profile_pic': post.post.user.profile_pic.url,
                'file_url': post.file.url,
                'instagram_time': post.instagram_time
            })
        return JsonResponse({
            'posts': posts_data,
            'has_next': page_obj.has_next(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None
        })

    # Return standard HTML for regular page loads
    context = {'page_obj': page_obj, 'user': request.user}
    return render(request, 'home.html', context)