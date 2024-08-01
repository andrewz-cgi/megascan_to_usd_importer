from ..preset.geometry_preset import GeometryPreset

class GeometrySettings(GeometryPreset):

    def __init__(
            self,
            render_geomerty='',
            render_polyreduce_enable=False,
            render_polyreduce=0.0,
            enable_proxy_geometry=False,
            proxy_geomerty=None,
            proxy_geometry_polyreduce_enable=False,
            proxy_polyreduce=0.0,
            enable_sim_proxy_geometry=False,
            sim_proxy_geomerty=None,
            sim_proxy_geometry_polyreduce_enable=False,
            sim_proxy_polyreduce=0.0
        ):

        super().__init__(
            render_polyreduce_enable,
            render_polyreduce,
            enable_proxy_geometry,
            proxy_geometry_polyreduce_enable,
            proxy_polyreduce,
            enable_sim_proxy_geometry,
            sim_proxy_geometry_polyreduce_enable,
            sim_proxy_polyreduce
        )

        self.render_geomerty = render_geomerty
        self.proxy_geomerty = proxy_geomerty
        self.sim_proxy_geomerty = sim_proxy_geomerty