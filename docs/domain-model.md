# Purpose of the Domain of the project

> The project domain. The formal description of the energy system BVOLT reasons about, 
> independent of how data is collected, stored, transmitted, or visualized.

The domain is an abstraction. It is independent of everything else in the system.
If you strip away DB, dashboards, REST APIs, polling, secrets, microservices etc.,
the *domain must still make sense*. Domain is not data, API or control algorithms.
It is "what exists" and "what it means". 
The domain defines meaning, not measurement mechanics.

## Structure vs. State

Domain state and domain structure are not the same thing. Structure
is intrinsic, static. State varies over time; it is dynamic. This does matter:
telemetry and API semantics depend on this distinction.

> Structure is *what defines an asset/apparel/device*
> State is *what varies over time*

The domain models both, without caring how state is obtained.

## Time and Domain Objects

Domain objects do not manage time.
Time is applied by telemetry and services.
Domain states represent logical state, not samples.
None of the project entities should include a timestamp.

## Entities

* Battery
  * Stores energy
  * Can charge or discharge
  * Has a State of Charge (SOC)
  * Has temperature
  * Has physical limits

* Inverter
  * Has 3 phases
  * Has working modes for managing energy
  * Convertes energy between DC and AC adapters
  * Has operational limits

* Microgrid
  * Logical aggregation of assets operating under a shared electrical and control context.

* PV
  * Generates power from the sun
  * Has physical limits