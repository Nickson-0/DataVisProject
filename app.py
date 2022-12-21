# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import json
import plotly.figure_factory as ff

app = Dash(__name__)


happiness_df_2019 = pd.read_csv("data/2019.csv")
happiness_df_2019['Country or region'] = happiness_df_2019['Country or region'].replace(['United States'],
                                                                                        'United States of America')

world_map_json = json.load(open("geojson/custom.geo.json", encoding="utf8"))

# choropleth_mapbox
fig1 = px.choropleth_mapbox(happiness_df_2019, geojson=world_map_json, color="Score",
                               locations="Country or region", featureidkey="properties.geounit",
                               mapbox_style="carto-positron", labels={"Score": "Happiness Score"},
                               title="2019 Happiness Report", center={"lat": 4.0383, "lon": 21.7587},
                               zoom=1.5, opacity=0.80)
fig1.update_layout(margin={"r": 40, "t": 40, "l": 40, "b": 20})

# correlation_heat_map
temp_df = happiness_df_2019
temp_df.drop("Overall rank", inplace=True, axis=1)

data = pd.DataFrame(temp_df.corr().values.tolist())
data = data.round(2).values.tolist()
fig2 = ff.create_annotated_heatmap(data, x=temp_df.corr().columns.tolist(),
                                  y=temp_df.corr().columns.tolist())
fig2.update_layout(title="Correlation Heatmap")

# distribution_of_happiness
fig3 = px.histogram(happiness_df_2019, x="Score", nbins=20, histnorm="percent",
                       labels={'Score': 'Happiness Score'},
                       opacity=0.80, title='Distribution of Happiness all over the world')

# bar_chart_no_distopia
fig4 = px.bar(happiness_df_2019.iloc[:60, :], x="Country or region", y=happiness_df_2019.columns.tolist()[3:],
                 title='Rankings of happiness explained by happiness factors (Top 60)',
                 labels={'variable': 'Happiness Score factors',
                         'value': 'Happiness Score'})
fig4.update_layout(xaxis_tickangle=-45)


# bar_chart_distopia
fig5 = px.bar(happiness_df_2019.iloc[:60, :], x="Country or region", y="Score",
                 title='Rankings of happiness (Top 60)',
                 labels={'value': 'Happiness Score'})
fig5.update_layout(xaxis_tickangle=-45)


app.layout = html.Div(children=[
    html.H1(
        children='World Happiness Visualisation 2019',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div(
        children='''
        DashBoard: An interactive dashboard on the data of happiness around the world.
    ''', style={
            'textAlign': 'center'
        }
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig1,
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig2,
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig3,
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig4,
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig5,
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
