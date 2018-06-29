#########################################################################
# FILE: bmi.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: calculates the bmi as boolean, if inside limits
#########################################################################

UPPER_BMI_BOUND = 24.9
LOWER_BMI_BOUND = 18.5

def is_normal_bmi(spells_per_hour, wand_length):
    '''Returns true if BMI is between certain bounds, and False if not.
    BMI calculated according to the given parameters.'''

    boolean = False
    BMI = int(spells_per_hour) / (float(wand_length) ** 2)

    if (BMI >= LOWER_BMI_BOUND) and (BMI <= UPPER_BMI_BOUND):
        boolean = True

    return boolean

