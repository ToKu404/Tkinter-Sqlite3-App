from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Init Of Tkinter
root = Tk()
#Connect DB
conn = sqlite3.connect("perpustakaan.db")
cursor = conn.cursor()

# Update Treeview
def update_trv(rows):
    trv.delete(*trv.get_children())
    for i in rows: 
        trv.insert('','end',values=i)

# Search Data
def search():
    q2 = q.get()
    query = """
    SELECT ID, JUDUL, KATEGORI, NO_RAK, PENULIS, PENERBIT, TAHUN, STOK FROM LIBRARY WHERE JUDUL LIKE {} OR NO_RAK LIKE {}
    """.format("'%"+q2+"%'", "'%"+q2+"%'")
    print(query)
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)

# Clear Treeview
def clear():
    query = "SELECT ID, JUDUL, KATEGORI, NO_RAK, PENULIS, PENERBIT, TAHUN, STOK FROM LIBRARY"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    update_trv(rows)
    clear_field()

# Get Row Select from Treeview
def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)
    v_id.set(item['values'][0])
    v_judul.set(item['values'][1])
    v_kategori.set(item['values'][2])
    v_no_rak.set("00"+str(item['values'][3]))
    v_penulis.set(item['values'][4])
    v_penerbit.set(item['values'][5])
    v_tahun_terbit.set(item['values'][6])
    v_stok.set(item['values'][7])

# Create Family Table
def create_table():
    cursor.execute("DROP TABLE IF EXISTS LIBRARY")
    query = """ 
    CREATE TABLE LIBRARY(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        JUDUL TEXT NOT NULL,
        KATEGORI TEXT NOT NULL,
        NO_RAK TEXT NOT NULL,
        PENULIS TEXT,
        PENERBIT TEXT,
        TAHUN TEXT, 
        STOK INT
    )
    """
    cursor.execute(query)
    conn.commit()

# Clear Field Of Form
def clear_field():
    judul_field.delete(0, 'end')
    penulis_field.delete(0, 'end')
    penerbit_field.delete(0, 'end')
    tahun_field.delete(0, 'end')
    kategori_field.set('')
    no_rak_field.set('')
    stok_field.delete(0, 'end')
# Update People Data
def update_people():
    if messagebox.askyesno("Harap Konfirmasi", "Apakah Anda Serius ingin memperbaharui data ini?"):
        query = """
            UPDATE LIBRARY
            SET JUDUL=:JUDUL, KATEGORI=:KATEGORI, NO_RAK=:NO_RAK, PENULIS=:PENULIS, PENERBIT=:PENERBIT, TAHUN=:TAHUN, STOK=:STOK
            WHERE ID=:ID
        """
        params = {
            'ID':v_id.get(),
            'JUDUL': v_judul.get(),
            'KATEGORI': v_kategori.get(),
            'NO_RAK' : v_no_rak.get(),
            'PENULIS': v_penulis.get(),
            'PENERBIT': v_penerbit.get(),
            'TAHUN': v_tahun_terbit.get(),
            'STOK': v_stok.get()
        }
        cursor.execute(query, params)
        conn.commit()
        clear()
    else:
        return True

def add_new():
    # GENERATE KODE
    query = """
        INSERT INTO LIBRARY
        (JUDUL, KATEGORI, NO_RAK, PENULIS, PENERBIT, TAHUN, STOK)
        VALUES (:JUDUL, :KATEGORI, :NO_RAK, :PENULIS, :PENERBIT, :TAHUN, :STOK)
        """
    params = {
        'JUDUL': v_judul.get(),
        'KATEGORI': v_kategori.get(),
        'NO_RAK' : v_no_rak.get(),
        'PENULIS': v_penulis.get(),
        'PENERBIT': v_penerbit.get(),
        'TAHUN': v_tahun_terbit.get(),
        'STOK': v_stok.get()
    }
    cursor.execute(query, params)
    conn.commit()
    clear()

# Delete People
def delete_book():
    id = v_id.get()
    if(messagebox.askyesno("Konfirmasi Hapus?", "Apakah kami serius ingin menghapus data buku ini?")):
        query = "DELETE FROM LIBRARY WHERE ID = {}".format(id)
        cursor.execute(query)
        conn.commit()
        clear()
    else:
        return True

# Select All From TABLE
def select_all():
    query = "SELECT ID, JUDUL, KATEGORI, NO_RAK, PENULIS, PENERBIT, TAHUN, STOK FROM LIBRARY"
    cursor.execute(query)
    rows = cursor.fetchall()
    update_trv(rows)

# Check IF Table not exist
def isFirst(table_name):
    query = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}' '''.format(table_name)
    cursor.execute(query)
    conn.commit()
    if cursor.fetchone()[0]==1 : 
        return False
    else :
        return True


#Wrapper of Section
wrapper1 = LabelFrame(root, text="Daftar Buku")
wrapper2 = LabelFrame(root, text="Pencarian")
wrapper3 = LabelFrame(root, text="Data Buku")
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", padx=20, pady=10)
wrapper3.pack(fill="both", padx=20, pady=10)

