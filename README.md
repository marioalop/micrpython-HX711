# HX711 MicroPython Driver for ESP32

This project provides a MicroPython driver and usage example for the HX711 load cell amplifier connected to an ESP32. It supports reading from one or more load cells with basic tare and scale calibration.

## 📦 Features

- Raw and averaged readings
- Tare (zeroing)
- Scale factor calibration
- Multi-sensor support
- Compatible with ESP32 running MicroPython

---

## 🔌 Wiring Diagram

**Load Cell (4-wire)** → **HX711 module**

```
Green   (A+)  ─────────────▶  E+ (Signal +)  
Red     (E+)  ─────────────▶  E- (Excitation +)  
White   (A-)  ─────────────▶  A- (Signal -)  
Black   (E-)  ─────────────▶  A+ (Excitation -)
```

**HX711** should be connected to the ESP32 using GPIO pins for `DOUT` and `PD_SCK`.

---

## 📲 Example: Reading from 4 Load Cells

```python
from hx711 import HX711
import utime

def main():
    print("Starting...")
    hx1, hx2, hx3, hx4 = setup()
    run(hx1, hx2, hx3, hx4)

hx1 = HX711(5, 4)

# Perform tare (zero)
hx1.tare()
    
# Set arbitrary scale factor (to be calibrated)
hx1.set_scale(1000)
print("Setup done!")

print("Running...")
while True:
    t = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), t) < 500:
        print(hx1.instant_read())

```

---

## 🛠️ Calibration

You must calibrate each sensor individually using a known weight:

1. Call `.tare()` with no load.
2. Place a known weight on the load cell.
3. Adjust `.set_scale(scale)` until the reading matches the known weight.

---

## 📋 Requirements

- ESP32 with MicroPython firmware
- HX711 modules
- Load cells (4-wire)
- Proper 5V → 3.3V logic level conversion if necessary

---

## 📄 License

