#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick translation script for .ts files
"""

translations = {
    "File": "Dosya",
    "Project": "Proje",
    "Commands": "Komutlar",
    "New": "Yeni",
    "Open...": "Aç...",
    "Save": "Kaydet",
    "Save As...": "Farklı Kaydet...",
    "Exit": "Çıkış",
    "Update Repo": "Repo Güncelle",
    "Packages...": "Paketler...",
    "Languages...": "Diller...",
    "Make Image": "İmaj Oluştur",
    "Make Repo": "Repo Oluştur",
    "Check Repo": "Repo Kontrol",
    "Make Live": "Live Oluştur",
    "Pack Live": "Live Paketle",
    "Make Iso": "ISO Oluştur",
    "Repository": "Depo",
    "Browse": "Gözat",
    "Release files": "Sürüm dosyaları",
    "Plugin package": "Eklenti paketi",
    "Work folder": "Çalışma klasörü",
    "Image type": "İmaj tipi",
    "Installation Image": "Kurulum İmajı",
    "Live Image": "Canlı İmaj",
    "Add": "Ekle",
    "Remove": "Kaldır",
    "Modify": "Düzenle",
    "Set as Default": "Varsayılan Yap",
    "Languages": "Diller",
    "Available:": "Mevcut:",
    "Selected:": "Seçili:",
    "Packages": "Paketler",
    "Component": "Bileşen",
    "All Packages": "Tüm Paketler",
    "Selected Packages": "Seçili Paketler",
    "Component Packages": "Bileşen Paketleri",
    "Package": "Paket",
    "Size": "Boyut",
    "Version": "Sürüm",
    "Release": "Yayın",
    "Total Size:": "Toplam Boyut:",
    "Dialog": "İletişim",
    "Title:": "Başlık:",
    "Description:": "Açıklama:",
    "No Icon": "İkon Yok",
    "Select Photo": "Fotoğraf Seç",
    "Clear Photo": "Fotoğrafı Temizle",
    "Terminal": "Terminal",
    "Missing Packages": "Eksik Paketler",
    "Check": "Kontrol",
    "Remove Missing Packages": "Eksik Paketleri Kaldır",
    "Installation Collections": "Kurulum Koleksiyonları",
    "Collection Base": "Koleksiyon Tabanı",
    "Icon Selection": "İkon Seçimi",
    "Remove Icon": "İkonu Kaldır",
    "Add Icon": "İkon Ekle",
    "Repo Name": "Depo Adı",
    "Repo Address": "Depo Adresi",
    "Ok": "Tamam",
    "Cancel": "İptal",
    "Name": "İsim",
    "Address": "Adres",
    "Form": "Form",
    "Image title": "İmaj başlığı",
    "Extra parameters": "Ekstra parametreler",
    "Image Title": "İmaj Başlığı",
    "Live iso repo": "Canlı iso deposu",
}

import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print("Usage: python translate_ts.py <ts_file>")
    sys.exit(1)

ts_file = sys.argv[1]

# Parse the .ts file
tree = ET.parse(ts_file)
root = tree.getroot()

# Find all messages and translate them
translated_count = 0
for context in root.findall('context'):
    for message in context.findall('message'):
        source = message.find('source')
        translation = message.find('translation')
        
        if source is not None and translation is not None:
            source_text = source.text
            if source_text in translations:
                translation.text = translations[source_text]
                if 'type' in translation.attrib:
                    del translation.attrib['type']
                translated_count += 1

# Write back
tree.write(ts_file, encoding='utf-8', xml_declaration=True)
print(f"Translated {translated_count} strings")
