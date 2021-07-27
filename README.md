# Penjelasan Projek 

## :book: Pengumpulan Data
Melakukan Observasi ke RT/RW dan mengumpulkan data berikut
1. Pendataan Kelahiran
2. Pendataan Kematian
3. Penarikan iuran sampah
4. Penarikan iuran keamanan
5. Pendataan jumlah sampah yang dihasilkan warga
6. Pendataan luas wilayah RT

## :computer: Pembuatan Program
### Kriteria Program

- Program Dibuat dengan Bahasa Python 3
- Hasil dari pengerjaan program ditampilkan di konsole
- Database bisa berupa txt, json, ataupun SQL 

### Fitur Wajib
#### A. Insialisasi Awal
Memilih salah satu data RT yang dikumpulkan untuk dijadikan sample
1. Memasukkan Nama Desa/Kelurahan
3. Memasukkan Nama RT dan RW
4. Memasukkan Luas Wilayah RT
5. Memasukkan iuran sampah dan kemanan
#### B. Menambahkan data Keluarga
Gunakan 5 atau lebih data sample untuk uji coba program, dan input data **minimal** berikut :
1. Nomor KK
2. Jumlah Anggota Keluarga
3. Menginput Data Setiap Anggota Keluarga Sesuai **Tabel 3** 

#### C. Menghapus data Keluarga
1. Fitur untuk menghapus data keluarga

#### D. Mengedit dan mengupdate data Wilayah dan Keluarga
1. Fitur untuk mengedit data wilayah
2. Fitur untuk mengedit data keluarga

#### E. Menambahkan data Kelahiran dan Kematian
1. Menambahkan data jika terdapat bayi yang lahir pada suatu keluarga, dengan input no seperti pada **Tabel 4**, jika belum masuk KK, sedangkan jika sudah data mengikuti kk berupa
2. Menambahkan data kematian, jika terdapat seseorang yang meninggal di wilayah RT terkait, maka data kematian tersimpan berupa [NIK, Waktu Kematian (Tanggal, Bulan, Tahun)], dan data keluarga akan otomatis tertambah di data kependudukan

#### F. Menampilkan data
1. Menampilkan data RT, berupa luas wilayah, iuran sampah dan kelurahan, jumlah penduduk yang telah didata, jumlah kelahiran yang telah didata, jumlah kematian yang telah didata
2. Menampilkan data keluarga yang telah diinput pada suatu RT
3. Menampilkan data anggota keluarga
4. Menampilkan data kelahiran
5. Menampilkan data kematian

#### G. Fitur Pencarian
1. Mencari data menggunakan nama, NIK anggota keluarga atau no KK, kemudian akan menampilkan data keluarga yang sesuai



## :abcd: Logic Table
### 1. Tabel Wilayah 
| Attribut         | Tipe Data |
| ---------------- | --------- |
| ID               | Integer   |
| Nama Desa        | String    |
| RW               | Integer   |
| RT               | Integer   |
| Jumlah Keluarga  | Integer   |
| Jumlah Penduduk  | Integer   |
| Jumlah Kelahiran | Integer   |
| Jumlah Kematian  | Integer   |
| Iuran Sampah     | Integer   |
| Iuran Keamanan   | Integer   |

### 2. Tabel Keluarga
| Attribut        | Tipe Data |
| --------------- | --------- |
| No Kk           | Integer   |
| RW              | Integer   |
| RT              | Integer   |
| Jumlah Keluarga | Integer   |


### 3. Tabel Anggota Keluarga

| Attribut              | Tipe Data |
| --------------------- | --------- |
| NIK                   | Integer   |
| Nama                  | String    |
| Jenis Kelamin         | Char      |
| Pendidikan            | String    |
| Pekerjaan             | String    |
| Tempat Lahir          | String    |
| Tanggal Lahir         | String    |
| Status Pernikahan     | String    |
| Status Dalam Keluarga | String    |
| Status Kematian       | Boolean   |
| Nama Ayah             | String    |
| Nama Ibu              | String    |


### 4. Tabel Kelahiran

| Attribut         | Tipe Data |
| ---------------- | --------- |
| No KK (Jika Ada) | Integer   |
| NIK (Jika Ada)   | Integer   |
| Nama             | String    |
| Jenis Kelamin    | Char      |
| TTL              | String    |
| Nama Ayah        | String    |
| Nama Ibu         | String    |

### 5. Tabel Kematian
| Attribut       | Tipe Data |
| -------------- | --------- |
| NIK            | Integer   |
| Nama           | String    |
| Waktu Kematian | String    |

## :lemon: Contoh Hasil Program
### Contoh 1
Database : txt
Tampilan : Console



### Contoh 2
Database : PyMySQL 
Tampilan : Tkinter