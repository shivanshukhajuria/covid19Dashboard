import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache
import json

import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.SUPERHERO]) #Creates an empty Dash screen with Superhero(Blue) theme

globaldeath=pd.read_csv('deathsglobal.csv')
confirmedcase=pd.read_csv('confirmglobal.csv')
recovered=pd.read_csv('recoveredglobal.csv')

finalconfirmeddata= confirmedcase.melt(id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date', value_name='total_confirmed_case') #a new column date is created and a column total_confirmed_case is created corresponding to it
finaldeathdata= globaldeath.melt(id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date', value_name='total_confirmed_deaths')
finalrecovereddata=recovered.melt(id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date', value_name='total_confirmed_recoveries')

mergesample2=pd.merge(finalconfirmeddata,finaldeathdata)
finalmergedata=pd.merge(mergesample2,finalrecovereddata) #merging the three data frames

finalmergedata['Date']=pd.to_datetime(finalmergedata['Date'],errors ='coerce') #converting date(string) to date

finalcov=finalmergedata.copy()
finalcov['Active_cases']=finalcov['total_confirmed_case']-finalcov['total_confirmed_deaths']-finalcov['total_confirmed_recoveries'] #Active_case = (confirm_case-deaths-recovered)
cov_matrix1=finalcov.groupby(['Date'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date
cov_matrix=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country

app.layout=dbc.Container([
	dbc.Row([ #created new row
		dbc.Col([ #created new column
            html.Div([ #creates new container
			html.Img(src="assets/covid.png",style={"width":400,"height":100}) #insert image
            ])
			],width=1)
		]),
	html.Hr(), #horizontal line
	dbc.Row([
		dbc.Col([
            dbc.Row([
            	html.Div(id="container1",children=[
            		html.H2('Global Cases',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}),
            		html.P(f"{cov_matrix1['total_confirmed_case'].iloc[-1]:,.0f}",style={'text-align':'center','color':'orange','font-size':25}), #prints total_confirmed_case
            		html.P("Latest cases :"+f"{cov_matrix1['total_confirmed_case'].iloc[-1]-cov_matrix1['total_confirmed_case'].iloc[-2]:,.0f}" +"----" +"ROC" '(' #new cases = total_confirmed_case today - total_confirmed_case yesterday
            			+str(round(((cov_matrix1['total_confirmed_case'].iloc[-1]-cov_matrix1['total_confirmed_case'].iloc[-2])/cov_matrix1['total_confirmed_case'].iloc[-2])*100,2))+'%)' # rate of change = (total_confirmed_case today - total_confirmed_case yesterday) / total_confirmed_case yesterday
            			,style={'text-align':'center','color':'orange'})
            		],style={'backgroundColor':'#1F2C56','height':140,'width':800,'margin-left':15})
            	]), 
            dbc.Row([
            	html.Div(id="container2",children=[
            		html.H2('Global Death',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}),
            		html.P(f"{cov_matrix1['total_confirmed_deaths'].iloc[-1]:,.0f}",style={'text-align':'center','color':'red','font-size':25}), #prints total_confirmed_death
            		html.P("Latest deaths :"+f"{cov_matrix1['total_confirmed_deaths'].iloc[-1]-cov_matrix1['total_confirmed_deaths'].iloc[-2]:,.0f}" +"----" +"ROC" '(' #new deaths = total_confirmed_deaths today - total_confirmed_deaths yesterday
            			+str(round(((cov_matrix1['total_confirmed_deaths'].iloc[-1]-cov_matrix1['total_confirmed_deaths'].iloc[-2])/cov_matrix1['total_confirmed_deaths'].iloc[-2])*100,2))+'%)' #rate of change = (total_confirmed_deaths today - total_confirmed_deaths yesterday) / total_confirmed_deaths yesterday
            			,style={'text-align':'center','color':'red'})
            		],style={'backgroundColor':'#1F2C56','height':140,'width':800,'margin-left':15,'margin-top':20})
            	]),
            dbc.Row([
                    html.Div(id="container3",children=[
                    html.H2('Global Recovered',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}),
            		html.P(f"{cov_matrix1['total_confirmed_recoveries'].iloc[-1]:,.0f}",style={'text-align':'center','color':'green','font-size':25}), #prints total_confirmed_recoveries
            		html.P("Latest Recoveries :"+f"{cov_matrix1['total_confirmed_recoveries'].iloc[-1]-cov_matrix1['total_confirmed_recoveries'].iloc[-2]:,.0f}" +"----" +"ROC" '(' #new recoveries = total_confirmed_recoveries today - total_confirmed_recoveries yesterday
            			+str(round(((cov_matrix1['total_confirmed_recoveries'].iloc[-1]-cov_matrix1['total_confirmed_recoveries'].iloc[-2])/cov_matrix1['total_confirmed_recoveries'].iloc[-2])*100,2))+'%)' #rate of change = (total_confirmed_recoveries today - total_confirmed_recoveries yesterday) / total_confirmed_recoveries yesterday
            			,style={'text-align':'center','color':'green'})
            		],style={'backgroundColor':'#1F2C56','height':140,'width':800,'margin-left':15,'margin-top':20})
            	]),
             dbc.Row([
                    html.Div(id="container4",children=[
                    html.H2('Global Active',style={'text-align':'center','color':'white','margin-top':8,'fontsize':30}), 
            		html.P(f"{cov_matrix1['Active_cases'].iloc[-1]:,.0f}",style={'text-align':'center','color':'#FFEF78','font-size':25}), #prints total_active_cases
            		html.P("Latest Recoveries :"+f"{cov_matrix1['Active_cases'].iloc[-1]-cov_matrix1['Active_cases'].iloc[-2]:,.0f}" +"----" +"ROC" '(' #new active_cases = total_active_cases today - total_active_cases yesterday
            			+str(round(((cov_matrix1['Active_cases'].iloc[-1]-cov_matrix1['Active_cases'].iloc[-2])/cov_matrix1['total_confirmed_recoveries'].iloc[-2])*100,2))+'%)'#rate of change = (total_active_cases today - total_active_cases yesterday) / total_active_cases yesterday
            			,style={'text-align':'center','color':'yellow'})
            		],style={'backgroundColor':'#1F2C56','height':140,'width':800,'margin-left':15,'margin-top':20})
            	])
			],width=3),

		dbc.Col([
			dbc.Row([
			html.Div([
			html.Div(["Select Country"],style={'color':'#8FC1D4','margin-bottom':10}),	
            dcc.Dropdown( #creates a dropdown to select country
            id='select_country',
            options=[{'label':c, 'value':c} for c in (cov_matrix['Country/Region'].unique())],
            value='India',
            multi=False,
            placeholder="CLICK-HERE",
            clearable=True,
            ),
            html.Div(id='dd-output-container')
            ],style={'margin-left':50}),
            ]),
            dbc.Row([
            	html.Div([
            		dcc.Graph(id='pie_chart', #creates pie chart to visualise active cases, deaths, recoveries
            			config={'displayModeBar':'hover'})
            		]
            		 ,style={'margin-left':50,'margin-top':20}),
            	])
			],width=5),

		dbc.Col([
             dbc.Row([
			html.Div([
				html.Img(src="assets/cov.jpg",style={"width":300,"height":200,'margin-left':70,'margin-top':0}) #insert image
				],style={'margin-left':10})

			]),
             dbc.Row([
		     	html.Div([
		     	html.P('Total New Cases  on ' + ' '  +str(cov_matrix['Date'].iloc[-1].strftime("%B %d %Y"))+' country specific',style={'color':'white','text-align':'center'}) #display last available date
		     		],style={'width':400,'margin-left':60,'height':50})
		     	],className='ml-10'),
                  dbc.Row([
                  	html.Div([
            	 dcc.Graph(id='newconfirmedcases', config={'displayModeBar': False}, #display newconfirmedcases
                        style={}
                ),
             dcc.Graph(id='newdeaths', config={'displayModeBar': False}, #display newdeaths
                        style={}
                ),
             dcc.Graph(id='newrecoveredcase', config={'displayModeBar': False}, #display newrecoveredcase
                        style={}
                ),
             dcc.Graph(id='newactivecase', config={'displayModeBar': False}, #display newactivecase
                        style={}
                )
            	],style={'margin-top':20})

            ],style={'margin-left':60})

              ]),
		],className="mt-5 mr-4"),

	dbc.Row([
    html.Div([
	dcc.Graph(id='line_chart') #line chart for daily confirmed cases
            		])
		],style={'padding-top':20}
		),
	dbc.Row([
		dbc.Col([
    html.Div([
	dcc.Graph(id='line_chart1') #line chart for daily recoveries
            ])
		],style={'padding-top':20}
		),
		]),

	dbc.Row([
	dbc.Col([
    html.Div([
	dcc.Graph(id='line_chart2') #line chart for daily deaths
            		])
		],style={'padding-top':20}
		),
	dbc.Col([
    html.Div([
	dcc.Graph(id='line_chart3') #line chart for daily active cases
  			])
		],style={'padding-top':20}
		)
		]),
	],fluid=True)

#daily confirmed cases graph
@app.callback(
Output('line_chart','figure'), #gives output to line chart
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_graph(v):
	cov=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	cov1=cov[cov['Country/Region']==v][['Country/Region','Date','total_confirmed_case']].reset_index() #date and confirmed cases for a certain country
	cov1['daily_based_confirm']=cov1['total_confirmed_case']-cov1['total_confirmed_case'].shift(1) #daily confirmed cases = total confirmed cases today - total confirmed cases yesterday
	return{
	'data':[go.Scatter(
		x=cov1[cov1['Country/Region']==v]['Date'], #date on x-axis
		y=cov1[cov1['Country/Region']==v]['daily_based_confirm'], #daily cases on y-axis
		mode='lines',
		line=dict(width=3,color='orange'),
		hoverinfo='text',
		hovertext=
		'<b>Date</b>: ' + cov1[cov1['Country/Region'] == v]['Date'].astype(str) + '<br>' +
                           '<b>Daily Confirmed</b>: ' + [f'{x:,.0f}' for x in cov1[cov1['Country/Region'] == v]['daily_based_confirm']] + '<br>')], #date and daily cases will be displayed on hovering over the graph
	'layout':go.Layout(
		plot_bgcolor='#1F2C56',
		paper_bgcolor='#1F2C56',
		title={
		'text':'Confirmed cases  :'+(v),
		'y':0.93,
		'x':0.5,
		'xanchor':'center',
		'yanchor':'top'
		},
		titlefont={
		'color':'white',
		'size':20

		},
		hovermode='x',
		xaxis=dict( #x-axis layout description
			title='<b>Date</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'

				)
			),
		yaxis=dict( #y-axis layout description
			title='<b>Cumulative Cases</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'

				)
			),
		legend={ #legend layout description
		'orientation':'h',
		'bgcolor':'#1F2C56',
		'xanchor':'center','x':0.5,'y':-0.3
		},
		font=dict(
			family='sans-serif',
			size=12,
			color='white'
			),
		)
	}

#daily recoveries graph
@app.callback(
Output('line_chart1','figure'), #gives output to line chart
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_graph(v):
	cov=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	cov1=cov[cov['Country/Region']==v][['Country/Region','Date','total_confirmed_recoveries']].reset_index() #date and confirmed recoveries for a certain country
	cov1['daily_based_confirm']=cov1['total_confirmed_recoveries']-cov1['total_confirmed_recoveries'].shift(1) #daily confirmed recoveries = total confirmed recoveries today - total confirmed recoveries yesterday

	return{
	'data':[go.Scatter(
		x=cov1[cov1['Country/Region']==v]['Date'], #date on x-axis
		y=cov1[cov1['Country/Region']==v]['daily_based_confirm'], #daily recoveries on y-axis
		mode='lines',
		line=dict(width=3,color='green'),
		hoverinfo='text',
		hovertext=
		'<b>Date</b>: ' + cov1[cov1['Country/Region'] == v]['Date'].astype(str) + '<br>' +
                           '<b>Daily Confirmed</b>: ' + [f'{x:,.0f}' for x in cov1[cov1['Country/Region'] == v]['daily_based_confirm']] + '<br>')], #date and daily recoveries will be displayed on hovering over the graph
	'layout':go.Layout(
		plot_bgcolor='#1F2C56',
		paper_bgcolor='#1F2C56',
		title={
		'text':'Confirmed Recoveries  :'+(v),
		'y':0.93,
		'x':0.5,
		'xanchor':'center',
		'yanchor':'top'
		},
		titlefont={
		'color':'white',
		'size':20

		},
		hovermode='x',
		xaxis=dict( #x-axis layout description
			title='<b>Date</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'
				)
			),
		yaxis=dict( #y-axis layout description
			title='<b>Cumulative Cases</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'

				)

			),
		legend={ #legend layout description
		'orientation':'h',
		'bgcolor':'#1F2C56',
		'xanchor':'center','x':0.5,'y':-0.3
		},
		font=dict(
			family='sans-serif',
			size=12,
			color='white'
			),
		)
	}

