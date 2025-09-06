# ICS43434 Microphone Setup on Raspberry Pi

## 1. Compatibility

- **Raspberry Pi 5**: Not supported (overlay too complex, poor driver support)  
  ➤ Recommended: Use USB microphone instead  
- **Raspberry Pi 4**: Supported  
  ➤ Recommended OS: Raspberry Pi OS (Legacy, 64-bit)

---

## 2. System Preparation

1. Download and install Raspberry Pi Imager  
   🔗 https://www.raspberrypi.com/software/

2. Use the following options in Imager:
   - **Device**: Raspberry Pi 4
   - **OS**: Raspberry Pi OS (Other → Raspberry Pi OS (Legacy, 64-bit))

3. Flash to SD card, insert, and boot the Raspberry Pi

---

## 3. Hardware Wiring

```
ICS43434 Module      Raspberry Pi 4

VCC / 3V     →       3.3V
GND          →       GND
BCLK / SCK   →       BCM 18 / Pin 12
LRCL / WS    →       BCM 19 / Pin 35
DOUT / SD    →       BCM 20 / Pin 38
SEL          →       GND (Left channel)
               or    3.3V (Right channel)
```

---

## 4. Configuration

### Edit config file

```bash
sudo nano /boot/config.txt
# or (for some systems)
sudo nano /boot/firmware/config.txt
```

### Add the following lines at the end:

```
dtoverlay=googlevoicehat-soundcard
dtparam=i2s=on
```

### Save and reboot:

```bash
sudo reboot
```

---

## 5. Verification and Recording

### Check audio devices:

```bash
arecord -l
```

Expected output should include a card like:

```
card 1: voicehat [Voice HAT DAC], device 0: simple-card_codec_link [simple-card_codec_link]
```

### Record 10 seconds of stereo audio:

```bash
arecord -d 10 -f S32_LE -r 48000 -c 2 test-audio.wav
```

### Play back the recording:

```bash
aplay test-audio.wav
```

---

## 6. FAQ

### ❓ No device detected with `arecord -l`
- Make sure the following lines exist in `/boot/config.txt` or `/boot/firmware/config.txt`:
  ```
  dtoverlay=googlevoicehat-soundcard
  dtparam=i2s=on
  ```
- Then run:
  ```bash
  sudo reboot
  ```

### Recording is silent or empty？
- Check wiring: confirm **DOUT** is connected to **BCM 20 (Pin 38)**
- Ensure **SEL** is set properly:
  - `GND` → Left channel
  - `3.3V` → Right channel

### ICS43434 doesn't work on Raspberry Pi 5？
- Use a **USB microphone** instead
- Pi 5 has different device tree and overlay handling
- ICS43434 I2S input not officially supported on Pi 5 as of now

---

## 7. Notes

- `googlevoicehat-soundcard` overlay provides a universal I2S audio device compatible with ICS43434
- `arecord` format explanation:
  - `-f S32_LE` → Signed 32-bit Little Endian
  - `-r 48000` → 48kHz sample rate
  - `-c 2` → 2 channels (stereo)
