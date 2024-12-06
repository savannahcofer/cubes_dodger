import asyncio
from bleak import BleakScanner, BleakClient



class BleakEvalClient:
    def __init__(self):
        self.client = None
        self.rx_buffer = ""
        self.accel_x = self.accel_y = self.accel_z = 0
        self.gyro_x = self.gyro_y = self.gyro_z = 0
        self.mag_x = self.mag_y = self.mag_z = 0
        self.prox = 0

        # Nordic UART Service UUID
        self.UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
        # Nordic UART Service characteristics
        self.UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Write
        self.UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Read/Notify

    async def connect(self):
        print("Scanning for Bluefruit UART Friend...")
        devices = await BleakScanner.discover()
        print("All discovered devices:")
        for d in devices:
            print(f"Name: {d.name}, Address: {d.address}")

        # Find your Bluefruit device
        uart_device = None
        for device in devices:
            if device.name and "Bluefruit" in device.name:
                uart_device = device
                break

        if not uart_device:
            print("No Bluefruit device found")
            return False

        self.client = BleakClient(uart_device.address)
        await self.client.connect()
        print(f"Connected to {uart_device.name}")

        # Start notifications
        await self.client.start_notify(self.UART_TX_CHAR_UUID, self.handle_rx)
        return True

    async def send_message(self, message):
        """Send a message to the Bluetooth device."""
        if not self.client:
            print("Not connected to any device")
            return

        # Add newline if it's not already there
        if not message.endswith('\n'):
            message += '\n'

        # Convert string to bytes and send
        message_bytes = message.encode()
        await self.client.write_gatt_char(self.UART_RX_CHAR_UUID, message_bytes)
    def handle_rx(self, sender, data):
        try:
            # Append new data to buffer
            self.rx_buffer += data.decode()

            # Process complete lines
            while '\n' in self.rx_buffer:
                line, self.rx_buffer = self.rx_buffer.split('\n', 1)
                values = line.strip().split(',')

                if len(values) == 10:  # Ensure we have all 10 sensor values
                    (self.accel_x, self.accel_y, self.accel_z,
                     self.gyro_x, self.gyro_y, self.gyro_z,
                     self.mag_x, self.mag_y, self.mag_z,
                     self.prox) = map(float, values)
                    # Print formatted sensor data
                    print("Gyroscope:")
                    print("X: %0.2f  Y: %0.2f  Z: %0.2f  rad/s" % (self.gyro_x, self.gyro_y, self.gyro_z))
        except Exception as e:
            print(f"Error parsing data: {e}")
            print(f"Raw data: {data.decode()}")
            self.rx_buffer = ""  # Clear buffer on error

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()

