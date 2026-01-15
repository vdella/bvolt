from datetime import datetime
from typing import Iterable

from bvolt.infrastructure import config
from bvolt.telemetry.reader import TelemetryReader
from bvolt.telemetry.writer import TelemetryWriter
from bvolt.infrastructure.config import *

from influxdb_client import InfluxDBClient

class InfluxAdapter(TelemetryReader):

    _client = InfluxDBClient(
        url=config.influx_url,
        token=config.influx_token,
        org=config.influx_org
    )

    _query = _client.query_api()

    def __init__(self, reader: TelemetryReader) -> None:
        self._reader = reader

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
