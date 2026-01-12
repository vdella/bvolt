# What Telemetry Represents in BVOLT

> Telemetry. The transport and persistence of the domain state.
> It does not define meaning, as domain does. Telemetry in BVOLT is the recording and 
> retrieval of domain state over time.

It is a historical and current record of “what the system state was”.

## Read Semantics

What does "latest" mean?
It means the most recent recorded state. It is not real-time, it is not "now". Just
the last record.

What does "timeseries" mean?
A timeseries is an ordered sequence of historical domain state samples
for a given asset over a defined time range. It is always associated
with a single asset. Always bound by a time interval. The order matters
and aggregation of data (mean, min, max) is optional and external to this
concept. The domain does not care how dense or sparse the timeseries is.

## Write Semantics

Only trusted internal processes write telemetry, such as
* Polling runtime
* Energy Management System (EMS) services

External clients never write telemetry directly. Telemetry write operations
consist of snapshots of domain state, such as entities states. It is agnostic
to decisions, commands, forecasts, alarms and UIs.

## Identity and Scope

In BVOLT, an asset is uniquely identified by `{asset}_id`, which is
stable over time, refers to a single physical or logical asset, and
does not change with measurement methods. But what is an `asset`?

> Asset. Any physical or logical energy system component whose state
> is meaningful over time. All assets may have state conceptually,
> albeit only some of them have telemetry-backed states.

They have domain state, can be observed and can be reasoned about by EMS logic.
If something has no evolving state, it is not an asset.