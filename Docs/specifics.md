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

# Data

val1 = random.randint(1, 100)
val2 = random.randint(1, 100)
val3 = random.randint(0, 2)
val4 = random.randint(1, 100)
val4a = random.randint(1, 9)
val5 = random.randint(1, 100)
val6 = random.randint(1, 100)
val6a = random.randint(1, 9)

from integer/float -> convert to Binary
100 -> 1100100
2 -> 10

55.7 ->float
55 -> separate whole number
7 -> decimal
55 + (7/10) = 55 + .7 = 55.7
sending of floating point data

Byte array:
dbus.Array([dbus.Byte(46), dbus.Byte(60), dbus.Byte(0), dbus.Byte(1), dbus.Byte(55), dbus.Byte(7), dbus.Byte(73), dbus.Byte(1), dbus.Byte(68), dbus.Byte(5)], signature=dbus.Signature('y'))
