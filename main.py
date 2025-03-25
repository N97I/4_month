import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'Todo List'
    page.padding = 40
    page.bgcolor = ft.colors.GREY_600
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column(spacing=10)
    sort_by_date_desc = True
    sort_by_status = False

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks(sort_by_date_desc, sort_by_status)
        for task in tasks:
            task_list.controls.append(create_task_row(*task))
        page.update()

    def create_task_row(task_id, task_text, created_at, completed):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        date_text = ft.Text(value=f"🕒 {created_at}", color=ft.colors.GREY_400, size=12)
        completed_checkbox = ft.Checkbox(
            value=bool(completed), 
            on_change=lambda e: toggle_status(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            load_tasks()

        def delete_task(e):
            main_db.delete_task(task_id)
            load_tasks()

        return ft.Row([
            completed_checkbox,
            ft.Column([task_field, date_text], spacing=2),
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=delete_task)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value.strip():
            main_db.add_task(task_input.value)
            task_input.value = ""
            load_tasks()

    def toggle_status(task_id, new_status):
        main_db.update_task_status(task_id, new_status)
        load_tasks()

    def toggle_sort_by_date(e):
        nonlocal sort_by_date_desc
        sort_by_date_desc = not sort_by_date_desc
        sort_date_button.text = "📅 Новые выше" if sort_by_date_desc else "📅 Старые выше"
        load_tasks()

    def toggle_sort_by_status(e):
        nonlocal sort_by_status
        sort_by_status = not sort_by_status
        sort_status_button.text = "✅ Выполненные внизу" if sort_by_status else "✅ Выполненные вверху"
        load_tasks()

    task_input = ft.TextField(hint_text='Добавьте задачу', expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.icons.ADD)
    sort_date_button = ft.ElevatedButton("📅 Новые выше", on_click=toggle_sort_by_date, icon=ft.icons.DATE_RANGE)
    sort_status_button = ft.ElevatedButton("✅ Выполненные внизу", on_click=toggle_sort_by_status, icon=ft.icons.CHECK)

    page.add(
        ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([sort_date_button, sort_status_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            task_list
        ])
    )

    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)