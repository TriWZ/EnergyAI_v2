# Triphorium 智能建筑能效平台（Streamlit 版）

本项目为建筑数字孪生 + 能耗分析 + 节能策略建议的一体化 AI 平台，适用于智能楼宇、数据中心、园区、商业综合体等场景。

## 🔧 快速启动

1. 克隆本仓库并安装依赖：

```bash
pip install -r requirements.txt
```

2. 新建 `.env` 文件：

```bash
cp .env.template .env
```

3. 运行平台：

```bash
streamlit run Triphorium_Hub.py
```

## 📦 模块说明

- `Triphorium_Hub.py`: 平台总入口导航页
- `Forecast.py` ~ `Assets.py`: 各子功能模块
- 所有页面支持上传数据后自动分析，部分页面可使用 OpenAI GPT 自动生成节能建议与 ESG 报告。

## ✅ 示例数据字段要求

上传的 CSV 应包含以下列之一：
- `timestamp`
- `electricity_kwh`
- `water_tons`
- `gas_m3`
- `co2_tons`

可选字段（如多项目分析）：`project`, `building_type`, 等。