#daily deaths graph
@app.callback(
Output('line_chart2','figure'), #gives output to line chart
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_graph(v):
	cov=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	cov1=cov[cov['Country/Region']==v][['Country/Region','Date','total_confirmed_deaths']].reset_index() #date and confirmed deaths for a certain country
	cov1['daily_based_confirm']=cov1['total_confirmed_deaths']-cov1['total_confirmed_deaths'].shift(1) #daily confirmed deaths = total confirmed deaths today - total confirmed deaths yesterday

	return{
	'data':[go.Scatter(
		x=cov1[cov1['Country/Region']==v]['Date'], #date on x-axis
		y=cov1[cov1['Country/Region']==v]['daily_based_confirm'], #daily deaths on y-axis
		mode='lines',
		line=dict(width=3,color='red'),
		hoverinfo='text',
		hovertext=
		'<b>Date</b>: ' + cov1[cov1['Country/Region'] == v]['Date'].astype(str) + '<br>' +
                           '<b>Daily Confirmed</b>: ' + [f'{x:,.0f}' for x in cov1[cov1['Country/Region'] == v]['daily_based_confirm']] + '<br>')], #date and daily deaths will be displayed on hovering over the graph
		
	'layout':go.Layout(
		plot_bgcolor='#1F2C56',
		paper_bgcolor='#1F2C56',
		title={
		'text':'Confirmed Deaths  :'+(v),
		'y':0.93,
		'x':0.5,
		'xanchor':'center',
		'yanchor':'top'
		},
		titlefont={
		'color':'white',
		'size':20

		},
		hovermode='x',
		xaxis=dict( #x-axis layout description
			title='<b>Date</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'

				)
			),
		yaxis=dict( #y-axis layout description
			title='<b>Cumulative Cases</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'
				)
			),
		legend={ #legend layout description
		'orientation':'h',
		'bgcolor':'#1F2C56',
		'xanchor':'center','x':0.5,'y':-0.3

		},
		font=dict(
			family='sans-serif',
			size=12,
			color='white'
			),
		)
	}

