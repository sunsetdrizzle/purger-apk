import flet as ft
import shutil, os
from pathlib import Path

def get_size(p):
    try:
        return sum(f.stat().st_size for f in Path(p).rglob('*') if f.is_file())
    except:
        return 0

def main(page: ft.Page):
    page.title = "Dark Gemini Purger"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    status_text = ft.Text("System stable. Awaiting purge command...", size=14, color=ft.colors.GREY_400)

    def purge_click(e):
        status_text.value = "Purge protocol engaged..."
        page.update()
        
        targets = [
            Path.home() / ".cache",
            Path.home() / ".npm" / "_cacache",
            Path.home() / ".codex" / "cache",
            Path.home() / ".codex" / "tmp"
        ]
        
        total_reclaimed = 0
        log_msgs = []
        for path in targets:
            if path.exists():
                size_before = get_size(path)
                try:
                    shutil.rmtree(path)
                    path.mkdir(parents=True, exist_ok=True)
                    reclaimed_mb = size_before / (1024 * 1024)
                    log_msgs.append(f"Purged: {path.name} ({reclaimed_mb:.2f} MB)")
                    total_reclaimed += size_before
                except Exception as ex:
                    log_msgs.append(f"Failed {path.name}: {ex}")
            else:
                log_msgs.append(f"Skipped: {path.name}")
                
        total_mb = total_reclaimed / (1024 * 1024)
        status_text.value = f"Success! Reclaimed {total_mb:.2f} MB.\n" + "\n".join(log_msgs)
        page.update()

    purge_btn = ft.ElevatedButton(
        text="PURGE DIGITAL DECAY",
        icon=ft.icons.CLEANING_SERVICES,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.RED_900,
        on_click=purge_click
    )

    page.add(
        ft.Text("DARK GEMINI PURGER", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.RED_400),
        ft.Container(height=10),
        status_text,
        ft.Container(height=20),
        purge_btn
    )

if __name__ == "__main__":
    ft.app(target=main)
