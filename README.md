# MTR Line Status for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Monitor the real-time status of Hong Kong MTR lines (Green / Yellow / Red) in Home Assistant.

數據來源： [MTR Line Status](https://www.mtr.com.hk/alert/ryg_line_status_lite.xml)

## Features

- 支援全部 10 條主要港鐵線路
- 每條線獨立 Sensor
- Overall Status 總體狀態 Sensor
- UI 設定（Config Flow），無需寫 YAML
- 可自訂更新間隔
- 支援 HACS

## Supported Lines

| Code | English Name              | 中文名稱     |
|------|---------------------------|--------------|
| TWL  | Tsuen Wan Line            | 荃灣綫       |
| KTL  | Kwun Tong Line            | 觀塘綫       |
| ISL  | Island Line               | 港島綫       |
| SIL  | South Island Line         | 南港島綫     |
| TKL  | Tseung Kwan O Line        | 將軍澳綫     |
| TCL  | Tung Chung Line           | 東涌綫       |
| DRL  | Disneyland Resort Line    | 迪士尼綫     |
| AEL  | Airport Express           | 機場快綫     |
| EAL  | East Rail Line            | 東鐵綫       |
| TML  | Tuen Ma Line              | 屯馬綫       |

## Installation

### HACS (Recommended)

1. 打開 HACS → Integrations
2. 右上角 ⋮ → **Custom repositories**
3. 輸入你的 GitHub repo 網址
4. Category 選擇 **Integration**
5. 搜尋 **MTR Line Status** → Download
6. 重啟 Home Assistant
7. 去 **Settings → Devices & Services → Add Integration** → 搜尋 **MTR Line Status**

### Manual Installation

1. 下載本 zip
2. 解壓後將 `custom_components/mtr_line_status` 資料夾複製到你的 Home Assistant `config/custom_components/` 目錄
3. 重啟 Home Assistant
4. 新增 Integration

## Configuration

安裝後直接透過 UI 新增即可，無需任何 YAML。

可在 Integration 的 **Configure** 調整更新間隔（預設 60 秒）。

## Entities

安裝後會自動產生：

- `sensor.mtr_line_status_overall_status`（總體狀態）
- 每條線一個 sensor

### Sensor States

- `green`：正常
- `yellow`：輕微延誤 / 服務調整
- `red`：嚴重延誤 / 暫停服務
- `unknown`：無法取得資料

### Attributes

每條線的 sensor 都有以下 attributes：

- `line_code`
- `name_en`
- `name_zh`
- `color`
- `last_update`

## Example Automation

```yaml
automation:
  - alias: "MTR 將軍澳綫有延誤通知"
    trigger:
      - platform: state
        entity_id: sensor.mtr_line_status_tseung_kwan_o_line_將軍澳綫
        to:
          - "yellow"
          - "red"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "港鐵延誤通知"
          message: "將軍澳綫目前狀態：{{ trigger.to_state.state }}"
```

## License

MIT
