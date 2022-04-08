import tkinter
from tkinter import ttk
import center_tk_window
import time
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import qrcode


def introducirReceta():                 #Mete una receta
    aux1=cajaTextoTitulo.get()
    aux2= cajaTextoIngredientes.get("1.0","end")
    if aux1 != "" and aux2 != "" and aux2 != '' and aux2 != '' and aux2 != "\n" and aux2 != " " and aux1 != " " and aux1 != "\n" and len(aux1.replace(" ",""))!=0 and len(aux2.replace(" ",""))!=2:
        recetas[aux1]=aux2
        etiquetaComprobacion["text"] = "RECETA INTRODUCIDA"
        ventana.after(5000, quitarComprobacion)

def meterEnLista(event=None):
    listaBuscar.delete(0,tkinter.END)
    elAux=recetas.items()
    for t,i in elAux:
        if cajaTextoBuscar.get().lower() in t.lower() and t not in listaBuscar.get(0, tkinter.END):
            listaBuscar.insert(tkinter.END,t)
    listaBuscar.selection_clear(0, tkinter.END)

def verIngredientes(event=None):
    if listaBuscar.get(tkinter.ACTIVE)!="":
        result=recetas[listaBuscar.get(tkinter.ACTIVE)].replace("\n","\n  - ")
        result=result[:-2]
        etiquetaResultado["text"]="Ingredientes: \n  - "+result
        etiquetaTituloBusqueda["text"]="Receta: "+listaBuscar.get(tkinter.ACTIVE).upper()

def limpiarTexto():
    cajaTextoTitulo.delete(0, tkinter.END)
    cajaTextoIngredientes.delete("1.0", "end")

def quitarComprobacion():
    etiquetaComprobacion["text"]=""

def eliminarReceta():
    laRec = listaBuscar.get(tkinter.ACTIVE)
    if laRec != "" and laRec != '' and laRec != "\n" and laRec != " " and len(laRec.replace(" ",""))!=0:
        mensajeConfirmacion = tkinter.messagebox.askquestion ('Confirmación','Estas seguro que quieres eliminar la receta: '+listaBuscar.get(tkinter.ACTIVE).upper()+'?')
        if mensajeConfirmacion == 'yes':
            del recetas[listaBuscar.get(tkinter.ACTIVE)]
            meterEnLista()
        else:
            meterEnLista()

def crearMostrarQR():
    if listaBuscar.get(tkinter.ACTIVE)!="":
        tab_control.select(tabQR)
        img = qrcode.make(listaBuscar.get(tkinter.ACTIVE).upper()+":\n\n"+recetas[listaBuscar.get(tkinter.ACTIVE)])
        with open('myfile.png', 'wb') as f:
            img.save(f)
        img = Image.open('myfile.png')
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.image=img
        panel['image']=panel.image
        panel.pack(side = "bottom", expand = "yes")

def modificarReceta():
    if listaBuscar.get(tkinter.ACTIVE)!="":
        tab_control.select(tabIntroducir)
        cajaTextoTitulo.delete(0,tkinter.END)
        cajaTextoTitulo.insert(tkinter.END,listaBuscar.get(tkinter.ACTIVE))
        cajaTextoIngredientes.delete("1.0", "end")
        cajaTextoIngredientes.insert(tkinter.END,recetas[listaBuscar.get(tkinter.ACTIVE)])


result=""
recetas={}
nombre=""
ingredientes=""
receta=""
array=[]

fichero = open('recetas.txt','r')
for f in fichero:
    f=f.replace("\n","")
    if f!="" and f!=None:
        if f.startswith("**"):
            array.append(receta)
            receta=""
            f=f.replace("**","")
        receta=receta+f+"~~"
array.append(receta)
array.pop(0)

for n in range(len(array)):
    array[n]=array[n].split("~~")
    array[n].pop(-1)
    for i in range(len(array[n])):
        if i==0:
            nombre=array[n][i]
        else:
            ingredientes=ingredientes+array[n][i]+"\n"
    recetas[nombre]=ingredientes
    nombre=""
    ingredientes=""

fichero.close()

#VENTANAS Y TABS

ventana = tkinter.Tk()
ventana.geometry("820x530")
ventana.title("RECETAS")
center_tk_window.center_on_screen(ventana)

tab_control = ttk.Notebook(ventana)

tabIntroducir = ttk.Frame(tab_control)
tabBuscar = ttk.Frame(tab_control)
tabQR = ttk.Frame(tab_control)


s = ttk.Style()
s.configure('TFrame', background='#B1DCFC',borderwidth = 1, relief = tkinter.GROOVE)
s.configure("TNotebook", background='#d8edfe', foreground='red',lightcolor='red', borderwidth = 1, relief = tkinter.GROOVE)
s.map("TNotebook.Tab", foreground=[("selected", '#04599f')])

tab_control.add(tabIntroducir, text='Introducir')
tab_control.add(tabBuscar, text='Buscar')
tab_control.add(tabQR, text='QR')

#INTRODUCIR

