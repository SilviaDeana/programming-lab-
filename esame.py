
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
            raise ExamException('il nome nel file non e` una stringa')

        # apriamo il file e chiamiamo "time_series_file"
        try: 
            time_series_file = open(self.name, 'r')
        except:
            # se il file inserito non si chiama correttamente, verra alzata un'eccezione 
            raise ExamException('file non esiste')
        
        # controlliamo che il file non sia vuoto, se vuoto viene alzata un'eccezione
        if len(time_series_file.readlines()) == 0:
            raise ExamException('file vuoto')

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
                    
                except: 
                    print("una delle due variabili vuota",cont)
                    continue
               
                if cont == 1:
                    # primo giro
                    prec = epoch                  
                    try:
                        # provo a fare la conversione
                        prec = round(float(prec))   
                        epoch = round(float(epoch))
                        temp = round(float(temp), 2)                           
      
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
                        prec = round(float(prec))    
                        epoch = round(float(epoch))
                        temp = round(float(temp), 2) 

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
        # il return della funzione "get_data" e la lista annidata "time series"
        return(time_series)

# la funzione "hourly_trend_changes" calcola separatamente i cambi di trend delle T
# ricordiamo che la lista "time_series" e una lista annidata, composta da due liste da un elemento ciascuna
def hourly_trend_changes(time_series):

    decrescente = 0
    crescente = 0
    cont = 1
    trend = -1
    lista_trend = []
    lista = []
    for item in time_series:
        cambio_ora = item[0] % 3600
        lista.append([item[0],item[1], cambio_ora])

    for item in lista:
        if item[2] == 0:
            # siamo in un'ora nuova
            if cont == 1:
                # primo giro, della prima ora 
                temp_corrente = item[1]
                trend = 0 
                decrescente,"cres:",crescente)

            else: 
                # siamo in un'ora nuova, ma non la prima, 
                # valuto se ce un cambiamento di trend rispetto all'ora precedente 
                # significa che la prima ora aveva solo una misurazione 
            
                lista_trend.append(trend) # append delle misurazioni precedenti
                trend = 0
                temp_prec = temp_corrente
                temp_corrente = item[1]   

                # rimane decrescente
                if temp_prec - temp_corrente > 0 and decrescente == 0 and crescente == 0:
                    decrescente = 1 
                    crescente = 0      

                # rimane crescente   
                elif temp_prec - temp_corrente < 0 and crescente == 0 and decrescente == 0:
                    crescente = 1
                    decrescente = 0

                # caso da crescente a decrescente
                elif temp_prec - temp_corrente > 0 and crescente == 1 and decrescente == 0:
                    trend = trend + 1 
                    decrescente = 1 
                    crescente = 0      

                # caso da decrescente a crescente     
                elif temp_prec - temp_corrente < 0 and decrescente == 1 and crescente == 0:
                    trend = trend + 1  
                    crescente = 1
                    decrescente = 0

        else:
            # siamo nella stessa ora 
            temp_prec = temp_corrente
            temp_corrente = item[1]

            # rimane decrescente
            if temp_prec - temp_corrente > 0 and decrescente == 0 and crescente == 0:
                decrescente = 1 
                crescente = 0      

            # rimane crescente   
            elif temp_prec - temp_corrente < 0 and crescente == 0 and decrescente == 0:
                crescente = 1
                decrescente = 0

            # caso da crescente a decrescente
            elif temp_prec - temp_corrente > 0 and crescente == 1 and decrescente == 0:
                trend = trend + 1 
                decrescente = 1 
                crescente = 0      

            # caso da decrescente a crescente     
            elif temp_prec - temp_corrente < 0 and decrescente == 1 and crescente == 0:
                trend = trend + 1  
                crescente = 1
                decrescente = 0

        cont = cont + 1
    lista_trend.append(trend)
    print(lista_trend)

    return lista_trend