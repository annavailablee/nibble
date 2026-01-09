from plyer import notification

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Nibble",
        timeout=5
    )
