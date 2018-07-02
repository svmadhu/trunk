import sys
import json
import pandas as pd
import numpy as np
import pandas_datareader.data as webdr
import requests
from datetime import date, datetime
import plotly.utils as putils
import plotly.plotly as py
import plotly.tools as tls
import plotly.figure_factory as FF
import plotly.graph_objs as go
import plotly.offline as pop
import flask
from flask import Flask, request, render_template, Markup
import dash
import dash_html_components as html
import dash_core_components as dcc
import stocks_for_prototype as sfp
from dash.dependencies import Input, Output
api_key='yRhCkqG4jVrioxN2DYtx'
app = Flask(__name__)

#@app.callback(Output('searchRes1', 'children'),
#              [Input('http://localhost/ticker/', 'search')])

@app.route('/stock', methods=['GET', 'POST']) 
def pandas_plot():
	ticker = request.args['ticker']
	ticker= str(ticker)
	start_date = '2016-01-01'
	end_date = date.today()
	start_dt_iex = date(2016, 1, 1)
	end_dt_iex=date(int(end_date.year), int(end_date.month), int(end_date.day))
	if ticker.upper() in sfp.list_of_stocks:
		findata = webdr.DataReader(ticker.lower(), 'morningstar', start_date, end_date)
		#findata = webdr.DataReader(ticker.upper(), 'iex', start_dt_iex, end_dt_iex)
	else:
		return "Ticker not in stock list for prototype"
	
	#	if findata.empty:
	#		findata = webdr.DataReader(ticker.upper(), 'iex', start_dt_iex, end_dt_iex)
	datelist= [ date(*map(int, (((str(x[1]).split(" "))[0]).split("-")))) for x in findata.index]
	MA50 = np.round((findata.Close).rolling(window = 50, center = False).mean(), 2)
	MA200= np.round((findata.Close).rolling(window = 200, center = False).mean(), 2)
	trace = go.Candlestick(
					x=datelist, 
					open=findata.Open, 
					high=findata.High, 
					low=findata.Low, 
					close=findata.Close,
					increasing=dict(line=dict(color= '#30bf77')),
                    decreasing=dict(line=dict(color= '#cd3637')),
					yaxis='y1')

	trace50d = go.Scatter(
					x=datelist,
					y=MA50, 
					name = ticker + '50day MA',
					line = dict(color = '#17BECF'),
					opacity = 0.8,
					yaxis='y1')
	trace200d = go.Scatter(
					x=datelist,
					y=MA200, 
					name = ticker + '200day MA',
					line = dict(color = '#7F7F7F'),
					opacity = 0.8,
					yaxis='y1')
				
	'''trace_high = go.Scatter(
					x=datelist,
					y=findata.High,
					name = ticker + ' High',
					line = dict(color = '#17BECF'),
					opacity = 0.8)



	trace_low = go.Scatter(
					x=datelist,
					y=findata.Low,
					name = ticker + ' Low',
					line = dict(color = '#7F7F7F'),
					opacity = 0.8)
	'''
	
	trace_vol = go.Bar(
					x=datelist,
					y=findata.Volume,
					name = ticker + ' Vol',
					marker = dict(color = '#d9d9f4'),
					#mode= 'markers',
					opacity = 0.8,
					yaxis='y2')


	data = [trace, trace50d, trace200d, trace_vol]

	layout = go.Layout(
		xaxis= dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
		),
		yaxis=dict(
			title= 'Price',
			side='left',
			spikedash='dash',
			),	
		yaxis2=dict(
			title='Volume',
			overlaying='y',
			side='right',
			spikedash='longdash',
			showgrid=True,
			)
		)
	
	#graphJSON=py.plot(fig1, config={"displayModeBar": False}, show_link=False, include_plotlyjs=False, output_type='div')
	#graphJSON=json.dumps(fig1,cls=putils.PlotlyJSONEncoder)
	#graphJSON1=json.parse(graphJSON)
	#graphJSON2 = requests.get(graphJSON)
	#graphJSON=json.dumps(fig1,cls=putils.PlotlyJSONEncoder)
	#return(py.plot(fig1 , filename='sv-cs', Validate=False))
	#plot_html = pop.plot(fig1, include_plotlyjs=False, output_type='div')

	fig1=go.Figure(data=data,layout=layout)
	graphJSON=json.dumps(fig1,cls=putils.PlotlyJSONEncoder)
	return render_template('index.html', graphJSON=graphJSON)
	
app.run(debug=True,port=5555)