# active cases graph
@app.callback(
Output('line_chart3','figure'), #gives output to line chart
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_graph(v):
	cov=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	cov1=cov[cov['Country/Region']==v][['Country/Region','Date','Active_cases']].reset_index() #date and active cases for a certain country
	
	return{
	'data':[go.Scatter(
		x=cov1[cov1['Country/Region']==v]['Date'], #date on x-axis
		y=cov1[cov1['Country/Region']==v]['Active_cases'], #daily active cases on y-axis
		mode='lines',
		line=dict(width=3,color='yellow'),
		hoverinfo='text',
		hovertext=
		'<b>Date</b>: ' + cov1[cov1['Country/Region'] == v]['Date'].astype(str) + '<br>' +
                           '<b>Daily Confirmed</b>: ' + [f'{x:,.0f}' for x in cov1[cov1['Country/Region'] == v]['Active_cases']] + '<br>')], #date and daily active cases will be displayed on hovering over the graph
		
	'layout':go.Layout(
		plot_bgcolor='#1F2C56',
		paper_bgcolor='#1F2C56',
		title={
		'text':'Active Cases  :'+(v),
		'y':0.93,
		'x':0.5,
		'xanchor':'center',
		'yanchor':'top'
		},
		titlefont={
		'color':'white',
		'size':20

		},
		hovermode='x',
		xaxis=dict( #x-axis layout description
			title='<b>Date</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'

				)


			),
		yaxis=dict( #y-axis layout description
			title='<b>Cumulative Cases</b>',
			color='white',
			showline=True,
			showgrid=True,
			showticklabels=True,
			linecolor='white',
			linewidth=2,
			ticks='outside',
			tickfont=dict(
				family='Arial',
				size=12,
				color='white'
				)
			),
		legend={ #legend layout description
		'orientation':'h',
		'bgcolor':'#1F2C56',
		'xanchor':'center','x':0.5,'y':-0.3
		},
		font=dict(
			family='sans-serif',
			size=12,
			color='white'
			),
		)
	}

