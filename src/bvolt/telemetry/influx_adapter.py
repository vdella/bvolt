from datetime import datetime
from typing import Iterable

from bvolt.domain.state import State
from bvolt.infrastructure import config
from bvolt.telemetry.reader import TelemetryReader
from bvolt.telemetry.writer import TelemetryWriter
from bvolt.infrastructure.config import *

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxTelemetryReader(TelemetryReader):

    def __init__(self) -> None:
        self._client = InfluxDBClient(
            url=config.influx_url,
            token=config.influx_token,
            org=config.influx_org
        )

        self._query = self._client.query_api()

    def latest_state(self, asset_id: str) -> State:
        """
        Return the most recent recorded State for the given asset.
        """

        flux = f"""
        from(bucket: "{config.influx_bucket}")
          |> range(start: -30d)
          |> filter(fn: (r) => r["asset_id"] == "{asset_id}")
          |> last()
        """

        tables = self._query.query(flux, org=config.influx_org)

        if not tables:
            raise LookupError(f"No telemetry found for asset_id={asset_id}")

        # TODO:
        # Translate FluxRecord(s) into a domain State instance.
        # This must be implemented once concrete State subclasses
        # (e.g. BatteryState) are defined in the domain layer.

        raise NotImplementedError(
            "State construction is pending domain implementation."
        )

    def timeseries(self,
                   asset_id: str,
                   start: datetime,
                   end: datetime,
                   ) -> Iterable[State]:
        """
        Return an ordered sequence of State snapshots for the given asset
        over the specified time range.
        """

        flux = f"""
        from(bucket: "{config.influx_bucket}")
          |> range(start: {start.isoformat()}, stop: {end.isoformat()})
          |> filter(fn: (r) => r["asset_id"] == "{asset_id}")
          |> sort(columns: ["_time"])
        """

        tables = self._query.query(flux, org=config.influx_org)

        if not tables:
            return []

        # TODO:
        # Iterate over FluxRecords and construct domain State objects.
        # Ordering is guaranteed by the Flux query.
        # Aggregation is intentionally NOT performed here.

        raise NotImplementedError(
            "Timeseries State construction is pending domain implementation."
        )


class InfluxTelemetryWriter(TelemetryWriter):

    def __init__(self) -> None:
        self._client = InfluxDBClient(
            url=config.influx_url,
            token=config.influx_token,
            org=config.influx_org,
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)

    def record_state(
            self,
            asset_id: str,
            state: State,
            timestamp: datetime,
    ) -> None:
        # Do NOT assume State structure yet.
        # Only assume it can be represented as key/value pairs.

        if not hasattr(state, "to_dict"):
            raise NotImplementedError(
                "State serialization not implemented yet"
            )

        fields = state.to_dict()

        record = (
            Point("asset_state")
            .tag("asset_id", asset_id)
            .time(timestamp)
        )

        for key, value in fields.items():
            point = record.field(key, value)

        self._write_api.write(
            bucket=config.influx_bucket,
            org=config.influx_org,
            record=record,
        )
