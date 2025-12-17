# Contrast Adjustment Techniques for Low-Light Images

Bu proje, düşük ışıklı görüntüler için farklı kontrast artırma tekniklerini karşılaştırmayı amaçlamaktadır.

## 📋 Proje Hakkında

Düşük ışıklı görüntülerde kontrast düşüktür ve görüntü kalitesi kötüleşir. Bu projede, görüntü kontrastını artırmak için üç farklı yöntem uygulanmaktadır:

1. **Power-Law Transformation (Gamma Correction)** - Ana yöntem
2. **CLAHE (Contrast Limited Adaptive Histogram Equalization)** - CLAHE ile kontrast eşitleme yöntemi
3. **Thresholding** - Eşik değeri yöntemi

## 🔧 Kurulum

### Gereksinimler

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız var:

```bash
pip install -r requirements.txt
```

### Gerekli Kütüphaneler

- `opencv-python` - Görüntü işleme için
- `numpy` - Sayısal hesaplamalar için
- `matplotlib` - Görselleştirme için

## 📁 Proje Yapısı

```
projectSC/
│
├── main.py                    # Ana Python dosyası (tüm fonksiyonlar)
├── demo_analysis.py           # Histogram ve CDF analiz grafikleri (Matematiksel analiz)
├── requirements.txt           # Gerekli kütüphaneler
├── README.md                  # Bu dosya
├── dataset_info.md            # Veri seti toplama rehberi
│
├── dataset/                   # Veri seti görüntüleri
│   └── *.jpg, *.png          # Düşük ışıklı görüntüler
│
└── results/                   # Sonuçlar (otomatik oluşturulur)
    └── dataset_results/
        ├── power_law/         # Power-Law Transformation sonuçları
        ├── clahe/             # CLAHE sonuçları
        ├── thresholding/      # Thresholding sonuçları
        └── comparisons/       # Karşılaştırma görselleri (orijinal + 3 yöntem)
```

## 🚀 Kullanım

### 1. Klasör Yapısını Oluşturma (İlk Kez)

```bash
python main.py --create
```

Bu komut gerekli klasörleri oluşturur.

### 2. Görüntüleri Hazırlama

Düşük ışıklı görüntülerinizi `dataset/` klasörüne ekleyin.

### 3. Veri Setini İşleme

Tüm görüntülere yöntemleri uygulayın:

```bash
python main.py
```
Seçilen görüntüler üzerinde yöntemleri uygulayıp, histogramlarını çizin:
```bash
python demo_analysis.py
```

Bu komut:
- `dataset/` klasöründeki tüm görüntüleri işler
- Her görüntü için 3 yöntem uygular
- Sonuçları `results/dataset_results/` klasörüne kaydeder
- Her görüntü için karşılaştırma görseli oluşturur (orijinal + 3 yöntem yan yana)

### Tek Görüntü İşleme

Eğer tek bir görüntü üzerinde test yapmak isterseniz:

```python
from main import (
    power_law_transformation,
    clahe_enhancement,
    thresholding_enhancement,
    load_image
)

# Görüntüyü yükle
image = load_image("your_image.jpg")

# Yöntemleri uygula
enhanced_power_law = power_law_transformation(image, gamma=0.5)
clahe_hist = clahe_enhancement(image)
enhanced_threshold = thresholding_enhancement(image, threshold_type='adaptive')
```
## 📈 Analiz ve Histogram Değerlendirmesi

Proje kapsamında sadece görüntü iyileştirme yapılmamış, aynı zamanda algoritmaların başarısı Histogram ve CDF (Cumulative Distribution Function) analizleriyle doğrulanmıştır. demo_analysis.py dosyası ile üretilen grafikler şunları kanıtlar:

- Kontrast Yayılımı: CLAHE ve Power-Law yöntemlerinin, dar bir alana sıkışmış piksel değerlerini (düşük kontrast) histogram üzerinde nasıl genişlettiği.

- Parlaklık Değişimi: Histogramın koyu bölgelerden (sol taraf) aydınlık bölgelere (sağ taraf) nasıl kaydırıldığı.

- CDF Doğrusallığı: İşlem sonrası CDF eğrisinin daha lineer hale gelmesi, görüntüdeki bilgi dağılımının dengelendiğini gösterir.

## 📖 Yöntemler

### 1. Power-Law Transformation (Gamma Correction)

**Uygulayan:** Enes Ayaydın

**Açıklama:**
Power-Law Transformation, görüntü kontrastını ayarlamak için kullanılan temel bir yöntemdir. Formülü:

```
s = c * r^γ
```

Burada:
- `s`: Çıkış piksel değeri
- `r`: Giriş piksel değeri
- `c`: Sabit (genellikle 1)
- `γ`: Gamma değeri

**Gamma Değerinin Etkisi:**
- `γ < 1`: Görüntüyü parlaklaştırır (düşük ışıklı görüntüler için uygun)
- `γ = 1`: Değişiklik yapmaz
- `γ > 1`: Görüntüyü koyulaştırır

**Kod İçinde:**
```python
enhanced = power_law_transformation(image, gamma=0.5)
```

**Test Edilen Gamma Değerleri:**
- γ = 0.2 (en parlak)
- γ = 0.5 (orta parlaklık)
- γ = 0.8 (hafif parlaklık)
- γ = 1.0 (orijinal)

### 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)

**Uygulayan:** Muhammed Enes Uluç

Burada:
- `clipLimit`: Kontrast artışı sınırlar
- `tileGridSize`: Görüntüyü küçük bölgelere ayırır

**Değerinin Etkisi:**
- ` 2.0 < clipLimit < 4.0`: Yüksek olursa kontrast artar, düşük olursa azalır
- ` 8,8 < tileGridSize < 16,16`: Küçükse lokal detay artar ama mozaik efekti oluşabilir, büyükse daha global ve yumuşak olur


