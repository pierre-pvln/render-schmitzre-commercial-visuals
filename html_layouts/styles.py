# ############################################################################
#
# GEEN FUNCTIES/LOGICA UITVOEREN IN DIT BESTAND.
# ENKEL BEDOELD OM EEN LAYOUT ELEMENT TE DEFINIEREN
# AANPASSINGEN VIA CALLBACK OUTPUTS
#
# @version    v0.0.5  2022-11-20
# @author     pierre@ipheion.eu
# @copyright  (C) 2020-2022 Pierre Veelen
#
# ############################################################################
#
# - styling in .\assets\styles.css
#                 python <-> css
#                tagname <-> tagname
#             id=some-id <-> #some-id
#   className=some-class <-> .some-class
#
# ############################################################################

# Basic style settings
# =====================
# Please note:
# - Should use dict() in stead of {}
# - {} gives an error in the browser
# - do not use CSS syntax!

noStyle = dict()

borderStyle = dict(borderStyle="solid",)

labelTextStyle = dict(
    fontSize="14px", fontWeight="bold", textAlign="center", color="#263473",
)

labelTextStyleLarge = dict(
    fontSize="18px", fontWeight="bold", textAlign="center", color="#263473",
)
switchCol = dict(
    #    borderStyle='solid',
    #    height='130px',
)
