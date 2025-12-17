# Dataset Collection Guide

## 📸 What Is a Dataset?

A dataset is a collection of **low-light images** that you will test in your project. Your instructor expects you to test your methods on different images and compare the results.

## 🎯 Types of Images to Be Collected

### 1. **Different Lighting Conditions**
- Night images (very dark)
- Twilight images (moderately dark)
- Indoor images (low light)
- Shadowed areas

### 2. **Different Content Types**
- Human portraits
- Nature / landscape images
- City / cityscape images
- Indoor scene images
- Objects / items

### 3. **Different Resolutions**
- Low resolution (640×480, 800×600)
- Medium resolution (1280×720, 1920×1080)
- High resolution (larger sizes)

### 4. **Different Formats**
- JPG / JPEG
- PNG
- (Optional: RAW formats)

## 📊 Recommended Dataset Size

- **Minimum**: 10–15 images
- **Ideal**: 20–30 images
- **Excellent**: 50+ images

## 📁 Dataset Organization

Recommended folder structure:

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


## 🔍 Image Sources

### 1. **Images You Capture Yourself**
- Photos taken with a phone/camera in low-light conditions
- Different scenarios (night, indoor, etc.)

### 2. **Open-Source Datasets**
- **LOL Dataset** (Low-Light Dataset)
- **ExDark Dataset** (Extreme Dark Dataset)
- **SID Dataset** (See in the Dark)
- **MIT-Adobe FiveK Dataset**

### 3. **Online Resources**
- Unsplash (free images)
- Pexels (free images)
- Pixabay (free images)
- **Note**: Pay attention to copyright!

## ✅ Dataset Quality Control

Ensure that the collected images:
- ✅ Are genuinely low-light
- ✅ Are clear (not overly blurry)
- ✅ Contain diverse content
- ✅ Represent different difficulty levels

## 📝 Dataset Documentation

For each image, record the following information:
- Image name / ID
- Shooting conditions (night, indoor, etc.)
- Resolution
- Content description
- Capture date (optional)

## 🚀 Next Steps

1. **Collect images** (10–30 images)
2. **Create the folder structure**
3. **Organize the images**
4. **Run the dataset processing script** (apply methods to all images)
5. **Analyze and report the results**

---

**Note**: Dataset collection is a critical part of your project. Testing on diverse images helps demonstrate how well your methods perform.

