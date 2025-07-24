# HR Appraisal Custom Tab Module

## Deskripsi
Module ini menambahkan tab baru bernama "Informasi Tambahan" pada form hr.appraisal di Odoo 18.

## Fitur
- Tab baru "Informasi Tambahan" pada form appraisal
- Custom fields:
  - Catatan Tambahan (Text)
  - Penilaian Custom (Selection)
  - Tanggal Custom (Date)
  - Opsi Tambahan (Boolean)
  - User Custom (Many2one)
  - Ringkasan (Computed)

## Instalasi
1. Copy folder `hr_appraisal_custom` ke dalam folder `custom/` di direktori Odoo
2. Restart Odoo service
3. Aktifkan module melalui Apps menu
4. Cari "HR Appraisal Custom Tab" dan install

## Penggunaan
Setelah module terinstall, tab baru "Informasi Tambahan" akan muncul di form hr.appraisal.

## Struktur File
```
hr_appraisal_custom/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── hr_appraisal.py
├── views/
│   └── hr_appraisal_views.xml
├── security/
│   └── ir.model.access.csv
├── i18n/
│   └── id.po
└── README.md
```

## Dependencies
- hr_appraisal (built-in Odoo module)
