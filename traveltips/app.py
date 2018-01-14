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
        return '{} ({})'.format(self.name, self.symbol)


CURRENCIES = [
    Currency('AU Dollars', symbol='$', forex=1.26),
    Currency('BR Real', symbol='R$', forex=3.21, format='%.0f'),
    Currency('CA Dollars', symbol='$', forex=1.25),
    Currency('CH Franc', symbol='Fr.', forex=0.97),
    Currency('CN Yuan', symbol='¥', forex=6.45, format='%.0f'),
    Currency('Euro', symbol='€', forex=0.82),
    Currency('GB Pounds', symbol='£', forex=0.73),
    Currency('HK Dollars', symbol='$', forex=7.82, format='%.0f'),
    Currency('ID Rupiah', symbol='Rp', forex=13323.50, format='%.0f'),
    Currency('JP Yen', symbol='¥', forex=111.06, format='%.0f'),
    Currency('MX Peso', symbol='$', forex=19.04, format='%.0f'),
    Currency('MY Ringgit', symbol='RM', forex=3.97, format='%.0f'),
    Currency('NZ Dollars', symbol='$', forex=1.38),
    Currency('TH Baht', symbol='฿', forex=31.88, format='%.0f'),
    Currency('US Dollars', symbol='$', forex=1.0),
]

FOREX = {
    str(currency): currency
    for currency in CURRENCIES
}


class TravelTips(toga.App):
    def calculate(self):
        try:
            value = float(self.amount.value)

            local = FOREX[self.local_currency.value]
            my = FOREX[self.my_currency.value]
            self.tip_10.value = local.format % (value * 0.1)
            self.tip_15.value = local.format % (value * 0.15)
            self.tip_20.value = local.format % (value * 0.2)

            my_amount = value / local.forex * my.forex
            self.my_amount.value = my.format % my_amount

            self.my_tip_10.value = my.format % (my_amount * 0.1)
            self.my_tip_15.value = my.format % (my_amount * 0.15)
            self.my_tip_20.value = my.format % (my_amount * 0.2)

        except ValueError:
            if self.amount.value:
                value = '?'
            else:
                value = ''

            self.tip_10.value = value
            self.tip_15.value = value
            self.tip_20.value = value

            self.my_amount.value = value

            self.my_tip_10.value = value
            self.my_tip_15.value = value
            self.my_tip_20.value = value

    def on_select(self, widget):
        self.calculate()

    def on_change(self, widget):
        self.calculate()

    def startup(self):
        self.main_window = toga.MainWindow(self.name, size=(320, 568))

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
            style=Pack(
                font_family='Helvetica',
                font_size=48,
                text_align=RIGHT
            )
        )
        box.add(self.amount)

        tip_label_box = toga.Box(style=Pack(padding_top=10))
        self.tip_label_10 = toga.Label(
            '10%',
            style=Pack(flex=1, text_align=RIGHT)
        )

        tip_label_box.add(self.tip_label_10)
        self.tip_label_15 = toga.Label(
            '15%',
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )

        tip_label_box.add(self.tip_label_15)
        self.tip_label_20 = toga.Label(
            '20%',
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )

        tip_label_box.add(self.tip_label_20)

        box.add(tip_label_box)

        tip_box = toga.Box(style=Pack())

        self.tip_10 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, text_align=RIGHT)
        )
        tip_box.add(self.tip_10)

        self.tip_15 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        tip_box.add(self.tip_15)

        self.tip_20 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        tip_box.add(self.tip_20)

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

        my_tip_label_box = toga.Box(style=Pack(padding_top=10))
        self.my_tip_label_10 = toga.Label(
            '10%',
            style=Pack(flex=1, text_align=RIGHT)
        )
        my_tip_label_box.add(self.my_tip_label_10)

        self.my_tip_label_15 = toga.Label(
            '15%',
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        my_tip_label_box.add(self.my_tip_label_15)

        self.my_tip_label_20 = toga.Label(
            '20%',
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        my_tip_label_box.add(self.my_tip_label_20)

        box.add(my_tip_label_box)

        my_tip_box = toga.Box(style=Pack())
        self.my_tip_10 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_10)
        self.my_tip_15 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_15)
        self.my_tip_20 = toga.TextInput(
            readonly=True,
            style=Pack(flex=1, padding_left=5, text_align=RIGHT)
        )
        my_tip_box.add(self.my_tip_20)

        box.add(my_tip_box)

        self.main_window.content = box
        self.main_window.show()


def main():
    return TravelTips('Travel Tips', 'com.keith-magee.traveltips')


if __name__ == '__main__':
    main().main_loop()
