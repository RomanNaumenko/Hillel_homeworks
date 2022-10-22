from django.http import HttpResponse, HttpResponseRedirect
from Coffee_night import models
from django.shortcuts import render


# Create your views here.
def route_filter(request, route_type=None, country=None, location=None):
    query_filter = {}
    if route_type is not None:
        query_filter['route_type'] = route_type
    if country is not None:
        query_filter['country'] = country
    if location is not None:
        query_filter['loc'] = location
    result = models.Route.objects.all().filter(**query_filter)
    # print(result)
    # filter_output = [{'Id': itm.id, 'Country': itm.country, 'Location': itm.loc, 'Type': itm.route_type,
    #                   'Start Point': itm.start_point, 'Destination Point': itm.destination_point,
    #                   "Duration": itm.duration, "Description": itm.desc} for itm in result]

    return render(request, 'route_filter.html', {'result': result})


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


def add_event(request, route_id):
    if request.method == 'GET':
        return render(request, 'add_event.html')
    if request.method == 'POST':
        date = request.POST.get('start_date')
        price = request.POST.get('price')
        new_event = models.Event(id_route=route_id, event_admin=1, approved_users={},
                                 pending_users={}, start_data=date, price=price)

        new_event.save()
    return HttpResponse('Event added successfully!')


def event_handler(request, event_id):  # Інформація про івент
    result = models.Event.objects.all().filter(id=event_id)
    return render(request, 'event_handler.html', {'event_id': result[0].id, 'id_route': result[0].id_route,
                                                  'event_admin': result[0].event_admin,
                                                  'approved_users': result[0].approved_users,
                                                  'pending_users': result[0].pending_users,
                                                  'start_data': result[0].start_data,
                                                  'price': result[0].price})
