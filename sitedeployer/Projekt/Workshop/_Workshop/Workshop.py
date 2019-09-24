from sitedeployer.Projekt._Projekt.Projekt import Projekt


class Workshop(
    Projekt
):
    def __init__(self):
        Projekt.__init__(self)

    # names:
    def projekt(self) -> str:
        return 'workshop'
