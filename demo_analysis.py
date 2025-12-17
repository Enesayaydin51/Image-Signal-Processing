"""
PROJECT ANALYSIS MODULE
-----------------------
Bu script, proje kapsamında kullanılan görüntü işleme tekniklerinin (CLAHE, Power Law, Thresholding)
matematiksel etkilerini analiz etmek ve görselleştirmek amacıyla oluşturulmuştur.

Amaç:
1. İşlenmemiş (Raw) ve işlenmiş (Processed) görüntülerin histogram dağılımlarını karşılaştırmak.
2. Piksel yoğunluklarındaki değişimi (CDF) grafik üzerinde göstermek.
3. Hangi yöntemin veri seti üzerinde neden daha iyi çalıştığını kanıtlamak.
"""
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

def visualize_plot(subplot_1, subplot_2, image, hist, cdf_norm, text, figure_name):
    """
        Görüntüyü ve histogram/CDF grafiğini yan yana çizen yardımcı fonksiyon.
        Matplotlib RGB beklediği için renk dönüşümü kontrolü yapar.
        """
    plt.figure(num=f'{figure_name}')
    plt.subplot(subplot_1)
    plt.imshow(image, cmap='gray')
    plt.subplot(subplot_2)
    plt.plot(hist)
    plt.plot(cdf_norm, color='red')
    plt.xlabel(f'pixel intensity ({text})')
    plt.ylabel('number of pixels')

def calculate_hist(image):
    # Tek kanallı histogram hesaplar (Genel yoğunluk analizi için)
    return cv2.calcHist([image], [0], None, [256], [0, 256])
def calculate_cdf(hist):
    # Kümülatif Dağılım Fonksiyonu (Piksellerin birikimli artışı)
    return hist.cumsum()

def clahe():
    """
        CLAHE Yöntemi Analizi:
        Görüntüyü LAB formatına çevirip sadece L (Parlaklık) kanalına bölgesel eşitleme uygular.
        Standart Histogram Eşitleme'nin aksine gürültüyü (noise) artırmadan kontrastı düzeltir.
        """
    root = os.getcwd()
    img_path = os.path.join(root, 'dataset','deneme17.png')
    image = cv2.imread(img_path)

    if image is None:
        return print("Error: Image is not found. (CLAHE)")
    figure_name = "CLAHE Analysis Window"
    hist = calculate_hist(image)
    cdf = calculate_cdf(hist)
    cdf_norm = cdf * float(hist.max()) / cdf.max()

    visualize_plot(231, 234, image, hist, cdf_norm, "Before", figure_name)


    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    clahe_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    clahe_hist = calculate_hist(clahe_image)
    clahe_cdf = calculate_cdf(clahe_hist)
    clahe_cdf_norm = clahe_cdf * float(clahe_hist.max()) / clahe_cdf.max()

    visualize_plot(232, 235, clahe_image, clahe_hist, clahe_cdf_norm, "After clahe()", figure_name)
    plt.show()

def thresholding_enhancement():
    """
        Thresholding Analizi:
        Görüntüyü ön plandaki nesneler ve arka plan olarak ayırmak için kullanılır (Segmentasyon).
        Burada her renk kanalı (R, G, B) için ayrı ayrı Adaptive Threshold uygulanmıştır.
        """
    root = os.getcwd()
    img_path = os.path.join(root, 'dataset','deneme.jpg')
    image = cv2.imread(img_path)

    figure_name = "Thresholding Analysis Window"
    if image is None:
        return print("Error: Image is not found.(Thresholding_enhancement)")

    max_value = 255
    block_size = 11
    C=2

    hist = calculate_hist(image)
    cdf = calculate_cdf(hist)
    cdf_norm = cdf * float(hist.max()) / cdf.max()
    visualize_plot(231, 234, image, hist, cdf_norm, "Before", figure_name)

    b, g, r = cv2.split(image)

    b_thresh = cv2.adaptiveThreshold(b, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, block_size, C)
    g_thresh = cv2.adaptiveThreshold(g, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, block_size, C)
    r_thresh = cv2.adaptiveThreshold(r, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, block_size, C)


    enhanced_image = cv2.merge([b_thresh, g_thresh, r_thresh])

    equa_hist = calculate_hist(enhanced_image)
    equa_cdf = calculate_cdf(equa_hist)
    equa_cdf_norm = equa_cdf * float(equa_hist.max()) / equa_cdf.max()


    visualize_plot(232, 235, enhanced_image, equa_hist, equa_cdf_norm, "After thresholding_enhancement()", figure_name)
    plt.show()

def power_law_transformation():
    """
        Power Law (Gamma) Analizi:
        Piksel parlaklıklarını üssel bir fonksiyonla (s = c * r^gamma) değiştirir.
        Gamma < 1: Karanlık bölgeleri aydınlatır (Histogramı sağa çeker).
        Gamma > 1: Parlak bölgeleri koyultur.
        """
    root = os.getcwd()
    img_path = os.path.join(root, 'dataset','deneme19.png')
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return print("Error: Image is not found.(power_law_transformation)")

    figure_name = "Power Low Analysis Window"
    gamma = 0.5

    hist = calculate_hist(image)
    cdf = calculate_cdf(hist)
    cdf_norm = cdf * float(hist.max()) / cdf.max()
    visualize_plot(231, 234, image, hist, cdf_norm, "Before", figure_name)

    normalized = image.astype(np.float32) / 255.0
    enhanced = np.power(normalized, gamma)
    enhanced_image = (enhanced * 255).astype(np.uint8)

    equa_hist = calculate_hist(enhanced_image)
    equa_cdf = calculate_cdf(equa_hist)
    equa_cdf_norm = equa_cdf * float(equa_hist.max()) / equa_cdf.max()


    visualize_plot(232, 235, enhanced_image, equa_hist, equa_cdf_norm, "After power_law_transformation()", figure_name)
    plt.show()


if __name__ == '__main__':
    power_law_transformation()
    clahe()
    thresholding_enhancement()




