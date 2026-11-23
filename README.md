# MTR Line Status for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/Wereling1992/ha-mtr-line-status.svg)](https://github.com/Wereling1992/ha-mtr-line-status/releases)
[![License](https://img.shields.io/github/license/Wereling1992/ha-mtr-line-status.svg)](LICENSE)

Monitor the real-time status (Green / Yellow / Red) of Hong Kong MTR lines in Home Assistant.

## Features

- Supports all 10 major MTR lines
- One sensor per line (`green` / `yellow` / `red` / `unknown`)
- Provides both English and Chinese line names (`name_en` / `name_zh`)
- Last Update diagnostic sensor
- Fully UI-based setup (Config Flow) — no YAML required
- Configurable update interval (default: 60 seconds)
- HACS support

## Supported Lines

| Code | Line Name                 |
|------|---------------------------|
| TWL  | Tsuen Wan Line            |
| KTL  | Kwun Tong Line            |
| ISL  | Island Line               |
| SIL  | South Island Line         |
| TKL  | Tseung Kwan O Line        |
| TCL  | Tung Chung Line           |
| DRL  | Disneyland Resort Line    |
| AEL  | Airport Express           |
| EAL  | East Rail Line            |
| TML  | Tuen Ma Line              |

## Installation

### HACS (Recommended)

1. Open **HACS** → **Integrations**
2. Click the three dots (⋮) in the top right → **Custom repositories**
3. Add the following repository and select category **Integration**:
   ```
   https://github.com/Wereling1992/ha-mtr-line-status
   ```
4. Search for **MTR Line Status** and download it
5. Restart Home Assistant
6. Go to **Settings → Devices & services → Add Integration** and search for **MTR Line Status**

### Manual Installation

1. Download the latest [Release](https://github.com/Wereling1992/ha-mtr-line-status/releases)
2. Copy the `custom_components/mtr_line_status` folder into your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant
4. Add the integration from the UI

## Configuration

After installation, you can change the update interval via the integration's **Configure** option (default is 60 seconds).

No YAML configuration is required.

## Entities

The integration creates a device named **MTR Line Status** with the following entities:

**Sensors**
- One sensor for each MTR line  
  Possible states: `green`, `yellow`, `red`, `unknown`

**Diagnostic**
- `sensor.mtr_line_status_last_update` — Timestamp of the last successful data update

### Attributes (per line sensor)

| Attribute   | Description                  |
|-------------|------------------------------|
| `line_code` | Line code (e.g. `TKL`)       |
| `name_en`   | English name of the line     |
| `name_zh`   | Chinese name of the line     |
| `color`     | Official line color          |

## Example Automation

```yaml
automation:
  - alias: "Notify on Tseung Kwan O Line disruption"
    trigger:
      - platform: state
        entity_id: sensor.mtr_line_status_tseung_kwan_o_line
        to:
          - "yellow"
          - "red"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "MTR Alert"
          message: "Tseung Kwan O Line status: {{ trigger.to_state.state }}"
```

## Notes

- Data is fetched directly from the official MTR XML feed. Update frequency depends on the official source.
- It is recommended not to set the update interval lower than 30 seconds to avoid excessive requests.
- If a sensor shows `unknown`, it usually means the data could not be retrieved temporarily.

## License

MIT
