function [] = three_wheel_RRT_draw(ax, tree, p_goal, goal_path, params)
%THREE_WHEEL_RRT_DRAW draws the RRT algorithm. ax is the axis to be drawn,
%tree is the RRT containing configurations [x y theta] (in global coords)
%p_goal is the goal position as a 2x1 array [x y] (in global coords).
%goal_path is an 3xn array representing the goal_path (defined in
%three_wheel_RRT_find_goal_path). If the path is not found or the goal_path
%is not to be drawn, simply supply [] for goal_path.
%params is the misc. parameter struct regarding the robot,map, and the algorithm.
    hold(ax,'on');
    axis(ax,'equal');
    xlim(ax,params.xlim);
    ylim(ax,params.ylim);
    for map_circ = params.map
        m_x = map_circ(1);
        m_y = map_circ(2);
        m_r = map_circ(3);
        rectangle(ax, 'Position',[m_x-m_r, m_y-m_r, 2*m_r, 2*m_r],...
                  'FaceColor',[0.5 0.5 0.5],'Curvature',1.0);
    end
    xlabel(ax,'x (m)');
    ylabel(ax,'y (m)');
    plot(ax, p_goal(1),p_goal(2),'-x','Color','g','MarkerSize',20,'LineWidth',2);
    plot_robot(ax,tree.value,'r',params.r);
    draw_RRT(ax,tree,params);
    
    if ~isempty(goal_path)
        for i = 1:size(goal_path,2)-1
            [x,y,~,~] = draw_arc(goal_path(:,i),goal_path(1:2,i+1));
            plot(ax,x,y,'Color','red');
        end
    end
end

function [] = draw_RRT(ax,tree,params)
    
    for child = tree.children
        [x,y,theta,t] = draw_arc(tree.value, child.value(1:2));
        plot_robot(ax,child.value,'none',0.1);
        plot(ax,x,y,'Color','blue');
        draw_RRT(ax,child,params);
    end
end