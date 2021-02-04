"""Script to create an impossible staircase in Maya"""
from __future__ import print_function, division
import pymel.core as pm


def create_stairs(stair_height=0.2, stair_width=1.0, main_edge_length=10):
    """Create an impossible staircase template model that can be modifed by hand to look realistic from a certain perspective

    Args:
        stair_height (float, optional): The height of each stair. Defaults to 0.2.
        stair_width (float, optional): The width and depth of each stair. Defaults to 1.0.
        main_edge_length (int, optional): The number of stairs on the main edge. Defaults to 10.
    """
    stairs = []
    x_offset = 0
    y_offset = 0
    z_offset = 0

    # First edge
    for i in range(main_edge_length-1):
        # create stair object
        name = pm.polyCube(name='stair#', depth=stair_width,
                           height=stair_height, width=stair_width)[0]

        # Move stair to correct place
        pm.move(name, [x_offset, i*stair_height, i*stair_width])

        # Add this stair to the list of stairs
        stairs.append(name)

    x_offset = stair_width
    y_offset = (i + 1) * stair_height
    z_offset = i * stair_width

    # Main edge
    for i in range(main_edge_length-1):
        # create stair object
        name = pm.polyCube(name='stair#', depth=stair_width,
                           height=stair_height, width=stair_width)[0]

        # Move stair to correct place
        pm.move(name, [i*stair_width + x_offset, i *
                       stair_height + y_offset, z_offset])

        # Add this stair to the list of stairs
        stairs.append(name)

    x_offset += i * stair_width
    y_offset += (i + 1) * stair_height
    z_offset = (i - 1) * stair_width

    # Third edge
    for i in range(3):
        # create stair object
        name = pm.polyCube(name='stair#', depth=stair_width,
                           height=stair_height, width=stair_width)[0]

        # Move stair to correct place
        pm.move(name, [x_offset, i*stair_height +
                       y_offset, -(i*stair_width) + z_offset])

        # Add this stair to the list of stairs
        stairs.append(name)

    x_offset -= stair_width
    y_offset += (i + 1) * stair_height
    z_offset -= i*stair_width

    # Final edge
    for i in range(3):
        # create stair object
        name = pm.polyCube(name='stair#', depth=stair_width,
                           height=stair_height, width=stair_width)[0]

        # Move stair to correct place
        pm.move(name, [-i*stair_width + x_offset,
                       i*stair_height + y_offset, z_offset])

        # Add this stair to the list of stairs
        stairs.append(name)

    pm.group(*stairs, name='impossibleStairs#')


if __name__ == "__main__":
    """Main execution of this file. Creates a window with parameters that can be modified and then used to make the staircase
    """
    window = pm.window(title='Impossible Stair Creator', sizeable=True,
                       resizeToFitChildren=True)

    layout = pm.columnLayout()
    stair_height_slider = pm.floatSliderGrp(label='Stair Height',
                                            minValue=0.1,
                                            maxValue=10.0,
                                            value=0.2,
                                            field=True,
                                            parent=layout)
    stair_width_slider = pm.floatSliderGrp(label='Stair Width',
                                           minValue=1.0,
                                           maxValue=10.0,
                                           value=1.0,
                                           field=True,
                                           parent=layout)
    main_edge_slider = pm.intSliderGrp(label='Main Edge Length',
                                       minValue=0,
                                       maxValue=20,
                                       value=10,
                                       field=True,
                                       parent=layout)

    button = pm.button(label='Create', parent=layout)

    def callback(*args):
        """The callback function used for this window
        """
        create_stairs(stair_height=stair_height_slider.getValue(),
                      stair_width=stair_width_slider.getValue(),
                      main_edge_length=main_edge_slider.getValue())

    button.setCommand(callback)
    window.show()
