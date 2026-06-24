import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Jaya Jaya Institut — Student Dropout Predictor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Jaya Jaya Institut — Student Dropout Predictor")
st.markdown("""
Prototype machine learning untuk memprediksi risiko dropout mahasiswa.
Masukkan data mahasiswa di bawah ini untuk mendapatkan prediksi status.
""")

@st.cache_resource
def load_model():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model   = joblib.load(os.path.join(base_dir, 'model', 'gb_model.pkl'))
    scaler  = joblib.load(os.path.join(base_dir, 'model', 'scaler.pkl'))
    encoder = joblib.load(os.path.join(base_dir, 'model', 'label_encoder.pkl'))
    return model, scaler, encoder

try:
    model, scaler, encoder = load_model()
    model_loaded = True
except:
    model_loaded = False
    st.warning("Model belum tersedia. Jalankan notebook.ipynb terlebih dahulu untuk melatih model.")

st.sidebar.header("Input Data Mahasiswa")

marital_status         = st.sidebar.selectbox("Status Pernikahan", [1,2,3,4,5,6], index=0,
                            help="1=Single, 2=Married, 3=Widower, 4=Divorced, 5=Facto union, 6=Legally separated")
application_mode       = st.sidebar.selectbox("Mode Aplikasi", [1,2,5,7,10,15,16,17,18,26,27,39,42,43,44,51,53,57])
application_order      = st.sidebar.slider("Urutan Pilihan Program", 0, 9, 1)
daytime_attendance     = st.sidebar.radio("Kelas", [1, 0], format_func=lambda x: "Pagi/Siang" if x==1 else "Malam")
prev_qual_grade        = st.sidebar.slider("Nilai Kualifikasi Sebelumnya", 0.0, 200.0, 120.0)
admission_grade        = st.sidebar.slider("Nilai Masuk (Admission Grade)", 0.0, 200.0, 130.0)
displaced              = st.sidebar.radio("Displaced (pindahan)", [0,1], format_func=lambda x: "Ya" if x else "Tidak")
debtor                 = st.sidebar.radio("Memiliki Utang", [0,1], format_func=lambda x: "Ya" if x else "Tidak")
tuition_up_to_date     = st.sidebar.radio("Biaya Kuliah Terbayar", [0,1], format_func=lambda x: "Ya" if x else "Tidak")
gender                 = st.sidebar.radio("Jenis Kelamin", [1,0], format_func=lambda x: "Laki-laki" if x else "Perempuan")
scholarship_holder     = st.sidebar.radio("Penerima Beasiswa", [0,1], format_func=lambda x: "Ya" if x else "Tidak")
age_at_enrollment      = st.sidebar.slider("Usia saat Mendaftar", 17, 70, 20)

st.sidebar.subheader("Semester 1")
cu1_enrolled   = st.sidebar.slider("MK Diambil Sem 1", 0, 26, 6)
cu1_approved   = st.sidebar.slider("MK Lulus Sem 1", 0, 26, 5)
cu1_grade      = st.sidebar.slider("Rata-rata Nilai Sem 1", 0.0, 20.0, 12.0)
cu1_eval       = st.sidebar.slider("MK Dievaluasi Sem 1", 0, 45, 6)

st.sidebar.subheader("Semester 2")
cu2_enrolled   = st.sidebar.slider("MK Diambil Sem 2", 0, 23, 6)
cu2_approved   = st.sidebar.slider("MK Lulus Sem 2", 0, 20, 5)
cu2_grade      = st.sidebar.slider("Rata-rata Nilai Sem 2", 0.0, 20.0, 12.0)
cu2_eval       = st.sidebar.slider("MK Dievaluasi Sem 2", 0, 33, 6)

unemployment_rate = st.sidebar.slider("Tingkat Pengangguran (%)", 0.0, 20.0, 10.8)
inflation_rate    = st.sidebar.slider("Tingkat Inflasi (%)", -1.0, 5.0, 1.4)
gdp               = st.sidebar.slider("GDP", -5.0, 5.0, 1.74)

