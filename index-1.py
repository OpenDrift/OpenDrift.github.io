from datetime import timedelta
from opendrift.models.openoil import OpenOil
from opendrift.readers import reader_netCDF_CF_generic
o = OpenOil()

reader_arome = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
reader_norkyst = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

o.add_reader([reader_norkyst, reader_arome])

lon = 4.6; lat = 60.0; # Outside Bergen

time = [reader_arome.start_time, reader_arome.start_time + timedelta(hours=30)]

# Seed oil elements at defined position and time
o.seed_elements(lon, lat, radius=50, number=3000, time=time,
                wind_drift_factor=.02)

# Adjusting some configuration
o.set_config('processes:dispersion', True)
o.set_config('processes:evaporation', True)
o.set_config('processes:emulsification', True)
o.set_config('drift:current_uncertainty', .1)
o.set_config('drift:wind_uncertainty', 1)

# Running model
o.run(steps=60, time_step=1800)

# Print and plot results
o.plot(background=['x_sea_water_velocity', 'y_sea_water_velocity'], buffer=.5)