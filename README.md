# MTR Line Status for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/Wereling1992/ha-mtr-line-status.svg)](https://github.com/Wereling1992/ha-mtr-line-status/releases)

Monitor the real-time status of Hong Kong MTR lines (Green / Yellow / Red) in Home Assistant.

Data source: [MTR Line Status](https://www.mtr.com.hk/alert/ryg_line_status_lite.xml)

## Features

- All 10 major MTR lines
- One sensor per line
- Last Update diagnostic sensor (`lastBuildDate`)
- UI setup (Config Flow), no YAML required
- Configurable update interval
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

1. Open HACS → Integrations
2. Menu (⋮) → **Custom repositories**
3. Add:
   ```
   https://github.com/Wereling1992/ha-mtr-line-status
   ```
   Category: **Integration**
4. Search **MTR Line Status** → Download
5. Restart Home Assistant
6. Go to **Settings → Devices & Services → Add Integration** → search **MTR Line Status**

### Manual Installation

1. Download this repo or the [latest Release](https://github.com/Wereling1992/ha-mtr-line-status/releases)
2. Copy `custom_components/mtr_line_status` into your Home Assistant `config/custom_components/` folder
3. Restart Home Assistant
4. Add the integration from the UI

## Configuration

No YAML needed. After install, use **Configure** on the integration to change the update interval (default 60 seconds).

## Entities

Creates a device **MTR Line Status** with:

**Sensors**
- One sensor per line (`green` / `yellow` / `red` / `unknown`)

**Diagnostic**
- Last Update (from the feed `lastBuildDate`)

### Attributes (per line)

- `line_code`
- `name_en`
- `name_zh`
- `color`

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

## License

MIT
