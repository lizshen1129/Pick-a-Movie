from graph import *

def get_inputs(request_form):
    l_type = ['Less than 1 hour', 'Less than 2 hours', 'Less than 3 hours', '3 hours and above']
    r_type = ['Below 8', '8-9', '9-10']
    c_type = ['R', 'PG-13', 'Approved', 'PG', 'Not Rated', 'G', 'Passed', 'TV-PG', 'Unrated', 'X', 'M', 'GP', 'TV-MA']
    not_check = ['from_year', 'to_year', 'Directors', 'Writers', 'Stars']
    from_year = request_form['from_year']
    to_year = request_form['to_year']

    directors = [dir.strip().lower() for dir in request_form['Directors'].split(',')]
    directors = None if directors == [''] else directors
    writers = [wri.strip().lower() for wri in request_form['Writers'].split(',')]
    writers = None if writers == [''] else writers
    stars = [star.strip().lower() for star in request_form['Stars'].split(',')]
    stars = None if stars == [''] else stars

    genres = []
    length = []
    rating = []
    classification = []
    for key in request_form.keys():
        if key in l_type:
            length.append(key)
        elif key in r_type:
            rating.append(key)
        elif key in c_type:
            classification.append(key)
        else:
            if key not in not_check:
                genres.append(key)
    input_dict = {'from_year': from_year, 'to_year': to_year, 'Directors': directors, 'Writers': writers, 'Stars': stars,
                  'Genres': genres, 'Length': length, 'Rating': rating, 'Classification': classification}
    return input_dict


def handle_single(feature_type, feature_content, graph):
    verts = graph.getVerts()
    for vert in verts:
        if vert.getValue() == 'Stanley Kubrick':
            if vert.getValue().lower() == feature_content.lower():
                print(vert.getFeature(), feature_type)

        if vert.getFeature() == feature_type and vert.getValue().lower() == feature_content.lower():
            return vert.getConnections()
    return []


def handle_years(from_year, to_year, graph):
    if from_year == '----':
        from_year = '1921'
    if to_year == '----':
        to_year = '2021'
    year_list = []
    if from_year == to_year:
        year_list = handle_single('Year', from_year, graph)
    else:
        from_year, to_year = min(from_year, to_year), max(from_year, to_year)
        for year in range(int(from_year), int(to_year) + 1):
            if handle_single('Year', str(year), graph):
                year_list += handle_single('Year', str(year), graph)
        year_list = list(set(year_list))
    return year_list


def handle_multiples_one_type(selected, feature_type, graph):
    union_list = []
    for single in selected:
        union_list += handle_single(feature_type, single, graph)
    if union_list:
        return list(set(union_list))


def handle_all_intersection(union_lists):
    intersection = [movie_id for movie_id in range(250)]  # all movies without conditions
    for union_list in union_lists:
        if not union_list:
            return None
        intersection = list(set(union_list) & set(intersection))
    if intersection:
        return intersection
