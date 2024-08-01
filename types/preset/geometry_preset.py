class GeometryPreset():

    def __init__(
            self,
            render_polyreduce_enable=False,
            render_polyreduce=80.0,
            enable_proxy_geometry=False,
            proxy_geometry_polyreduce_enable=False,
            proxy_polyreduce=50.0,
            enable_sim_proxy_geometry=False,
            sim_proxy_geometry_polyreduce_enable=False,
            sim_proxy_polyreduce=50.0):
        
        self.render_polyreduce_enable = render_polyreduce_enable
        self.render_polyreduce = render_polyreduce
        self.enable_proxy_geometry = enable_proxy_geometry
        self.proxy_geometry_polyreduce_enable = proxy_geometry_polyreduce_enable
        self.proxy_polyreduce = proxy_polyreduce
        self.enable_sim_proxy_geometry = enable_sim_proxy_geometry
        self.sim_proxy_geometry_polyreduce_enable = sim_proxy_geometry_polyreduce_enable
        self.sim_proxy_polyreduce = sim_proxy_polyreduce