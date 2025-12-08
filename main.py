"""
Contrast Adjustment Techniques for Low-Light Images
Bu proje düşük ışıklı görüntüler için farklı kontrast artırma tekniklerini içerir.

Kullanım:
    python main.py                    # Veri setini işle
    python main.py --create           # Klasör yapısını oluştur
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================================
# KONTRAST ARTIRMA FONKSİYONLARI
# ============================================================================

def power_law_transformation(image, gamma=1.5):
    """
    Power-Law Transformation (Gamma Correction) ile kontrast artırma
    Bu yöntem: Enes tarafından implement edilmiştir.
    
    Parametreler:
    ------------
    image : numpy.ndarray
        Giriş görüntüsü (BGR formatında)
    gamma : float
        Gamma değeri. gamma < 1: parlaklık artar, gamma > 1: parlaklık azalır
    
    Döndürür:
    --------
    enhanced_image : numpy.ndarray
        Kontrast artırılmış görüntü
    """
    # Görüntüyü 0-1 aralığına normalize et
    normalized = image.astype(np.float32) / 255.0
    
    # Power-law transformation uygula: s = c * r^gamma
    # Burada c=1 alıyoruz
    enhanced = np.power(normalized, gamma)
    
    # Tekrar 0-255 aralığına dönüştür
    enhanced_image = (enhanced * 255).astype(np.uint8)
    
    return enhanced_image


def clahe_enhancement(image):
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) ile kontrast artırma
    Bu yöntem görüntünün lokal histogramını eşitleyerek kontrastı artırır ve
    aşırı parlaklık oluşumunu sınırlar.

    Parametreler:
    ------------
    image : numpy.ndarray
        Giriş görüntüsü (BGR formatında)

    Döndürür:
    --------
    enhanced_image : numpy.ndarray
        CLAHE uygulanmış kontrast artırılmış görüntü
    """

    # Renkli görüntüyü LAB renk uzayına çevir
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # CLAHE objesi oluştur (clipLimit ve tileGridSize parametreleri ayarlanabilir)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    # Sadece parlaklık (L) kanalına CLAHE uygula
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])

    # LAB renk uzayından tekrar BGR'ye çevir
    clahe_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return clahe_image


