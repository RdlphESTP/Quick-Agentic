<picture>
  <source media="(prefers-color-scheme: dark)" srcset="public/logo_dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="public/logo_light.svg">
  <img alt="Quick-Agentic Logo" src="public/logo_light.svg">
</picture>

## Build environment with _uv_

```
uv sync
```

## Launch the _LangGraph_ server

```powershell
langgraph dev
```

## Launch the Agent

```powershell
uv run chainlit run app.py
```

## Customize UI

Replace **assets** in the `public/` directory. Change the **color theme** in `custom.css`
