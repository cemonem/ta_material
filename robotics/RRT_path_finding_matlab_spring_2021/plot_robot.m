function [] = plot_robot(ax, pose,FaceColor,SIZE)
%PLOT_ROBOT plots a circular robot, ax is the axis drawn on, pose is a
%3x1 column array of [x y theta], theta being the orientation
%SIZE is a scalar that corresponds to the radius of the drawing
%FaceColor is the color of the robot drawn
rectangle(ax, 'Position', [pose(1)-SIZE/2 pose(2)-SIZE/2 SIZE SIZE], 'Curvature', 1,'FaceColor',FaceColor);
line(ax, [pose(1) pose(1)+SIZE/2*cos(pose(3)+pi/2)],[pose(2) pose(2)+SIZE/2*sin(pose(3)+pi/2)],'Color','k','LineWidth',1);

end