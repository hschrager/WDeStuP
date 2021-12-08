"""
This is where the implementation of the plugin code goes.
The ReachAllPlaces-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('ReachAllPlaces')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ReachAllPlaces(PluginBase):
    def main(self):
        json = self.modules['json']
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        logger = self.logger
        META = self.META

        name = core.get_attribute(active_node, 'name')
        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))
        core.set_attribute(active_node, 'name', 'newName')
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))

        # code from HW 7        
        graph_elements = {}
        ports = {}
        tracks = {}
        nodes = core.load_sub_tree(active_node)
        logger.info(nodes)
        for node in nodes:
            if core.is_instance_of(node, META['Port']):
                ports[core.get_path(node)] = node
                graph_elements[core.get_path(node)] = []
            elif core.is_instance_of(node, META['Track']):
                tracks[core.get_path(node)] = node
        
        for track in tracks.keys():
            myT = tracks[track]
            graph_elements[core.get_pointer_path(myT, 'src')].append({'dst':core.get_pointer_path(myT,'dst'),'length':core.get_attribute(myT,'length')})
    
        def place_exists(start_place):
            nodes = core.load_sub_tree(active_node)
            start_true = False
            for node in nodes:
                if core.is_instance_of(node, META['Station']):
                    if core.get_attribute(node, 'name') == start_place:
                        start_true = True
            return start_true
        
        path2node = {}    
        for node in nodes:
            path2node[core.get_path(node)] = node
        
        def find_paths(start_place):
            all_paths = {}
            if station_exists(start_place):
                start_node = None
                start_node_path = ''
                logger.info(start_node)
                for node in nodes:
                    if core.is_instance_of(node, META['Place']) and core.get_attribute(node, 'name') == start_place:
                        start_node_path = core.get_path(node) #station value
                        start_node = node
                    else if core.is_instance_of(node, META['Transition']) and core.get_attribute(node, 'name') == start_place:
                        start_node_path = core.get_path(node) #station value
                        start_node = node
                
                for child in core.get_children_paths(start_node):
                    logger.warn('starting DFS for {0}'.format(core.get_attribute(path2node[child], 'name')))
                    visited = []
                    visited.append(start_node.get("nodePath"))
                    dfs(visited, graph_elements, child, child, all_paths)
                #create output text file and format all_paths correctly for that
            else:
                logger.error("Node does not exist")
            return all_paths
                
        def dfs(visited, graph, node, original_node, path_dict):  #function for dfs 
            parent_node = core.get_parent(path2node[node])
            parent_name = ''
            if node not in visited:
                logger.info(node)
                visited.append(node)
                if core.is_instance_of(parent_node, META['Place']) or core.is_instance_of(parent_node, META['Transition']):
                    parent_name = core.get_attribute(parent_node, 'name')
                    try:
                        path_dict[original_node].append(parent_name)
                    except KeyError:
                        path_dict[original_node] = [parent_name]
                if node in graph: 
                    for neighbour in graph[node]:
                        logger.info(neighbour)
                        dfs(visited, graph, neighbour['dst'], original_node, path_dict)
                
        paths = find_paths(start_place)
        path_for_file = json.dumps(paths)
        string1 = "From " + start_place + " you can travel : "
        for path in paths:
            string2 = "To "
            i = 0
            for station in paths[path]:
                if i % 2 is 0:
                string2 += station + " via "
                i = i+1
            string2 += '\n'
            string1 += string2
        file_hash = self.add_file('output.txt', string1)
        logger.info('The file is stored under hash: {0}'.format(file_hash))