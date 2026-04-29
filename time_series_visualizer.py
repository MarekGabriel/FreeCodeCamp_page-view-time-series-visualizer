import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('https://raw.githubusercontent.com/freeCodeCamp/boilerplate-page-view-time-series-visualizer/refs/heads/main/fcc-forum-pageviews.csv',
                header = 0, parse_dates = True, index_col = 0)
#df.index


# Clean data
# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.

df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]
#df = df.copy()
# UWAGA - test_module.py nie przechodziło, pojawiał się jeden error. Mianowicie test przeczyszczonych danych sprawdza, ile jest rekordów w df, ale robi to 
# w ten sposób, że nakłada funkcję 'int()' na ramkę danych 'int(time_series_visualizer.df.count(numeric_only=True))'. W wersji pythona i jego bibliotek,
# które posiadam, ta komenda zwraca poprawną liczbę, ale o typie 'pandas.Series'. Niestety funkcja 'int()' wywala błąd (nie dopuszcza Series jako argument).
# Natomiast rozwiązanie umieściłem na githubie i podałem link do rozwiązania na FCC (tam automat sprawdza wszystko, ale na swojej wersji pythona etc.).


def draw_line_plot():
    # Draw line plot
    # Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". The title should be Daily
    # freeCodeCamp Forum Page Views 5/2016-12/2019. The label on the x axis should be Date and the label on the y axis should be Page Views.

    ### Metoda .subplots() w Matplotlib to podstawowy sposób tworzenia wykresów — zwraca jednocześnie figurę (Figure) i osie (Axes),
    ### na których rysujemy dane.
    ### Składnia: import matplotlib.pyplot as plt
    ###           fig, ax = plt.subplots(nrows = None, ncols = None, figsize = (None, None), share x= True, sharey = True)
    ### Parametry:
    ### figsize - rozmiar wykresu
    ### sharex, sharey - współdzielenie osi
    ### nrows, ncols - liczba wykresów wierszowo i kolumnowo
    ### UWAGA - .subplots() jest lepsze niż .plot(), bo łatwo robi się więcej wykresów i jest nad nimi lepsza kontrola (object-oriented)
    
    #stworzenie fizycznej kopii podstawowej ramki danych
    df_copy_for_plot = df.copy()
    
    #przykład z FCC ma rozdzielczość 3200x1000
    fig, axis = plt.subplots(nrows = 1, ncols = 1, figsize = (32,10))
    axis.plot(df_copy_for_plot, 'r')
    axis.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    axis.set_xlabel('Date')
    axis.set_ylabel('Page Views');


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    #stworzenie fizycznej kopii podstawowej ramki danych
    df_copy = df.copy()
    
    ##grupowanie po roku i miesiącu (nr m-ca oraz jego nazwa) i wyznaczanie dla każdej grupy średniej ilości odwiedzin strony www
    #df_bar = df_copy.groupby([df_copy.index.year, df_copy.index.month, df_copy.index.month_name()])['value'].mean().to_frame()
    ##zmiana nazw Multiindex-u (żeby nie było powtórzeń)
    #df_bar.index.names = ['Years', 'Months_no', 'Months']
    ##przeniesienie indeksu do kolumn w ramce danych
    #df_bar.reset_index(inplace = True)
    
    #wyciągnięcie roku z indeksu daty i dodanie jako nowa kolumna 
    #UWAGA - wyłącznie dla przypadku indeksu nie trzeba stosować dodatkowo "akcesora" .dt (np. 'df_copy.index.dt.year')
    df_copy['Years'] = df_copy.index.year
    #wyciągnięcie nr miesiąca z indeksu daty i dodanie jako nowa kolumna
    #df_copy['Months_no'] = df_copy.index.month
    #wyciągnięcie miesiąca z indeksu daty i dodanie jako nowa kolumna
    df_copy['Months'] = df_copy.index.month_name()

    #grupowanie po roku i miesiącu (nr m-ca oraz jego nazwa) i wyznaczanie dla każdej grupy średniej ilości odwiedzin strony www
    #parametr 'as_index = False' powoduje, że indeks w zgrupowanej ramce danych nie staje się multiindeksem (rok,m-c)
    df_bar = df_copy.groupby(['Years', 'Months'], as_index=False)['value'].mean()#.to_frame()

    # wzorzec na kolejność wyświetlania m-cy na wykresie
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    #dodatkowe zabiegi z indeksami, ażeby w zgrupowanych danych otrzymać m-ce z 2016, które nie miały danych (styczeń-kwiecień)
    years = df_bar['Years'].unique()
    full_index = pd.MultiIndex.from_product([years, months_order], names=['Years', 'Months'])
    df_bar = df_bar.set_index(['Years', 'Months']).reindex(full_index).reset_index()
    
    #wstawienie wartości 0 (zamiast występujących NaN) dla brakujących m-cy
    df_bar.fillna(0, inplace = True)

    # Draw bar plot
    #przykład z FCC ma rozdzielczość 1500x1300
    fig, axis = plt.subplots(nrows = 1, ncols = 1, figsize = (15,13))

    #wyznaczenie legendy (nazw miesięcy) posortowanej chronologicznie
    #print(df_bar.sort_values('Months_no')['Months'].unique())

    ### seaborn.barplot() - dla każdej kategorii: a.zbiera dane, b.liczy statystykę (domyślnie średnią), c.rysuje słupek o tej wysokości, 
    ### d.opcjonalnie dodaje error bars (np. przedziały ufności)
    ### Składnia: sns.barplot(x = None, y = None, data = DataFrame, hue = None, hue_order = , palette = , estimator = , order = , ax = )
    ### x, y - kolumny z ramki danych, które "wejdą" na osie
    ### hue - kolumna z ramki danych, która podzieli wykres na serie
    ### hue_order - ustalona kolejność wyświetlania serii (podawana jako lista stringów)
    ### palette - paleta barw dla różnych serii (np. tab10 to podstawowa paleta z matplotlib)
    ### estimator - metoda agregacji danych, domyślnie to średnia, ale można zmieniać na np.sum/np.median z biblioteki NumPy
    ### order - kolejność wyświetlania danych na osi X (podana jako lista)
    ### ax - wskazanie, gdzie (tj. na jakich osiach) ma zostać narysowany wykres

    # kolumnę 'Months' zamieniamy na tzw. kolumnę kategorii (generalnie przyspiesza to operacje na niej, ale też pozwala ustalić 
    # np. kolejność wyświetlania i wtedy: January < February < March < ... < December
    df_bar['Months'] = pd.Categorical(df_bar['Months'], categories = months_order, ordered = True)
    
    #axis = sns.barplot(x = 'Years', y = 'value', hue = 'Months', hue_order = df_bar.sort_values('Months_no')['Months'].unique(), 
    #                   palette = 'tab10', errorbar = None, data = df_bar)
    # alternatywnie można najpierw wywołać metodę .barplot() i jako jeden z parametrów wskazać, gdzie ma zostać narysowany wykres (na jakich osiach)
    sns.barplot(x = 'Years', y = 'value', hue = 'Months', hue_order = months_order, #df_bar.sort_values('Months_no')['Months'].unique(), 
                palette = 'tab10', errorbar = None, data = df_bar, ax = axis, legend = False)
    axis.set_ylabel('Average Page Views')
    # UWAGA - w podejściu bez atrybutu 'legend = False' rysowałem poprawny wykres, ale testy nie przechodziły (do prostokątów na wykresie zaliczało się
    # 12 kolejnych z generowanej na podstawie 'hue' legendy. W związku z tym wyłączyłem automatyczną legendę na rzecz tej poniżej:
    plt.legend(months_order, title = 'Months');

    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    ### .dt.strftime('%b') w Pandas służy do formatowania dat jako tekstu. Zamienia datę na string i formatuje wg wzorca '%b'.
    ### %b - skrócona nazwa miesiąca
    ### Alternatywnie zamiast pętli for jak wyżej można tak (przy czym .dt to tzw. "akcesor" do danych typu 'date'):
    #df_box['date'].dt.strftime('%b')
    #df_box['date'].dt.year
    ### UWAGA - używałem tego już wcześniej przy funkcji draw_bar_plot(), ale tam wyciągając składowe daty z indeksu nie trzeba używać .dt !!!
    
    #dodałem nr miesiąca, żeby potem użyć tego do ustalenia hue_order na boxplocie
    df_box['Month_no'] = df_box['date'].dt.month

    
    # Draw box plots (using Seaborn)
    #przykład z FCC ma rozdzielczość 2880x1080
    fig, [ax1, ax2] = plt.subplots(nrows = 1, ncols = 2, figsize = (28,10))

    ### seaborn.boxplot() - rysowanie wykresu pudełkowego, czyli wizualizacja, jak wartości są rozłożone w danej kategorii.
    ### Dla każdej grupy danych rysuje „pudełko”: linia w środku → mediana, dolna krawędź pudełka → 25 percentyl (Q1), 
    ### górna krawędź → 75 percentyl (Q3), „wąsy” (whiskers) → zakres danych (bez outlierów), kropki poza → wartości odstające (outliers)
    ### Składnia: sns.boxplot(x = None, y = None, data = DataFrame, hue = None, hue_order = , palette = , order = , ax = , legend = )
    ### x, y - kolumny z ramki danych, które "wejdą" na osie
    ### hue - kolumna z ramki danych, która podzieli wykres na serie
    ### hue_order - ustalona kolejność wyświetlania serii (podawana jako lista stringów)
    ### palette - paleta barw dla różnych serii (np. tab10 to podstawowa paleta z matplotlib)
    ### order - kolejność wyświetlania danych na osi X (podana jako lista)
    ### ax - wskazanie, gdzie (tj. na jakich osiach) ma zostać narysowany wykres
    ### legend - domyślnie True, ale można ukryć legendę ustawiając False
    ### UWAGA - palette już od wersji v.14 Seaborn będzie działać wyłącznie z hue, dlatego jeżeli nie mamy serii danych, to żeby uzyskać różne kolory 
    ### boxplotów "sztucznie" pod hue trzeba podstawić kolumnę, która przekazana jest jako x, a także ustawić legend = False.

    # UWAGA - rysując boxploty (kopod niżej):
    # sns.boxplot(x = 'Year', y = 'value', data = df_box, ax = ax1, palette = 'tab10')
    # dostałem komunikat: Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0. Assign the `x` variable to `hue` 
    #                     and set `legend=False` for the same effect.
    #                     sns.boxplot(x = 'Year', y = 'value', data = df_box, ax = ax1, palette = 'tab10')
    
    #ustawienie stylu rysowanych outlierów na boxplocie
    flierprops = dict(marker = 'd', markersize = 3, markerfacecolor='black')
    sns.boxplot(x = 'Year', y = 'value', data = df_box, ax = ax1, palette = 'tab10', hue = 'Year', legend = False, flierprops = flierprops)
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)');
    
    #print(df_box.sort_values('Month_no')['Month'].unique())
    sns.boxplot(x = 'Month', y = 'value', data = df_box, ax = ax2, order = df_box.sort_values('Month_no')['Month'].unique(), 
                hue = 'Month', legend = False, flierprops = flierprops)#, palette = 'pastel')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)');


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
