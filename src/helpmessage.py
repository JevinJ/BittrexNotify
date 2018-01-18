from config import SLOWTICK_RATE, FASTTICK_RATE, FASTTICK_LOOKBACK

slowtick_help_message = ('This section shows % change from '
                         'the previous measurement, recorded once every '
                         f'{int(SLOWTICK_RATE)} seconds.({SLOWTICK_RATE/60:.1f} minutes)\n\n'
                         'The arrow buttons can be used to '
                         'sort data according to the '
                         'label it is under.\n\n'
                         'The bell button can be toggled '
                         'on and off to play a sound '
                         'when the ticker has been updated.')

fasttick_help_message = ('This section shows % change over '
                         f'{FASTTICK_LOOKBACK+1} measurements, recorded once every '
                         f'{int(FASTTICK_RATE)} seconds.({FASTTICK_RATE/60:.1f} minutes)\n\n'
                         'The arrow buttons can be used to '
                         'sort data according to the '
                         'label it is under.\n\n'
                         'The bell button can be toggled '
                         'on and off to play a sound '
                         'when the ticker has been updated.')

