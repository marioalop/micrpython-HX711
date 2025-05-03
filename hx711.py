import machine
import utime


class HX711:
    """Driver for the HX711 load cell amplifier using MicroPython."""

    def __init__(
        self, dout_pin: int, pd_sck_pin: int, gain: int = 128
    ) -> None:
        """
        Initialize the HX711 sensor.

        Args:
            dout_pin (int): GPIO pin number connected to DOUT.
            pd_sck_pin (int): GPIO pin number connected to PD_SCK.
            gain (int, optional): Amplifier gain (128, 64, or 32). 
            Defaults to 128.

        Raises:
            ValueError: If an invalid gain value is provided.
        """
        self._dout = machine.Pin(
            dout_pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP
        )
        self._pd_sck = machine.Pin(pd_sck_pin, mode=machine.Pin.OUT)
        self._pd_sck.value(0)

        self._gain = 0
        self._set_gain(gain)

        self._offset = 0
        self._scale = 1.0

    def _set_gain(self, gain: int) -> None:
        """
        Set the amplifier gain.

        Args:
            gain (int): Gain value (128, 64, or 32).

        Raises:
            ValueError: If an unsupported gain is provided.
        """
        if gain == 128:
            self._gain = 1
        elif gain == 64:
            self._gain = 3
        elif gain == 32:
            self._gain = 2
        else:
            raise ValueError(
                "Invalid gain: {}. Use 128, 64 or 32.".format(gain)
            )

        self._read_raw()

    def _read_raw(self) -> int:
        """
        Read raw 24-bit value from the HX711.

        Returns:
            int: Signed 24-bit raw value.
        """
        while self._dout.value() == 1:
            utime.sleep_ms(10)

        raw_data = 0
        for _ in range(24):
            self._pd_sck.value(1)
            raw_data <<= 1
            self._pd_sck.value(0)
            if self._dout.value():
                raw_data += 1

        for _ in range(self._gain):
            self._pd_sck.value(1)
            self._pd_sck.value(0)

        # Convert to signed integer
        if raw_data & 0x800000:
            raw_data |= ~0xFFFFFF
        return raw_data

    def read_average(self, times: int = 3) -> int:
        """
        Read multiple raw values and return their average.

        Args:
            times (int, optional): Number of samples to average. 
            Defaults to 3.

        Returns:
            int: Averaged raw value.
        """
        total = 0
        for _ in range(times):
            total += self._read_raw()
            utime.sleep_us(10000)
        return total // times

    def tare(self, times: int = 15) -> None:
        """
        Tare the scale (set the current load as zero).

        Args:
            times (int, optional): Number of samples to average for offset. 
            Defaults to 15.
        """
        self._offset = self.read_average(times)
        print("Tare complete. Offset =", self._offset)

    def set_scale(self, scale: float) -> None:
        """
        Set the scale factor.

        Args:
            scale (float): Value used to scale the raw data.
        """
        self._scale = scale

    def get_weight(self, times: int = 3) -> float:
        """
        Get the current weight reading.

        Args:
            times (int, optional): Number of samples to average. 
            Defaults to 3.

        Returns:
            float: Calculated weight.
        """
        raw_avg = self.read_average(times)
        return (raw_avg - self._offset) / self._scale

    def instant_read(self) -> float:
        """
        Perform a single instant reading.

        Returns:
            float: Scaled weight reading.
        """
        return (self._read_raw() - self._offset) / self._scale