# callback for new confirmed cases
@app.callback(
Output('newconfirmedcases','figure'), #outputs to newconfirmedcases
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_confirmed(v):
	cov_matrix2=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	no_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_case'].iloc[-1]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_case'].iloc[-2] #new cases = total_confirmed_case today - total_confirmed_case yesterday
	diff_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_case'].iloc[-2]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_case'].iloc[-3] #new cases yesterday = total_confirmed_case yesterday - total_confirmed_case day before yesterday
	
	return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=no_confirmed,
                    delta={'reference': diff_confirmed,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]}
            )],
            'layout': go.Layout(
                    title={'text':'New Confirmed Case',
                           'y': 0.87,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='orange'),
                    paper_bgcolor='#1F2C56',
                    plot_bgcolor='#1F2C56',
                    height=50)
            	}

#callback for new deaths
@app.callback(
Output('newdeaths','figure'), #outputs to newdeaths
Input('select_country','value') #takes input from dropdown menu (country selected)
	)

def update_confirmed(v):
	cov_matrix2=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	no_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_deaths'].iloc[-1]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_deaths'].iloc[-2] #new deaths = total_deaths today - total_deaths yesterday
	diff_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_deaths'].iloc[-2]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_deaths'].iloc[-3] #new deaths yesterday = total_deaths yesterday - total_deaths day before yesterday
	
	return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=no_confirmed,
                    delta={'reference': diff_confirmed,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]}
            )],
            'layout': go.Layout(
                    title={'text':'New Deaths',
                           'y': 0.87,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='orange'),
                    paper_bgcolor='#1F2C56',
                    plot_bgcolor='#1F2C56',
                    height=50)
           



            	}

