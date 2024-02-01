import json
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.utils.timezone import make_aware

# Path to the JSON file where user game access data is stored
temp_path = "media/tmp"
JSON_FILE_PATH = os.path.join(temp_path, "user_game_access.json")


def index(request):
    return render(request, "index.html")


# def home(request):
#     return render(request, "home.html", {"data": data})


data = [
    {"id": 1, "img_path": "/static/images/ludo.png", "game_title": "Ludo",
     "cards": [{"id": 1, "content": "500Rs"}, {"id": 2, "content": "100Rs"}, {"id": 3, "content": "200Rs"}],
     "playing_frequency": 3},
    {"id": 2, "img_path": "/static/images/carrom.jpeg", "game_title": "Carrom",
     "cards": [{"id": 1, "content": "100Rs"}, {"id": 2, "content": "1000Rs"}, {"id": 3, "content": "300Rs"}],
     "playing_frequency": 5},
    {"id": 3, "img_path": "/static/images/chess.jpeg", "game_title": "Chess",
     "cards": [{"id": 1, "content": "200Rs"}, {"id": 2, "content": "10Rs"}, {"id": 3, "content": "500Rs"}],
     "playing_frequency": 2},
]


def load_user_game_data():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'access_data': {}, 'history_data': {}}


def save_user_game_data(game_access_data, game_history_data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump({'access_data': game_access_data, 'history_data': game_history_data}, file)


@csrf_exempt
def scratch_details(request):
    if request.method == 'POST':
        decoded_data = json.loads(request.body)
        card_id = decoded_data.get('cardId')
        content = decoded_data.get('content')
        game_title = decoded_data.get('gameTitle')
        user_email = request.GET.get('email')

        if user_email:
            user_key = f"{user_email}_{game_title}"
            user_game_data = load_user_game_data()
            access_data = user_game_data.setdefault('access_data', {})

            # Check playing frequency based on cards scratched
            play_count = access_data.get(user_key, 0)
            clicked_game_data = next((x for x in data if game_title == x.get("game_title")), None)
            if clicked_game_data and play_count >= clicked_game_data['playing_frequency']:
                return JsonResponse(
                    {'status': 'error', 'message': f"You have reached the maximum playing frequency for {game_title}."})

            # Record the play in history data
            user_game_data.setdefault('history_data', {}).setdefault(user_email, []).append({
                'game_title': game_title,
                'played_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            })

            # Update user access data
            access_data[user_key] = play_count + 1
            save_user_game_data(access_data, user_game_data['history_data'])

            print(f"Card ID: {card_id}, Content: {content}, Game: {game_title}")

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def games(request, id=None):
    user_email = request.GET.get('email')
    user_game_data = load_user_game_data()

    if user_email:
        # Ensure 'access_data' and 'history_data' keys are present in user_game_data
        access_data = user_game_data.setdefault('access_data', {})

        if id:
            clicked_game_data = next((x for x in data if str(id) == str(x.get("id"))), None)

            if clicked_game_data:
                user_key = f"{user_email}_{clicked_game_data['game_title']}"
                last_accessed_at = access_data.get(user_key)

                if last_accessed_at is not None:
                    last_accessed_at = make_aware(timezone.datetime.fromtimestamp(last_accessed_at))
                    time_since_last_access = timezone.now() - last_accessed_at

                    if time_since_last_access.total_seconds() < 86400:
                        return render(request, 'access_denied.html', {'game_name': clicked_game_data['game_title'],
                                                                      'message': f"You cannot access the {clicked_game_data['game_title']} game at the moment. Please try again later."})

                # Check playing frequency
                play_count = access_data.get(user_key, 0)
                if play_count >= clicked_game_data['playing_frequency']:
                    return render(request, 'access_denied.html', {'game_name': clicked_game_data['game_title'],
                                                                  'message_freq': f"You have reached the maximum playing frequency for {clicked_game_data['game_title']}."})

                return render(request, "game.html", clicked_game_data)

    # Ensure 'access_data' key is present in user_game_data
    access_data = user_game_data.setdefault('access_data', {})

    game_context = [
        {"game_data": game, "played": f"{user_email}_{game['game_title']}" in access_data}
        for game in data
    ]
    return render(request, "games.html", {"game_context": game_context})


def game_history(request):
    user_email = request.GET.get('email')
    user_game_data = load_user_game_data()

    # Retrieve user's game history
    history_data = user_game_data.get('history_data', {}).get(user_email, [])

    # Group the history data by game_title
    grouped_history_data = {}
    for entry in history_data:
        game_title = entry['game_title']
        grouped_history_data.setdefault(game_title, []).append(entry)

    return render(request, "history.html", {"grouped_history_data": grouped_history_data, "history_data": history_data})
