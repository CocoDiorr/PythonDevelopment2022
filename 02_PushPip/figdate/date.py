from pyfiglet import Figlet
from datetime import datetime

def date(format="%Y %d %b, %A", font="graceful"):
    f = Figlet(font)
    return f.renderText(datetime.now().strftime(format))
