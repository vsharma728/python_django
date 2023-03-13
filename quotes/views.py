
import json
from django.shortcuts import render, redirect
import requests
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests
    import json
    
    #pk_50bcccda4993422f86b46658a5e002c4
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_50bcccda4993422f86b46658a5e002c4")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': "Enter a ticker symbol above to fetch stock details."})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Success! Stock has been added."))
            return redirect('add_stock')
    else:      
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_50bcccda4993422f86b46658a5e002c4")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'tickers':ticker, 'output': output})
    

def delete_stock(request, stock_id):
    
    item = Stock.objects.get(pk = stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted."))
    return redirect(delete_stocks)


def delete_stocks(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})

