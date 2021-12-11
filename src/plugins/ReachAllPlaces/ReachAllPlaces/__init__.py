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

# named incorrectly. This is about classification of petri nets
# type 1: Free-choice petri net​ - if the intersection of the inplaces sets of two transitions are not
    # empty, then the two transitions should be the same (or in short, each transition has its
    # own unique set if ​inplaces)​
# type 2: State machine​ - a petri net is a state machine if every transition has exactly one ​inplace
    # and one ​outplace​.
# type 3: Marked graph​ - a petri net is a marked graph if every place has exactly one out transition
    # and one in transition.
# type 4: Workflow net ​- a petri net is a workflow net if it has exactly one source place s where *s
    # =∅, one sink place o where o* =∅, and every x∈P∪T is on a path from s to o.
class ReachAllPlaces(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')
        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))
        core.set_attribute(active_node, 'name', 'newName')
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('committed :{0}'.format(commit_info))

        nodes = core.load_sub_tree(active_node)
        place_elements = {}
        transition_elements = {}
        graph = {}
        for node in nodes:
            if core.is_instance_of(node, META['Place']):
                place_elements[core.get_path(node)] = []
            if core.is_instance_of(node, META['Transition']):
                transition_elements[core.get_path(node)] = []
        for node in nodes:
            if core.is_type_of(node, META['Arc']):
                if core.get_pointer_path(node, 'src') in graph:
                    graph[core.get_pointer_path(node, 'src')].append(core.get_pointer_path(node, 'dst'))
                else:
                    graph[core.get_pointer_path(node, 'src')] = [core.get_pointer_path(node, 'dst')]

        classifications = []
        if free_choice(nodes, graph):
            classifications.append("Free-choice")
        if state_machine(nodes, transition_elements, graph):
            classifications.append("State machine")
        if marked_graph(nodes, place_elements, graph):
            classifications.append("Marked graph")
        if workflow_net(nodes, place_elements, transition_elements, graph):
            classifications.append("Workflow net")
        logger.info('This Petrinet is of type: ${}'.format(classifications))

    def free_choice(nodes, graph):
        fc = True
        transitions_in_pn: []
        for elem in graph:
            if core.is_instance_of(elem, META['Place']):
                for link in elem:
                    if link in transitions_in_pn:
                        fc = False
                    else:
                        transitions_in_pn.append(link)
        return fc

    def state_machine(nodes, transition_elements, graph):
        sm = True
        transitions: {}
        for trans in transition_elements:
            transitions[core.get_path(trans)] = {
                src_count: 0,
                dst_count: 0
            }
        for node in nodes:
            if core.is_instance_of(node, META['Place']):
                for connection in graph[node]:
                    if core.is_instance_of(connection, META['Transition']):
                        transitions[core.get_path(connection)].dst_count = transitions[core.get_path(connection)].dst_count + 1
            if ore.is_instance_of(node, META['Transition']):
                for connection in graph[node]:
                    if core.is_instance_of(connection, META['Place']):
                        transitions[core.get_path(node)].src_count = transitions[core.get_path(node)].src_count + 1
        for trans in transitions:
            if trans.src_count != 1 or trans.dst_count != 1:
                sm = False
        return sm

    def marked_graph(nodes, place_elements, graph):
        mg = True
        places: {}
        for place in place_elements:
            places[core.get_path(place)] = {
                src_count: 0,
                dst_count: 0
            }
        for node in nodes:
            if core.is_instance_of(node, META['Place']):
                for connection in graph[node]:
                    if core.is_instance_of(connection, META['Transition']):
                        places[core.get_path(connection)].src_count = places[core.get_path(connection)].src_count + 1
            if ore.is_instance_of(node, META['Transition']):
                for connection in graph[node]:
                    if core.is_instance_of(connection, META['Place']):
                        places[core.get_path(node)].dst_count = places[core.get_path(node)].dst_count + 1
        for place in places:
            if place.src_count != 1 or place.dst_count != 1:
                mg = False
        return mg

    def workflow_net(nodes, place_elements, transition_elements, graph):
        wn = False
        source = find_source(nodes, place_elements, grpah)
        sink = find_sink(nodes, graph)
        if source is None or sink is None:
            return False
        else:
            wn = find_path(source, sink, graph, nodes)
        return wn

    def find_source(nodes, place_elements, graph):
        # no transition has this node listed as a dst
        found_places = []
        one_source = False
        source = None
        for node in graph:
            if core.is_instance_of(node, META['Transition']):
                for link in node:
                    if link not in found_places:
                        found_places.push(link)
        for place in place_elements:
            if place not in found_places and one_source == False:
                one_source = True
                source = place
            if place not in found_places and one_source == True:
                return None
        return source

    def find_sink(nodes, graph):
        # no transition has this node listed as a src
        found_places = []
        one_sink = False
        sink = None
        for node in graph:
            if core.is_instance_of(node, META['Place']):
                if node.length == 0 and one_sink == False:
                    one_sink = True
                    sink = node
                if node.length == 0 and one_sink == True:
                    return None
        return sink

    def find_path(source, sink, graph, nodes):
        valid_path = True
        visited = []
        queue = []
        visited.append(source)
        queue.append(source)
        while queue:
            node = queue.pop(0)
            for next_node in graph[node]:
                visited.append(next_node)
                queue.append(next_node)
        for node in nodes:
            if node not in visited:
                valid_path = False
        return valid_path