import logging
import os
import sys
from logging import getLogger, Logger
from pathlib import Path
from typing import Dict, Optional

from abeja.exceptions import InvalidPathException
from abeja.models.api.client import APIClient as ModelClient
from abeja.training.api.client import APIClient as TrainingClient
from abeja.training.statistics import Statistics as ABEJAStatistics
from abeja.tracking.metric import Metric
from tensorboardX import SummaryWriter


tracking_logger = getLogger('tracking')
if len(tracking_logger.handlers) == 0:
    tracking_logger.addHandler(logging.StreamHandler(stream=sys.stdout))
if tracking_logger.level == logging.NOTSET:
    tracking_logger.setLevel(logging.WARN)


class Tracking:
    """Model Tracking

    Usage:
        .. code-block:: python

            from abeja.tracking import Tracking


            NUM_EPOCHS = 10
            for epoch in range(NUM_EPOCHS):
                with Tracking(total_steps=NUM_EPOCHS) as tk:
                    # Write your modeling code here.
                    tk.log_description("Example")
                    tk.log_param(key="LR", value="0.03")
                    tk.log_param(key="DROPOUT", value="0.7")
                    tk.log_metric(key="main/acc", value=0.95)
                    tk.log_metric(key="main/loss", value=0.01)
                    tk.log_artifact(filepath='filepath_to_your_model', delete_flag=True)
    """

    def __init__(
            self,
            total_steps: Optional[int] = None,
            logger: Optional[Logger] = tracking_logger):
        self.logger = logger
        self._organization_id = os.environ.get('ABEJA_ORGANIZATION_ID')
        self._job_definition_name = os.environ.get(
            'TRAINING_JOB_DEFINITION_NAME')
        self._training_job_id = os.environ.get('TRAINING_JOB_ID')
        self._is_valid_job = \
            self._organization_id and self._job_definition_name and self._training_job_id

        self._params = dict()
        self._metrics = dict()
        self._description = ""
        self._filepath = None
        self._file_delete_flag = False
        self._step = None
        self._total_steps = total_steps
        self._need_flush = False

        ABEJA_TRAINING_RESULT_DIR = os.environ.get(
            'ABEJA_TRAINING_RESULT_DIR', '.')
        log_path = os.path.join(ABEJA_TRAINING_RESULT_DIR, 'logs')
        self._summary_writer = SummaryWriter(log_dir=log_path)

        if self._is_valid_job:
            TrainingClient().get_training_job(
                organization_id=self._organization_id,
                job_definition_name=self._job_definition_name,
                training_job_id=self._training_job_id)
        else:
            self.logger.warning(
                'WARNING: No params/metrics/artifact will be uploaded to ABEJA Platform. '
                'Please specify "ABEJA_ORGANIZATION_ID", "TRAINING_JOB_DEFINITION_NAME" '
                'and "TRAINING_JOB_ID" for uploading.')

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.flush()
        self._summary_writer.close()

    def clear(self) -> None:
        self._params = dict()
        self._metrics = dict()
        self._description = ""
        self._filepath = None
        self._file_delete_flag = False
        self._step = None
        self._need_flush = False

    @property
    def total_steps(self) -> int:
        return self._total_steps

    @total_steps.setter
    def total_steps(self, value: int) -> None:
        if isinstance(value, int):
            self._total_steps = value
        else:
            raise TypeError

    def log_step(self, step: int) -> None:
        if isinstance(step, int):
            self._step = step
        else:
            raise TypeError

    def log_description(self, description: str) -> None:
        if isinstance(description, str):
            self._description = description
        else:
            raise TypeError

    def log_param(self, key: str, value: str) -> None:
        if isinstance(key, str) and isinstance(value, str):
            self._params.update({key: value})
        else:
            raise TypeError

    def log_params(self, params: Dict[str, str]) -> None:
        for key, value in params.items():
            self.log_param(key, value)

    def log_metric(self, key: str, value: float) -> None:
        metric = Metric(key, value)
        if self._step is not None and metric.is_scalar():
            self._summary_writer.add_scalar(
                metric.key, metric.value, self._step)
        self._metrics.update(metric.to_dict())

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        for key, value in metrics.items():
            self.log_metric(key, value)

    def log_artifact(
            self,
            filepath: str,
            delete_flag: Optional[bool] = False) -> None:
        if Path(filepath).is_file():
            self._need_flush = True
            self._filepath = Path(filepath)
            self._file_delete_flag = delete_flag
        else:
            raise InvalidPathException(filepath)

    def flush(self) -> None:
        description = ""
        if self._step is not None:
            self.logger.debug('step {}'.format(self._step))
            description = 'STEP {}. '.format(self._step)
        self.logger.debug('description={}'.format(self._description))
        self.logger.debug('params={}'.format(self._params))
        self.logger.debug('metrics={}'.format(self._metrics))
        self.logger.debug('artifact={}'.format(str(self._filepath)))
        description += self._description

        self._summary_writer.flush()
        if self._is_valid_job and self._total_steps is not None and self._step is not None:
            statistics = ABEJAStatistics(
                num_epochs=self._total_steps, epoch=self._step)
            kwargs = {**self._params, **self._metrics}
            kwargs.pop('main_acc', None)
            kwargs.pop('main_loss', None)
            kwargs.pop('test_acc', None)
            kwargs.pop('test_loss', None)

            train_acc = self._metrics.get('main_acc')
            train_loss = self._metrics.get('main_loss')
            if train_acc is not None or train_loss is not None:
                statistics.add_stage(
                    ABEJAStatistics.STAGE_TRAIN,
                    train_acc,
                    train_loss,
                    **kwargs)
            val_acc = self._metrics.get('test_acc')
            val_loss = self._metrics.get('test_loss')
            if val_acc is not None or val_loss is not None:
                statistics.add_stage(
                    ABEJAStatistics.STAGE_VALIDATION,
                    val_acc,
                    val_loss,
                    **kwargs)
            if statistics.get_statistics():
                try:
                    res = TrainingClient().update_statistics(
                        organization_id=self._organization_id,
                        job_definition_name=self._job_definition_name,
                        training_job_id=self._training_job_id,
                        statistics=statistics.get_statistics())
                    self.logger.debug(res)
                except Exception as e:
                    self.logger.error(e)

        if self._need_flush:
            if self._is_valid_job:
                with open(str(self._filepath)) as fp:
                    parameters = {
                        'training_job_id': self._training_job_id,
                        'description': description,
                        'user_parameters': self._params,
                        'metrics': self._metrics,
                    }
                    res = ModelClient().create_training_model(
                        organization_id=self._organization_id,
                        job_definition_name=self._job_definition_name,
                        model_data=fp, parameters=parameters)
                    self.logger.debug(res)
                if self._file_delete_flag:
                    self._filepath.unlink()
        else:
            self.logger.warning(
                'No output. Need to add "artifact" by "log_artifact()".')

        self.clear()
