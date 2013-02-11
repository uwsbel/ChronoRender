import pymel.all as pm


# def show():
    # window = pm.window(title='Chrono::Render')
    # window.show()

# def close():
    # pm.deleteUI(window)


def setTextBoxText(tb):
    tb.text = pm.fileDialog()
    tb.insertText(tb.text)
