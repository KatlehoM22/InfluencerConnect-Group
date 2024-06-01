from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserTBL, Sponsor, Influencer, Platform
from django.http import HttpResponse

#############-For YouTube API-##################
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#############-For YouTube API-##################


import random
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

#############-sign up-##################
def signUp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        account_type = request.POST.get('type')

        if UserTBL.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, 'signin.html')

        new_user = UserTBL(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password), 
            account_type=account_type,
        )
        
        new_user.save()
        context = {'username': username, 'account_type': account_type}
        return render(request, 'platform.html', context)
    return render(request, 'signup.html')

#############-Sponser##################
def sponsorPlatform(request):
    if request.method == 'POST':
        content_category = request.POST.get('content_category')
        website = request.POST.get('website')
        username = request.POST.get('username')

        try:
            user = UserTBL.objects.get(username=username)
        except UserTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

        new_sponsor = Sponsor(
            user_id=user,
            content_category=content_category,
            website=website,
        )
        new_sponsor.save()

        messages.success(request, "Your account is set up successfully. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')

#############-Influecer-##################
def influencerPlatform(request):
    if request.method == 'POST':
        platform_name = request.POST.get('platform_name')
        platform_url = request.POST.get('platform_url')
        content_category = request.POST.get('content_category')
        username = request.POST.get('username')

        try:
            user = UserTBL.objects.get(username=username)
        except UserTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

        new_influencer = Influencer(
            user_id=user,
            content_category=content_category,
        )
        new_influencer.save()
   
        new_platform = Platform(
            influencer_id=new_influencer,
            platform_name=platform_name,
            platform_url=platform_url,
        )
        new_platform.save()

        messages.success(request, "Your account is active. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')

#############-log in-##################
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials, try again.')
                return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

#############-log out-##################
def signOut(request):
    logout(request)
    messages.success(request,'You have logged out')
    return redirect('index')

def sponser(request):
    return render(request, 'sponser.html')
    
#############-home-##################
@login_required(login_url='index')
def home(request):
  
    platforms = Platform.objects.select_related('influencer_id__user_id').all()
    youtube_data = []

    for platform in platforms:
        if platform.platform_name == 'YouTube':
            channel_id = platform.platform_url.split('/')[-1]
            # Get YouTube channel data
            channel_data = get_youtube_channel_data(channel_id)

            if channel_data:
                # Store channel data along with influencer ID
                youtube_data.append({
                    'influencer_id': platform.influencer_id_id,
                    'channel_data': channel_data
                })
    print("YouTube Data:", youtube_data)            
    context = {
        'username': request.user.username,
        'youtube_data': youtube_data
    }
    return render(request, 'home.html', context)


#############-Profile-##################
@login_required(login_url='index')
def profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        user.username = username
        user.email = email
        user.phone_number = phone_number
        
        user.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('home')
    else:
        return render(request, 'profile.html')
#############-Charting-##################


#############-Delete account-##################
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    else:
        return render(request, 'delete_account.html')

#############-Feaching YouTube data-##################
def get_youtube_channel_data(channel_id):

    # Initialize the YouTube Data API client
    api_key = 'AIzaSyDUU7CJNvqCpvkhlrieuZhQel8JpjIm7bI'
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Call the channels.list method to retrieve channel statistics
        details_response = youtube.channels().list(
            part='statistics,snippet,contentDetails',
            id=channel_id
        ).execute()

        channel = details_response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']
        uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

        channel_title = snippet.get('title', '')
        creation_date = snippet.get('publishedAt', '')
        views = statistics.get('viewCount', 0)
        subscribers = statistics.get('subscriberCount', 0)
        videos = statistics.get('videoCount', 0)

        # Initialize totals
        total_likes = 0
        total_comments = 0

        # Retrieve all videos in the uploads playlist
        next_page_token = None
        while True:
            playlist_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]

            # Get statistics for each video
            video_response = youtube.videos().list(
                part='statistics',
                id=','.join(video_ids)
            ).execute()

            for video in video_response['items']:
                video_stats = video['statistics']
                total_likes += int(video_stats.get('likeCount', 0))
                total_comments += int(video_stats.get('commentCount', 0))

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        channel_data = {
            'likes': total_likes,
            'views': views,
            'subscribers': subscribers,
            'comments': total_comments,
            'videos': videos,
            'channel_title': channel_title,
            'creation_date': creation_date
        }

        return channel_data
    
    except HttpError as e:
        print('An error occurred:', e)
        return None
    

