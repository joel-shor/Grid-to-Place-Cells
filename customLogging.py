'''
Loggin file used to keep track of the program as it completes simulations.
'''

import logging.handlers as log_h
import logging

# Send email for exceptions
smtp_h = log_h.SMTPHandler(("smtp.gmail.com",587), 'shor.joel@gmail.com',
               'shor.joel@gmail.com', "Completed a simulation",
               ('shor.joel@gmail.com','divide9And6Conquer3'), ())
smtp_h.setLevel("DEBUG")


# Name and generate logging object
logger = logging.Logger(__name__)
logger.addHandler(smtp_h)

    