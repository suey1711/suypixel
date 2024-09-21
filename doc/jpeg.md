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
- ### Marker 0xFFDD
- ### Payload
    | name | length | value |
    |------|--------| ----- |
    | 数据长度 | 2bytes | 0x0004 |
    | MCU重新开始间隔 | 2bytes | n |

- ### MCU重新开始间隔
    -  设其值为n，则表示每n个MCU块就有一个RSTn标记
    -  第一个标记是RST0，第二个是RST1等，RST7后再从RST0重复

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