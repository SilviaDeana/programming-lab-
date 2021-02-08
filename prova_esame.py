class ExamException(Exception):
    pass

class CSVFile:

    def __init__(self, name):
        self.name = name
    
    def get_data(self):

        lista = []
        file = open('data.csv', 'r')
        cont = 0 
        prec = 0 

        for line in file:
            # nb elem e` una lista 
            elem = line.split(',')
            if elem[0] != 'epoch':
                try:     
                    epoch = elem[0]
                    temp = elem[1]
                    #print("sono qui")
                    lista.append([int(epoch), float(temp)])
                    for item in lista:
                        if cont == 0:
                            prec = 0 
                            epoch = item[0]
                        else: 
                            prec = epoch                  
                            epoch = item[0]
                            
                        print("epoch: {}".format(epoch))
                        print("prec: {}".format(prec)) 
                        cont = cont + 1      

                        if epoch > prec:
                            raise ExamException('due elementi non sono in ordine')
                            print("riga: {}".format(cont))
                        elif epoch == prec:
                            raise ExamException('due elementi sono uguali')
                            print("riga{} sono uguali:" .format(cont))


        # eccezzione per tipi diversi 
                except: 
                    if type(epoch) != int and type(temp) != float: 
                        print(" ho saltato riga: {}".format(cont))
                        pass

                    elif type(epoch) == None and type(temp) == None:
                            print("ho saltato riga: {}".format(cont))
                            pass 
                            



file = CSVFile('data.csv')
lista = file.get_data()