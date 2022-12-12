# Fundamentals
## Domain and boundaries
## Energy systems

System functions:

* `sf_dispatchable_sink`: A unit consuming a dispatchable amount of energy. For example can consume waste heat produced by other units.
* `sf_dispatchable_source`: A unit producing a dispatchable amount of energy, drawing it from outside the system boundary. For example drawing in heat from the ambient environment.
* `sf_fixed_sink`: A unit consuming an amount of energy fixed within a time step. For example a demand of hot water for heating.
* `sf_fixed_source`: A unit producing an amount of energy fixed within a time step. For example a photovoltaic power plant.
* `sf_transformer`: A unit transforming energy in at least one medium to energy in at least one medium. For example a heat pump using lower temperature heat and electricity to produce higher temperature heat.
* `sf_storage`: A unit storing energy in a given medium. For example a buffer tank providing hot water.
* `sf_bus`: A special type of unit used to facilitate the transport of energy from and to other units. Has only one implementation.
