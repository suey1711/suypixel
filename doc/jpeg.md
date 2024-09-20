# Jpeg

## Segments

### SOI - Start of Image
- ### Marker 0xFFD8

### SOF0 - Baseline DCT-based JPEG
- ### Marker 0xFFC0

### SOF2 - Progressive DCT-based JPEG
- ### Marker 0xFFC2

### DHT - Define Huffman Tables
- ### Marker 0xFFC4

### DQT- Define Quantization Table
- ### Marker 0xFFDB

### DRI Define Restart Interval
- ### RST中的marker
- ### Marker 0xFFDD

### SOS - Start of Scan
- ### Marker 0xFFDA

### RSTn - Restart
- ### DRImarker中插入r个块
- ### Marker 0xFFDn

### APPn Application-specific
- ### Exif JPEG使用APP1, JFIF JPEG使用APP0
- ### Marker 0xFFEn

### COM - Comment 注释内容
- ### Marker 0xFFFE

### EOI - End of Image
- ### Marker 0xFFD9