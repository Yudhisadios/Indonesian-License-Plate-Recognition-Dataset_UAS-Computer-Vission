# Indonesian-License-Plate-Recognition-Dataset_UAS-Computer-Vission

Proyek ini menggunakan dataset **Indonesian License Plate Dataset** dari Kaggle, yang dapat diakses melalui tautan berikut: [https://www.kaggle.com/datasets/juanthomaswijaya/indonesian-license-plate-dataset](https://www.kaggle.com/datasets/juanthomaswijaya/indonesian-license-plate-dataset). Dataset terdiri dari folder *labels* dan *images*, yang kemudian digabungkan ke dalam satu folder bernama **Plate\_test** untuk keperluan pengujian. Di dalam folder tersebut juga terdapat dua file Python utama: `predict_ocr.py` dan `evaluate_cer.py`.

File `predict_ocr.py` berfungsi untuk mengolah gambar-gambar dalam folder *test* dan menghasilkan file CSV berisi kolom: **image**, **ground\_truth**, **prediction**, dan **CER\_score**. Proses dalam file ini mencakup pembacaan setiap gambar, permintaan prediksi teks dari model LLaVA yang sudah di-load di LM Studio, serta perhitungan skor Character Error Rate (CER) untuk tiap hasil prediksi. CER dihitung dengan rumus:
**CER = (S + D + I) / N**,
dengan **S** adalah jumlah karakter yang salah (substitusi), **D** adalah jumlah karakter yang dihapus (deletion), **I** adalah jumlah karakter yang disisipkan (insertion), dan **N** adalah jumlah total karakter pada ground truth.

File kedua, `evaluate_cer.py`, digunakan untuk membaca file CSV hasil dari `predict_ocr.py`, kemudian menghitung dan menampilkan nilai CER secara keseluruhan dari seluruh gambar uji. Ini memberikan evaluasi kuantitatif terhadap performa model OCR yang digunakan.

Sebelum menjalankan skrip, pengguna perlu membuka LM Studio dan memuat (load) model **llava-llama-3-8b-v1\_1**. Setelah itu, buka *Windows PowerShell*, masuk ke direktori proyek, dan jalankan perintah `py predict_ocr.py` untuk memulai prediksi. Selanjutnya, aktifkan server LM Studio dengan perintah `lms server start`. Setelah server aktif, jalankan `py evaluate_cer.py` untuk menghitung dan menampilkan hasil evaluasi akhir menggunakan CER. Dengan proses ini, model akan menjalankan prediksi OCR pada gambar-gambar plat nomor dan mengevaluasi akurasinya secara otomatis.
