# Service Settings

## Sensor Service

```json
{
  "uuid": "00001812-0000-1000-8000-00805f9b34fb",
  "name": "Human Interface Device",
  "serviceName": "Sensor Service",
  "characteristics": [
    "PulseCharacteristic",
    "BodyTempCharacteristic",
    "GSRCharacteristic",
    "TempHumidCharacteristic"
  ],
  "mode": ["write", "notify"]
}
```

```json
{
  "characteristic": "Pulse Characteristic",
  "uuid": "00000540-0000-1000-8000-00805f9b34fb",
  "descriptor": "tbd"
}
```

```json
{
  "characteristic": "BodyTemp Characteristic",
  "uuid": "00000541-0000-1000-8000-00805f9b34fb",
  "descriptor": "tbd"
}
```

```json
{
  "characteristic": "GSR Characteristic",
  "uuid": "00000542-0000-1000-8000-00805f9b34fb",
  "descriptor": "tbd"
}
```

```json
{
  "characteristic": "TempHumid Characteristic",
  "uuid": "00000543-0000-1000-8000-00805f9b34fb",
  "descriptor": "tbd"
}
```

## Alert Service

```json
{
  "uuid": "00001802-0000-1000-8000-00805f9b34fb",
  "name": "Immediate Alert",
  "serviceName": "GPIO Alert Service",
  "characteristics": ["AlertCharacteristic"],
  "mode": ["write", "notify"]
}
```

```json
{
  "characteristic": "Alert Characteristic",
  "uuid": "00002a06-0000-1000-8000-00805f9b34fb",
  "descriptor": "tbd"
}
```
