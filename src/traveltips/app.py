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
    # Last updated Jan 8 2020
    Currency('AU Dollars', symbol='$', forex=1.45),
    Currency('AE Dirham', symbol=None, forex=3.67),
    Currency('AR Peso', symbol=None, forex=59.75, format='%.0f'),
    Currency('BR Real', symbol='R$', forex=4.07, format='%.0f'),
    Currency('CA Dollars', symbol='$', forex=1.3),
    Currency('CH Franc', symbol='Fr.', forex=0.97),
    Currency('CN Yuan', symbol='¥', forex=6.95, format='%.0f'),
    Currency('CO Peso', symbol='$', forex=3276.0, format='%.0f'),
    Currency('DA Krone', symbol='Kr', forex=6.70, format='%.0f'),
    Currency('ET Birr', symbol='Br', forex=32.12, format='%.0f'),
    Currency('Euro', symbol='€', forex=0.9),
    Currency('GB Pounds', symbol='£', forex=0.76),
    Currency('HK Dollars', symbol='$', forex=7.78, format='%.0f'),
    Currency('IN Rupee', symbol='₹', forex=72.02, format='%.0f'),
    Currency('ID Rupiah', symbol='Rp', forex=13925.8, format='%.0f'),
    Currency('IS Króna', symbol='kr', forex=123.07, format='%.0f'),
    Currency('IL New Shekel', symbol='₪', forex=3.47, format='%.0f'),
    Currency('JP Yen', symbol='¥', forex=108.37, format='%.0f'),
    Currency('KR Won', symbol='₩', forex=1171.31, format='%.0f'),
    Currency('MX Peso', symbol='$', forex=18.9, format='%.0f'),
    Currency('MY Ringgit', symbol='RM', forex=4.11, format='%.0f'),
    Currency('NZ Dollars', symbol='$', forex=1.5),
    Currency('PH Peso', symbol='₱', forex=50.9, format='%.0f'),
    Currency('PL Złoty', symbol='zł', forex=3.81, format='%.0f'),
    Currency('RS Dinar', symbol='дин', forex=105.38, format='%.0f'),
    Currency('RU Ruble', symbol='₽', forex=3.81, format='%.0f'),
    Currency('SE Krona', symbol='kr', forex=9.45, format='%.0f'),
    Currency('SG Dollars', symbol='$', forex=1.35),
    Currency('TH Baht', symbol='฿', forex=30.27, format='%.0f'),
    Currency('TR Lira', symbol='₺', forex=5.96, format='%.0f'),
    Currency('TW Dollars', symbol='NT$', forex=30.06, format='%.0f'),
    Currency('US Dollars', symbol='$', forex=1.0),
    Currency('ZA Rand', symbol='R', forex=14.32),
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

        except (ValueError, TypeError) as e:
            if self.amount.value:
                value = '?'
            else:
                value = ''

            self.tip.value = value
            self.tip_total.value = value

            self.my_amount.value = value

            self.my_tip.value = value
            self.my_tip_total.value = value

    def on_select(self, widget):
        self.calculate()

    def on_change(self, widget):
        self.calculate()

    def startup(self):
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(320, 568)
        )

        box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        local_box = toga.Box(
            style=Pack(
                padding=(20, 0, 5, 0),
                alignment=CENTER
            )
        )
        local_box.add(toga.Label(
            'Local Currency:',
            style=Pack(
                width=120,
                padding_right=5,
                font_family='Helvetica',
                font_size=16,
                font_weight=BOLD,
                text_align=RIGHT,
            )
        ))

        self.local_currency = toga.Selection(
            items=[str(c) for c in CURRENCIES],
            on_select=self.on_select,
            style=Pack(flex=1)
        )
        local_box.add(self.local_currency)

        box.add(local_box)

        self.amount = toga.NumberInput(
            on_change=self.on_change,
            min_value=0,
            step='0.01',
            style=Pack(
                font_family='Helvetica',
                font_size=48,
                text_align=RIGHT
            )
        )
        box.add(self.amount)

        tip_box = toga.Box(style=Pack(padding_top=10))

        self.tip_rate = toga.Selection(
            items=["20%", "15%", "10%"],
            on_select=self.on_select,
            style=Pack(flex=1)
        )
        tip_box.add(self.tip_rate)

        self.tip = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
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
                padding=(10, 0, 5, 0),
                alignment=CENTER
            )
        )
        my_box.add(toga.Label(
            'My Currency:',
            style=Pack(
                width=120,
                padding_right=5,
                font_family='Helvetica',
                font_size=16,
                font_weight=BOLD,
                text_align=RIGHT
            )
        ))

        self.my_currency = toga.Selection(
            items=[str(c) for c in CURRENCIES],
            on_select=self.on_select,
            style=Pack(flex=1)
        )
        my_box.add(self.my_currency)

        box.add(my_box)

        self.my_amount = toga.TextInput(
            readonly=True,
            style=Pack(
                font_family='Helvetica',
                font_size=48,
                text_align=RIGHT
            )
        )
        box.add(self.my_amount)

        my_tip_box = toga.Box(style=Pack(padding_top=10))

        self.my_tip_label = toga.Label(
            '20%',
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_label)

        self.my_tip = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
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
