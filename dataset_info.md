# Veri Seti Toplama Rehberi

## 📸 Veri Seti Nedir?

Veri seti, projenizde test edeceğiniz **düşük ışıklı görüntülerden** oluşan bir koleksiyondur. Hocanız, yöntemlerinizi farklı görüntüler üzerinde test etmenizi ve sonuçları karşılaştırmanızı istiyor.

## 🎯 Toplanması Gereken Görüntü Türleri

### 1. **Farklı Işık Koşulları**
- Gece görüntüleri (çok karanlık)
- Alacakaranlık görüntüleri (orta karanlık)
- Kapalı alan görüntüleri (az ışık)
- Gölgeli alanlar

### 2. **Farklı İçerikler**
- İnsan portreleri
- Doğa/peyzaj görüntüleri
- Şehir/şehir manzaraları
- İç mekan görüntüleri
- Nesneler/objeler

### 3. **Farklı Çözünürlükler**
- Düşük çözünürlük (640x480, 800x600)
- Orta çözünürlük (1280x720, 1920x1080)
- Yüksek çözünürlük (daha büyük)

### 4. **Farklı Formatlar**
- JPG/JPEG
- PNG
- (İsteğe bağlı: RAW formatları)

## 📊 Önerilen Veri Seti Boyutu

- **Minimum**: 10-15 görüntü
- **İdeal**: 20-30 görüntü
- **Mükemmel**: 50+ görüntü

## 📁 Veri Seti Organizasyonu

Önerilen klasör yapısı:

```
projectSC/
├── dataset/
│   ├── low_light_images/
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   ├── image_003.jpg
│   │   └── ...
│   └── categories/  (opsiyonel)
│       ├── night/
│       ├── indoor/
│       ├── shadow/
│       └── ...
```

## 🔍 Görüntü Kaynakları

### 1. **Kendi Çektiğiniz Görüntüler**
- Telefon/kamera ile düşük ışıkta çekim
- Farklı senaryolar (gece, kapalı alan, vs.)

### 2. **Açık Kaynak Veri Setleri**
- **LOL Dataset** (Low-Light Dataset)
- **ExDark Dataset** (Extreme Dark Dataset)
- **SID Dataset** (See in the Dark)
- **MIT-Adobe FiveK Dataset**

### 3. **Online Kaynaklar**
- Unsplash (ücretsiz görüntüler)
- Pexels (ücretsiz görüntüler)
- Pixabay (ücretsiz görüntüler)
- **Not**: Telif hakkına dikkat edin!

## ✅ Veri Seti Kalite Kontrolü

Topladığınız görüntülerin:
- ✅ Gerçekten düşük ışıklı olması
- ✅ Net olması (çok bulanık olmamalı)
- ✅ Farklı içerikler içermesi
- ✅ Farklı zorluk seviyelerinde olması

## 📝 Veri Seti Dokümantasyonu

Her görüntü için şu bilgileri kaydedin:
- Görüntü adı/ID
- Çekim koşulları (gece, kapalı alan, vs.)
- Çözünürlük
- İçerik açıklaması
- Çekim tarihi (opsiyonel)

## 🚀 Sonraki Adımlar

1. **Görüntüleri toplayın** (10-30 görüntü)
2. **Klasör yapısını oluşturun**
3. **Görüntüleri organize edin**
4. **Veri seti işleme scriptini çalıştırın** (tüm görüntülere yöntemleri uygulayın)
5. **Sonuçları analiz edin ve raporlayın**

---

**Not**: Veri seti toplama, projenizin önemli bir parçasıdır. Farklı görüntüler üzerinde test yapmak, yöntemlerinizin ne kadar iyi çalıştığını göstermenize yardımcı olur.

