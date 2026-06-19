# Manim Cloud IDE 🎬

A cloud-based development environment for creating mathematical animations with Manim.

## Features

- **Python 3.11** with Manim pre-installed
- **Beautiful IDE** with Monokai theme and JetBrains Mono font
- **FFmpeg & LaTeX** ready for rendering
- **Jupyter support** for interactive development
- **GitHub Codespaces** - code from anywhere in your browser

## Quick Start

### Option 1: Use GitHub Codespaces (Recommended)

1. **Create a new repository** on GitHub
2. **Push these files** to your repository:

   ```bash
   git init
   git add .
   git commit -m "Add Manim Cloud IDE configuration"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Open in Codespace**:
   - Go to your repository on GitHub
   - Click the green **"Code"** button
   - Select **"Create codespace"**
   - Wait for the environment to build (~5 minutes first time)

4. **Start coding!** The IDE will open in your browser with:
   - Python with Manim installed
   - All extensions pre-configured
   - Terminal ready for rendering

### Option 2: Use Locally with VS Code

1. Install the **"Dev Containers"** extension in VS Code
2. Press `F1` → **"Dev Containers: Open Folder in Container"**
3. Select this folder and wait for the container to build

## Rendering Manim

Once in the cloud IDE, render your scenes:

```bash
# Render a scene
manim -pql scene_example.py CircleToSquare

# High quality render
manim -pqh scene_example.py CircleToSquare

# With preview (opens video player)
manim -pql scene_example.py CircleToSquare --preview
```

### Render Commands

| Flag | Meaning |
|------|---------|
| `-p` | Play video after rendering |
| `-q` | Quality (`l`=720p, `m`=1080p, `h`=1440p, `k`=4K) |
| `-l` | Low quality (faster) |
| `--preview` | Open video player after render |

## Project Structure

```
.
├── .devcontainer/         # Codespace configuration
│   ├── devcontainer.json # Main settings
│   └── Dockerfile        # Container definition
├── .vscode/               # VS Code settings
│   ├── settings.json    # Editor configuration
│   └── extensions.json  # Recommended extensions
├── requirements.txt      # Python dependencies
├── scene_example.py      # Example Manim scenes
└── MANIM_CLOUD_IDE.md    # This file
```

## Customization

### Change the Theme

Edit `.vscode/settings.json`:
```json
"workbench.colorTheme": "Monokai"  // Try: "One Dark Pro", "Dracula", "SynthWave"
```

### Add More Extensions

Edit `.devcontainer/devcontainer.json` and add extensions to the `extensions` array.

### Adjust System Resources

In GitHub Codespaces, you can select:
- **2 cores, 4GB RAM** (default)
- **4 cores, 8GB RAM** (for faster rendering)
- **8 cores, 16GB RAM** (for complex animations)

Click your profile → **Codespaces** → **Configure** to adjust.

## Tips

1. **Use Jupyter cells** in `.py` files for interactive development:
   ```python
   # %% [markdown]
   # This is a markdown cell

   # %%
   from manim import *
   ```

2. **Preview rendered videos** using the `--preview` flag

3. **Download rendered videos** from the Files panel (right-click → Download)

4. **Save your work** - codespaces persist but create backups in GitHub

## Troubleshooting

### Slow rendering?
- Upgrade to more cores in codespace settings
- Use lower quality (`-ql`) while developing

### LaTeX errors?
- Make sure `texlive-latex-extra` is installed
- Check the log output for specific missing packages

### Missing fonts?
- Run `fc-cache -fv` to refresh font cache
- The container includes Liberation and CMU fonts

## License

MIT License - Feel free to use and modify!