import googlemaps
import json
import time

gmaps = googlemaps.Client(key='')
search_query = 'alzabox'
center_location_of_search = '50.08804,14.42076' # 50.08804,14.42076 ... center of Prague
searched_radius = 10000 # 20000 ... 20 km


print('--------------- Found places ---------------')
places = gmaps.places(
    query=search_query, 
    location=center_location_of_search,
    radius=searched_radius,
    language='cs')

next_page_token = places.get('next_page_token', None)

places = [x['formatted_address'] for x in places['results']]

print('%s places found' % len(places))

places.append('Jateční 33a, 170 00 Praha-Holešovice-Praha 7')

while next_page_token:
    print('* next_page_token found')
    time.sleep(4) # google needs some time to make the token available

    places_next = gmaps.places(
        query=search_query, 
        location=center_location_of_search,
        radius=searched_radius,
        language='cs',
        page_token=next_page_token)

    print('Adding more places: %s' % len(places_next['results']))
    places.extend([x['formatted_address'] for x in places_next['results']])
    next_page_token = places_next.get('next_page_token', None)

print('\n'.join(places))


print('--------------- Distance matrix ---------------')
res_dict_dist = {}
res_dict_time = {}
true_locations_names_sorted = []
for place in places:
    print('=== %s' % place)

    try:
        dists = gmaps.distance_matrix([place], places, mode='driving', language='cs')
        #print(dists)
        true_locations_names_sorted = dists['destination_addresses']
        origin_addresses = dists['origin_addresses'][0]
        res_dict_dist[origin_addresses] = [x['distance']['value'] for x in dists['rows'][0]['elements']]
        res_dict_time[origin_addresses] = [x['duration']['value'] for x in dists['rows'][0]['elements']]
    except Exception:
        print('ERROR')
    
print('--------------- Print results ---------------')
print(res_dict_dist)
with open('res_dists.json', 'w', encoding='utf-8') as f:
    json.dump(res_dict_dist, f, indent=4, ensure_ascii=False)

print(res_dict_time)
with open('res_times.json', 'w', encoding='utf-8') as f:
    json.dump(res_dict_time, f, indent=4, ensure_ascii=False)

print(true_locations_names_sorted)
with open('true_locations_names_sorted.json', 'w', encoding='utf-8') as f:
    json.dump(true_locations_names_sorted, f, indent=4, ensure_ascii=False)