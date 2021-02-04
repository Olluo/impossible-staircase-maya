"""Script to create a tower in Maya"""
from __future__ import print_function, division
import pymel.core as pm


def create_tower_section(y_position, height, radius):
    """Create a main tower section

    Args:
        y_position (float): The position in y for this tower section
        height (float): The height of this tower section
        radius (float): The radius of this tower section

    Returns:
        str: The name of the tower section
    """
    # create cylinder
    name = pm.polyCylinder(name='towerSection#',
                           height=height,
                           radius=radius,
                           subdivisionsY=3,
                           subdivisionsCaps=5)[0]

    # move so bottom in correct location compared to previous section
    pm.move(name, y_position, y=True)

    return name


def create_tower_connection(y_position, height, radius):
    """Create a tower connection that connects the main tower sections

    Args:
        y_position (float): The position in y for this tower section
        height (float): The height of this tower section
        radius (float): The radius of this tower section

    Returns:
        str: The name of the tower connection
    """
    # create cylinder
    name = pm.polyCylinder(name='towerConnection#',
                           height=height,
                           radius=radius,
                           subdivisionsY=3,
                           subdivisionsCaps=10)[0]

    # move so bottom in correct location compared to previous section
    pm.move(name, y_position, y=True)

    return name


def create_tower_top(y_position, radius):
    """Create the top of the tower which consists of a cylinder, then some parapets on top to look like a medieval tower

    Args:
        y_position (float): The position in y for this tower section
        radius (float): The radius of this tower section
    """
    tower_top_parts = []

    # create cylinder
    name = pm.polyCylinder(name='towerTopBase#',
                           height=3.0,
                           radius=radius,
                           subdivisionsY=3,
                           subdivisionsCaps=10)[0]

    # move so bottom in correct location compared to previous section
    pm.move(name, y_position, y=True)
    
    tower_top_parts.append(name)

    # create parapets
    # create cylinder
    name = pm.polyCylinder(name='towerTopParapets#',
                           height=5.0,
                           radius=radius + 0.5,
                           subdivisionsY=2,
                           subdivisionsCaps=10)[0]

    # move so bottom in correct location compared to previous section
    pm.move(name, y_position + 5.0/2 + 3.0/2, y=True)

    # Extrude the central faces of the tower inwards to make hollowed section
    pm.polyExtrudeFacet(
        name + '.f[240:399]', name + '.f[420:440]', divisions=2, localTranslateZ=-4.5)

    # Select the even faces on the edge of the tower for extruding
    pm.polyExtrudeFacet(
        [name + '.f[' + str(x) + ']' for x in range(220, 240) if x % 2 == 0], localTranslateZ=2)
    
    tower_top_parts.append(name)

    return pm.group(*tower_top_parts, name='towerTop#')


def create_tower(num_sections=5, radius=10.0, height_section=10.0, height_connection=1.0):
    """Creates a medieval tower with parapets on top

    Args:
        num_sections (int, optional): The number of main sections to have in the tower. Defaults to 5.
        radius (float, optional): The radius of the tower. Defaults to 10.0.
        height_section (float, optional): The height of each main section of the tower. Defaults to 10.0.
        height_connection (float, optional): The height of each of the connections in the tower. Defaults to 1.0.
    """
    tower_sections = []
    tower_connections = []

    # Create bottom
    tower_connections.append(create_tower_connection(y_position=height_connection / 2.0,
                                                     height=height_connection,
                                                     radius=radius+0.5))

    # Create mid-sections
    for i in range(num_sections):
        tower_sections.append(create_tower_section(y_position=height_section / 2.0 + i * (height_section + height_connection),
                                                   height=height_section,
                                                   radius=radius))
        tower_connections.append(create_tower_connection(y_position=height_connection / 2.0 + height_section + i * (height_section + height_connection),
                                                         height=height_connection,
                                                         radius=radius+0.5))

    # Create top
    tower_top_name = create_tower_top(y_position=3 / 2.0 + num_sections * (height_section + height_connection),
                                      radius=radius+1)

    tower_sections_name = pm.group(*tower_sections, name='towerSections#')
    tower_connections_name = pm.group(*tower_connections, name='towerConnections#')

    tower_connections_name = pm.group(tower_top_name, tower_sections_name, tower_connections_name, name='tower#')


if __name__ == "__main__":
    """Main execution of this file. Creates a window with parameters that can be modified and then used to make the tower
    """
    window = pm.window(title='Tower Creator', sizeable=True,
                       resizeToFitChildren=True)

    layout = pm.columnLayout()
    sections_slider = pm.intSliderGrp(label='Number of sections',
                                      minValue=0,
                                      maxValue=10,
                                      value=5,
                                      field=True,
                                      parent=layout)
    radius_slider = pm.floatSliderGrp(label='Radius',
                                      minValue=1.0,
                                      maxValue=100.0,
                                      value=10.0,
                                      field=True,
                                      parent=layout)
    section_height_slider = pm.floatSliderGrp(label='Section Height',
                                              minValue=1.0,
                                              maxValue=100.0,
                                              value=10.0,
                                              field=True,
                                              parent=layout)
    connection_height_slider = pm.floatSliderGrp(label='Connection Height',
                                                 minValue=0.1,
                                                 maxValue=10.0,
                                                 value=1.0,
                                                 field=True,
                                                 parent=layout)

    button = pm.button(label='Create', parent=layout)

    def callback(*args):
        """The callback function used for this window
        """
        create_tower(num_sections=sections_slider.getValue(),
                     radius=radius_slider.getValue(),
                     height_section=section_height_slider.getValue(),
                     height_connection=connection_height_slider.getValue())

    button.setCommand(callback)
    window.show()
