
# creazione della classe eccezzione 
class ExamException(Exception):
    pass

# creazione della classe csv
class CSVTimeSeriesFile():

    def __init__(self, name):
        self.name = name
    
    def get_data(self):
        
        time_series = []  # lista vuota che conterra i valori del file 
        cont = 0          # variabile flag di controllo 
        prec = 0          # variabile flag che contiene la data precedente 

        # controllo sul tipo del nome del file, deve essere una stringa
        if(isinstance(self.name, str) != True):
            raise Exception('il nome nel file non e` una stringa')

        # apriamo il file e chiamiamo "time_series_file"
        try: 
            time_series_file = open(self.name, 'r')
        except: 
            raise Exception('impossibile aprire il file')

        # applichiamo un ciclo for per ogni riga del file 
        for line in time_series_file:
            # il tipo di elem e "list" 
            # elem e una lista annidata, ogni riga e formata dagli epoch e dalla temperatura
            elem = line.split(',')
            # con questo if ci assicuriamo che nella prima colonna ci siano gli epoch
            if elem[0] != 'epoch':
                try:
                    # i tipi di epoch e temp sono stringa     
                    epoch = elem[0]
                    temp = elem[1]
                    # aggiungiamo i valori alla lista "time_series"
                    # e ci assicuriamo che siano dei tipi corretti
                    time_series.append([int(epoch), float(temp)])
                    # applichiamo un ciclo for per ogni "item" della lista "time_series"
                    # ricodiamo che item e a sua volta una lista, costituita dall'epoch e dalla temperatura 
                    for item in time_series:
                        if cont == 0:
                            # siamo al primo giro 
                            prec = 0 
                            # il tipo di epoch e int
                            epoch = item[0]
                        else: 
                            # facciamo in modo che "prec" assuma il valore che epoch aveva nel giro precedente 
                            prec = epoch                  
                            epoch = item[0]
                        # in ogni caso incrementiamo di 1 il contatore         
                        cont = cont + 1      

                        # alziamo le eccezzioni escusivamente in questi due casi:
                        if epoch > prec:
                            # se l'ordine cronologico tra gli epoch non e rispettato
                            raise ExamException('due elementi non sono in ordine')
                            print("riga: {}".format(cont))

                        elif epoch == prec:
                            # se sono presenti dei doppioni tra gli epoch
                            raise ExamException('due elementi sono uguali')
                            print("riga: {}".format(cont))

                # invece, ci limitiamo a saltare una riga nei seguenti casi         
                except: 
                    if type(epoch) != int and type(temp) != float: 
                        print(" ho saltato riga: {}".format(cont))
                        pass

                    elif type(epoch) == None and type(temp) == None:
                            print("ho saltato riga: {}".format(cont))
                            pass 


        # chiudo il file 
        time_series_file.close()
        # il return della funzione "get_data" e la lista annidata "time series"
        return(time_series)

# funzione separata che calcola il minimo, massimo e la media 
# la funzione "daily_stats" prende il argomento la lista "time_series" con i dati puliti
# siccome i controlli sono stati svolti precedentemente, nel corpo della funzione non sono necessari
def daily_stats(time_series):

    delta_secondi = 0   # variabile che conterra gli intervalli di tempo (in secondi) che occorono tra gli epoch (quindi tra le rilevazioni di temperatura)
    contatore = 0      # variabile flag di controllo 
    lista_ore = []     # lista che conterra gli interavalli di tempo, trasformati in ore 

    # applichiamo un ciclo for che scorre gli elementi della lista "time_series"
    # ricordiamo che la lista "time_series" e una lista annidata, costituita dagli epoch e dalle T
    # il tipo di "i" - come nei casi precedenti - e una lista 
    for i in time_series: 
        if contatore == 0:
            # quindi siamo al primo giro
            # i[0] permette di eccedere al primo valore della prima colonna della lista "time_series"
            contatore = contatore + 1
            precedente = i[0] 
            # aggiungiamo gli elementi alla lista_ore 
            # siccome delta_secondi in questo caso vale 0, non ha senso trasformarlo in secondi 
            lista_ore.append([i, int(delta_secondi)])
        
        else:
            # non siamo nel primo giro
            # calcoliamo l'intervallo dei secondi tra gli epoch 
            contatore = contatore + 1
            delta_secondi = i[0] - precedente
            precedente = i[0]
            # aggiungiamo gli elementi alla lista_ore 
            # trasformiamo il valore di della variabile "delta_secondi" in ore 
            lista_ore.append([i, int(delta_secondi / 3600)])


    lista_temp_giorno = [] # lista vuota, che sara il return della funzione (quindi conterra i valori delle temperature rilevate)
    conta = 0  # variabile flag di controllo 
    # imponiamo i valori di "massimo", "minimo" e "media" pari a  "-1", perche "0" muterebe i valori
    minimo = -1
    massimo = -1
    media = -1 

    # applichiamo un ciclo for alla lista "lista_ore"
    # ricordiamo che la lista "lista_ore" e una lista annidata, costiuita a dua volta da una lista che contiene gli epoch e una che contiene le temperature 
    # ricodiamo che il tipo di "i" e a sua volta una lista 
    for i in lista_ore:
        data = i[0][0]
        temp = i[0][1]
        #ora = i[1]

        # siccome per specifiche si considera una giornata costituita da 86400 secondi - costante - 
        # se il risultato dell'operazione "modulo" tra la data considerata per 86400 meno la stessa data e pari alla data di partenza, allora siamo passati ad un giorno nuovo 
        if (data - (data % 86400) == data):
            # siamo in un giorno nuovo 
            if minimo == -1:
                # entra solo la prima volta, dopo non era piu 
                # prima rilevazione, quindi imponiamo tutte le variabili alla temperatura segnata
                # questo permette di salvare i valori anche nel caso questa sia l'unica rilevazione di quella specifica giornata  
                minimo = temp
                massimo = temp
                media = temp
                conta = 1
            else:
                # cambio giorno
                # non prima rilevazione
                media = media / conta
                conta = 1
                # salva gli ultimi valori rilevati del giorno precedente
                # aggiungiamo i valori alla lista "lista_temp_giorno"
                lista_temp_giorno.append([(minimo), (massimo), (media)])
        else: 
            # stesso giorno
            # valuta le varie temperature specifiche del giro
            if temp < minimo:
                minimo = temp
            if temp > massimo:
                massimo = temp
            media = media + temp
            conta = conta + 1
        
    for i in lista_temp_giorno:
            print(i)
        
    return lista_temp_giorno   
               
