from typing import Dict, Any, Optional

STATISTICS = Dict[str, Any]
STAGES = Dict[str, STATISTICS]


class Statistics:

    STAGE_TRAIN = 'train'
    STAGE_VALIDATION = 'validation'

    def __init__(
            self,
            num_epochs: int=None,
            epoch: int=None,
            progress_percentage: float=None,
            **kwargs) -> None:
        """
        :param num_epochs: number of total epoch.
        :param epoch: epoch.
        :param progress_percentage: percentage of progress that value needs between 0 and 1.
        """
        self.num_epochs = num_epochs
        self.epoch = epoch
        self.progress_percentage = progress_percentage
        self.other_information = kwargs
        self.stages = {}  # type: STAGES

    @classmethod
    def from_response(
            klass, response: Optional[Dict[str, Any]]) -> Optional['Statistics']:
        if response is None:
            return None

        stages = {}
        if 'stages' in response:
            stages = response.pop('stages')

        statistics = klass(**response)
        for name, values in stages.items():
            statistics.add_stage(name=name, **values)
        return statistics

    def add_stage(
            self,
            name: str,
            accuracy: float=None,
            loss: float=None,
            **kwargs) -> None:
        """ add stage information

        Params:
            - **name** (str): name of stage. It have prepared `STAGE_TRAIN` and `STAGE_VALIDATION` as constants, but you can set arbitrary character strings.
            - **accuracy** (float): accuracy rate that value needs between 0 and 1.
            - **loss** (float): loss rate that value needs between 0 and 1.

        Returns:
            None

        Raises:
            - ValueError
        """
        if accuracy is None and loss is None and kwargs is None:
            raise ValueError("something statistics information need")

        stat = {}  # type: STATISTICS
        if kwargs:
            stat.update(**kwargs)
        if accuracy:
            stat['accuracy'] = accuracy
        if loss:
            stat['loss'] = loss
        self.stages[name] = stat

    def get_statistics(self) -> dict:
        """ get stage information

        Return type:
            dict

        Returns:
            Response Syntax:

            .. code-block:: python

                {
                    'num_epochs': 10,
                    'epoch': 1,
                    'progress_percentage': 90,
                }
        """
        ret = {}  # type: STATISTICS
        if self.other_information:
            ret.update(**self.other_information)
        if self.num_epochs:
            ret['num_epochs'] = self.num_epochs
        if self.epoch:
            ret['epoch'] = self.epoch
        if self.progress_percentage:
            ret['progress_percentage'] = self.progress_percentage
        if self.stages:
            ret['stages'] = self.stages
        return ret
