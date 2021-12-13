from flask import Flask, render_template, request
from handle_form import get_inputs, handle_years, handle_multiples_one_type, handle_all_intersection, result_dict
from load_save_graph import load_graph, save_graph
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pick_a_movie.html')

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    g = load_graph()
    save_graph(g)
    input_dict = get_inputs(request.form)
    year_list = handle_years(input_dict['from_year'], input_dict['to_year'], g)
    list_of_lists = [year_list]
    for feature in input_dict.keys():
        if feature != 'from_year' and feature != 'to_year':
            if input_dict[feature] and input_dict[feature] != []:
                feature_list = handle_multiples_one_type(input_dict[feature], feature, g)
                list_of_lists.append(feature_list)
    result_list = handle_all_intersection(list_of_lists)
    if not result_list:
        result_list = [random.randint(0, 249) for _ in range(9)]
        rand = True
    else:
        rand = False
    result = result_dict(result_list)
    return render_template('response.html', result=result, rand=rand, categ=None)

@app.route('/<categ>')
def category(categ):
    g = load_graph()
    save_graph(g)
    verts = g.getVerts()
    result_list = []
    try:
        year = int(categ)
        if year == 2000:
            year_list = handle_years('2000', '2010', g)
            categ = '2000~2010'
        elif year == 2011:
            year_list = handle_years('2011', '2021', g)
            categ = '2011~2021'
        else:
            year_list = handle_years(str(year), str(year + 9), g)
            result_list = year_list
            categ = categ[2:] + 's'
        result_list = year_list
    except:
        for vert in verts:
            if vert.getValue() == categ:
                result_list = vert.getConnections()
    if not result_list:
        result_list = [random.randint(0, 249) for _ in range(9)]
        rand = True
    else:
        rand = False
    result = result_dict(result_list)
    return render_template('response.html', result=result, rand=rand, categ=categ)


if __name__ == '__main__':  
    print('starting Flask app', app.name)
    app.run(debug=True)
