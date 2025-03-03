from flask import Flask, render_template, request
import pandas as pd
import pandas as pd

app = Flask(__name__)

# Load your data
data = pd.read_csv('kegg_pathways_afm.csv')

# Function to get unique pathways
def get_unique_pathways(df):
    pathways = df['Pathway IDs'].dropna().str.split(',').explode()
    unique_pathways = set(pathways.str.strip())
    return sorted(list(unique_pathways))

def filter_by_pathways(df, pathway_names):
    # Ensure 'Pathway IDs' is not NaN and is a string
    df['Pathway IDs'] = df['Pathway IDs'].fillna('').astype(str)
    
    # Filter rows where the pathway id contains the specified pathways
    filtered_df = df[df['Pathway IDs'].apply(lambda x: any(pathway in x for pathway in pathway_names))]
    
    # Return only the first three columns
    return filtered_df[['Entry', 'Reaction Name', 'Description']]

# Get unique pathways
unique_pathways = get_unique_pathways(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_pathways = request.form.getlist('pathways')
        filtered_df = filter_by_pathways(data, selected_pathways)
        return render_template('result.html', df=filtered_df.to_dict(orient='records'), pathways=selected_pathways)
    return render_template('index.html', pathways=unique_pathways)

if __name__ == '__main__':
    app.run(debug=True)