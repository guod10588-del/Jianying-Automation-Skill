# Jianying UI Automation

## Preferred Tools

Use these on Windows:

- `pywinauto` for window discovery, focus, menus, and controls exposed through UI Automation.
- `pyautogui` for keyboard shortcuts, mouse clicks, screenshots, and template matching.
- Appium only when a stable Windows app automation setup already exists.

## Stability Hierarchy

Prefer actions in this order:

1. Native control selection through `pywinauto`.
2. Keyboard shortcuts and menu accelerators.
3. Image/template matching against screenshots.
4. Absolute coordinates only as a last resort.

## Common Flow

1. Start Jianying:

```powershell
Start-Process -FilePath "D:\JianyingPro\JianyingPro.exe" -ArgumentList "--src1","剪辑工具"
```

2. Wait for the main window.
3. Click or activate `开始创作`.
4. Import source media.
5. Select imported assets and place them on the timeline.
6. Import subtitle sidecar if available.
7. Trigger export.
8. Wait for export completion and verify the output file.

## Keyboard-First Operations

Useful shortcuts vary by Jianying version, so verify in the current UI. Common editing keys include:

- `Space`: play/pause.
- `Ctrl+B`: split/cut at playhead.
- `Backspace` or `Delete`: remove selected item.
- `Ctrl+A`: select all in focused panel.
- `Ctrl+S`: save draft if supported by the current version.

## Template Matching Tips

- Store screenshots of buttons at the same display scaling as the user's machine.
- Match small unique regions, not whole windows.
- After a click, verify the next UI state before continuing.
- Re-capture templates if Jianying updates, theme changes, or display scaling changes.

## Guardrails

- Do not automate deletion of existing timeline content unless the user explicitly requested it.
- Do not export over a user-provided final file; choose a new output name.
- Do not assume the active Jianying project is disposable.
- If a modal dialog appears unexpectedly, stop and report the state instead of blindly clicking.
