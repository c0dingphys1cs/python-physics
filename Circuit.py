# This code works as is. Some lines are commented out — leftovers from trial and error.
!pip install schemdraw --quiet

# Run this pip
# First cell: !pip install schemdraw --quiet
# Then run below code

import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(show=False) as d:
    d.config(unit=2.5)

# Photodiode, oriented so cathode points up toward the op-amp input
    d += (PD := elm.Photodiode().up().label('Photodiode\n(at fringe output)', loc='bottom'))

# Ground at the bottom of the photodiode
    d += elm.Ground().at(PD.start)


# Wire from photodiode top to the op-amp's inverting input
#d += elm.Line().right().length(1.5)
    d += elm.Line().at(PD.end).right().length(0.5).to(op.in1)


# Op-amp (transimpedance configuration)
    d += (op := elm.Opamp().right().anchor('in2').anchor('in1').label('Op-Amp', loc='bottom'))


# Feedback resistor Rf from output back to inverting input
    d += elm.Line().at(op.in1).left().length(0.5)
    d += elm.Line().up().length(1)
    d += (R :=elm.Resistor().right().label('Rf\n100k–1M', loc='left'))
    d += elm.Line().at(R.end).right().length(0.9)
    d += elm.Line().down().to(op.out)


# Feedback capacitor Cf in parallel with Rf (drawn slightly offset)
    d += elm.Line().at(op.in1).left().length(0.5)
    d += elm.Line().up().length(1.5)
    d += elm.Capacitor().right().length(2.6).theta(15).label('Cf\n~5–20pF', loc='top').to(op.out)
    d += elm.Line().down().to(op.out).length(2.5).theta(-15)

# Non-inverting input tied to ground
    d += elm.Line().at(op.in2).left().length(0.5)
    d += elm.Line().down().length (1.4)
    d += elm.Ground()
#d += elm.Ground()
#d += elm.Line().at(op.in2).down()
#d += elm.Line().down().at(op.in2)

# Output wire continuing to the next stage
    d += elm.Line().at(op.out).right().length(1.5)
    d += elm.Dot(open=True).label('To ADC', loc='right')

#d.save('/mnt/user-data/outputs/tia_schematic.png', dpi=200)
    d.save('tia_schematic.png', dpi=200)

    print("Schematic saved.")

   # from IPython.display import Image( run separately)
   # Image('tia_schematic.png')

from IPython.display import Image
Image('tia_schematic.png')