**Açıklama:**
CLAHE, görüntüyü küçük bölgelere (tile) ayırarak her birinin histogramını ayrı ayrı eşitler. Böylece kontrast artırılır ve aşırı parlaklık oluşumu sınırlandırılır. Bu yöntem, düşük ışıklı görüntülerde detayların daha iyi görünmesini sağlar.

**Implementasyon:**
- LAB renk uzayına dönüştürülür
- Sadece L (Lightness) kanalına clahe eşitleme uygulanır
- Tekrar BGR renk uzayına dönüştürülür

**Kod İçinde:**
```python
enhanced = clahe_enhancement(image)
```

### 3. Thresholding

**Açıklama:**
Thresholding (Eşik Değeri), görüntüdeki pikselleri belirli bir eşik değerine göre ikili (binary) hale getirerek kontrastı artırır. Adaptive Thresholding, görüntünün farklı bölgeleri için farklı eşik değerleri kullanarak daha iyi sonuçlar verir.

**Thresholding Türleri:**
- **Adaptive Thresholding**: Her piksel için komşu piksellerin ortalamasına göre eşik değeri belirler
- **Otsu's Thresholding**: Otomatik olarak optimal eşik değerini belirler
- **Binary Thresholding**: Sabit bir eşik değeri kullanır

**Implementasyon:**
- Her BGR kanalına ayrı ayrı thresholding uygulanır
- Sonuçlar birleştirilerek renkli görüntü oluşturulur

**Parametreler:**
- `threshold_type`: 'adaptive', 'otsu', veya 'binary' (varsayılan: 'adaptive')
- `max_value`: Maksimum piksel değeri (varsayılan: 255)
- `block_size`: Adaptive threshold için blok boyutu (varsayılan: 11)
- `C`: Adaptive threshold için sabit değer (varsayılan: 2)

**Kod İçinde:**
```python
enhanced = thresholding_enhancement(image, threshold_type='adaptive', block_size=11, C=2)
```

## 🔍 Yöntem Karşılaştırması

| Yöntem                       | Avantajlar                                                                               | Dezavantajlar |
|------------------------------|------------------------------------------------------------------------------------------|---------------|
| **Power-Law Transformation** | Basit ve hızlı, parametre kontrolü kolay, gamma değeri ile ince ayar yapılabilir         | Global uygulama, yerel detayları korumayabilir |
| **CLAHE**                    | Lokal kontrast arttırma, düşük ışıkta detayları iyi çıkarır, gürültüyü sınırlı arttırır. | Parametre ayarı gerekir (clipLimit, tileGridSize), küçük tileGridSize ile mozaik efekti oluşabilir.
| **Thresholding**             | İkili görüntü oluşturur, kenar tespiti için uygun, hızlı, adaptif                        | Renk bilgisi kaybolur, sadece siyah-beyaz sonuç |

## 📊 Sonuçlar

### Veri Seti İşleme Sonuçları

`main.py` çalıştırıldığında:

1. **Her yöntem için ayrı klasörler:**
   - `results/dataset_results/power_law/` - Power-Law Transformation sonuçları
   - `results/dataset_results/clahe/` - CLAHE sonuçları
   - `results/dataset_results/thresholding/` - Thresholding sonuçları

2. **Karşılaştırma görselleri:**
   - `results/dataset_results/comparisons/` - Her görüntü için orijinal + 3 yöntem yan yana

### Örnek Çıktı

Her görüntü için 4'lü karşılaştırma görseli:
- Sol: Orijinal görüntü
- Sağ: Power-Law Transformation (γ=0.5)
- Sağ: Clahe Enhancement
- Sağ: Thresholding (Adaptive)

## 📸 Veri Seti

Proje, düşük ışıklı görüntülerden oluşan bir veri seti kullanmaktadır. Veri seti toplama rehberi için `dataset_info.md` dosyasına bakın.

**Önerilen Veri Seti:**
- 10-30 düşük ışıklı görüntü
- Farklı senaryolar (gece, kapalı alan, gölgeli alanlar)
- Farklı içerikler (portre, doğa, şehir, iç mekan)

## 📝 Dosya Açıklamaları

- **main.py**: Tüm kontrast artırma fonksiyonları ve veri seti işleme kodunu içeren ana dosya
- **requirements.txt**: Gerekli Python kütüphaneleri
- **dataset_info.md**: Veri seti toplama ve hazırlama rehberi
- **README.md**: Bu dosya

## 👥 Katkıda Bulunanlar

- **Enes Ayaydın** - Power-Law Transformation implementasyonu ve proje koordinasyonu
- **M. Enes Uluc** - Clahe Enhancement implementasyonu
- **Arkadaş 2** - Thresholding implementasyonu

## 🔗 Referanslar

1. Gonzalez, R. C., & Woods, R. E. (2017). *Digital Image Processing* (4th ed.). Pearson.
2. OpenCV Documentation: https://docs.opencv.org/
3. Thresholding Tutorial: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
4. Clahe Equalization: https://docs.opencv.org/4.x/d6/db6/classcv_1_1CLAHE.html

## 📝 Notlar

- Görüntü dosyası BGR formatında yüklenir (OpenCV standardı)
- Tüm görselleştirmeler RGB formatında gösterilir (matplotlib için)
- Gamma değerini ihtiyacınıza göre ayarlayabilirsiniz
- Farklı görüntüler için farklı parametreler daha iyi sonuç verebilir
- Veri seti işleme için `python main.py` komutunu kullanın

## 📄 Lisans

Bu proje eğitim amaçlıdır.

---

**İyi çalışmalar! 🚀**
