#Importing required libraries.
from toolbox.p7_dashboard_fonctions_aide import*
from toolbox.p7_traitement_données_et_modélisation_fonctions_aide import*

#Flask:: App configuration.
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '75441f27d441f27567d441f2b6176a'

#Get current directory.
cd = os.getcwd()

#Load Data.
final_dict_df = load_object('static/data/final_dict_df.pkl')

#Load classifier.
classifier = load_object('static/classifiers/classifier_gd_sr.pkl')
classifier = classifier.best_estimator_


#formulaire d'appel à l'API (facultatif)
class SimpleForm(Form):
    form_id = TextField('id:', validators=[validators.required()])
    @app.route("/", methods=['GET', 'POST'])
    def form():
        form = SimpleForm(request.form)
        print(form.errors)

        if request.method == 'POST':
            form_id=request.form['id']
            print(form_id)
            return(redirect('credit/'+form_id)) 
    
        if form.validate():
            # Save the comment here.
            flash('Vous avez demandé l\'ID : ' + form_id)
            redirect('')
        else:
            flash('Veuillez compléter le champ.')
    
        return render_template('formulaire_id.html', form=form)


#Give name after selection.
@app.route('/credit/<id_client>', methods=['GET'])
def credit(id_client):
    
    #Obtain probability.
    prob = get_default_probability_client(get_client_row_from_df(int(id_client),final_dict_df['X_total']),classifier)
    risk = get_risk_classification_client(get_client_row_from_df(int(id_client),final_dict_df['X_total']),classifier)

    dict_client = {
        'risk' : int(risk),
        'def_prob' : round(float(prob), 3)
    }
    
    #return jsonify(dictionary_data), jsonify(dict_info_client), jsonify(dict_log)
    return jsonify(dict_client)
    
#lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
    
