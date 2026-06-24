# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000. Selama lebih dari dua dekade beroperasi, institusi ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun di balik reputasi tersebut, terdapat permasalahan serius yang belum terselesaikan: tingginya angka mahasiswa yang tidak menyelesaikan pendidikannya alias **dropout**.

Dengan tingkat dropout yang mencapai lebih dari 32% dari total mahasiswa, Jaya Jaya Institut membutuhkan pendekatan berbasis data untuk mendeteksi mahasiswa berisiko sedini mungkin agar dapat diberikan bimbingan dan intervensi yang tepat sebelum mereka benar-benar keluar dari institusi.

### Permasalahan Bisnis

1. **Tingginya angka dropout** — Sebanyak 1.421 dari 4.424 mahasiswa (32.1%) tidak menyelesaikan studi mereka, yang berdampak negatif pada reputasi dan pendapatan institusi.
2. **Tidak adanya sistem deteksi dini** — Institusi belum memiliki mekanisme otomatis untuk mengidentifikasi mahasiswa yang berisiko dropout sebelum kondisinya semakin parah.
3. **Keterbatasan monitoring berbasis data** — Manajemen dan staf akademik kesulitan memantau tren performa mahasiswa secara real-time dan menyeluruh.

### Cakupan Proyek

1. Melakukan eksplorasi dan analisis mendalam terhadap dataset mahasiswa Jaya Jaya Institut (EDA)
2. Melakukan preprocessing dan persiapan data untuk pemodelan machine learning
3. Membangun dan membandingkan beberapa model klasifikasi (Logistic Regression, Random Forest, Gradient Boosting)
4. Mengevaluasi model menggunakan metrik accuracy, precision, recall, F1-score, dan confusion matrix
5. Membuat business dashboard interaktif menggunakan Metabase untuk monitoring performa mahasiswa
6. Mengembangkan prototype sistem prediksi dropout berbasis Streamlit yang dapat diakses secara online

### Persiapan

**Sumber data:**
Dataset mahasiswa Jaya Jaya Institut tersedia di:
[https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

Dataset terdiri dari **4.424 baris** dan **37 kolom**, mencakup informasi demografis, akademik, dan ekonomi mahasiswa. Tidak terdapat missing values.

**Setup environment:**
```bash
# Clone atau download repository ini, lalu jalankan:
pip install -r requirements.txt

# Jalankan notebook untuk melatih model
jupyter notebook notebook.ipynb

# Jalankan Streamlit prototype secara lokal
streamlit run app.py
```

**Setup Metabase via Docker:**
```bash
docker pull metabase/metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase

# Setelah selesai, export database:
docker cp metabase:/metabase.db/metabase.db.mv.db ./
```

## Business Dashboard

Dashboard dibuat menggunakan **Metabase** dan berisi visualisasi untuk membantu Jaya Jaya Institut memahami data mahasiswa serta memonitor performa secara berkala.

Dashboard mencakup:
- **Distribusi Status Mahasiswa** — proporsi Graduate, Dropout, dan Enrolled secara keseluruhan
- **Dropout Rate per Program Studi (Course)** — mengidentifikasi program studi dengan angka dropout tertinggi
- **Pengaruh Pembayaran Biaya Kuliah** — perbandingan status mahasiswa berdasarkan `Tuition_fees_up_to_date`
- **Distribusi Usia saat Mendaftar** — segmentasi usia mahasiswa berdasarkan status akhir
- **Performa Akademik Semester 1 & 2** — rata-rata MK yang disetujui berdasarkan status mahasiswa
- **Tren Penerima Beasiswa vs Dropout** — hubungan antara scholarship dan kelulusan

**Akses Dashboard Metabase:**
- Email: `root@mail.com`
- Password: `root123`

## Menjalankan Sistem Machine Learning

Prototype sistem prediksi dropout mahasiswa dibangun menggunakan **Streamlit** dan model **Gradient Boosting** yang telah dilatih pada dataset Jaya Jaya Institut.

**Fitur prototype:**
- Input parameter mahasiswa melalui sidebar interaktif (demografis, akademik, finansial)
- Prediksi status mahasiswa: **Graduate**, **Dropout**, atau **Enrolled**
- Visualisasi probabilitas tiap kelas
- Rekomendasi intervensi otomatis jika mahasiswa diprediksi Dropout

**Menjalankan secara lokal:**
```bash
# Pastikan model sudah dilatih (jalankan notebook.ipynb terlebih dahulu)
streamlit run app.py
```

**Akses prototype online (Streamlit Community Cloud):**
> 🔗 **https://jaya-jaya-institut-linda.streamlit.app**

**Struktur file model:**
```
model/
├── gb_model.pkl        # Model Gradient Boosting terlatih
├── scaler.pkl          # StandardScaler untuk normalisasi fitur
└── label_encoder.pkl   # LabelEncoder untuk dekode prediksi
```

## Conclusion

Berdasarkan analisis terhadap dataset Jaya Jaya Institut, ditemukan bahwa **32.1% mahasiswa mengalami dropout** dari total 4.424 mahasiswa. Model Gradient Boosting berhasil memprediksi status mahasiswa dengan **akurasi 75.93%** dan **F1-score weighted 0.75**.

Faktor-faktor yang paling berpengaruh terhadap dropout adalah:
1. **Jumlah mata kuliah yang berhasil lulus di semester 2** (`Curricular_units_2nd_sem_approved`) — kontributor terbesar (55.1% importance). Mahasiswa yang tidak lulus mata kuliah di semester kedua memiliki risiko dropout sangat tinggi.
2. **Status pembayaran biaya kuliah** (`Tuition_fees_up_to_date`) — mahasiswa yang menunggak UKT jauh lebih berisiko dropout.
3. **Jumlah mata kuliah yang lulus di semester 1** (`Curricular_units_1st_sem_approved`) — performa awal sangat menentukan keberlangsungan studi.
4. **Usia saat mendaftar** (`Age_at_enrollment`) — mahasiswa yang mendaftar di usia lebih tua cenderung memiliki risiko dropout lebih tinggi.

### Rekomendasi Action Items

- **Implementasikan Early Warning System otomatis** — Integrasikan model prediksi ke sistem informasi akademik institusi agar mahasiswa berisiko dapat di-flag secara otomatis setiap akhir semester, sehingga staf akademik dapat segera menindaklanjuti.

- **Prioritaskan intervensi finansial di semester awal** — Mahasiswa dengan status `Tuition_fees_up_to_date = 0` harus segera dihubungi dalam 30 hari pertama keterlambatan. Buat program keringanan UKT atau cicilan khusus untuk mencegah dropout akibat kendala finansial.

- **Luncurkan program bimbingan akademik wajib di semester 1** — Mahasiswa yang lulus kurang dari 3 mata kuliah di semester pertama harus otomatis mendapatkan pendampingan intensif dari dosen wali sebelum mengambil mata kuliah di semester 2.

- **Buat program onboarding khusus mahasiswa non-tradisional** — Mahasiswa yang mendaftar di usia lebih dari 25 tahun, mahasiswa internasional, dan mahasiswa pindahan (displaced) memerlukan dukungan adaptasi ekstra berupa mentoring teman sebaya dan konseling akademik.

- **Gunakan dashboard Metabase untuk rapat evaluasi bulanan** — Wajibkan penggunaan dashboard oleh koordinator program studi untuk memantau tren performa dan dropout rate per program secara rutin, sehingga keputusan intervensi didasarkan pada data, bukan intuisi.
