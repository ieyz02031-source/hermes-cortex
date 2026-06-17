# 电脑操控与视觉工具

## 工具清单

| 工具 | 位置 | 功能 |
|------|------|------|
| **mcp-windows** | D:/Hermes/tools/mcp-windows/Sbroenne.WindowsMcp.exe | UI Automation，按名字找元素 |
| **ai_computer.py** | D:/Hermes/tools/ai_computer.py | 截图+视觉分析+操控 |
| **ai_eyes_v2.py** | D:/Hermes/tools/ai_eyes_v2.py | 纯图片分析 |
| **computer_control.py** | D:/Hermes/tools/computer_control.py | 截图+分析+点击+输入 |

## 视觉模型

**当前使用**：nvidia vision API
- 模型：meta/llama-3.2-90b-vision-instruct
- 免费，90B参数
- 支持中英文，OCR，视觉问答

**vision_analyze bug**：hermes内置工具硬编码Gemma（GitHub #24842），返回403。
**解决方案**：用ai_computer.py或ai_eyes_v2.py直接调用nvidia API。

## mcp-windows 工具

| 工具 | 功能 |
|------|------|
| ui_find | 查找UI元素（按名字） |
| ui_click | 点击元素 |
| ui_type | 输入文字 |
| ui_read | 读取文字 |
| window_management | 窗口管理 |
| app | 启动应用 |
| keyboard_control | 键盘操作 |
| mouse_control | 鼠标操作 |
| screenshot_control | 截图（备用） |
| file_save | 保存文件 |

## 操控模式

| 模式 | 工具 | 截图？ | 适用场景 |
|------|------|--------|----------|
| **UI Automation** | mcp-windows | ❌ | 普通应用 |
| **视觉分析** | ai_computer.py | ✅ | 游戏、canvas |

**默认流程**：先UI Automation，失败才截图。

## 详细文档

详见 `computer-use/computer-control` skill。
