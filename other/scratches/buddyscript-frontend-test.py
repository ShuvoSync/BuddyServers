# Initialize buddyscript engine for static testing
def init_bs_engine():
    import source.core.server.buddyscript as buddyscript
    import source.core.telepath as telepath
    import source.core.constants as constants
    import source.core.server.manager as svrmgr
    import time

    constants.server_manager = svrmgr.ServerManager()
    constants.server_manager.open_server(server_name)
    while not constants.server_manager.current_server.script_manager:
        time.sleep(0.1)

    constants.server_manager.current_server.run_data = {
        'log': [], 'network': {'address': None}, 'player-list': {},
        'process-hooks': [],
        'performance': {'ram': 0, 'cpu': 0, 'uptime': '00:00:00:00',
        'current-players': []}
    }
    so = buddyscript.ScriptObject(constants.server_manager.current_server)
    so.construct()
    return so.server_script_obj


# Server to test
server_name = 'Shop Test'
server = init_bs_engine()


# Test buddyscript code below
print(server.get_player('KChicken', offline=True).position)
