import tkinter as tk
from itertools import cycle


class Band(tk.Frame):
    values = {"black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4, "green": 5, "blue": 6, "violet": 7, "grey": 8,
              "white": 9}
    multipliers = {"black": 1, "brown": 10, "red": 100, "orange": 1000, "yellow": 10000, "green": 100000,
                   "blue": 1000000, "violet": 10000000, "gold": 0.1, "silver": 0.01}
    tolerances = {"brown": 1, "red": 2, "orange":3, "yellow":4, "green": 0.5, "blue": 0.25, "violet": 0.1, "grey": 0.05, "gold": 5,
                  "silver": 10}

    def __init__(self, master, trace, colour=None, **kwargs):
        super().__init__(master, **kwargs)
        self.trace = trace
        self.colours = cycle(("black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white", "gold", "silver"))
        self.colour = colour
        self.bind("<1>", self.nextcolour)

    def nextcolour(self, _):
        self.focus_set()
        self.colour = next(self.colours)
        self.trace()

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, new):
        self._colour = new
        if self._colour == "brown":
            self.config(bg="#78400c")
        else:
            self.config(bg=self._colour)

    @property
    def value(self):
        try:
            return Band.values[self.colour]
        except KeyError:
            raise ValueError(f"Colour {self.colour} does not map to a value")

    @property
    def multiplier(self):
        try:
            return Band.multipliers[self.colour]
        except KeyError:
            raise ValueError(f"Colour {self.colour} does not map to a multiplier")

    @property
    def tolerance(self):
        try:
            return Band.tolerances[self.colour]
        except KeyError:
            raise ValueError(f"Colour {self.colour} does not map to a tolerance")


class Resistor(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bandFrame = tk.Frame(self, bg="#f5dea9")
        self.bands = [Band(self.bandFrame, self.update_value, "#f5dea9", width=20, height=60, borderwidth=2, relief=tk.RAISED) for x in range(4)]
        self.text = tk.StringVar()
        self.text.set("Click a band to cycle colours")
        for b in self.bands:
            b.pack(side=tk.LEFT, padx=10)
        self.bandFrame.pack(padx=20)
        tk.Label(self, textvariable=self.text).pack(pady=(10,5))

    def resistance(self):
        return (10*self.bands[0].value + self.bands[1].value) * self.bands[2].multiplier, self.bands[3].tolerance

    def update_value(self):
        try:
            r, t = self.resistance()
        except ValueError:
            self.text.set(f"Invalid Colour Code")
        else:
            if r >= 1000000:
                rout = str(r)[:-6] + "M"
            elif r >= 1000:
                rout = str(r)[:-3] + "k"
            else:
                rout = r
            self.text.set(f"{rout}Ω  ±{t}%")


if __name__ == "__main__":
    root = tk.Tk()
    r = Resistor(root)
    r.pack(padx=10, pady=10)
    root.mainloop()
