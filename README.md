# Indonesian-License-Plate-Recognition-Dataset_UAS-Computer-Vission

Proyek ini menggunakan Indonesian License Plate Dataset dari Kaggle, yang tersedia melalui tautan berikut: https://www.kaggle.com/datasets/juanthomaswijaya/indonesian-license-plate-dataset. Dataset terdiri dari folder labels dan images, yang kemudian digabungkan ke dalam satu folder bernama Plate_test untuk keperluan pengujian model OCR. Di dalam folder tersebut, terdapat dua file Python utama: predict_ocr.py dan evaluate_cer.py.

File predict_ocr.py bertugas membaca gambar-gambar plat nomor pada folder Plate_test, mengambil ground truth dari label yang tersedia, dan mengirimkan permintaan ke model LLaVA (yang dijalankan melalui LM Studio) untuk melakukan prediksi teks. Hasil prediksi kemudian disimpan dalam sebuah file CSV berformat dua kolom: image dan prediction.

File evaluate_cer.py digunakan untuk membaca hasil CSV dari predict_ocr.py, kemudian mencocokkannya dengan data ground truth yang relevan. Dari perbandingan antara prediksi dan ground truth ini, program menghitung Character Error Rate (CER) untuk setiap sampel, dan mencatat hasil evaluasi dalam file CSV baru dengan empat kolom: image, ground_truth, prediction, dan CER_score. CER dihitung dengan rumus:
CER = (S + D + I) / N
dengan S adalah jumlah karakter yang salah (substitution), D adalah karakter yang dihapus (deletion), I adalah karakter yang disisipkan (insertion), dan N adalah jumlah karakter pada ground truth.

Sebelum menjalankan skrip, pengguna perlu membuka LM Studio dan memuat model llava-llama-3-8b-v1_1. Setelah itu, buka PowerShell, masuk ke direktori proyek, dan jalankan py predict_ocr.py untuk memulai proses prediksi. Pastikan server LM Studio aktif dengan menjalankan perintah lms server start. Setelah server aktif dan prediksi selesai, jalankan py evaluate_cer.py untuk menghitung dan menampilkan evaluasi akhir menggunakan CER. Dengan tahapan ini, pengguna dapat mengukur akurasi model OCR terhadap gambar plat nomor secara otomatis dan objektif.