def thresholding_enhancement(image, threshold_type='adaptive', max_value=255, block_size=11, C=2):
    """
    Thresholding ile kontrast artırma
    Bu yöntem eşik değeri (threshold) kullanarak kontrastı artırır.
    
    Parametreler:
    ------------
    image : numpy.ndarray
        Giriş görüntüsü (BGR formatında)
    threshold_type : str
        Threshold tipi: 'adaptive', 'otsu', veya 'binary' (varsayılan: 'adaptive')
    max_value : int
        Maksimum piksel değeri (varsayılan: 255)
    block_size : int
        Adaptive threshold için blok boyutu (varsayılan: 11, tek sayı olmalı)
    C : int
        Adaptive threshold için sabit değer (varsayılan: 2)
    
    Döndürür:
    --------
    enhanced_image : numpy.ndarray
        Kontrast artırılmış görüntü
    """
    # Yöntem: Her BGR kanalına ayrı ayrı thresholding uygula
    # Bu yöntem renkli görüntüler için daha iyi sonuç verir
    b, g, r = cv2.split(image)
    
    if threshold_type == 'adaptive':
        b_thresh = cv2.adaptiveThreshold(b, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, block_size, C)
        g_thresh = cv2.adaptiveThreshold(g, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, block_size, C)
        r_thresh = cv2.adaptiveThreshold(r, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, block_size, C)
    elif threshold_type == 'otsu':
        _, b_thresh = cv2.threshold(b, 0, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, g_thresh = cv2.threshold(g, 0, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, r_thresh = cv2.threshold(r, 0, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:  # binary
        _, b_thresh = cv2.threshold(b, 127, max_value, cv2.THRESH_BINARY)
        _, g_thresh = cv2.threshold(g, 127, max_value, cv2.THRESH_BINARY)
        _, r_thresh = cv2.threshold(r, 127, max_value, cv2.THRESH_BINARY)
    
    enhanced_image = cv2.merge([b_thresh, g_thresh, r_thresh])
    return enhanced_image


def load_image(image_path):
    """
    Görüntüyü yükle
    
    Parametreler:
    ------------
    image_path : str
        Görüntü dosyasının yolu
    
    Döndürür:
    --------
    image : numpy.ndarray
        Yüklenen görüntü
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Görüntü yüklenemedi: {image_path}")
    return image


# ============================================================================
# VERİ SETİ İŞLEME FONKSİYONLARI
# ============================================================================

def create_comparison_image(original, power_law, histogram, thresholding, image_name, save_path):
    """
    Orijinal ve 3 yöntemin sonuçlarını yan yana gösteren karşılaştırma görseli oluşturur
    
    Parametreler:
    ------------
    original : numpy.ndarray
        Orijinal görüntü (BGR)
    power_law : numpy.ndarray
        Power-Law Transformation sonucu (BGR)
    clahe : numpy.ndarray
        Clahe Enhancement sonucu (BGR)
    thresholding : numpy.ndarray
        Thresholding sonucu (BGR)
    image_name : str
        Görüntü adı
    save_path : str
        Kayıt yolu
    """
    # BGR'den RGB'ye dönüştür (matplotlib için)
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    power_law_rgb = cv2.cvtColor(power_law, cv2.COLOR_BGR2RGB)
    clahe_rgb = cv2.cvtColor(histogram, cv2.COLOR_BGR2RGB)
    threshold_rgb = cv2.cvtColor(thresholding, cv2.COLOR_BGR2RGB)
    
    # 4 görseli yan yana göster
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    axes[0].imshow(original_rgb)
    axes[0].set_title('Orijinal', fontsize=14, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(power_law_rgb)
    axes[1].set_title('Power-Law (γ=0.5)', fontsize=14, fontweight='bold')
    axes[1].axis('off')
    
    axes[2].imshow(clahe_rgb)
    axes[2].set_title('Clahe Enhancement', fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    axes[3].imshow(threshold_rgb)
    axes[3].set_title('Thresholding (Adaptive)', fontsize=14, fontweight='bold')
    axes[3].axis('off')
    
    plt.suptitle(f'Karşılaştırma: {image_name}', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()  # Belleği temizle


def process_dataset(dataset_folder="dataset", output_folder="results/dataset_results"):
    """
    Veri setindeki tüm görüntülere kontrast artırma yöntemlerini uygular
    
    Parametreler:
    ------------
    dataset_folder : str
        Veri seti görüntülerinin bulunduğu klasör
    output_folder : str
        Sonuçların kaydedileceği klasör
    """
    # Klasörleri oluştur
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Alt klasörleri oluştur
    methods = ["power_law", "clahe", "thresholding"]
    for method in methods:
        Path(f"{output_folder}/{method}").mkdir(parents=True, exist_ok=True)
    
    # Karşılaştırma görselleri için klasör
    Path(f"{output_folder}/comparisons").mkdir(parents=True, exist_ok=True)
    
    # Desteklenen görüntü formatları
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    # Veri seti klasöründeki tüm görüntüleri bul
    image_files = []
    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(dataset_folder, file))
    else:
        print(f"Uyarı: '{dataset_folder}' klasörü bulunamadı!")
        print(f"Lutfen once veri seti klasorunu olusturun ve goruntuleri ekleyin.")
        print(f"Ornek: dataset/ klasorune goruntulerinizi koyun.")
        return
    
    if len(image_files) == 0:
        print(f"Uyarı: '{dataset_folder}' klasorunde goruntu bulunamadi!")
        return
    
    print(f"Veri Seti Isleme Baslatiliyor...")
    print(f"Klasor: {dataset_folder}")
    print(f"Toplam {len(image_files)} goruntu bulundu\n")
    
    # Her görüntüyü işle
    for idx, image_path in enumerate(image_files, 1):
        image_name = os.path.basename(image_path)
        image_name_no_ext = os.path.splitext(image_name)[0]
        
        print(f"[{idx}/{len(image_files)}] Isleniyor: {image_name}")
        
        try:
            # Görüntüyü yükle
            image = cv2.imread(image_path)
            if image is None:
                print(f"  Hata: Goruntu yuklenemedi: {image_name}")
                continue
            
            # 1. Power-Law Transformation (gamma=0.5)
            enhanced_power_law = power_law_transformation(image, gamma=0.5)
            cv2.imwrite(
                f"{output_folder}/power_law/{image_name_no_ext}_power_law.jpg",
                enhanced_power_law
            )
            
            # 2. Histogram Equalization
            enhanced_clahe = clahe_enhancement(image)
            cv2.imwrite(
                f"{output_folder}/clahe/{image_name_no_ext}_clahe.jpg",
                enhanced_clahe
            )
            
            # 3. Thresholding
            enhanced_threshold = thresholding_enhancement(image, threshold_type='adaptive')
            cv2.imwrite(
                f"{output_folder}/thresholding/{image_name_no_ext}_thresholding.jpg",
                enhanced_threshold
            )
            
            # Karşılaştırma görseli oluştur (Orijinal + 3 yöntem yan yana)
            create_comparison_image(
                image,
                enhanced_power_law,
                enhanced_clahe,
                enhanced_threshold,
                image_name_no_ext,
                f"{output_folder}/comparisons/{image_name_no_ext}_comparison.png"
            )
            
            print(f"  Tamamlandi: {image_name}")
            
        except Exception as e:
            print(f"  Hata: {image_name} - {str(e)}")
            continue
    
    print(f"\nIslem Tamamlandi!")
    print(f"Sonuclar: {output_folder}/")
    print(f"   ├── power_law/     ({len(image_files)} goruntu)")
    print(f"   ├── clahe/     ({len(image_files)} goruntu)")
    print(f"   ├── thresholding/  ({len(image_files)} goruntu)")
    print(f"   └── comparisons/   ({len(image_files)} karsilastirma gorseli)")


def create_sample_structure():
    """
    Örnek veri seti klasör yapısını oluşturur
    """
    folders = [
        "dataset",
        "results/dataset_results/power_law",
        "results/dataset_results/clahe",
        "results/dataset_results/thresholding",
        "results/dataset_results/comparisons"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    print("Klasor yapisi olusturuldu:")
    print("   dataset/  <- Goruntulerinizi buraya koyun")
    print("   results/dataset_results/   <- Sonuclar buraya kaydedilecek")


# ============================================================================
# ANA PROGRAM
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Eğer '--create' argümanı verilmişse klasör yapısını oluştur
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_sample_structure()
        print("\nSimdi goruntulerinizi 'dataset/' klasorune ekleyin")
        print("Sonra scripti tekrar calistirin: python main.py")
    else:
        # Veri setini işle
        process_dataset()

