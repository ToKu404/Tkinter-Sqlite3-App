from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Init Of Tkinter
root = Tk()
#Connect DB
conn = sqlite3.connect("data_penduduk.db")
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
    SELECT * FROM FAMILY WHERE NIK LIKE {} OR NAMA LIKE {}
    """.format("'%"+q2+"%'", "'%"+q2+"%'")
    print(query)
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    update_trv(rows)

# Clear Treeview
def clear():
    query = "SELECT * FROM FAMILY"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    update_trv(rows)
    clear_field()

# Get Row Select from Treeview
def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(rowid)
    v_nik.set(item['values'][0])
    v_nama.set(item['values'][1])
    v_jk.set(item['values'][2])
    v_pendidikan.set(item['values'][3])
    v_pekerjaaan.set(item['values'][4])

    ttl = str(item['values'][5]).split(",")
    v_tempat_lahir.set(ttl[0])
    
    date = ttl[1].split("/")
    v_tgl_lahir.set(date[0])
    v_bln_lahir.set(date[1])
    v_thn_lahir.set(date[2])

    v_s_pernikahan.set(item['values'][6])
    v_s_dlm_keluarga.set(item['values'][7])
    v_nama_ayah.set(item['values'][8])
    v_nama_ibu.set(item['values'][9])


# Create Family Table
def create_table():
    cursor.execute("DROP TABLE IF EXISTS FAMILY")
    query = """ 
    CREATE TABLE FAMILY(
        NIK INT PRIMARY KEY NOT NULL,
        NAMA TEXT NOT NULL,
        JK TEXT NOT NULL,
        PENDIDIKAN TEXT,
        PEKERJAAN TEXT,
        TTL TEXT,
        STATUS_PERNIKAHAN TEXT, 
        STATUS_DALAM_KELUARGA TEXT,
        NAMA_AYAH TEXT,
        NAMA_IBU TEXT
    )
    """
    cursor.execute(query)
    conn.commit()

# Clear Field Of Form
def clear_field():
    nik_field.delete(0, 'end')
    nama_field.delete(0, 'end')
    pekerjaan_field.delete(0, 'end')
    tempat_lahir_field.delete(0, 'end')
    tgl_field.delete(0, 'end')
    bln_field.delete(0, 'end')
    thn_field.delete(0, 'end')
    nama_ayah_field.delete(0, 'end')
    nama_ibu_field.delete(0, 'end')
    jk1_field.deselect()
    jk2_field.deselect()
    v_jk.set(None)
    pendidikan_field.set('')
    s_pernikahan_field.set('')
    s_dlm_keluarga_field.set('')

# Update People Data
def update_people():
    if messagebox.askyesno("Harap Konfirmasi", "Apakah Anda Serius ingin memperbaharui data ini?"):
        query = """
            UPDATE FAMILY
            SET NAMA = :NAMA, JK = :JK, PENDIDIKAN = :PENDIDIKAN, TTL = :TTL, STATUS_PERNIKAHAN = :STATUS_PERNIKAHAN, STATUS_DALAM_KELUARGA = :STATUS_DALAM_KELUARGA, NAMA_AYAH = :NAMA_AYAH, NAMA_IBU = :NAMA_IBU
            WHERE NIK = :NIK
        """
        params = {
            'NIK': v_nik.get(),
            'NAMA': v_nama.get(),
            'JK': v_jk.get(),
            'PENDIDIKAN' : v_pendidikan.get(),
            'PEKERJAAN': v_pekerjaaan.get(),
            'TTL': (v_tempat_lahir.get()+", "+v_tgl_lahir.get()+"/"+v_bln_lahir.get()+"/"+v_thn_lahir.get()),
            'STATUS_PERNIKAHAN': v_s_pernikahan.get(),
            'STATUS_DALAM_KELUARGA': v_s_dlm_keluarga.get(),
            'NAMA_AYAH': v_nama_ayah.get(),
            'NAMA_IBU': v_nama_ibu.get(),
        }
        cursor.execute(query, params)
        conn.commit()
        clear()
    else:
        return True


# Add New People Data
def add_new():
    query = """
        INSERT INTO FAMILY
        (NIK, NAMA, JK, PENDIDIKAN, PEKERJAAN, TTL, STATUS_PERNIKAHAN, STATUS_DALAM_KELUARGA, NAMA_AYAH, NAMA_IBU)
        VALUES (:NIK, :NAMA, :JK, :PENDIDIKAN, :PEKERJAAN, :TTL, :STATUS_PERNIKAHAN, :STATUS_DALAM_KELUARGA, :NAMA_AYAH, :NAMA_IBU)
        """
    params = {
        'NIK': v_nik.get(),
        'NAMA': v_nama.get(),
        'JK': v_jk.get(),
        'PENDIDIKAN' : v_pendidikan.get(),
        'PEKERJAAN': v_pekerjaaan.get(),
        'TTL': (v_tempat_lahir.get()+", "+v_tgl_lahir.get()+"/"+v_bln_lahir.get()+"/"+v_thn_lahir.get()),
        'STATUS_PERNIKAHAN': v_s_pernikahan.get(),
        'STATUS_DALAM_KELUARGA': v_s_dlm_keluarga.get(),
        'NAMA_AYAH': v_nama_ayah.get(),
        'NAMA_IBU': v_nama_ibu.get(),
    }
    cursor.execute(query, params)
    conn.commit()
    clear()

# Delete People
def delete_people():
    nik = v_nik.get()
    if(messagebox.askyesno("Konfirmasi Hapus?", "Apakah kami serius ingin menghapus data orang ini?")):
        query = "DELETE FROM FAMILY WHERE NIK = {}".format(nik)
        cursor.execute(query)
        conn.commit()
        clear()
    else:
        return True

# Select All From TABLE
def select_all():
    query = "SELECT * FROM FAMILY"
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
wrapper1 = LabelFrame(root, text="Daftar Penduduk")
wrapper2 = LabelFrame(root, text="Pencarian")
wrapper3 = LabelFrame(root, text="Data Individu")
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", padx=20, pady=10)
wrapper3.pack(fill="both", padx=20, pady=10)

# SECTION : TREE VIEW
# Treeview Configure
trv = ttk.Treeview(wrapper1, column=(0,1,2,3,4,5,6,7,8,9), height=8)
trv["show"] = "headings"
style = ttk.Style(root)
style.theme_use("clam")
trv.pack(side=RIGHT)
trv.place(x=0, y=0)
# Treeview Heading
trv.heading(0, text="NIK")
trv.heading(1, text="Nama")
trv.heading(2, text="JK")
trv.heading(3, text="Pendidikan")
trv.heading(4, text="Pekerjaaan")
trv.heading(5, text="TTL")
trv.heading(6, text="Status Pernikahan")
trv.heading(7, text="Status dalam Keluarga")
trv.heading(8, text="Nama Ayah")
trv.heading(9, text="Nama Ibu")
# Treeview Column
trv.column(0, width=70, minwidth=150, anchor=CENTER)
trv.column(1, width=70, minwidth=150, anchor=CENTER)
trv.column(2, width=0, minwidth=70, anchor=CENTER)
trv.column(3, width=70, minwidth=150,anchor=CENTER)
trv.column(4, width=70, minwidth=150,anchor=CENTER)
trv.column(5, width=70, minwidth=150,anchor=CENTER)
trv.column(6, width=70, minwidth=150, anchor=CENTER)
trv.column(7, width=70, minwidth=150,anchor=CENTER)
trv.column(8, width=70, minwidth=150,anchor=CENTER)
trv.column(9, width=70, minwidth=150,anchor=CENTER)

trv.bind('<Double 1>', getrow)

#Scrollbar of TRV
yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=trv.yview)
yscrollbar.pack(side=RIGHT, fill="y")
xscrollbar = ttk.Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
xscrollbar.pack(side=BOTTOM,fill=X)
trv.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)



# SECTION : SEARCH
q = StringVar()
lbl = Label(wrapper2, text="Search")
lbl.pack(side=LEFT, padx=10, pady=15)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=LEFT, padx=6, pady=15)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=LEFT, padx=6, pady=15)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=LEFT, padx=6, pady=15)

# SECTION = FAMILY DATA FORM
p_style = ('Calibri 10')
# Select Label of From
nik = tk.Label(wrapper3, text="NIK",  font= p_style)
nama = tk.Label(wrapper3, text="Nama", font= p_style)
jk = tk.Label(wrapper3, text="Jenis Kelamin", font= p_style)
pendidikan = tk.Label(wrapper3, text="Pendidikan", font= p_style)
pekerjaan = tk.Label(wrapper3, text="Pekerjaan", font= p_style)
tempat_lahir = tk.Label(wrapper3, text="Tempat Lahir", font= p_style)
tgl_lahir = tk.Label(wrapper3, text="Tanggal Lahir", font= p_style)
status_pernikahan = tk.Label(wrapper3, text="Status Pernikahan", font= p_style)
status_keluarga = tk.Label(wrapper3, text="Status dalam Keluarga", font= p_style)
nama_ayah = tk.Label(wrapper3, text="Nama Ayah", font= p_style)
nama_ibu = tk.Label(wrapper3, text="Nama Ibu", font= p_style)
# Place Label of Form
nik.grid(row=1, column=0, sticky="w", pady=4, padx=(0,30))
nama.grid(row=2, column=0, sticky="w", pady=4)
jk.grid(row=3, column=0, sticky="w", pady=4)
pendidikan.grid(row=4, column=0, sticky="w", pady=4)
pekerjaan.grid(row=5, column=0, sticky="w", pady=4)
tempat_lahir.grid(row=6, column=0, sticky="w", pady=4)
tgl_lahir.grid(row=1, column=6, sticky="w", pady=4, padx=10)
status_pernikahan.grid(row=2, column=6, sticky="w", pady=4,  padx=10)
status_keluarga.grid(row=3, column=6, sticky="w", pady=4,  padx=10)
nama_ayah.grid(row=4, column=6, sticky="w", pady=4,  padx=10)
nama_ibu.grid(row=5, column=6, sticky="w", pady=4,  padx=10)
# Variabel to Save value of Field
v_nik = tk.IntVar()
v_nama = tk.StringVar()
v_jk = tk.StringVar()
v_jk.set(None)
v_pendidikan = tk.StringVar()
v_pekerjaaan = tk.StringVar()
v_tempat_lahir = tk.StringVar()
v_tgl_lahir = tk.StringVar()
v_bln_lahir = tk.StringVar()
v_thn_lahir = tk.StringVar()
v_s_pernikahan = tk.StringVar()
v_s_dlm_keluarga = tk.StringVar()
v_nama_ayah = tk.StringVar()
v_nama_ibu = tk.StringVar()
# Field to Input data
nik_field = Entry(wrapper3, font=p_style, textvariable=v_nik)
nama_field = Entry(wrapper3, font=p_style, textvariable=v_nama)
jk1_field = Radiobutton(wrapper3, text="Laki-laki", variable=v_jk, value="L", font=p_style)
jk2_field = Radiobutton(wrapper3, text="Perempuan", variable=v_jk, value="P", font=p_style)
pendidikan_field = ttk.Combobox(wrapper3, width = 17, textvariable = v_pendidikan, font=p_style)
pendidikan_field['values'] = ('Tidak/Belum Sekolah', 
                'Belum Tamat SD/Sederajat',
                'Tamat SD/Sederajat',
                'SLTP/Sederajat',
                'SLTA/Sederajat',
                'Diploma I/II',
                'Akademi/Diploma III/S.Muda',
                'Diploma IV/Strata I',
                'Strata II',
                'Strata III',
                )
pekerjaan_field = Entry(wrapper3, font=p_style, textvariable=v_pekerjaaan)
tempat_lahir_field = Entry(wrapper3, font=p_style, textvariable=v_tempat_lahir)

frame_tgl = tk.Frame(wrapper3)
tgl_field = Entry(frame_tgl, font=p_style, width=4, textvariable=v_tgl_lahir)
bln_field = Entry(frame_tgl, font=p_style, width=4, textvariable=v_bln_lahir)
thn_field = Entry(frame_tgl, font=p_style, width=8, textvariable=v_thn_lahir)
label_1 = tk.Label(frame_tgl, text='/', font=p_style)
label_2 = tk.Label(frame_tgl, text='/', font=p_style)

s_pernikahan_field = ttk.Combobox(wrapper3, width = 17, textvariable = v_s_pernikahan, font=p_style)
s_pernikahan_field['values']=('Belum Kawin','Kawin','Cerai Hidup', 'Cerai Mati')
s_dlm_keluarga_field = ttk.Combobox(wrapper3, width = 17, textvariable = v_s_dlm_keluarga, font=p_style)
s_dlm_keluarga_field['values'] = ('Kepala Keluaga', 'Suami', 'Istri', 'Anak', "Menantu",'Cucu','Orang Tua','Mertua') 
nama_ayah_field = Entry(wrapper3, font=p_style, textvariable=v_nama_ayah)
nama_ibu_field = Entry(wrapper3, font=p_style, textvariable=v_nama_ibu)

# Place Field
nik_field.grid(row=1, column=2, columnspan=2,  sticky="w", pady=4, padx=10)
nama_field.grid(row=2, column=2, columnspan=2,sticky="w", pady=4, padx=10)
jk1_field.grid(row=3, column=2, sticky="W", pady=4, padx=10)
jk2_field.grid(row=3, column=3, sticky="W", pady=4)
pendidikan_field.grid(row=4, column=2,columnspan=2,  sticky="w", pady=4, padx=10)
pekerjaan_field.grid(row=5, column=2 ,columnspan=2, sticky="w", pady=4, padx=10)
tempat_lahir_field.grid(row=6, column=2, columnspan=2,sticky="w", pady=4,padx=10)

frame_tgl.grid(row=1, column=7, columnspan=2, sticky="w",pady=4)
tgl_field.pack(side=LEFT)
label_1.pack(side=LEFT)
bln_field.pack(side=LEFT)
label_2.pack(side=LEFT)
thn_field.pack(side=LEFT)

s_pernikahan_field.grid(row=2, column=7, columnspan=2,sticky="w", pady=4)
s_dlm_keluarga_field.grid(row=3, column=7, columnspan=2,sticky="w", pady=4)
nama_ayah_field.grid(row=4, column=7, columnspan=2,sticky="w", pady=4)
nama_ibu_field.grid(row=5, column=7, columnspan=2,sticky="w", pady=4)

frame_btn = Frame(wrapper3)
up_btn = Button(frame_btn, text="Update", command=update_people)
add_btn = Button(frame_btn, text="Tambah Baru", command=add_new)
delete_btn = Button(frame_btn, text="Hapus", command=delete_people)
add_btn.pack(side=LEFT, padx=5)
up_btn.pack(side=LEFT, padx=5)
delete_btn.pack(side=LEFT, padx=5)
frame_btn.grid(row=7, column=0, columnspan=8, sticky=W, pady=10)

if __name__ == '__main__':
    root.title("Aplikasi Data Penduduk Sederhana")
    root.geometry("700x600")
    root.resizable(FALSE, FALSE)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    first = isFirst("FAMILY")
    if(first):
        create_table()
    else:
        select_all()
    root.mainloop()


