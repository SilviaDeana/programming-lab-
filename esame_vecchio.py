
# creazione della classe eccezione 
class ExamException(Exception):
    pass

# creazione della classe csv
class CSVTimeSeriesFile():

    # inizialliazione della classe 
    def __init__(self, name):
        self.name = name
    
    # definizione metodo "get data" che avra come risultato la lista "time_series" riempita
    def get_data(self):
        
        time_series = []  # lista vuota che conterra i valori del file 

        # controllo sul tipo del nome del file, deve essere una stringa
        #in caso contrario alzo un'eccezione         
        if(isinstance(self.name, str) != True):
            raise Exception('il nome nel file non e` una stringa')

        # apriamo il file e chiamiamo "time_series_file"
        try: 
            time_series_file = open(self.name, 'r')
        except:
            # se il file inserito non si chiama correttamente, verra alzata un'eccezione 
            raise Exception('file non esiste')
        
        # controlliamo che il file non sia vuoto, se vuoto viene alzata un'eccezione
        if len(time_series_file.readlines()) == 0:
            raise Exception('file vuoto')

        # il metodo ".readlines()" una volta completata la lettura del file, lo stesso si trova all'ultima linea, quindi per fare le operazioni richiestie torniamo alla prima linea
        # viene usato il metodo .seek() per non riaprire nuovamente il file 
        time_series_file.seek(0)
        # applichiamo un ciclo for per ogni riga del file 
        cont = 0   # variabile flag di controllo 
        for line in time_series_file:
            # slittiamo la linea del file "timer_series_file"
            # ricordiamo che "elem" e di tipo <list>
            elem = line.split(',')
            #print("elem:",elem)
            if elem[0] != 'epoch':
                try:
                    # proviamo a fare l'assegnazione delle variabili 
                    # ricordiamo che il tipo di "elem[0]" ed "elem[1]" e <str>
                    epoch = elem[0]              
                    temp = elem[1]  
                    #print("elem[0]:",elem[0],"elem[1]:",elem[1])
                except: 
                    print("una delle due variabili vuota",cont)
                    continue
               
                if cont == 1:
                    # primo giro
                    prec = epoch                  
                    try:
                        # provo a fare la conversione
                        #prec = round(float(prec))   
                        #epoch = round(float(epoch))
                        #temp = round(float(temp), 2)                           

                        prec = float(prec)
                        #prec = round(prec)
                        temp = float(temp)  
                        print(type(prec))
                        print(type(temp))             
                        # i tipi di "prec" e "epoch" sono stati silenzionamente covertiti in <int> mentre il tipo di "temp" in <float> con due cifre di apporosimazione dopo la virgola 
                        
                    except:
                        # stampiamo riga e il suo contenuto 
                        print("problema nel casting a riga", cont,"salto:",elem)  
                        continue              

                else:      
                    # siamo almeno al secondo giro     
                    epoch = elem[0]                    
                    try:
                        # provo a fare la conversione
                        #prec = round(float(prec))    
                        #epoch = round(float(epoch))
                        #temp = round(float(temp), 2) 
                        prec = float(prec)
                        print(type(prec))
                        #prec = round(prec)
                        temp = float(temp) 
                        print(type(temp))

                        # i tipi di "prec" e "epoch" sono stati silenzionamente covertiti in <int> mentre il tipo di "temp" in <float> con due cifre di apporosimazione dopo la virgola 
 
                    except:
                        # stampiamo riga e il suo contenuto 
                        print("problema nel casting a riga", cont,"la salto:",elem)
                        continue    

                    # controlliamo che non ci siano doppioni 
                    if epoch == prec:
                        # stampiamo riga e il suo contenuto 
                        print("prec:",prec,"- epoch:",epoch)
                        raise ExamException('due elementi sono uguali',"riga:",cont)

                    # controlliamo che l'ordine sia seguito    
                    elif prec > epoch:
                        # stampiamo riga e il suo contenuto 
                        print("prec:",prec,"- epoch:",epoch)
                        raise ExamException('due elementi non sono in ordine', "riga:",cont)                    

                time_series.append([epoch,temp])
                # l'append viene eseguito solamente nel caso la riga abbia passato tutti i controlli, quindi la lista risultante e pulita
                prec = epoch # aggiorniamo i contatori 
            cont = cont + 1  # aggiorniamo i contatori 

        # chiudo il file 
        time_series_file.close()
        for item in time_series:
            print(item)
        # il return della funzione "get_data" e la lista annidata "time series"
        return(time_series)

# la funzione "hourly_trend_changes" calcola separatamente i cambi di trend delle T
# ricordiamo che la lista "time_series" e una lista annidata, composta da due liste da un elemento ciascuna
def hourly_trend_changes(time_series):

    # dichiaro delle variabili di controllo 
    cont = 0          # contatore generale, del for 
    trend = 0         # variabile che andra a contenere i numeri di cambio di trend
    cont_ora = 0      # contatore delle ore che passano
    lista_trend = []  # lista annidata che conterra i trend e l'ora 

    # ciclo for che si applica alla lista "time_series"
    # ricordiamo che "time_series" e una lista annidata, costitita nella prima collona dagli epoch e nella seconda colonna dalle rilevazioni di temperatura
    for item in time_series:
        if (cont == 0):
            # siamo al primo giro 
            temp_prec = 0        # temperatura precedente
            temp_succ = item[1]  # temperatura sucessiva         
            epoch_prec = 0       # epoch precedente
            epoch_succ = item[0] # epoch sucessivo           
            delta_secondi = 0    # variabile che contiene l'intervallo in secondi tra l'epoch sucessivo e l'epoch precedente   
            cambio_ora = 0       # variabile di controllo 

        else:
            # siamo almeno al secondo giro 
            # assegnamo le variabili in modo da poter analizzare i valori corretti             
            temp_prec = temp_succ
            temp_succ = item[1]         
            epoch_prec = epoch_succ
            epoch_succ = item[0]       
            # calcoliamo il delta secondi             
            delta_secondi = epoch_succ - epoch_prec
            # calcoliamo il valore di "cambio_d'ora" e lo volutiamo 
            # la variabile "cambio_d'ora" serve per capire quando si passa all'ora successiva
            cambio_ora = cambio_ora + delta_secondi
            if (cambio_ora >= 3600): 
                # siamo in un'ora nuova, siccome "cambio d'ora" e una quantita di secondi maggiore ai secondi presenti in un'ora (3600)
                cambio_ora = 0
                cont_ora = cont_ora + 1
                lista_trend.append(trend) 
                # aggiungiamo gli elementi alla lista    
                trend = 0       
                if (epoch_succ == time_series[-1][0]):
                    # caso in cui l'ultima rilevazione registrata, appartiene ad un'ora nuova
                    if(temp_succ < temp_prec): 
                    # siamo nel caso di un cambio di trend
                        trend = trend + 1   
            
            else: 
                # siamo nella stessa ora
                # valutiamo le temperature
                if(temp_succ < temp_prec): 
                    # siamo nel caso di un cambio di trend
                    trend = trend + 1   

        cont = cont + 1

    # scrivo l'ultimo trend 
    cont_ora = cont_ora + 1
    #aggiungo l'ultima rilevazione alla lista     
    lista_trend.append(trend)   
    for item in lista_trend:
        print(item)
    return lista_trend

##################### chiamata delle funzioni ########################

time_series_file = CSVTimeSeriesFile(name = 'data.csv')
time_series = time_series_file.get_data()
time_series
hourly_trend_changes(time_series)