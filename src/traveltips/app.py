import toga

from toga.style import Pack
from toga.style.pack import COLUMN, BOLD, RIGHT, CENTER


class Currency:
    def __init__(self, name, symbol, forex, format='%.2f'):
        self.name = name
        self.symbol = symbol
        self.forex = forex
        self.format = format

    def __str__(self):
        if self.symbol:
            return '{} ({})'.format(self.name, self.symbol)
        else:
            return self.name


CURRENCIES = [
    # forex is the value of USD1 in the currency
    # Last updated May 1 2025
    # https://www.xe.com/en-au/currencyconverter/convert/?Amount=1&From=USD&To=AUD
    Currency('AU Dollars', symbol='$', forex=1.56),
    Currency('AE Dirham', symbol=None, forex=3.67),
    Currency('AR Peso', symbol=None, forex=1172.06, format='%.0f'),
    Currency('BR Real', symbol='R$', forex=5.67, format='%.0f'),
    Currency('CA Dollars', symbol='$', forex=1.38),
    Currency('CH Franc', symbol='Fr.', forex=0.82),
    Currency('CN Yuan', symbol='¥', forex=7.27, format='%.0f'),
    Currency('CO Peso', symbol='$', forex=4247.16, format='%.0f'),
    Currency('CZ Koruna', symbol='Kč', forex=22.08, format='%.0f'),
    Currency('DA Krone', symbol='Kr', forex=6.60, format='%.0f'),
    Currency('ET Birr', symbol='Br', forex=134.55, format='%.0f'),
    Currency('Euro', symbol='€', forex=0.88),
    Currency('GB Pounds', symbol='£', forex=0.75),
    Currency('HK Dollars', symbol='$', forex=7.75, format='%.0f'),
    Currency('IN Rupee', symbol='₹', forex=84.57, format='%.0f'),
    Currency('ID Rupiah', symbol='Rp', forex=16580.0, format='%.0f'),
    Currency('IS Króna', symbol='kr', forex=128.97, format='%.0f'),
    Currency('IL New Shekel', symbol='₪', forex=3.63, format='%.0f'),
    Currency('JP Yen', symbol='¥', forex=144.16, format='%.0f'),
    Currency('KR Won', symbol='₩', forex=1429.54, format='%.0f'),
    Currency('MX Peso', symbol='$', forex=19.63, format='%.0f'),
    Currency('MY Ringgit', symbol='RM', forex=4.31, format='%.0f'),
    Currency('NZ Dollars', symbol='$', forex=1.68),
    Currency('PH Peso', symbol='₱', forex=55.82, format='%.0f'),
    Currency('PL Złoty', symbol='zł', forex=3.79, format='%.0f'),
    Currency('RS Dinar', symbol='дин', forex=103.69, format='%.0f'),
    Currency('RU Ruble', symbol='₽', forex=82.08, format='%.0f'),
    Currency('SE Krona', symbol='kr', forex=9.69, format='%.0f'),
    Currency('SG Dollars', symbol='$', forex=1.30),
    Currency('TH Baht', symbol='฿', forex=33.50, format='%.0f'),
    Currency('TR Lira', symbol='₺', forex=38.52, format='%.0f'),
    Currency('TW Dollars', symbol='NT$', forex=32.08, format='%.0f'),
    Currency('US Dollars', symbol='$', forex=1.0),
    Currency('ZA Rand', symbol='R', forex=18.64),
]

FOREX = {
    str(currency): currency
    for currency in CURRENCIES
}


class TravelTips(toga.App):
    def calculate(self):
        try:
            self.my_tip_label.text = self.tip_rate.value

            value = float(self.amount.value)
            rate = int(self.tip_rate.value[:-1]) / 100.0
            local = FOREX[self.local_currency.value]
            my = FOREX[self.my_currency.value]
            self.tip.value = local.format % (value * rate)
            self.tip_total.value = local.format % (value * (rate + 1.0))

            my_amount = value / local.forex * my.forex
            self.my_amount.value = my.format % my_amount

            self.my_tip.value = my.format % (my_amount * rate)
            self.my_tip_total.value = my.format % (my_amount * (rate + 1.0))

        except (ValueError, TypeError):
            if self.amount.value:
                value = '?'
            else:
                value = ''

            self.tip.value = value
            self.tip_total.value = value

            self.my_amount.value = value

            self.my_tip.value = value
            self.my_tip_total.value = value

    def on_change(self, widget):
        self.calculate()

    def startup(self):
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(320, 568)
        )

        box = toga.Box(style=Pack(direction=COLUMN, margin=5))

        local_box = toga.Box(
            style=Pack(
                margin=(20, 0, 5, 0),
                align_items=CENTER
            )
        )
        local_box.add(toga.Label(
            'Local Currency:',
            style=Pack(
                flex=1,
                margin_right=5,
                font_size=14,
                font_weight=BOLD,
                text_align=RIGHT,
            )
        ))

        self.local_currency = toga.Selection(
            items=[str(c) for c in CURRENCIES],
            on_change=self.on_change,
            style=Pack(flex=1)
        )
        local_box.add(self.local_currency)

        box.add(local_box)

        self.amount = toga.NumberInput(
            on_change=self.on_change,
            min=0,
            step='0.01',
            style=Pack(
                font_size=48,
                text_align=RIGHT
            )
        )
        box.add(self.amount)

        tip_box = toga.Box(style=Pack(margin_top=10))

        self.tip_rate = toga.Selection(
            items=["20%", "15%", "10%"],
            on_change=self.on_change,
            style=Pack(flex=1)
        )
        tip_box.add(self.tip_rate)

        self.tip = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, margin_left=5, text_align=RIGHT)
        )
        tip_box.add(self.tip)

        self.tip_total = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, text_align=RIGHT)
        )
        tip_box.add(self.tip_total)

        box.add(tip_box)

        my_box = toga.Box(
            style=Pack(
                margin=(10, 0, 5, 0),
                align_items=CENTER
            )
        )
        my_box.add(toga.Label(
            'My Currency:',
            style=Pack(
                flex=1,
                margin_right=5,
                font_size=14,
                font_weight=BOLD,
                text_align=RIGHT
            )
        ))

        self.my_currency = toga.Selection(
            items=[str(c) for c in CURRENCIES],
            on_change=self.on_change,
            style=Pack(flex=1)
        )
        my_box.add(self.my_currency)

        box.add(my_box)

        self.my_amount = toga.TextInput(
            readonly=True,
            style=Pack(
                font_size=48,
                text_align=RIGHT
            )
        )
        box.add(self.my_amount)

        my_tip_box = toga.Box(style=Pack(margin_top=10))

        self.my_tip_label = toga.Label(
            '20%',
            style=Pack(flex=1, margin_left=5, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_label)

        self.my_tip = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, margin_left=5, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip)

        self.my_tip_total = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_total)

        box.add(my_tip_box)

        self.main_window.content = box
        self.main_window.show()


def main():
    return TravelTips()


if __name__ == '__main__':
    main().main_loop()
