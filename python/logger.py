#
# Logger module
#
import logging, sys

def getLogger(level='INFO', logFile=None):
  # If it already exist, return it
  logger = logging.getLogger('main')
  if logger.handlers:
    return logger

  numeric_level = getattr(logging, level.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError("Invalid log level: %s" % level)

  logger.setLevel(numeric_level)
  formatter = logging.Formatter('%(asctime)s %(module)20s %(levelname)7s - %(message)s')
  if logFile:
    # create the logging file handler
    fileHandler = logging.FileHandler(logFile, mode='w')
    fileHandler.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fileHandler)

  # create console handler and set level to debug
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  # log the exceptions to the logger
  def excepthook(*args):
    logger.error("Uncaught exception:", exc_info=args)

  sys.excepthook = excepthook
  logger.info('Command: ' + ' '.join(sys.argv))
  return logger

def logLevel(logger, level):
  return logger.getEffectiveLevel() <= logging.getLevelName(level)