#callback for new recoveries
@app.callback(
Output('newrecoveredcase','figure'), #outputs to newrecoveredcase
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_confirmed(v):
	cov_matrix2=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	no_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_recoveries'].iloc[-1]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_recoveries'].iloc[-2] #new recoveries = total_recoveries today - total_recoveries yesterday
	diff_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_recoveries'].iloc[-2]-cov_matrix2[cov_matrix2['Country/Region']==v]['total_confirmed_recoveries'].iloc[-3] #new recoveries yesterday = total_recoveries yesterday - total_recoveries day before yesterday
	
	return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=no_confirmed,
                    delta={'reference': diff_confirmed,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]}
            )],
            'layout': go.Layout(
                    title={'text':'New Confirmed Recoveries',
                           'y': 0.87,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='orange'),
                    paper_bgcolor='#1F2C56',
                    plot_bgcolor='#1F2C56',
                    height=50)
           



            	}

#callback for active cases
@app.callback(
Output('newactivecase','figure'), #outputs to newractivecase
Input('select_country','value') #takes input from dropdown menu (country selected)
	)

def update_confirmed(v):
	cov_matrix2=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	no_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['Active_cases'].iloc[-1]-cov_matrix2[cov_matrix2['Country/Region']==v]['Active_cases'].iloc[-2] #new active cases = total_active_cases today - total_active_cases yesterday
	diff_confirmed=cov_matrix2[cov_matrix2['Country/Region']==v]['Active_cases'].iloc[-2]-cov_matrix2[cov_matrix2['Country/Region']==v]['Active_cases'].iloc[-3]#new active cases yesterday = total_active_cases yesterday - total_active_cases day before yesterday
	
	return {
            'data': [ go.Indicator(
                    mode='number+delta',
                    value=no_confirmed,
                    delta={'reference': diff_confirmed,
                           'position': 'right',
                           'valueformat': ',g',
                           'relative': False,
                           'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20}},
                    domain={'y':[0,1], 'x':[0,1]}
            )],
            'layout': go.Layout(
                    title={'text':'New Confirmed Case',
                           'y': 0.87,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'},
                    font=dict(color='orange'),
                    paper_bgcolor='#1F2C56',
                    plot_bgcolor='#1F2C56',
                    height=50)
            	}

#callback for pie chart
@app.callback(
Output('pie_chart','figure'),  #outputs to pie_chart
Input('select_country','value') #takes input from dropdown menu (country selected)
	)
def update_graph(v):
	cov=finalcov.groupby(['Date','Country/Region'])[['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases']].sum().reset_index() #gives total cases, deaths, recoveries and active cases corresponding to each date for each country
	final_confirmed=cov[cov['Country/Region']==v]['total_confirmed_case'].iloc[-1] #total confirmed cases on the latest date
	final_death = cov[cov['Country/Region'] == v]['total_confirmed_deaths'].iloc[-1] #total confirmed deaths on the latest date
	final_recovered = cov[cov['Country/Region'] == v]['total_confirmed_recoveries'].iloc[-1] #total recovered cases on the latest date
	final_active = cov[cov['Country/Region'] == v]['Active_cases'].iloc[-1] #total active cases on the latest date

	colors=['orange','blue','green','#e55467'] #array for colors
	return {
		      'data':[go.Pie(
			   labels=['total_confirmed_case','total_confirmed_deaths','total_confirmed_recoveries','Active_cases'],
			   values=[final_confirmed,final_death,final_recovered,final_active],
			   marker=dict(colors=colors),
			   hoverinfo='label+value+percent',
			   textinfo='label+value',
			   textfont=dict(size=13),
			   hole=0.7,
			   rotation=45

			   )],
		      'layout': go.Layout(
	            plot_bgcolor='#1F2C56',
	            paper_bgcolor='#1F2C56',
	            hovermode='closest',
	            title={'text':'Total Cases : ' + (v),
	                   'y':0.93,
	                   'x':0.5,
	                   'xanchor':'center',
	                   'yanchor':'top'},
	            titlefont={'color':'white',
	                       'size':20},
	            legend={'orientation': 'h',
	                    'bgcolor': '#272b30',
	                    'xanchor': 'center',
	                    'x':0.5,
	                    'y':-0.07},
	            font=dict(
	                size=12,
	                color='white'
	            )
	        )
		}
if __name__ == '__main__':
    app.run_server(debug=True)
