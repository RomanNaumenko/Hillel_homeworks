from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from Coffee_night import models
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import connection

cursor = connection.cursor()


# Create your views here.
def route_filter(request, route_type=None, country=None, location=None):
    query_filter = []
    if route_type is not None:
        query_filter.append(f"route_type='{route_type}'")
    if country is not None:
        query_filter.append(f"country='{country}'")
    if location is not None:
        query_filter.append(f"loc='{location}'")

    filter_str = ' and '.join(query_filter)
    join_result = f"""SELECT Coffee_night_route.id, 
                             Coffee_night_route.country, 
                             Coffee_night_route.desc, 
                             Coffee_night_route.duration, 
                             Coffee_night_route.stop_point,
                             Coffee_night_route.loc, 
                             Coffee_night_route.route_type, 
                             start_point.name, destination_point.name FROM Coffee_night_route 
                             
                     JOIN Coffee_night_places as start_point
                     ON start_point.id = Coffee_night_route.start_point
                     
                     JOIN Coffee_night_places as destination_point
                     ON destination_point.id = Coffee_night_route.destination_point
                     
                     WHERE """ + filter_str

    cursor.execute(join_result)
    result = cursor.fetchall()

    # new_result = []
    # for itm in result:
    #     new_id = itm[0]
    #     new_country = itm[1]
    #     new_desc = itm[2]
    #     new_duration = itm[3]
    #     new_stop_point = itm[4]
    #     new_loc = itm[5]
    #     new_route_type = itm[6]
    #     new_start_point = itm[7]
    #     new_destination_point = itm[8]
    #
    #     buffer = {'id':new_id, 'country': new_country, 'desc': new_desc, 'duration': new_duration,
    #               'stop_point': new_stop_point, 'loc': new_loc, 'route_type': new_route_type,
    #               'start_point': new_start_point, 'destination_point': new_destination_point}

    new_result = [{'id': itm[0], 'country': itm[1], 'desc': itm[2], 'duration': itm[3], 'stop_point': itm[4],
                   'loc': itm[5], 'route_type': itm[6], 'start_point': itm[7], 'destination_point': itm[8]}
                  for itm in result]

    # result = models.Route.objects.raw(join_result + filter_str)
    # result = models.Route.objects.all().filter(**query_filter)
    return render(request, 'route_filter.html', {'result': new_result})


def route_details(request: object, id: object) -> object:
    route_result = models.Route.objects.all().filter(id=id)
    event_result = models.Event.objects.all().filter(id_route=id)
    event_result_list = [{'id': itm.id, 'id_route': itm.id_route, 'event_admin': itm.event_admin,
                          'approved_users': itm.approved_users, 'pending_users': itm.pending_users,
                          'start_data': itm.start_data, 'price': itm.price} for itm in event_result]

    return render(request, 'route_details.html', {'start_point': route_result[0].start_point,
                                                  'destination_point': route_result[0].destination_point,
                                                  'country': route_result[0].country, 'loc': route_result[0].loc,
                                                  'route_type': route_result[0].route_type,
                                                  'desc': route_result[0].desc,
                                                  'duration': route_result[0].duration, 'event': event_result_list})


def route_reviews(request, route_id):
    result = models.Review.objects.all().filter(id_route=route_id)
    return render(request, 'route_reviews.html', {'id_route': result[0].id_route, 'text': result[0].text,
                                                  'rating': result[0].rating})


def route_add(request):
    if request.user.has_perm('Coffee_night.add_route'):
        if request.method == 'GET':
            return render(request, 'add_route.html')
        if request.method == 'POST':
            start_point = request.POST.get('start_point')
            destination_point = request.POST.get('destination_point')
            country = request.POST.get('country')
            location = request.POST.get('loc')
            description = request.POST.get('desc')
            route_type = request.POST.get('route_type')
            duration = request.POST.get('duration')

            start_obj = models.Places.objects.get(name=start_point)
            dest_obj = models.Places.objects.get(name=destination_point)

            new_route = models.Route(start_point=start_obj.id, stop_point={}, destination_point=dest_obj.id,
                                     country=country, loc=location, desc=description, route_type=route_type,
                                     duration=duration)
            new_route.save()
        return HttpResponse('Route added successfully!')
    else:
        return HttpResponse('You have no permissions to add route')


def add_event(request, route_id):
    if request.user.has_perm('Coffee_night.add_event'):
        if request.method == 'GET':
            return render(request, 'add_event.html')

        if request.method == 'POST':
            date = request.POST.get('start_date')
            price = request.POST.get('price')
            new_event = models.Event(id_route=route_id, event_admin=1, approved_users={},
                                     pending_users={}, start_data=date, price=price)

            new_event.save()
            return HttpResponse('Event added successfully!')
    else:
        return HttpResponse('You have no permissions to add event')


def event_handler(request, event_id):  # Інформація про івент
    # result = models.Event.objects.all().filter(id=event_id)
    raw_query = f"""SELECT Coffee_night_event.id, start_point.name, destination_point.name,
                   Coffee_night_route.duration, Coffee_night_event.event_admin, Coffee_night_event.approved_users,
                     Coffee_night_event.pending_users, Coffee_night_event.start_data, Coffee_night_event.price
                        FROM Coffee_night_event 
                        
                        JOIN Coffee_night_route ON Coffee_night_event.id_route = Coffee_night_route.id
                        JOIN Coffee_night_places as start_point
                     ON start_point.id = Coffee_night_route.start_point
                     
                     JOIN Coffee_night_places as destination_point
                     ON destination_point.id = Coffee_night_route.destination_point
                     
                        WHERE Coffee_night_event.id = {event_id}"""
    cursor.execute(raw_query)
    result = cursor.fetchone()
    return render(request, 'event_handler.html', {'event_id': result[0], 'start_point': result[1], 'destination_point': result[2],
                                                    'duration': result[3], 'event_admin': result[4], 'approved_users': result[5],
                                                    'pending_users': result[6], 'start_data': result[7], 'price': result[8]})

    # return render(request, 'event_handler.html', {'event_id': result[0].id, 'start_point': result[0].start_point,
    #                                               'destination_point': result[0].destination_point,
    #                                               'duration': result[0].duration,
    #                                               'event_admin': result[0].event_admin,
    #                                               'approved_users': result[0].approved_users,
    #                                               'pending_users': result[0].pending_users,
    #                                               'start_data': result[0].start_data,
    #                                               'price': result[0].price})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'login.html')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('User is logged in!')
            else:
                return HttpResponse('No user')
    else:
        return HttpResponse('<a href="logout">logout</a>')


def user_registration(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'registration.html')
        if request.method == 'POST':
            user = User.objects.create_user(username=request.POST.get('username'),
                                            password=request.POST.get('password'),
                                            email=request.POST.get('email'),
                                            first_name=request.POST.get('first_name'),
                                            last_name=request.POST.get('last_name'))
            user.save()
            return HttpResponse('User created successfully!')
    else:
        return HttpResponse('<a href="logout">logout</a>')


def user_logout(request):
    logout(request)
    return redirect('/login')
