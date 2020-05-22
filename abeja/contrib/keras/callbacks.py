from logging import getLogger

from abeja.train.client import Client
from abeja.training.statistics import Statistics as ABEJAStatistics
from keras.callbacks import Callback

logger = getLogger('callback')


class Statistics(Callback):
    """A Keras callback for reporting statistics to ABEJA Platform"""

    def __init__(self, **kwargs):
        super(Statistics, self).__init__()
        self.client = Client(**kwargs)

    def on_epoch_end(self, epoch, logs=None):
        epochs = self.params['epochs']
        statistics = ABEJAStatistics(num_epochs=epochs, epoch=epoch + 1)
        statistics.add_stage(
            ABEJAStatistics.STAGE_TRAIN,
            logs['acc'],
            logs['loss'])
        statistics.add_stage(ABEJAStatistics.STAGE_VALIDATION,
                             logs['val_acc'], logs['val_loss'])
        try:
            self.client.update_statistics(statistics)
        except Exception:
            logger.warning('Failed to update statistics.')