etiquetaComprobacion = tkinter.Label(tabIntroducir,text = " ", font=('helvetica', 10, 'bold'),background='#B1DCFC',fg="#03214f")
etiquetaTitulo = tkinter.Label(tabIntroducir,text = "Receta: ", font=('helvetica', 12, 'bold'),background='#B1DCFC',fg="#03214f")
etiquetaIngredientes = tkinter.Label(tabIntroducir,text = "Ingredientes: ", font=('helvetica', 12, 'bold'),background='#B1DCFC',fg="#03214f")
cajaTextoIngredientes = tkinter.Text(tabIntroducir, height=22, width=44, bg='#f3f7f5',fg='#02193b',font='helvetica 13', borderwidth=2,relief=tkinter.GROOVE, highlightcolor="#011127")
cajaTextoTitulo = tkinter.Entry(tabIntroducir, font="Helvetica 14", bg='#f3f7f5',fg='#02193b', borderwidth=2,relief=tkinter.GROOVE, highlightcolor="#011127")
botIntroducir = tkinter.Button(tabIntroducir, text = "Introducir Receta", height=20, width=20, command = introducirReceta, bg='#89C9FB', font=('helvetica', 12, 'bold'),fg='#02193b', highlightcolor="#011127")
botLimpiar = tkinter.Button(tabIntroducir, text = "Limpiar\ntexto", command = limpiarTexto, bg='#89C9FB', font=('helvetica', 12, 'bold'),fg='#02193b', highlightcolor="#011127")

botIntroducir.grid(row = 1 , column = 4, padx=15, pady=5, sticky='we')
botLimpiar.grid(row = 1 , column = 0, padx=5, pady=5, sticky='s')
cajaTextoTitulo.grid(row = 0 , column = 1, padx=5, pady=5, sticky='we')
cajaTextoIngredientes.grid(row = 1 , column = 1, rowspan = 2, padx=5 , pady=5, sticky='n')
etiquetaComprobacion.grid(row = 2 , column = 4, padx=7, pady=10)
etiquetaTitulo.grid(row = 0 , column = 0, padx=7, pady=10,sticky='w')
etiquetaIngredientes.grid(row = 1 , column = 0, padx=7, pady=10,sticky='nw')

#BUSCAR

listaBuscar = tkinter.Listbox(tabBuscar, bg='#f3f7f5', width = 31, height = 24,fg='#02193b', highlightcolor="#011127",font=('helvetica', 10 , 'bold'))
etiquetaBuscar = tkinter.Label(tabBuscar,text = "Busqueda: ", font=('helvetica', 12, 'bold'),background='#B1DCFC',fg="#03214f")
etiquetaTituloBusqueda = tkinter.Label(tabBuscar,text="Receta: " , font=('helvetica', 15, 'bold', 'underline'),background='#B1DCFC',fg="#03214f")
etiquetaResultado = tkinter.Label(tabBuscar, font=('helvetica', 12, 'bold'),justify=tkinter.LEFT,background='#B1DCFC',fg="#03214f",text = "Ingredientes: ")
cajaTextoBuscar = tkinter.Entry(tabBuscar, font="Helvetica 13", bg='#f3f7f5',fg='#02193b', borderwidth=2,relief=tkinter.GROOVE, highlightcolor="#011127")
botBuscar = tkinter.Button(tabBuscar, text = "Pulsa para\nbuscar", width = 15, height = 3,command = meterEnLista,bg='#89C9FB', font=('helvetica', 11, 'bold'),fg='#02193b', highlightcolor="#011127")
botModificar = tkinter.Button(tabBuscar, text = "Pulsa para\nmodificar", width = 15, height = 3,command = modificarReceta,bg='#89C9FB', font=('helvetica', 11, 'bold'),fg='#02193b', highlightcolor="#011127")
botVer = tkinter.Button(tabBuscar, text = "Pulsa para ver\ningredientes", width = 15, height = 3,command = verIngredientes, bg='#89C9FB', font=('helvetica', 11, 'bold'),fg='#02193b', highlightcolor="#011127")
botEliminar = tkinter.Button(tabBuscar, text = "Pulsa para eliminar\nla receta", width = 15, height = 3,command = eliminarReceta, bg='#89C9FB', font=('helvetica', 11, 'bold'),fg='#02193b', highlightcolor="#011127")
botQR = tkinter.Button(tabBuscar, text = "Pulsa para ver\nel QR", width = 15, height = 3,command = crearMostrarQR, bg='#89C9FB', font=('helvetica', 11, 'bold'),fg='#02193b', highlightcolor="#011127")

botModificar.grid(row = 3 , column = 0, padx=10, pady=4)
botBuscar.grid(row = 1 , column = 0, padx=10, pady=4)
botVer.grid(row = 2 , column = 0, padx=10, pady=4)
botEliminar.grid(row = 4 , column = 0, padx=10, pady=4)
botQR.grid(row = 5 , column = 0, padx=10, pady=4)
cajaTextoBuscar.grid(row = 0 , column = 1, padx=5, pady=5, sticky='we')
listaBuscar.grid(row =1,column=1,rowspan=5, padx=5, pady=5)
etiquetaTituloBusqueda.grid(row = 0 , column = 2, columnspan=2, padx=5, pady=5, sticky='w')
etiquetaResultado.grid(row = 1 , column = 2, rowspan=5, columnspan=2, sticky='nw', padx=5, pady=5)
etiquetaBuscar.grid(row = 0 , column = 0, padx=5, pady=20, sticky='w')

cajaTextoBuscar.bind('<Return>', meterEnLista)
listaBuscar.bind('<Double-Button-1>', verIngredientes)

panel = tkinter.Label(tabQR)

tab_control.pack(expand=1, fill='both')
meterEnLista()
ventana.mainloop()


elementos=recetas.items()
fich = open('recetas.txt','w')

for titulo,ing in elementos:
    if titulo == "" or ing == "" or titulo == '' or ing == '' or ing == "\n" or ing == " " or titulo == " ":
        continue
    fich.write("**"+titulo+"**"+"\n")
    fich.write(ing+"\n")
fich.close()
