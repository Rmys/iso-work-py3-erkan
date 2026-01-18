# Pisiman (Pisi ISO Creator)

[Turkish](#türkçe) | [English](#english)

---

## Türkçe

Pisi Linux için ISO imajları oluşturma araçları ve GUI arayüzü.

### Özet
Pisiman, Pisi Linux tabanlı canlı (live) ve kurulum (install) ISO'ları hazırlamak için kullanılan kapsamlı bir araç setidir. Modernize edilmiş yapısı ile artık **Python 3** ve **PyQt6** kullanmaktadır.

### Özellikler
- **Modern GUI:** PyQt6 tabanlı, dinamik arayüz yükleme (`uic`) mimarisi.
- **Sadeleştirilmiş XML:** Proje yapılandırmaları `PisimanProject` kök etiketi altında, tekilleştirilmiş paket listeleri ile yönetilir.
- **Dinamik Kaynak Yönetimi:** Arayüz derlemesi gerektirmez, doğrudan `.ui` dosyalarını kullanır. İkonlar doğrudan `ui/pics` klasöründen yüklenir.
- **Gelişmiş ISO Araçları:** EFI desteği, hybrid ISO (`xorriso`), overlayfs desteği ve modüler yapı.

### Gereksinimler
- Python 3.11+
- PyQt6
- Pisi (Paket yönetimi için)
- xorriso, squashfs-tools, mtools, grub, dosfstools
- Diğer bağımlılıklar için `required_packages.txt` dosyasına göz atın.

### Kurulum ve Kullanım

#### Başlatma
Uygulamayı GUI ile başlatmak için:
```sh
sudo ./pisiman.py
```

#### Komut Satırı Kullanımı
CLI üzerinden imaj oluşturmak için:
```sh
sudo ./pisiman.py make project-files/pisi-2.0-minimal.xml
```

#### Klasör Yapısı
- `app/repotools/`: ISO oluşturma mantığı (maker, project, iso_ops, image_ops vb.)
- `app/gui/`: PyQt6 arayüz dosyaları.
- `app/gui/ui/`: Arayüz tasarım dosyaları (.ui) ve görseller (pics/).
- `project-files/`: Örnek proje XML dosyaları.

### Modernizasyon Notları
Bu proje üzerinde yapılan son güncellemeler şunları içerir:
- Python 2'den Python 3'e tam geçiş.
- PyQt5'ten **PyQt6**'ya teknoloji yükseltmesi.
- `uic.loadUi` ile dinamik arayüz yükleme (derleme gerektirmez).
- `raw.qrc` ve `raw_rc.py` bağımlılıklarının kaldırılması.
- XML yapısında `InstallImagePackages` ve `PackageSelection` bölümlerinin birleştirilmesi.
- Proje isimlendirmesinin `PisimanProject` olarak standardize edilmesi.

---

## English

ISO image creation tools and GUI for Pisi Linux.

### Overview
Pisiman is a comprehensive toolset used to prepare live and install ISOs based on Pisi Linux. With its modernized structure, it now uses **Python 3** and **PyQt6**.

### Features
- **Modern GUI:** PyQt6-based, dynamic interface loading (`uic`) architecture.
- **Simplified XML:** Project configurations are managed under the `PisimanProject` root tag, with unified package lists.
- **Dynamic Resource Management:** No interface compilation required, uses `.ui` files directly. Icons are loaded directly from the `ui/pics` folder.
- **Advanced ISO Tools:** EFI support, hybrid ISO (`xorriso`), overlayfs support, and modular structure.

### Requirements
- Python 3.11+
- PyQt6
- Pisi (For package management)
- xorriso, squashfs-tools, mtools, grub, dosfstools
- Check `required_packages.txt` for other dependencies.

### Installation and Usage

#### Launching
To start the application with GUI:
```sh
sudo ./pisiman.py
```

#### Command Line Usage
To create an image via CLI:
```sh
sudo ./pisiman.py make project-files/pisi-2.0-minimal.xml
```

#### Directory Structure
- `app/repotools/`: ISO creation logic (maker, project, iso_ops, image_ops, etc.)
- `app/gui/`: PyQt6 interface files.
- `app/gui/ui/`: Interface design files (.ui) and images (pics/).
- `project-files/`: Example project XML files.

### Modernization Notes
Recent updates to this project include:
- Full migration from Python 2 to Python 3.
- Technology upgrade from PyQt5 to **PyQt6**.
- Dynamic UI loading with `uic.loadUi` (no compilation needed).
- Removal of `raw.qrc` and `raw_rc.py` dependencies.
- Merging `InstallImagePackages` and `PackageSelection` sections in XML.
- Standardization of project naming as `PisimanProject`.

---
*Pisiman is developed by the Pisi Linux community.*