input_data = {
    'Marital_status': marital_status,
    'Application_mode': application_mode,
    'Application_order': application_order,
    'Course': 9254,
    'Daytime_evening_attendance': daytime_attendance,
    'Previous_qualification': 1,
    'Previous_qualification_grade': prev_qual_grade,
    'Nacionality': 1,
    'Mothers_qualification': 19,
    'Fathers_qualification': 12,
    'Mothers_occupation': 5,
    'Fathers_occupation': 9,
    'Admission_grade': admission_grade,
    'Displaced': displaced,
    'Educational_special_needs': 0,
    'Debtor': debtor,
    'Tuition_fees_up_to_date': tuition_up_to_date,
    'Gender': gender,
    'Scholarship_holder': scholarship_holder,
    'Age_at_enrollment': age_at_enrollment,
    'International': 0,
    'Curricular_units_1st_sem_credited': 0,
    'Curricular_units_1st_sem_enrolled': cu1_enrolled,
    'Curricular_units_1st_sem_evaluations': cu1_eval,
    'Curricular_units_1st_sem_approved': cu1_approved,
    'Curricular_units_1st_sem_grade': cu1_grade,
    'Curricular_units_1st_sem_without_evaluations': 0,
    'Curricular_units_2nd_sem_credited': 0,
    'Curricular_units_2nd_sem_enrolled': cu2_enrolled,
    'Curricular_units_2nd_sem_evaluations': cu2_eval,
    'Curricular_units_2nd_sem_approved': cu2_approved,
    'Curricular_units_2nd_sem_grade': cu2_grade,
    'Curricular_units_2nd_sem_without_evaluations': 0,
    'Unemployment_rate': unemployment_rate,
    'Inflation_rate': inflation_rate,
    'GDP': gdp
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Ringkasan Input")
    summary = {
        "Usia": age_at_enrollment,
        "Nilai Masuk": admission_grade,
        "MK Lulus Sem 1": cu1_approved,
        "MK Lulus Sem 2": cu2_approved,
        "Biaya Terbayar": "Ya" if tuition_up_to_date else "Tidak",
        "Beasiswa": "Ya" if scholarship_holder else "Tidak",
        "Memiliki Utang": "Ya" if debtor else "Tidak",
    }
    for k, v in summary.items():
        st.metric(k, v)

with col2:
    if model_loaded and st.button("🔍 Prediksi Status Mahasiswa", use_container_width=True):
        input_df = pd.DataFrame([input_data])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        label = encoder.classes_[prediction]

        st.subheader("🎯 Hasil Prediksi")
        if label == "Dropout":
            st.error(f"⚠️ Prediksi: **{label}** — Risiko Tinggi!")
        elif label == "Graduate":
            st.success(f"✅ Prediksi: **{label}** — Kemungkinan Lulus!")
        else:
            st.info(f"📚 Prediksi: **{label}** — Masih Aktif Studi")

        st.write("**Probabilitas setiap kelas:**")
        prob_df = pd.DataFrame({
            'Status': encoder.classes_,
            'Probabilitas': probabilities
        }).sort_values('Probabilitas', ascending=False)
        st.bar_chart(prob_df.set_index('Status'))

        if label == "Dropout":
            st.warning("""
            **Rekomendasi Intervensi:**
            - 📞 Hubungi mahasiswa untuk konseling
            - 💰 Cek status pembayaran dan tawarkan keringanan
            - 📚 Assign tutor akademik
            - 🎯 Review beban MK semester berikutnya
            """)
    elif not model_loaded:
        st.info("Latih model terlebih dahulu dengan menjalankan notebook.ipynb")
    else:
        st.info("Klik tombol di atas setelah mengatur parameter di sidebar.")

st.markdown("---")
st.markdown("*Dashboard ini dibuat untuk proyek akhir Jaya Jaya Institut — Data Science Track*")