# SECTION : TREE VIEW
# Treeview Configure
trv = ttk.Treeview(wrapper1, column=(0,1,2,3,4,5,6,7), height=6, show="headings")
style = ttk.Style()
style.theme_use("clam")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)
# Treeview Heading
trv.heading(0, text="Id")
trv.heading(1, text="Judul")
trv.heading(2, text="Kategori")
trv.heading(3, text="No Rak")
trv.heading(4, text="Penulis")
trv.heading(5, text="Penerbit")
trv.heading(6, text="Tahun Terbit")
trv.heading(7, text="Stok")
# Treeview Column
# trv.column(0, stretch=NO, minwidth=0, width=0)
# trv.column(1, width=95, minwidth=135, anchor=CENTER)
# trv.column(2, width=95, minwidth=135, anchor=CENTER)
# trv.column(3, width=95, minwidth=135,anchor=CENTER)
# trv.column(4, width=95, minwidth=135,anchor=CENTER)
# trv.column(5, width=95, minwidth=135,anchor=CENTER)
# trv.column(6, width=95, minwidth=135, anchor=CENTER)
# trv.column(7, width=65, minwidth=105,anchor=CENTER)
trv.column(0, stretch=NO, width=0)
trv.column(1, width=95, anchor=CENTER)
trv.column(2, width=95, anchor=CENTER)
trv.column(3, width=95,anchor=CENTER)
trv.column(4, width=95,anchor=CENTER)
trv.column(5, width=95,anchor=CENTER)
trv.column(6, width=95, anchor=CENTER)
trv.column(7, width=95,anchor=CENTER)

trv.bind('<Double 1>', getrow)

#Scrollbar of TRV
yscrollbar = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrollbar.pack(side=RIGHT, fill="y")
xscrollbar = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrollbar.pack(side=BOTTOM,fill="x")
trv.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)



# SECTION : SEARCHwh
q = StringVar()
lbl = Label(wrapper2, text="Search")
lbl.pack(side=LEFT, padx=10, pady=15)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=LEFT, padx=6, pady=15)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=15)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=6, pady=15)

# SECTION = LIBRARY DATA FORM
p_style = ('Calibri 10')
# Select Label of From
judul = tk.Label(wrapper3, text="Judul", font= p_style)
kategori = tk.Label(wrapper3, text="Kategori", font= p_style)
no_rak = tk.Label(wrapper3, text="No Rak", font= p_style)
penulis = tk.Label(wrapper3, text="Penulis", font= p_style)
penerbit = tk.Label(wrapper3, text="Penerbit", font= p_style)
tahun_terbit = tk.Label(wrapper3, text="Tahun Terbit", font= p_style)
stok = tk.Label(wrapper3, text="Stok", font= p_style)
# Place Label of Form
judul.grid(row=1, column=0, sticky="w", pady=4)
kategori.grid(row=2, column=0, sticky="w", pady=4)
no_rak.grid(row=3, column=0, sticky="w", pady=4)
penulis.grid(row=4, column=0, sticky="w", pady=4)
penerbit.grid(row=1, column=6, sticky="w", pady=4, padx=10)
tahun_terbit.grid(row=2, column=6, sticky="w", pady=4, padx=10)
stok.grid(row=3, column=6, sticky="w", pady=4,  padx=10)
# Variabel to Save value of Field
v_id = tk.IntVar()
v_judul = tk.StringVar()
v_kategori = tk.StringVar()
v_no_rak = tk.StringVar()
v_penulis = tk.StringVar()
v_penerbit = tk.StringVar()
v_tahun_terbit = tk.StringVar()
v_stok = tk.IntVar()
# Field to Input data
judul_field = Entry(wrapper3, font=p_style, textvariable=v_judul)
kategori_field = ttk.Combobox(wrapper3, width = 17, textvariable = v_kategori, font=p_style)
kategori_field['values'] = (
                    '000 - Umum',
                    '100 - Filsafat dan psikologi',
                    '200 - Agama',
                    '300 - Sosial',
                    '400 - Bahasa',
                    '500 - Sains dan Matematika',
                    '600 - Teknologi',
                    '700 - Seni dan rekreasi',
                    '800 - Literatur dan Sastra',
                    '900 - Sejarah dan Geografi',
                )

no_rak_field = ttk.Combobox(wrapper3, width = 17, textvariable = v_no_rak, font=p_style)
no_rak_field['values']=('001','002','003','004','005')
penulis_field = Entry(wrapper3, font=p_style, textvariable=v_penulis)
penerbit_field = Entry(wrapper3, font=p_style, textvariable=v_penerbit)
tahun_field = Entry(wrapper3, font=p_style, textvariable=v_tahun_terbit)
stok_field = Entry(wrapper3, font=p_style, textvariable=v_stok)


judul_field.grid(row=1, column=2, columnspan=2,sticky="w", pady=4, padx=10)
kategori_field.grid(row=2, column=2,columnspan=2,  sticky="w", pady=4, padx=10)
no_rak_field.grid(row=3, column=2, columnspan=2,sticky="w", pady=4, padx=10)
penulis_field.grid(row=4, column=2, columnspan=2,sticky="w", pady=4, padx=10)
penerbit_field.grid(row=1, column=7, columnspan=2,sticky="w", pady=4)
tahun_field.grid(row=2, column=7, columnspan=2,sticky="w", pady=4)
stok_field.grid(row=3, column=7, columnspan=2,sticky="w", pady=4)


frame_btn = Frame(wrapper3)
up_btn = Button(frame_btn, text="Update", command=update_people)
add_btn = Button(frame_btn, text="Tambah Baru", command=add_new)
delete_btn = Button(frame_btn, text="Hapus", command=delete_book)
add_btn.pack(side=LEFT, padx=5)
up_btn.pack(side=LEFT, padx=5)
delete_btn.pack(side=LEFT, padx=5)
frame_btn.grid(row=7, column=0, columnspan=8, sticky=W, pady=10)

if __name__ == '__main__':
    root.title("Aplikasi Data Perpustakaan Sederhana")
    root.geometry("700x500")
    root.resizable(FALSE, FALSE)
    first = isFirst("LIBRARY")
    if(first):
        create_table()
    else:
        select_all()
    root.mainloop()


