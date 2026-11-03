import flet as ft
import shutil, os
from pathlib import Path

def get_size(p):
    try:
        path = Path(p)
        if not path.exists():
            return 0
        if path.is_file():
            return path.stat().st_size
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    except:
        return 0

def main(page: ft.Page):
    page.title = "Dark Gemini Purger"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    status_text = ft.Text("System stable. Awaiting purge.", color=ft.Colors.WHITE, size=16)

    def purge_click(e):
        status_text.value = "Purge protocol engaged..."
        page.update()

        targets = [
            Path.home() / ".cache",
            Path.home() / ".npm" / "_cacache",
            Path.home() / ".codex" / "cache",
            Path.home() / ".codex" / "tmp",
        ]
        
        total_freed = 0
        for t in targets:
            total_freed += get_size(t)
            try:
                if t.exists():
                    if t.is_dir():
                        shutil.rmtree(t, ignore_errors=True)
                    else:
                        t.unlink(missing_ok=True)
            except:
                pass
        
        freed_mb = total_freed / (1024*1024)
        status_text.value = f"PURGED! Freed {freed_mb:.2f} MB 🔥"
        page.update()

    page.add(
        ft.Icon(ft.Icons.DELETE_FOREVER, size=80, color=ft.Colors.RED_400),
        ft.Text("DARK GEMINI PURGER", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Container(height=20),
        status_text,
        ft.Container(height=20),
        ft.ElevatedButton(
            "EXECUTE PURGE",
            icon=ft.Icons.BOLT,
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
            width=200,
            height=50,
            on_click=purge_click
        )
    )

ft.app(target=main)

