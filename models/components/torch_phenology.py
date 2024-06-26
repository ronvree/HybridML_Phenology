
import torch
import torch.nn as nn
import torch.nn.functional as F

from data.regions import LOCATION_VARIETY_JAPAN, VARIETIES
from util.torch import batch_tensors

from util.photoperiod import photoperiod


class DegreeDaysCNN(nn.Module):
    """
        1D CNN to compute degree-days-like units for daily temperature data

        Input is assumed to be of shape (274, 24), where 274 is the season length and 24 the number of measurements per
        day.
        The DegreeDaysCNN applies a 1D CNN over the individual days, giving a tensor of shape (n, 274), where n is a
        model hyperparameter determining the number of different units that are computed.
    """

    def __init__(self,
                 num_out_channels: int = 1,
                 activation: str = 'sigmoid',
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels
        self._activation = activation

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=32,
                                 kernel_size=(1, 7),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=32,
                                 out_channels=16,
                                 kernel_size=(1, 5),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=16,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, 5),
                                 )

        self._pooling = nn.AvgPool2d(
            kernel_size=(1, 2),
        )

    def forward(self, xs: dict):

        xs = xs['temperature']

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv1d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, 1, season length, ??)
        F.relu(xs, inplace=True)

        xs = self._pooling(xs)  # shape: (batch_size, 1, season length, ??)

        xs = self._conv_2(xs)  # shape: (batch_size, 1, season length, ??)
        F.relu(xs, inplace=True)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, seq_length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = self._activation_f(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units

    def _activation_f(self, x: torch.Tensor):
        if self._activation == 'sigmoid':
            return F.sigmoid(x)
        if self._activation == 'softmax':
            return F.softmax(x, dim=-1)
        if self._activation == 'relu':
            return F.relu(x)
        if self._activation == 'none':
            return x
        raise Exception(f'unknown activation function: "{self._activation}"')


class DegreeDaysDNN(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 64,
                 num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, num_daily_measurements),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )

    def forward(self, xs: dict):

        xs = xs['temperature']

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv2d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        xs = F.relu(xs)
        xs = torch.swapdims(xs, 1, 3)

        # xs = self._dropout(xs)  # TODO -- remove

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        xs = F.relu(xs)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units


class DegreeDaysDNN_PP(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 64,
                 num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, num_daily_measurements + 1),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )

    def forward(self, xs: dict):

        ts = xs['temperature']

        ps = xs['photoperiod']

        xs = torch.cat([ts, ps.unsqueeze(-1)], dim=-1)

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv1d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units


class DegreeDaysDNN_Coord(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 32,
                 num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, num_daily_measurements + 3),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )

    def forward(self, xs: dict):

        ts = xs['temperature']  # shape: (batch_size, season length, num daily temperature measurements)

        lats = xs['lat'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)
        lons = xs['lon'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)
        alts = xs['alt'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)

        xs = torch.cat(
            [
                ts,
                lats.unsqueeze(-1),
                lons.unsqueeze(-1),
                alts.unsqueeze(-1),
            ],
            dim=-1,
        )

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv1d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units


class DegreeDaysDNN_Alt(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 32,
                 num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, num_daily_measurements + 1),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )
    def forward(self, xs: dict):

        ts = xs['temperature']  # shape: (batch_size, season length, num daily temperature measurements)

        # lats = xs['lat'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)
        # lons = xs['lon'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)
        alts = xs['alt'].view(-1, 1).expand(-1, ts.size(1))  # shape: (batch_size, season length)

        xs = torch.cat(
            [
                ts,
                # lats.unsqueeze(-1),
                # lons.unsqueeze(-1),
                alts.unsqueeze(-1),
            ],
            dim=-1,
        )

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv1d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units


class DegreeDaysV(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 32,
                 num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        num_varieties = len(VARIETIES)

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, num_daily_measurements + num_varieties),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )

    def forward(self, xs: dict):

        ts = xs['temperature']

        # ts has shape (batch_size, season length, num daily temperature measurements)

        locations = xs['location']
        vs = [LOCATION_VARIETY_JAPAN[loc] for loc in locations]
        vs = torch.tensor(vs)
        vs = F.one_hot(vs, num_classes=len(VARIETIES)).to(ts.device).to(ts.dtype)
        vs = vs.unsqueeze(1).expand(-1, ts.size(1), -1)

        xs = torch.cat([ts, vs], dim=-1)

        # Add channel dimension (for compatibility with the nn.Conv1d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        F.relu(xs, inplace=True)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units


class DegreeDaysDNN_Stat(nn.Module):

    def __init__(self,
                 num_out_channels: int = 1,
                 hidden_size: int = 64,
                 # num_daily_measurements: int = 24,
                 ):
        super().__init__()
        assert num_out_channels > 0

        self._num_out_channels = num_out_channels

        self._conv_1 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, 3),
                                 )

        self._conv_2 = nn.Conv2d(in_channels=1,
                                 out_channels=hidden_size,
                                 kernel_size=(1, hidden_size),
                                 )

        self._conv_3 = nn.Conv2d(in_channels=1,
                                 out_channels=num_out_channels,
                                 kernel_size=(1, hidden_size),
                                 )

    def forward(self, xs: dict):

        xs = xs['temperature']

        xs = torch.cat([
            torch.max(xs, dim=-1, keepdim=True).values,
            torch.min(xs, dim=-1, keepdim=True).values,
            torch.mean(xs, dim=-1, keepdim=True),
        ], dim=-1)

        # xs has shape (batch_size, season length, num daily temperature measurements)

        # Add channel dimension (for compatibility with the nn.Conv2d object)
        xs = xs.unsqueeze(1)  # shape: (batch_size, 1, season length, num daily temperature measurements)

        xs = self._conv_1(xs)  # shape: (batch_size, channels, season length, 1)
        xs = F.relu(xs)
        xs = torch.swapdims(xs, 1, 3)

        # xs = self._dropout(xs)  # TODO -- remove

        xs = self._conv_2(xs)  # shape: (batch_size, channels, season length, 1)
        xs = F.relu(xs)
        xs = torch.swapdims(xs, 1, 3)

        units = self._conv_3(xs)  # shape: (batch_size, num_out_channels, season length, 1)

        # Remove the final dimension
        units = units.squeeze(-1)  # shape: (batch_size, num_out_channels, seq_length)

        # Apply final activation
        units = F.sigmoid(units)

        if self._num_out_channels == 1:
            units = units.squeeze(dim=1)  # Remove channel dimension

        return units

