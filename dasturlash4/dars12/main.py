class Hayvon:
    def nafas_ol(self):
        print("nafas olyapman")

class It(Hayvon):       # Hayvondan meros oldi
    def hur(self):
        print("pashol naxxuy!")

class Mushuk(Hayvon):   # Hayvondan meros oldi
    def miyovla(self):
        print("Miyov!")

it = It()
it.nafas_ol()  # → "nafas olyapman" (merosdan)
it.hur()       # → "Vov-vov!"