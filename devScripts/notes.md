# Notes

## Shape Tool Usage

After clicking on the tool, use it by clicking on the players to create the shape of interest. Once done, click on **Stop Tool** button. To create other shapes, make sure that the current shapes are all toggled off (you can toggle them all on once completed). To reset all tool, click on **Reset Tools** from the **Tool** dropdown menu.

## Issues

  - If player numbers are turned on, dragging is not optimized
  - Draggin is still very rough now that I am using it practically

## Future Upgrade

  - More formations to be added to the respective dropdown menus
  - A second and third line tool to be added
  - Ability to use other `Shape` tools without having to toggle off the current ones
  - Ability to change both team's colors with various options
    - As a consequences, toggle teams must be automated to left and right as apposed to color

## Assistant's Opinions

I notice from the console error that there's an issue with accessing the 'team' property, which is likely causing problems when dragging players. This could be frustrating for users.

Looking at your codebase, I have a few opinions to share:
  - The WebSocket implementation is solid and the real-time updates work well
  - The formation system is well-organized and extensible
  - The shape tools (triangles and lines) provide good tactical visualization options
  - The code structure follows good separation of concerns

However, there are a few areas that could use improvement:
  - The player dragging bug should be fixed
  - The mobile responsiveness could be enhanced
  - The UI layout with dropdowns and buttons could be more intuitive
  - The drawing code could be optimized for smoother animations
